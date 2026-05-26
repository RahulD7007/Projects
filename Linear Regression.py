# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:11:52 2026

@author: RAJE7007
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_csv(r"C:\Users\rahul\Downloads\EXCEL_DATA\Advertising.csv")
dataset

# Data Gathering
dataset.head()

dataset.describe()


# Data cleaning
# Null Values
dataset.isnull()

# Duplicates
print(dataset.duplicated().sum())


# Specific rows & Columns
dataset.loc[0:5, ["TV", "Sales"]]

sns.pairplot(dataset, x_vars=["TV", "Newspaper", "Radio"], y_vars = "Sales", kind = "scatter")


sns.heatmap(dataset.corr(), annot=True, cmap="coolwarm")
plt.show()

sns.heatmap(dataset.corr(), annot = True, cmap = "coolwarm")

# 1. Start model training
x = dataset[["TV"]]  # Feature Selection
y = dataset[["Sales"]]  # Target Variable

# 2. train test split
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2, random_state=100)

# 3. Import Linear Regression
from sklearn.linear_model import LinearRegression

lr = LinearRegression()

# 4. Train Model
lr.fit(x_train, y_train)

# 5. Check Intercept
lr.intercept_

# 6. Check Coefficients
lr.coef_

# 7. Predict on Test Data
y_pred = lr.predict(x_test)

# 8. View Predictions
y_pred


# 9. Import Metrics
from sklearn.metrics import mean_squared_error, r2_score

# 10. Calculate Mean Squared Error
mean_squared_error(y_test, y_pred)

# 11. Calculate R2 Square:-
r2_score(y_test, y_pred)


# 12. Plot Regression Line:-
import matplotlib.pyplot as plt
plt.scatter(x_test, y_test)

plt.plot(x_test, y_pred, color="red")

plt.xlabel("TV")
plt.ylabel("Sales")

plt.show()

# 13. Residuals
residuals = y_test - y_pred
residuals

# 15. Residual Plot:- 
import seaborn as sns
sns.histplot(residuals, kde=True)
