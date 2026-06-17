
--1.  Write create table syntax for employee table and Incentive table.

--2.  Write syntax for insert data into table of employee table and Incentive table.

CREATE TABLE EMPLOYEE
(
       EMP_ID NUMBER,
       FIRST_NAME VARCHAR2(50),
       LAST_NAME VARCHAR2(50),
       SALARY NUMBER,
       JOINING_DATE DATE,
       DEPARTMENT VARCHAR2(30)
);

INSERT INTO EMPLOYEE VALUES(1,'John','Abraham',1000000,to_date('01/jan/13','dd/mon/yy'),'Banking');
INSERT INTO EMPLOYEE VALUES(2,'Michael','Clarke',800000,to_date('01/jan/13','dd/mon/yy'),'Insurance');
INSERT INTO EMPLOYEE VALUES(3,'Roy','Thomas',700000,to_date('01/feb/13','dd/mon/yy'),'Banking');
INSERT INTO EMPLOYEE VALUES(4,'Tom','Jose',600000,to_date('01/feb/13','dd/mon/yy'),'Insurance');
INSERT INTO EMPLOYEE VALUES(5,'Jerry','Pinto',650000,to_date('01/feb/13','dd/mon/yy'),'Insurance');
INSERT INTO EMPLOYEE VALUES(6,'Philip','Mathew',750000,to_date('01/jan/13','dd/mon/yy'),'Services');

SELECT * FROM EMPLOYEE;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE INCENTIVES
(
       EMPLOYEE_REF_ID NUMBER,
       INCENTIVE_DATE DATE,
       INCENTIVE_AMOUNT NUMBER
);

INSERT INTO INCENTIVES VALUES(1,to_date('01/Feb/13','dd/mon/yy'),5000);
INSERT INTO INCENTIVES VALUES(2,to_date('01/Feb/13','dd/mon/yy'),3000);
INSERT INTO INCENTIVES VALUES(3,to_date('01/Feb/13','dd/mon/yy'),4000);
INSERT INTO INCENTIVES VALUES(1,to_date('01/Jan/13','dd/mon/yy'),4500);
INSERT INTO INCENTIVES VALUES(2,to_date('01/Jan/13','dd/mon/yy'),3500);

SELECT * FROM INCENTIVES;

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

--3.  Get all employee details from the employee table

      SELECT * FROM EMPLOYEE;

--4.  Get First_Name, Last_Name from employee table

      SELECT FIRST_NAME,LAST_NAME FROM EMPLOYEE;

--5.  Get First_Name from employee table using alias name “Employee Name”

      SELECT FIRST_NAME AS Employee_Name FROM EMPLOYEE;

--6.  Get First_Name from employee table in upper case

      SELECT UPPER(FIRST_NAME) AS FIRST_NAME FROM EMPLOYEE;

--7.  Select First 3 characters of FIRST_NAME from EMPLOYEE

      SELECT FIRST_NAME,SUBSTR(FIRST_NAME,1,3)AS F_3_CHAR FROM EMPLOYEE;
      
--8.  Get position of 'o' in name 'John' from employee table.      
            
      SELECT INSTR(LOWER(first_name), 'o') AS position_of_o FROM employee
      WHERE LOWER(first_name) = 'john';
          
--9.  Get FIRST_NAME from employee table after removing white spaces from right side.

      SELECT RTRIM(FIRST_NAME) FIRST_NAME FROM EMPLOYEE;

--10. Get First_Name from employee table after replacing 'o' with '$'
           
      SELECT first_name, REPLACE(LOWER(first_name), 'o', '$') AS New_name FROM employee;

--11. Get First_Name and Last_Name as single column from employee table separated by a '_'

      SELECT FIRST_NAME ||'_'||LAST_NAME AS FULL_NAME FROM EMPLOYEE;

--12. Get FIRST_NAME, Joining year, Joining Month and Joining Date from employee table

      SELECT FIRST_NAME,
      EXTRACT(YEAR FROM JOINING_DATE) AS JOINING_YEAR,
      EXTRACT(MONTH FROM JOINING_DATE) AS JOINING_MONTH,
      EXTRACT(DAY FROM JOINING_DATE) AS JOINING_DATE 
      FROM EMPLOYEE;

--13. Get all employee details from the employee table order by First_Name Ascending

      SELECT * FROM EMPLOYEE
      ORDER BY FIRST_NAME;
      
-- OR
      
      SELECT * FROM EMPLOYEE
      ORDER BY FIRST_NAME ASC;

--14. Get all employee details from the employee table order by First_Name Ascending and Salary Descending?

      SELECT * FROM employee
      ORDER BY FIRST_NAME ASC, SALARY DESC;
      
--15. Get employee details from employee table whose employee name is “John”

      SELECT * FROM EMPLOYEE
      WHERE UPPER(FIRST_NAME)='JOHN';

--16. Get employee details from employee table whose employee name are “John” OR “Roy”

      SELECT * FROM EMPLOYEE
      WHERE UPPER(FIRST_NAME)='JOHN' OR UPPER(FIRST_NAME)='ROY';

--17. Get employee details from employee table whose employee name are not “John” and “Roy”.

      SELECT * FROM EMPLOYEE
      WHERE UPPER(FIRST_NAME)!='JOHN'
      AND UPPER(FIRST_NAME)!='ROY';

--18. Get employee details from employee table whose first name starts with 'J'.

      SELECT * FROM EMPLOYEE
      WHERE FIRST_NAME LIKE 'J%';

--19. Get employee details from employee table whose first name contains 'o'.
      
      SELECT * FROM EMPLOYEE
      WHERE FIRST_NAME LIKE '%O%';

--20. Get employee details from employee table whose first name ends with 'n'.
            
      SELECT * FROM EMPLOYEE
      WHERE FIRST_NAME LIKE '%N';
      

--21. Get employee details from employee table whose first name ends with 'n' and name contains 4 letters.

      SELECT * FROM EMPLOYEE
      WHERE FIRST_NAME LIKE '%___N';

--22. Get employee details from employee table whose first name starts with 'J' and name contains 4 letters.

      SELECT * FROM EMPLOYEE
      WHERE FIRST_NAME LIKE 'J___';

--23. Get employee details from employee table whose Salary greater than 600000.

      SELECT * FROM EMPLOYEE
      WHERE SALARY > 600000;

--24. Get employee details from employee table whose joining year is “2013”.
      
      SELECT * FROM EMPLOYEE
      WHERE EXTRACT(YEAR FROM JOINING_DATE) = 2013;

--25. Get employee details from employee table whose joining month is “January”.
      
      SELECT * FROM EMPLOYEE
      WHERE EXTRACT (MONTH FROM JOINING_DATE) = 1;

--26. Get employee details from employee table who joined before February 1st 2013.

      SELECT * FROM EMPLOYEE
      WHERE TO_CHAR(JOINING_DATE,'DD/MM/YYYY') < '01/02/2013';

--27. Get employee details from employee table who joined after January 31st 2013.
      
      SELECT * FROM EMPLOYEE
      WHERE TO_CHAR(JOINING_DATE,'DD/MM/YYYY') > '01/01/2013';

--28. Get Joining Date and Time from employee table

      SELECT TO_CHAR(JOINING_DATE,'DD/MON/YYYY HH24:MI') FROM EMPLOYEE;

--29. Get Joining Date, Time including milliseconds from employee table

      SELECT TO_CHAR(JOINING_DATE,'DD-MM-YYYY HH24:MI:SS') FROM EMPLOYEE;     

--30. Get difference between JOINING_DATE and INCENTIVE_DATE from employee and incentives table.
               
      SELECT e.FIRST_NAME,(i.INCENTIVE_DATE - e.JOINING_DATE) AS days_difference
      FROM EMPLOYEE e
      JOIN INCENTIVES i ON e.EMP_ID = i.EMPLOYEE_REF_ID;
      
--31. Get department, total salary with respect to a department from employee table.

      SELECT DEPARTMENT,SUM(SALARY) AS TOTAL_SALARY FROM EMPLOYEE
      GROUP BY DEPARTMENT;

--32. Get department, total salary with respect to a department from employee table order by total salary descending.

      SELECT DEPARTMENT, SUM(SALARY) AS TOTAL_SALARY FROM EMPLOYEE
      GROUP BY DEPARTMENT
      ORDER BY SUM(SALARY) DESC;
      
--33. Get department, no of employees in a department, total salary with respect to a department from employee table 
-- order by total salary descending.

      SELECT DEPARTMENT, COUNT(*) AS no_of_employees, SUM(SALARY) AS TOTAL_SALARY FROM EMPLOYEE
      GROUP BY DEPARTMENT
      ORDER BY SUM(SALARY) DESC;
      

--34. Get department wise average salary from employee table order by salary ascending?

      SELECT DEPARTMENT, AVG(SALARY) AS AVG_SALARY FROM EMPLOYEE
      GROUP BY DEPARTMENT
      ORDER BY AVG_SALARY ASC;      

--35. Get department wise maximum salary from employee table order by salary ascending? 

      SELECT DEPARTMENT, MAX(SALARY) AS MAX_SALARY FROM EMPLOYEE
      GROUP BY DEPARTMENT
      ORDER BY MAX_SALARY ASC;


--36. Get department wise minimum salary from employee table order by salary ascending?

      SELECT DEPARTMENT, MIN(SALARY) AS MIN_SALARY FROM EMPLOYEE
      GROUP BY DEPARTMENT
      ORDER BY MIN_SALARY ASC;

--37. Select no of employees joined with respect to year and month from employee table.

      SELECT EXTRACT(YEAR  FROM joining_date) AS join_year,
             EXTRACT(MONTH FROM joining_date) AS join_month,
             COUNT(*) AS no_of_employees
      FROM employee
      GROUP BY EXTRACT(YEAR FROM joining_date),
               EXTRACT(MONTH FROM joining_date)
      ORDER BY join_year, join_month;

--38. Select department,total salary with respect to a department from employee table 
--    where total salary greater than 800000 order by Total_Salary descending

      SELECT department, SUM(salary) AS total_salary FROM employee
      GROUP BY department
      HAVING SUM(salary) > 800000
      ORDER BY total_salary DESC;

--39. Select employee details from employee table if data in incentive table?
   
     SELECT * FROM EMPLOYEE 
     WHERE EXISTS (SELECT * FROM INCENTIVES);

--- alternative 

     SELECT E.* FROM EMPLOYEE E
     WHERE EXISTS (
                   SELECT 1
                   FROM INCENTIVES I
                   WHERE E.EMP_ID = I.EMPLOYEE_REF_ID
                   );

--40. Select 20 % of salary from John, 10% of Salary for Roy and for other 15 % of salary from employee table

      SELECT EMP_ID, FIRST_NAME, SALARY,
      CASE
           WHEN FIRST_NAME = 'John' THEN SALARY * 0.20
           WHEN FIRST_NAME = 'Roy'  THEN SALARY * 0.10
           ELSE SALARY * 0.15
       END AS calculated_amount
       FROM EMPLOYEE;

--41. Select Banking as 'Bank Dept', Insurance as 'Insurance Dept' and Services as 'Services Dept' from employee table.

      SELECT EMP_ID, FIRST_NAME, DEPARTMENT,
      CASE
           WHEN DEPARTMENT = 'Banking'   THEN 'Bank Dept'
           WHEN DEPARTMENT = 'Insurance' THEN 'Insurance Dept'
           WHEN DEPARTMENT = 'Services'  THEN 'Services Dept'
       END AS department_name
       FROM EMPLOYEE;

--42. Delete employee data from employee table who got incentives in incentive table
      
       DELETE E FROM EMPLOYEE AS E
       INNER JOIN INCENTIVES AS I ON E.EMP_ID = I.EMPLOYEE_REF_ID;
       
--43. Select first_name, incentive amount from employee and incentives table for those employees who have incentives.

      SELECT e.FIRST_NAME, i.INCENTIVE_AMOUNT FROM EMPLOYEE e
      JOIN INCENTIVES i ON e.EMP_ID = i.EMPLOYEE_REF_ID;

--44. Select first_name, incentive amount from employee and incentives table for those employees who have incentives 
--    and incentive amount greater than 3000

      SELECT e.FIRST_NAME, i.INCENTIVE_AMOUNT FROM EMPLOYEE e
      JOIN INCENTIVES i ON e.EMP_ID = i.EMPLOYEE_REF_ID
      WHERE i.INCENTIVE_AMOUNT > 3000;
      

--45. Select first_name, incentive amount from employee and incentives table for all employees even if they didn't get 
--    incentives

      SELECT e.FIRST_NAME, i.INCENTIVE_AMOUNT FROM EMPLOYEE e
      LEFT JOIN INCENTIVES i
      ON e.EMP_ID = i.EMPLOYEE_REF_ID;

--46. Select first_name, incentive amount from employee and incentives table for all employees even if they didn't 
-- get incentives and set incentive amount as 0 for those employees who didn't get incentives.

      SELECT e.FIRST_NAME, NVL(i.INCENTIVE_AMOUNT, 0) AS incentive_amt
      FROM EMPLOYEE e
      LEFT JOIN INCENTIVES i
      ON e.EMP_ID = i.EMPLOYEE_REF_ID;

--47. Select first_name, incentive amount from employee and incentives table for all employees who got incentives 
-- using left join

     SELECT e.FIRST_NAME, i.INCENTIVE_AMOUNT FROM EMPLOYEE e
      LEFT JOIN INCENTIVES i 
      ON e.EMP_ID = i.EMPLOYEE_REF_ID
      WHERE i.INCENTIVE_AMOUNT IS NOT NULL;

--48. Select max incentive with respect to employee from employee and incentives table using sub query.
    
      SELECT e.EMP_ID, e.FIRST_NAME, e.LAST_NAME,
       (
        SELECT MAX(i.INCENTIVE_AMOUNT) FROM INCENTIVES i
        WHERE e.EMP_ID = i.EMPLOYEE_REF_ID) AS Max_Incentive
        FROM EMPLOYEE e;

--------------------------------------------- All Completed ----------------------------------------------------------







SELECT EMPLOYEE_ID, MANAGER_ID, 
( SELECT MAX(Salary) FROM EMPLOYEES e
  WHERE  e.EMPLOYEE_ID > m.MANAGER_ID) AS Max_Salary

SELECT * FROM HR.EMPLOYEES

GROUP BY 
ORDER BY DESC;



SELECT * FROM EMPLOYEE;
