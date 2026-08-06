import oracledb

def get_connection():
    return oracledb.connect(
        user="bank_modern",
        password="bank",
        dsn="localhost:1521/XEPDB1"
    )