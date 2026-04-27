-- Step 1: Connect as SYSDBA before running this
-- sqlplus / as sysdba

-- Step 2: Switch to PDB (IMPORTANT)
--ALTER SESSION SET CONTAINER = XEPDB1;

-- Step 3: Create User
CREATE USER bank IDENTIFIED BY bank;

-- Step 4: Grant Privileges
GRANT CREATE SESSION TO bank;
GRANT CREATE TABLE TO bank;
GRANT CREATE VIEW TO bank;
GRANT CREATE SEQUENCE TO bank;

-- Step 5: Tablespace
ALTER USER bank 
DEFAULT TABLESPACE users 
QUOTA UNLIMITED ON users;

---------------------------------------------------
-- Step 6: Login as BANK user
-- CONNECT bank/bank;

---------------------------------------------------
-- Step 7: CREATE TABLES
---------------------------------------------------

-- CUSTOMERS TABLE
CREATE TABLE customers (
    customer_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    phone VARCHAR2(15),
    email VARCHAR2(100),
    created_at DATE DEFAULT SYSDATE
);

-- ADDRESS TABLE
CREATE TABLE address (
    address_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    city VARCHAR2(50),
    state VARCHAR2(50),
    pincode NUMBER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ACCOUNTS TABLE
CREATE TABLE accounts (
    account_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    account_type VARCHAR2(20),
    balance NUMBER(12,2),
    created_at DATE DEFAULT SYSDATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- FD TABLE (Fixed Deposit)
CREATE TABLE fd (
    fd_id NUMBER PRIMARY KEY,
    account_id NUMBER,
    amount NUMBER(12,2),
    interest_rate NUMBER(5,2),
    start_date DATE,
    maturity_date DATE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- LOANS TABLE
CREATE TABLE loans (
    loan_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    loan_amount NUMBER(12,2),
    interest_rate NUMBER(5,2),
    loan_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
    transaction_id NUMBER PRIMARY KEY,
    account_id NUMBER,
    amount NUMBER(12,2),
    transaction_type VARCHAR2(10),
    transaction_date DATE DEFAULT SYSDATE,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- ADMIN TABLE
CREATE TABLE admin (
    admin_id NUMBER PRIMARY KEY,
    username VARCHAR2(50),
    password VARCHAR2(50)
);

-- ACCOUNTS_FD TABLE (Mapping)
CREATE TABLE accounts_fd (
    account_id NUMBER,
    fd_id NUMBER,
    PRIMARY KEY (account_id, fd_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (fd_id) REFERENCES fd(fd_id)
);

-- ACCOUNTS_LOANS TABLE (Mapping)
CREATE TABLE accounts_loans (
    account_id NUMBER,
    loan_id NUMBER,
    PRIMARY KEY (account_id, loan_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

---------------------------------------------------
-- Step 8: Verify Tables
---------------------------------------------------
SELECT table_name FROM user_tables;

---------------------------------------------------
-- Step 9: Sample Data (Optional)
---------------------------------------------------

INSERT INTO customers VALUES (1, 'Rahul', '9876543210', 'rahul@gmail.com', SYSDATE);

INSERT INTO accounts VALUES (101, 1, 'SAVINGS', 5000, SYSDATE);

INSERT INTO transactions VALUES (1001, 101, 1000, 'DEPOSIT', SYSDATE);

COMMIT;

---------------------------------------------------
-- Step 10: Test Queries
---------------------------------------------------

SELECT * FROM customers;
SELECT * FROM accounts;
SELECT * FROM transactions;