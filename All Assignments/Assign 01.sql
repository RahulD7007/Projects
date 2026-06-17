-- Q1. Write a query to generate following output.

CREATE TABLE Employee_Table
(
       Employee_id NUMBER,
       Full_Name VARCHAR2(50),
       Email VARCHAR2(50),
       Salary NUMBER
              
       SNUM NUMBER CONSTRAINT PK_SNUM PRIMARY KEY,
       SNAME VARCHAR2(20),
       CITY VARCHAR2(30),
       COMM NUMBER
);

INSERT INTO SALESPEOPLE VALUES(1001,'Peel','London',0.12);

SELECT employee_id,first_name||' '||last_name Full_name,email,salary
FROM employees;

-- Q2.Write a query to display job_id and number of manager under particular job. Show only those jobs that have more than one manager.

SELECT job_id,count(manager_id) from employees 
where manager_id>1
group by job_id;

-- Q3. Display the country name and number of employees those working in particular city that count of employee is greater than 30. (Hint: Using Equijoin and Group by )

SELECT count(employee_id),c.country_name
FROM employees e,departments d,locations l,countries c
WHERE e.department_id=d.department_id 
AND d.location_id=l.location_id
AND l.country_id=c.country_id
group by c.country_name
HAVING count(employee_id)>30;

-- Q4. Display cities name and number of departments present those cities. And exculde departments there are no any employees.

SELECT l.city,count(d.department_id)
from employees e,departments d,locations l
WHERE e.department_id=d.department_id 
AND d.location_id=l.location_id
AND employee_id is not null
group by l.city

-- Q5. Display the salary range and number of employees how are salary in between of range. (Hint : Job_Grade table , Equijoin , Group by )



-- Q6. Display Year list and number of Employees join in particular year.(Hint: Group by and To_Char Function)

SELECT to_char(hire_date,'yyyy'),count(employee_id)
FROM employees
group by to_char(hire_date,'yyyy')
order by 1;

-- Q7. Display Manager_id , Manager Full Name and Under number of employees only those managers how have more than 5 employees under working. Result sort by manager_ID




