__author__ = 'user'
import oracledb

# Connect using service name
#con = oracledb.connect(
#    user="BANK",
#    password="bank",
#    dsn="localhost:1521/XEPDB1"   # host:port/service_name
#)

# Connect using service name
con = oracledb.connect(
    user="bank_modern",
    password="bank",
    dsn="localhost:1521/FREEPDB1"   # host:port/service_name
)

print("✅ Connected to Oracle 18c!")

cur = con.cursor()