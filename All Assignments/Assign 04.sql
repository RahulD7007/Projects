CREATE TABLE EMPLOYEE_T
(
       Employee_id NUMBER,
       Full_Name VARCHAR2(100),
       SALARY NUMBER,
       Hire_Date DATE
);

SELECT * FROM EMPLOYEE_T;

INSERT INTO EMPLOYEE_T VALUES(100,'S.KING',24000,TO_DATE('06/17/2003','MM/DD/YYYY'));
INSERT INTO EMPLOYEE_T VALUES(116,'S.Baida',2900,TO_DATE('12/24/2005','MM/DD/YYYY'));
INSERT INTO EMPLOYEE_T VALUES(117,'S.Tobias',2800,TO_DATE('07/24/2005','MM/DD/YYYY'));
INSERT INTO EMPLOYEE_T VALUES(123,'S.Vollman',6500,TO_DATE('10/10/2005','MM/DD/YYYY'));
INSERT INTO EMPLOYEE_T VALUES(128,'S.Markle',2200,TO_DATE('03/08/2008','MM/DD/YYYY'));
INSERT INTO EMPLOYEE_T VALUES(138,'S.Stiles',3200,TO_DATE('10/26/2005','MM/DD/YYYY'));
INSERT INTO EMPLOYEE_T VALUES(161,'S.Sewall',7000,TO_DATE('11/03/2006','MM/DD/YYYY'));

-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
CREATE TABLE JOB_DETAIL
(
       Job_Title  VARCHAR2(100),
       Employees NUMBER,
       Managers  NUMBER       
);

SELECT * FROM JOB_DETAIL;

INSERT INTO JOB_DETAIL VALUES('Accountant',5,1);
INSERT INTO JOB_DETAIL VALUES('Accounting Manager',1,1);
INSERT INTO JOB_DETAIL VALUES('Administration Assistant',1,1);
INSERT INTO JOB_DETAIL VALUES('Administration Vice President',2,1);
INSERT INTO JOB_DETAIL VALUES('Finance Manager',1,1);
INSERT INTO JOB_DETAIL VALUES('Human Resources Representative',1,1);
INSERT INTO JOB_DETAIL VALUES('Marketing Manager',1,1);
INSERT INTO JOB_DETAIL VALUES('Sales Representative',30,5);
INSERT INTO JOB_DETAIL VALUES('Shipping Clerk',20,5);
INSERT INTO JOB_DETAIL VALUES('Stock Clerk',20,5);

-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
CREATE TABLE EMPLOYEE_T1
(
       EMP_ID NUMBER,
       Last_Name VARCHAR2(30),
       Weeks NUMBER,
       Months NUMBER,
       Year NUMBER       
);

SELECT * FROM EMPLOYEE_T1;

INSERT INTO EMPLOYEE_T1 VALUES(100,'King',24,166,14);
INSERT INTO EMPLOYEE_T1 VALUES(101,'Kochhar',20,139,12);
INSERT INTO EMPLOYEE_T1 VALUES(102,'De Haan',28,195,16);
INSERT INTO EMPLOYEE_T1 VALUES(103,'Hunold',19,136,11);
INSERT INTO EMPLOYEE_T1 VALUES(104,'Ernst',17,119,10);
INSERT INTO EMPLOYEE_T1 VALUES(105,'Austin',20,142,12);

-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------

CREATE TABLE EMPLOYEE_T2
(
       EM_ID NUMBER,
       FULL_NAME VARCHAR2(30),
       Email VARCHAR2(100),
       Salary VARCHAR2(100)   
);

SELECT * FROM EMPLOYEE_T2;


INSERT INTO EMPLOYEE_T2 VALUES(100,'Steven King','sking@gmail.com','$24,000');
INSERT INTO EMPLOYEE_T2 VALUES(101,'Neena Kochhar','nkochhar@gmail.com','$20,000');
INSERT INTO EMPLOYEE_T2 VALUES(102,'Lex De Haan','ldehaan@gmail.com','$17,000');
INSERT INTO EMPLOYEE_T2 VALUES(103,'Alexander Hunold','ahunold@gmail.com','$9,000');
INSERT INTO EMPLOYEE_T2 VALUES(104,'Bruce Ernst','bernst@gmail.com','$6,000');
INSERT INTO EMPLOYEE_T2 VALUES(105,'David Austin','daustin@gmail.com','$4,800');
INSERT INTO EMPLOYEE_T2 VALUES(106,'Valli Pataballa','vpatabal@gmail.com','$4,800');

-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------

CREATE TABLE EMPLOYEE_T3
(
       Manager_ID NUMBER,
       Fullname VARCHAR2(30),
       Number_Of_Employees NUMBER   
);

SELECT * FROM EMPLOYEE_T3;

INSERT INTO EMPLOYEE_T3 VALUES(100,'Steven King',14);
INSERT INTO EMPLOYEE_T3 VALUES(120,'Matthew Weiss',8);
INSERT INTO EMPLOYEE_T3 VALUES(121,'Adam Fripp',8);
INSERT INTO EMPLOYEE_T3 VALUES(122,'Payam Kaufling',8);
INSERT INTO EMPLOYEE_T3 VALUES(123,'Shanta Vollman',8);
-----------------------------------------------------------------------------------------------------

CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name  VARCHAR2(30),
    last_name   VARCHAR2(30)
);

SELECT * FROM employees;

INSERT INTO employees VALUES (1, 'Ellen', 'Abel');
INSERT INTO employees VALUES (2, 'Sundar', 'Ande');
INSERT INTO employees VALUES (3, 'Mozhe', 'Atkinson');
INSERT INTO employees VALUES (4, 'David', 'Austin');
INSERT INTO employees VALUES (5, 'Hermann', 'Baer');
INSERT INTO employees VALUES (6, 'Shelli', 'Baida');
INSERT INTO employees VALUES (7, 'Amit', 'Banda');
INSERT INTO employees VALUES (8, 'Elizabeth', 'Bates');
-------------------------------------------------------------------------------------------------------

CREATE TABLE employee_experience (
    employee_id NUMBER PRIMARY KEY,
    last_name   VARCHAR2(30),
    weeks       NUMBER,
    months      NUMBER,
    years       NUMBER
);

 SELECT * FROM employee_experience;

INSERT INTO employee_experience VALUES (100, 'King',    24, 166, 14);
INSERT INTO employee_experience VALUES (101, 'Kochhar', 20, 139, 12);
INSERT INTO employee_experience VALUES (102, 'De Haan', 28, 195, 16);
INSERT INTO employee_experience VALUES (103, 'Hunold',  19, 136, 11);
INSERT INTO employee_experience VALUES (104, 'Ernst',   17, 119, 10);
INSERT INTO employee_experience VALUES (105, 'Austin',  20, 142, 12);


-- Q1: Write a query to display the Full name only those employees whose first name start with ‘S’ character.

        SELECT Full_Name FROM EMPLOYEE_T 
        WHERE Full_Name LIKE 'S%';

-- If this then, Write a query to display the Full name only those employees whose Last name start with ‘S’ character.

       SELECT Full_Name FROM EMPLOYEE_T
       WHERE SUBSTR(Full_Name, INSTR(Full_Name, '.') + 1, 1) = 'S';
       
-- Q2. Find the highest, lowest, sum, and average salary of all employees. Label the columns Maximum ,Minimum, Sum, and 
-- Average, respectively. Round your results to the nearest whole number. 

       SELECT ROUND(MAX(SALARY)) AS "Highest",
              ROUND(MIN(SALARY)) AS "Lowest",
              ROUND(SUM(SALARY)) AS "Sum",
              ROUND(AVG(SALARY)) AS "Average"
        FROM EMPLOYEE_T;

 
--Q3. Display following output . Employee Details
--------------------------------------------------------------------------------------
King earns $24,000.00 monthly but wants $72,000.00.
Kochhar earns $20,000.00 monthly but wants $60,000.00.
De Haan earns $17,000.00 monthly but wants $51,000.00.
Hunold earns $9,000.00 monthly but wants $27,000.00.
Ernst earns $6,000.00 monthly but wants $18,000.00.
Austin earns $4,800.00 monthly but wants $14,400.00.
-------------------------------------------------------------------------------------
--Option 01
       SELECT Full_Name||' '||'earns'||to_char(salary,'$99999.00')||' '||'but wants'||' '||(to_char(salary*3,'$99999.00'))
       FROM EMPLOYEE_T;

--Option 02
       SELECT SUBSTR(Full_Name, INSTR(Full_Name, ' ') + 1) ||' earns $' || TO_CHAR(salary, 'FM99,999,999.00') ||
        ' monthly but wants $' || TO_CHAR(salary * 3, 'FM99,999,999.00') || '.' AS employee_details
       FROM EMPLOYEE_T
       ORDER BY Employee_id;

-- Q4. Determine the number of managers without listing them. Label the column  Number of Managers 
--Hint: Use the MANAGER_ID column to determine the number of managers. 

    SELECT COUNT(DISTINCT Manager_ID) AS "Number of Managers" FROM EMPLOYEE_T3
    WHERE Manager_ID IS NOT NULL;

-- Q5. Find the difference between the highest and lowest salaries. Label the column DIFFERENCE

       SELECT MAX(SALARY) - MIN(SALARY) difference FROM EMPLOYEE_T;

-- Q6. Display how many employees joined in each month (Hint: Grouping by month and count the employees.
--      use TO_CHAR functions also)

       SELECT TO_CHAR(Hire_Date,'Month')month, count(Employee_id) FROM EMPLOYEE_T
       group by TO_CHAR(Hire_Date,'Month')
       order by month;

-- Q7. Display employee id , full name of employees and their hire date only those employees 
--     that has greater than 10 year experience in company.

       SELECT Employee_id,Full_Name, Hire_Date FROM EMPLOYEE_T
       WHERE (to_char(Hire_Date) < sysdate - 365*10);

-- Q8. Write a query to multiply  salary to commission and calculate the average salary of employees.
        Hint: Commission column contain null values

-- Q9.Write a query to display department_id and number of manager under the particular department 
--     exclude the null department. (Hint: Grouping on department id)-- Question is wrong.

       SELECT department_id,COUNT(manager_id) AS number_of_managers FROM departments
       WHERE department_id IS NOT NULL
       GROUP BY department_id;

-- Q10.Display job title and number of employees working those job and number of manager they perform job.

      SELECT COUNT(EMP_ID),COUNT(Manager_ID),j.Job_Title 
      FROM EMPLOYEE_T3 e
      WHERE e.Job_Title = j.Job_Title AND Manager_ID IS NOT NULL
      GROUP BY j.Job_Title;

-- Q11. Display employee full name and pad both side asterisk sing 10 time . Example 

   SELECT RPAD( LPAD(first_name || ' ' || last_name,
                LENGTH(first_name || ' ' || last_name) + 10,'*'),
                LENGTH(first_name || ' ' || last_name) + 20,'*') AS employee_name
   FROM employees;
   
-- Q12. Display following output. (Hint: Use Months_between Function)


SELECT  employee_id, last_name,
       FLOOR(MONTHS_BETWEEN(SYSDATE, hire_date) * 4)  AS weeks,
       FLOOR(MONTHS_BETWEEN(SYSDATE, hire_date))      AS months,
       FLOOR(MONTHS_BETWEEN(SYSDATE, hire_date) / 12) AS years
FROM employee_experience;
-----------------------------------------------------------------------------------------------------------------------
---- Assignment 5

-- Q1. Write a query to generate following output.

CREATE TABLE EMPLOYEE_T2
(
       EM_ID NUMBER,
       FULL_NAME VARCHAR2(30),
       Email VARCHAR2(100),
       Salary VARCHAR2(100)   
);

SELECT * FROM EMPLOYEE_T2;


INSERT INTO EMPLOYEE_T2 VALUES(100,'Steven King','sking@gmail.com','$24,000');
INSERT INTO EMPLOYEE_T2 VALUES(101,'Neena Kochhar','nkochhar@gmail.com','$20,000');
INSERT INTO EMPLOYEE_T2 VALUES(102,'Lex De Haan','ldehaan@gmail.com','$17,000');
INSERT INTO EMPLOYEE_T2 VALUES(103,'Alexander Hunold','ahunold@gmail.com','$9,000');
INSERT INTO EMPLOYEE_T2 VALUES(104,'Bruce Ernst','bernst@gmail.com','$6,000');
INSERT INTO EMPLOYEE_T2 VALUES(105,'David Austin','daustin@gmail.com','$4,800');
INSERT INTO EMPLOYEE_T2 VALUES(106,'Valli Pataballa','vpatabal@gmail.com','$4,800');

SELECT EM_ID,FULL_NAME,Email,Salary FROM EMPLOYEE_T2;

-- Q2. Write a query to display job_id and number of manager under particular job. Show only those jobs 
-- that have more than one manager.

CREATE TABLE job_managers (
    job_id   VARCHAR2(20),
    managers NUMBER
);

SELECT * FROM job_managers;

INSERT INTO job_managers VALUES ('IT_PROG', 3);
INSERT INTO job_managers VALUES ('SH_CLERK', 5);
INSERT INTO job_managers VALUES ('SA_REP', 5);
INSERT INTO job_managers VALUES ('ST_CLERK', 5);


SELECT job_id, COUNT(DISTINCT managers) AS managers FROM job_managers
WHERE managers IS NOT NULL
GROUP BY job_id
ORDER BY job_id;

-- Q3. Display the country name and number of employees those working in particular city that count of employee 
-- is greater than 30. (Hint: Using Equijoin and Group by )

SELECT count(employee_id),c.country_name
FROM employees e,departments d,locations l,countries c
WHERE e.department_id=d.department_id 
AND d.location_id=l.location_id
AND l.country_id=c.country_id
group by c.country_name
HAVING count(employee_id)>30;

--Q4. Q4. Display cities name and number of departments present those cities. And exculde departments there are 
--     no any employees.

SELECT l.city,count(d.department_id) from employees e,departments d,locations l
WHERE e.department_id=d.department_id 
AND d.location_id=l.location_id
AND employee_id is not null
group by l.city;

--Q5. Display the salary range and number of employees how are salary in between of range. 
--   (Hint : Job_Grade table , Equijoin , Group by )

SELECT
    CASE
        WHEN salary BETWEEN 1000 AND 2999 THEN '1000-2999'
        WHEN salary BETWEEN 3000 AND 4999 THEN '3000-4999'
        WHEN salary BETWEEN 5000 AND 9999 THEN '5000-9999'
        WHEN salary BETWEEN 10000 AND 14999 THEN '10000-14999'
        WHEN salary BETWEEN 15000 AND 19999 THEN '15000-19999'
        WHEN salary BETWEEN 20000 AND 25000 THEN '20000-25000'
        ELSE 'Above 25000'
    END AS salary_range,
    COUNT(*) AS number_of_employees
FROM employees
GROUP BY
    CASE
        WHEN salary BETWEEN 1000 AND 2999 THEN '1000-2999'
        WHEN salary BETWEEN 3000 AND 4999 THEN '3000-4999'
        WHEN salary BETWEEN 5000 AND 9999 THEN '5000-9999'
        WHEN salary BETWEEN 10000 AND 14999 THEN '10000-14999'
        WHEN salary BETWEEN 15000 AND 19999 THEN '15000-19999'
        WHEN salary BETWEEN 20000 AND 25000 THEN '20000-25000'
        ELSE 'Above 25000'
    END
ORDER BY salary_range;


--Q6. Display Year list and number of Employees join in particular year.
--    (Hint: Group by and To_Char Function)

SELECT to_char(hire_date,'yyyy'),count(employee_id)
FROM employees
group by to_char(hire_date,'yyyy')
order by 1;

--Q7. Display Manager_id , Manager Full Name and Under number of employees only those managers how have 
--    more than 5 employees under working. Result sort by manager_ID

SELECT e.manager_id,
       m.first_name || ' ' || m.last_name AS full_name,
       COUNT(*) AS number_of_employees
FROM employees e
JOIN employees m
  ON e.manager_id = m.employee_id
GROUP BY e.manager_id, m.first_name, m.last_name
ORDER BY number_of_employees DESC;
