--- Essential SQL Queries for Data Analysts

-- 1. SELECT:- USED TO SELECT DATA FROM A DATABASE.

   SELECT * FROM STUDENT;
   
-- Note:- 1) If you fetch all rows & columns then 
       
              SELECT * FROM STUDENT;
              
--        2) If you want to fetch certain columns then 

              SELECT STUID,FNAME,CITY FROM STUDENT;            

   
-- 2. FROM:- SPECIFIES THE TABLE TO SELECT OR DELETE DATA FROM. 

   SELECT FNAME FROM STUDENT;  
   
-- 3. WHERE:- FILTERS RECORDS.

    SELECT * FROM EMPLOYEE
    WHERE SALARY > 800000;
    
-- 4. INSERT:- INSERTS NEW DATA INTO A TABLE.

    INSERT INTO STUDENT VALUES(1001,'Ankit','Pandey','Pune');

-- 5. UPDATE:- MODIFIES EXISTING DATA IN A TABLE.

    UPDATE EMPLOYEE SET SALARY = 800000
    WHERE FIRST_NAME = 'TOM';
   
    SELECT * FROM EMPLOYEE;
    
    UPDATE STUDENT SET Contact_no = 9511255655; 
    
    Rollback;
    
-- 6. DELETE:- DELETES DATA FROM A TABLE.

    DELETE FROM STUDENT
    WHERE CITY = 'Yavatmal'; 
    
    SELECT * FROM STUDENT;
    
    Rollback;   
    
-- 7. CREATE TABLE:- CREATES A NEW TABLE.

CREATE TABLE EMPLOYEE
  (
    EMP_ID NUMBER,
    FIRST_NAME VARCHAR2(50),
    LAST_NAME VARCHAR2(50),
    SALARY NUMBER,
    JOINING_DATE DATE,
    DEPARTMENT VARCHAR2(30)
   );    
   
-- 8. DROP TABLE:- DELETES A TABLE.
   
   DROP TABLE STUDENT;
    
   Rollback;

-- 9. TRUNCATE TABLE:- It is used to remove all rows from a table quickly and efficiently, 
--     while keeping the table's structure (schema, columns, and constraints) intact. 

   TRUNCATE TABLE STUDENT;
    
   Rollback;

-- 10. ALTER TABLE:- MODIFIES AN EXISTING TABLE.

   ALTER TABLE STUDENT 
   ADD (DOB  DATE, email VARCHAR2(30) ); 
   
   ALTER TABLE STUDENT 
   ADD Contact_no NUMBER; 
   
   SELECT * FROM STUDENT;
   
   Rollback;
   
-- 11. DISTINCT:- SELECTS ONLY DISTINCT (DIFFERENT) VALUES.

  SELECT DISTINCT DEPARTMENT FROM EMPLOYEE;
  
-- 12. LIMIT:- SPECIFIES THE NUMBER OF RECORDS TO RETURN.  

  SELECT * FROM EMPLOYEE
  LIMIT 3;

-- 13. Primary Key/ NOT NULL UNIQUE:- It is used to uniquely identify each record in a table, preventing duplicate or NULL values in 
-- the specified column(s). PRIMARY KEY in SQL is a column (or group of columns) that uniquely identifies the records 
-- in that table. So, it can be on a single column or a group of columns.  A primary key must contain unique values 
-- and can not have any NULL value. Each table can have only ONE primary key. A primary key automatically has a 
-- UNIQUE constraint defined on it, and it ensures that there are no duplicate or NULL values in that column.

  CREATE TABLE STUDENT
  ( STUID   NUMBER PRIMARY KEY, 
    FNAME   VARCHAR2(20), 
    LNAME   VARCHAR2(20), 
    CITY    VARCHAR2(10)  
   ); 
 
   SELECT * FROM STUDENT;
  
-- OR
  
  CREATE TABLE STUDENT
  ( STUID   NUMBER, 
    FNAME   VARCHAR2(20), 
    LNAME   VARCHAR2(20), 
    CITY    VARCHAR2(10),
    PRIMARY KEY (STUID)
   ); 
  
  SELECT * FROM STUDENT;

-- 14. Foreign Key:- is a concept in SQL that enforces a valid relationship between two tables by ensuring that 
-- the values stored in the child table correspond to existing values in the parent table. Ensures child table 
-- values match valid primary keys in parent table. It Keeps table relationships consistent by enforcing 
-- referential integrity rules.It ensures only existing student IDs can be used in the courses table.

 CREATE TABLE STUDENT
  ( STUID   NUMBER PRIMARY KEY, 
    FNAME   VARCHAR2(20), 
    LNAME   VARCHAR2(20), 
    CITY    VARCHAR2(10)  
   ); 
 
 SELECT * FROM STUDENT;
    
 CREATE TABLE SEM1 
  (  STUD_info   NUMBER PRIMARY KEY, 
     SUB1  NUMBER, 
     SUB2  NUMBER, 
     SUB3  NUMBER, 
     SUB4  NUMBER, 
     FOREIGN KEY(STUD_info) REFERENCES STUDENT(STUID) 
   ) 
 
 SELECT * FROM SEM1;    


INNER JOIN:- RETURNS RECORDS WITH MATCHING VALUES IN BOTH TABLES.   
