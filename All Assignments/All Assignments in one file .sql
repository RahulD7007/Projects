
-----------------------------  Assignments given on 21 Dec 2025  ------------------------------------------------------------------------------------------------

--- 1. Write create table syntax for employee table

CREATE TABLE EMPLOYEE
(
 Emp_id NUMBER,
 FIRST_NAME VARCHAR2(100),
 LAST_NAME VARCHAR2(100),
 SALARY VARCHAR2(50),
 JOINING_DATE DATE,
 DEPARTMENT VARCHAR2(100)
 );

select * from EMPLOYEE;

insert into EMPLOYEE values(1,'JOHN','ABRAHAM','1000000','01-JAN-13','BANKING');
insert into EMPLOYEE values(2,'MICHAEL','CLARKE','800000','01-JAN-13','INSURANCE');
insert into EMPLOYEE values(3,'ROY','THOMAS','700000','01-FEB-13','BANKING');
insert into EMPLOYEE values(4,'TOM','JOSE','600000','01-FEB-13','INSURANCE');
insert into EMPLOYEE values(5,'JERRY','PINTO','650000','01-FEB-13','INSURANCE');
insert into EMPLOYEE values(6,'PHILIP','MATHEW','750000','01-JAN-13','SERVICES');


--- 2. Write create table syntax for Incentive table

CREATE TABLE EMPLOYEE
(
 Emp_id NUMBER PRIMARY KEY,
 FIRST_NAME VARCHAR2(100) NOT NULL,
 LAST_NAME VARCHAR2(100),
 SALARY VARCHAR2(50),
 JOINING_DATE DATE,
 DEPARTMENT VARCHAR2(100)
 );
 

CREATE TABLE INCENTIVES
(
 Employee_ref_id NUMBER PRIMARY KEY,
 Incentive_date DATE,
 Incentive_amount NUMBER,
 foreign key(Employee_ref_id) REFERENCES EMPLOYEE(Emp_id)
);

SELECT * FROM EMPLOYEE;

SELECT * FROM INCENTIVES;

insert into EMPLOYEE values(1,'JOHN','ABRAHAM','1000000','01-JAN-13','BANKING');
insert into EMPLOYEE values(2,'MICHAEL','CLARKE','800000','01-JAN-13','INSURANCE');
insert into EMPLOYEE values(3,'ROY','THOMAS','700000','01-FEB-13','BANKING');
insert into EMPLOYEE values(4,'TOM','JOSE','600000','01-FEB-13','INSURANCE');
insert into EMPLOYEE values(5,'JERRY','PINTO','650000','01-FEB-13','INSURANCE');
insert into EMPLOYEE values(6,'PHILIP','MATHEW','750000','01-JAN-13','SERVICES');


insert into INCENTIVES values (1,'01-FEB-13',5000);
insert into INCENTIVES values (2,'01-FEB-13',3000);
insert into INCENTIVES values (3,'01-FEB-13',4000);
insert into INCENTIVES values (4,'01-JAN-13',4500);
insert into INCENTIVES values (5,'01-JAN-13',3500);

--- 3. Get all employee details from the employee table

SELECT * FROM EMPLOYEE;


--- 4.Get First_Name,Last_Name from employee table

SELECT FIRST_NAME,LAST_NAME FROM EMPLOYEE;


SELECT * FROM EMPLOYEE;

SELECT Emp_id, FIRST_NAME ||' '|| LAST_NAME as full_name FROM EMPLOYEE;

--- 5.	Get First_Name from employee table using alias name “Employee Name”

SELECT FIRST_NAME AS "Employee Name"
FROM employee;

--- 6.	Get First_Name from employee table in upper case

SELECT UPPER(first_name) AS first_name
FROM employee;

--- 7.	Select first 3 characters of FIRST_NAME from EMPLOYEE

SELECT SUBSTR(first_name, 1, 3) AS first_3_chars
FROM employee;

--- 8.	Get position of 'o' in name 'John' from employee table


SELECT INSTR(first_name, 'o') AS position_of_o
FROM EMPLOYEE
WHERE first_name = 'John';

--- 9.	Get FIRST_NAME from employee table after removing white spaces from right side.

SELECT TRIM(first_name) AS first_name
FROM employee;

--- 10.	Get First_Name from employee table after replacing 'o' with '$'

SELECT REPLACE(first_name, 'o', '$') AS first_name
FROM employee;

--- 11.	Get First_Name and Last_Name as single column from employee table separated by a '_'

SELECT first_name || '_' || last_name AS full_name
FROM employee;

--- 12.	Get FIRST_NAME, Joining year, Joining Month and Joining Date from employee table

SELECT first_name,
EXTRACT(YEAR  FROM joining_date) AS joining_year,
EXTRACT(MONTH FROM joining_date) AS joining_month,
EXTRACT(DAY   FROM joining_date) AS joining_date
FROM employee;

--- 13.	Get all employee details from the employee table order by First_Name Ascending

SELECT * FROM employee
ORDER BY first_name ASC;

--- 14.	Get all employee details from the employee table order by First_Name Ascending and Salary Descending?

SELECT * FROM employee
ORDER BY first_name ASC, salary DESC;

--- 15.	Get employee details from employee table whose employee name is “John”

SELECT * FROM employee
WHERE first_name = 'John';

--- 16.	Get employee details from employee table whose employee name are “John” and “Roy”

SELECT * FROM employee
WHERE first_name IN ('John', 'Roy');

--- 17.	Get employee details from employee table whose employee name are not “John” and “Roy”.

SELECT * FROM employee
WHERE first_name NOT IN ('John', 'Roy');

SELECT * FROM employee
WHERE first_name <> 'John' AND first_name <> 'Roy';


--- 18.	Get employee details from employee table whose first name starts with 'J'.

SELECT * FROM employee
WHERE first_name LIKE 'J%';

--- 19.	Get employee details from employee table whose first name contains 'o'.

SELECT * FROM employee
WHERE first_name LIKE '%o%';

--- 20.	Get employee details from employee table whose first name ends with 'n'.

SELECT * FROM employee
WHERE first_name LIKE '%n';

--- 21.	Get employee details from employee table whose first name ends with 'n' and name contains 4 letters.

SELECT * FROM employee
WHERE first_name LIKE '___n';

--- 22.	Get employee details from employee table whose first name starts with 'J' and name contains 4 letters.

SELECT * FROM employee
WHERE first_name LIKE 'J___';

--- 23.	Get employee details from employee table who’s Salary greater than 600000.

SELECT * FROM employee
WHERE salary > 600000;

--- 24.	Get employee details from employee table whose joining year is “2013”.

SELECT * FROM employee
WHERE EXTRACT(YEAR FROM joining_date) = 2013;

--- 25.	Get employee details from employee table whose joining month is “January”.

SELECT * FROM employee
WHERE TO_CHAR(joining_date, 'MONTH') = 'JANUARY';

--- 26.	Get employee details from employee table who joined before January 1st 2013.

SELECT * FROM employee
WHERE joining_date < DATE '2013-01-01';

--- 27.	Get employee details from employee table who joined after January 31st

SELECT * FROM employee
WHERE joining_date > DATE '2013-01-31';

--- 28.	Get Joining Date and Time from employee table

SELECT TO_CHAR(joining_date, 'DD-MON-YYYY HH24:MI:SS') AS joining_date_time
FROM employee;

--- 29.	Get Joining Date, Time including milliseconds from employee table

SELECT TO_CHAR(joining_date,'DD-MON-YYYY HH24:MI:SS.FF3') AS joining_date_time FROM employee;

--- 30.	Get difference between JOINING_DATE and INCENTIVE_DATE from employee and incentives table.

SELECT e.emp_id,
       e.first_name,
       i.incentive_date - e.joining_date AS days_difference
FROM employee e
JOIN incentive i
  ON e.emp_id = i.emp_id;
 
--- 31. Get department, total salary with respect to a department from employee table.

SELECT DEPARTMENT , SUM(SALARY) AS TOTAL_SALARY FROM EMPLOYEE 
GROUP BY DEPARTMENT;

--- 32.	Get department, total salary with respect to a department from employee table order by total salary descending.

SELECT department,SUM(salary) AS total_salary FROM employee
GROUP BY department
ORDER BY total_salary DESC;

--- 33.	Get department, no of employees in a department, total salary with respect to a department from employee table order by total salary descending.

SELECT department,
       COUNT(*)      AS no_of_employees,
       SUM(salary)   AS total_salary
FROM employee
GROUP BY department
ORDER BY total_salary DESC;

--- 34.	Get department wise average salary from employee table order by salary ascending?















---- Assignments on SALES, CUSTOMERS & ORDERS

CREATE TABLE Salespeople(
Snum_PK   NUMBER(10)    PRIMARY KEY,
Sname     VARCHAR2(10)  NOT NULL,
City      VARCHAR2(15)  NOT NULL,
Comm      DECIMAL(3,2)  NOT NULL
); 
 

CREATE TABLE Customers(
Cnum_PK   NUMBER(10)    PRIMARY KEY,
Cname     VARCHAR2(50)  NOT NULL,
City      VARCHAR2(50)  NOT NULL,
Rating    NUMBER(10),
Snum_FK   NUMBER(10),
FOREIGN KEY(Snum_FK) REFERENCES Salespeople(Snum_PK)
);


CREATE TABLE Orders(
Onum_PK   NUMBER(10)    PRIMARY KEY,
Amt       DECIMAL(10,2)  NOT NULL,
Odate     DATE        NOT NULL,
Cnum_FK   NUMBER(10),
Snum_FK   NUMBER(10),

FOREIGN KEY(Cnum_FK) REFERENCES Customers(Cnum_PK),
FOREIGN KEY(Snum_FK) REFERENCES Salespeople(Snum_PK)
);


SELECT * FROM Salespeople;

SELECT * FROM Customers;

SELECT * FROM Orders;


INSERT INTO Salespeople(Snum_PK,Sname,City,Comm) Values(1001,'Peel','London', .12);
INSERT INTO Salespeople(Snum_PK,Sname,City,Comm) Values(1002,'Serres','San Jose', .13);
INSERT INTO Salespeople(Snum_PK,Sname,City,Comm) Values(1004,'Monika','London', .11);
INSERT INTO Salespeople(Snum_PK,Sname,City,Comm) Values(1007,'Rifkin','Barcelona', .15);
INSERT INTO Salespeople(Snum_PK,Sname,City,Comm) Values(1003,'Axelrod','New York', .10);
INSERT INTO Salespeople(Snum_PK,Sname,City,Comm) Values(1005,'Franc','London', .26);

SELECT * FROM Customers;
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2001,'Hoffman','London',100,1001);
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2002,'Giovanni','ROME',200,1003);
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2003,'Liu','San Jose',200,1002);
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2004,'Grass','Berlin',300,1002);
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2006,'Clemens','London',100,1001);
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2008,'Cisneros','San Jos',300,1007);
INSERT INTO Customers(Cnum_PK,Cname,City,Rating,Snum_FK) Values(2007,'Pereira','Rome',100,1004);

SELECT * FROM Orders;
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3001,18.69,'03-OCT-96',2008,1007);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3003,767.19,'03-OCT-96',2001,1001);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3002,1900.10,'03-OCT-96',2007,1004);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3005,5160.45,'03-OCT-96',2003,1002);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3006,1098.16,'03-OCT-96',2008,1007);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3009,1713.23,'04-OCT-96',2002,1003);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3007,75.75,'04-OCT-96',2002,1003);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3008,4723.00,'05-OCT-96',2006,1001);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3010,1309.95,'06-OCT-96',2004,1002);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3011,9891.88,'06-OCT-96',2006,1001);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3012,3455.78,'04-OCT-96',2002,1003);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3013,1245.98,'04-OCT-96',2002,1003);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3014,3721.53,'05-OCT-96',2006,1001);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3015,734.50,'06-OCT-96',2004,1002);
INSERT INTO Orders(Onum_PK,Amt,Odate,Cnum_FK,Snum_FK) Values(3016,1729.67,'06-OCT-96',2006,1001);

----------------------------------------------------------------------------------------------------------------------------------------------------
