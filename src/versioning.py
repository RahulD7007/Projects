"""
versioning.py
─────────────
Model versioning engine.

Responsibilities
────────────────
• Assign a semantic version (v1, v2, …) to every trained model.
• Persist model binaries under ``models/registry/<model_name>/``.
• Maintain a JSON registry (``models/registry/model_registry.json``)
  that records metadata for every registered model.
• Provide helpers to list, load, and promote models to "champion" status.

Registry schema (model_registry.json)
──────────────────────────────────────
{
  "models": {
    "random_forest": {
      "champion": "v2",
      "versions": {
        "v1": {
          "version":    "v1",
          "model_name": "random_forest",
          "artifact":   "models/registry/random_forest/random_forest_v1.joblib",
          "roc_auc":    0.8851,
          "pr_auc":     0.8271,
          "accuracy":   0.8792,
          "f1_score":   0.7634,
          "trained_at": "2024-01-15T10:30:00",
          "n_train":    118936,
          "n_test":     29734,
          "params":     { ... }
        }
      }
    }
  }
}
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib

from src.config import MODELS_DIR
from src.logger import get_logger

logger = get_logger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
REGISTRY_DIR: Path = MODELS_DIR / "registry"
REGISTRY_FILE: Path = REGISTRY_DIR / "model_registry.json"
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _load_registry() -> dict:
    """Load the JSON registry; return empty scaffold if absent."""
    if not REGISTRY_FILE.exists():
        return {"models": {}}
    with REGISTRY_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_registry(registry: dict) -> None:
    """Persist the registry dict to disk as formatted JSON."""
    with REGISTRY_FILE.open("w", encoding="utf-8") as fh:
        json.dump(registry, fh, indent=2)
    logger.debug("Registry persisted → %s", REGISTRY_FILE)


def _next_version(existing_versions: dict) -> str:
    """
    Derive the next semantic version string.

    Parameters
    ----------
    existing_versions : dict
        Mapping of ``{"v1": {...}, "v2": {...}}`` from the registry.

    Returns
    -------
    str
        Next version tag, e.g. ``"v3"``.
    """
    if not existing_versions:
        return "v1"
    latest = max(int(v.lstrip("v")) for v in existing_versions)
    return f"v{latest + 1}"


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def register_model(
    model: object,
    model_name: str,
    metrics: dict[str, float],
    params: dict[str, Any],
    n_train: int,
    n_test: int,
    promote_to_champion: bool = False,
) -> str:
    """
    Register a trained model in the versioned registry.

    Performs three actions:
    1. Assigns the next version tag (v1, v2, …).
    2. Serializes the model binary to
       ``models/registry/<model_name>/<model_name>_<version>.joblib``.
    3. Updates ``model_registry.json`` with full metadata.

    Parameters
    ----------
    model : object
        Fitted scikit-learn / XGBoost compatible estimator.
    model_name : str
        Logical model name key (e.g. ``"random_forest"``).
    metrics : dict[str, float]
        Evaluation metrics dict with keys:
        ``roc_auc``, ``pr_auc``, ``accuracy``, ``f1_score``.
    params : dict[str, Any]
        Hyper-parameter dict used for this run.
    n_train : int
        Number of training samples used.
    n_test : int
        Number of test samples used for evaluation.
    promote_to_champion : bool
        If True, mark this version as the current champion.

    Returns
    -------
    str
        The assigned version tag (e.g. ``"v2"``).
    """
    registry = _load_registry()

    # Ensure model entry exists
    if model_name not in registry["models"]:
        registry["models"][model_name] = {
            "champion": None,
            "versions": {},
        }

    model_entry = registry["models"][model_name]
    version = _next_version(model_entry["versions"])

    # ── Persist model binary ──────────────────────────────────────────────────
    model_dir = REGISTRY_DIR / model_name
    model_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = model_dir / f"{model_name}_{version}.joblib"
    joblib.dump(model, artifact_path, compress=3)
    logger.info(
        "Model artifact saved → %s (version=%s)",
        artifact_path,
        version,
    )

    # ── Build metadata record ─────────────────────────────────────────────────
    record: dict[str, Any] = {
        "version":    version,
        "model_name": model_name,
        "artifact":   str(artifact_path),
        "trained_at": datetime.now().isoformat(timespec="seconds"),
        "n_train":    n_train,
        "n_test":     n_test,
        "params":     params,
        **metrics,   # roc_auc, pr_auc, accuracy, f1_score
    }

    model_entry["versions"][version] = record

    # ── Champion promotion ────────────────────────────────────────────────────
    if promote_to_champion or model_entry["champion"] is None:
        model_entry["champion"] = version
        logger.info(
            "Model '%s' champion promoted → %s (ROC-AUC: %.4f)",
            model_name,
            version,
            metrics.get("roc_auc", 0.0),
        )

    _save_registry(registry)
    logger.info(
        "Registered '%s' %s | ROC-AUC=%.4f | PR-AUC=%.4f",
        model_name,
        version,
        metrics.get("roc_auc", 0.0),
        metrics.get("pr_auc", 0.0),
    )
    return version


def load_champion_model(model_name: str) -> object:
    """
    Load the current champion version of a registered model.

    Parameters
    ----------
    model_name : str
        Logical model name (e.g. ``"random_forest"``).

    Returns
    -------
    object
        Deserialized fitted estimator.

    Raises
    ------
    KeyError
        If the model name is not found in the registry.
    FileNotFoundError
        If the champion artifact file is missing from disk.
    """
    registry = _load_registry()

    if model_name not in registry["models"]:
        raise KeyError(
            f"Model '{model_name}' not found in registry. "
            f"Available: {list(registry['models'].keys())}"
        )

    champion_ver = registry["models"][model_name]["champion"]
    if champion_ver is None:
        raise KeyError(f"No champion set for model '{model_name}'.")

    artifact_path = Path(
        registry["models"][model_name]["versions"][champion_ver]["artifact"]
    )

    if not artifact_path.exists():
        raise FileNotFoundError(
            f"Champion artifact not found at '{artifact_path}'."
        )

    logger.info(
        "Loaded champion '%s' %s from '%s'",
        model_name,
        champion_ver,
        artifact_path,
    )
    return joblib.load(artifact_path)


def load_model_version(model_name: str, version: str) -> object:
    """
    Load a specific version of a registered model.

    Parameters
    ----------
    model_name : str
        Logical model name.
    version : str
        Version tag (e.g. ``"v1"``).

    Returns
    -------
    object
        Deserialized fitted estimator.
    """
    registry = _load_registry()

    try:
        artifact_path = Path(
            registry["models"][model_name]["versions"][version]["artifact"]
        )
    except KeyError as exc:
        raise KeyError(
            f"Version '{version}' of model '{model_name}' not found."
        ) from exc

    logger.info("Loaded '%s' %s", model_name, version)
    return joblib.load(artifact_path)


def get_all_versions(model_name: str) -> dict:
    """
    Retrieve all version metadata for a registered model.

    Parameters
    ----------
    model_name : str
        Logical model name.

    Returns
    -------
    dict
        Mapping ``{version_tag: metadata_dict}``.
    """
    registry = _load_registry()
    return registry.get("models", {}).get(model_name, {}).get("versions", {})


def get_registry_summary() -> dict:
    """
    Return the full registry dictionary.

    Returns
    -------
    dict
        Complete registry content.
    """
    return _load_registry()


def promote_champion(model_name: str, version: str) -> None:
    """
    Manually promote a specific version to champion status.

    Parameters
    ----------
    model_name : str
        Logical model name.
    version : str
        Version tag to promote.
    """
    registry = _load_registry()

    if model_name not in registry["models"]:
        raise KeyError(f"Model '{model_name}' not in registry.")

    if version not in registry["models"][model_name]["versions"]:
        raise KeyError(
            f"Version '{version}' not found for model '{model_name}'."
        )

    old_champion = registry["models"][model_name]["champion"]
    registry["models"][model_name]["champion"] = version
    _save_registry(registry)

    logger.info(
        "Champion updated: '%s'  %s → %s",
        model_name,
        old_champion,
        version,
    )


def delete_model_version(model_name: str, version: str) -> None:
    """
    Remove a model version from the registry AND delete its artifact.

    Parameters
    ----------
    model_name : str
        Logical model name.
    version : str
        Version tag to delete.

    Raises
    ------
    ValueError
        If the version is currently the champion (must demote first).
    """
    registry = _load_registry()

    if model_name not in registry["models"]:
        raise KeyError(f"Model '{model_name}' not in registry.")

    model_entry = registry["models"][model_name]

    if model_entry["champion"] == version:
        raise ValueError(
            f"Cannot delete champion version '{version}'. "
            "Promote another version first via promote_champion()."
        )

    if version not in model_entry["versions"]:
        raise KeyError(
            f"Version '{version}' not found for model '{model_name}'."
        )

    # Delete artifact from disk
    artifact_path = Path(model_entry["versions"][version]["artifact"])
    if artifact_path.exists():
        artifact_path.unlink()
        logger.info("Deleted artifact: %s", artifact_path)

    del model_entry["versions"][version]
    _save_registry(registry)
    logger.info("Deleted '%s' %s from registry.", model_name, version)
