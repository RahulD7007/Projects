CREATE TABLE SALESPEOPLE
(
  SNUM NUMBER PRIMARY KEY,
  SNAME VARCHAR2(100),
  CITY  VARCHAR2(100),
  COMM  DECIMAL(10,2)
);

INSERT INTO SALESPEOPLE VALUES(1001,'Peel','London',0.12);
INSERT INTO SALESPEOPLE VALUES(1002,'Serres','San Jose',0.13);
INSERT INTO SALESPEOPLE VALUES(1004,'Monika','London',0.11);
INSERT INTO SALESPEOPLE VALUES(1007,'Rifkin','Barcelona',0.15);
INSERT INTO SALESPEOPLE VALUES(1003,'Axelrod','New York',0.10);
INSERT INTO SALESPEOPLE VALUES(1005,'Franc','London',0.26);

SELECT * FROM SALESPEOPLE;

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE CUSTOMERS
(
  CNUM  NUMBER PRIMARY KEY,
  CNAME VARCHAR2(100),
  CITY  VARCHAR2(100),
  RATING NUMBER,
  SNUM   NUMBER,
  FOREIGN KEY(SNUM) REFERENCES SALESPEOPLE(SNUM)
);

INSERT INTO CUSTOMERS VALUES(2001,'Hoffman','London',100,1001);
INSERT INTO CUSTOMERS VALUES(2002,'Giovanni','Rome',200,1003);
INSERT INTO CUSTOMERS VALUES(2003,'Liu','San Jose',200,1002);
INSERT INTO CUSTOMERS VALUES(2004,'Grass','Berlin',300,1002);
INSERT INTO CUSTOMERS VALUES(2006,'Clemens','London',100,1001);
INSERT INTO CUSTOMERS VALUES(2008,'Cisneros','San Jose',300,1007);
INSERT INTO CUSTOMERS VALUES(2007,'Pereira','Rome',100,1004);

SELECT * FROM CUSTOMERS;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE ORDERS
(
  ONUM   NUMBER PRIMARY KEY,
  AMT    DECIMAL(10,2),
  ODATE  DATE,
  CNUM   NUMBER,
  FOREIGN KEY(CNUM) REFERENCES CUSTOMERS(CNUM),
  SNUM   NUMBER,
  FOREIGN KEY(SNUM) REFERENCES SALESPEOPLE(SNUM)
);

INSERT INTO ORDERS VALUES(3001,18.69,TO_DATE('03/Oct/96 12:30','DD/Mon/YY HH24:MI'),2008,1007);
INSERT INTO ORDERS VALUES(3003,767.19,TO_DATE('03/Oct/96 13:45','DD/Mon/YY HH24:MI'),2001,1001);
INSERT INTO ORDERS VALUES(3002,1900.10,TO_DATE('03/Oct/96 12:05','DD/Mon/YY HH24:MI'),2007,1004);
INSERT INTO ORDERS VALUES(3005,5160.45,TO_DATE('03/Oct/96 14:00','DD/Mon/YY HH24:MI'),2003,1002);
INSERT INTO ORDERS VALUES(3006,1098.16,TO_DATE('03/Oct/96 13:37','DD/Mon/YY HH24:MI'),2008,1007);
INSERT INTO ORDERS VALUES(3009,1713.23,TO_DATE('04/Oct/96 15:21','DD/Mon/YY HH24:MI'),2002,1003);
INSERT INTO ORDERS VALUES(3007,75.75,TO_DATE('04/Oct/96 16:02','DD/Mon/YY HH24:MI'),2002,1003);
INSERT INTO ORDERS VALUES(3008,4723.00,TO_DATE('05/Oct/96 12:07','DD/Mon/YY HH24:MI'),2006,1001);
INSERT INTO ORDERS VALUES(3010,1309.95,TO_DATE('06/Oct/96 13:12','DD/Mon/YY HH24:MI'),2004,1002);
INSERT INTO ORDERS VALUES(3011,9891.88,TO_DATE('06/Oct/96 13:09','DD/Mon/YY HH24:MI'),2006,1001);
INSERT INTO ORDERS VALUES(3012,3455.78,TO_DATE('04/Oct/96 15:21','DD/Mon/YY HH24:MI'),2002,1003);
INSERT INTO ORDERS VALUES(3013,1245.98,TO_DATE('04/Oct/96 16:32','DD/Mon/YY HH24:MI'),2002,1003);
INSERT INTO ORDERS VALUES(3014,3721.53,TO_DATE('05/Oct/96 12:45','DD/Mon/YY HH24:MI'),2006,1001);
INSERT INTO ORDERS VALUES(3015,734.50,TO_DATE('06/Oct/96 13:16','DD/Mon/YY HH24:MI'),2004,1002);
INSERT INTO ORDERS VALUES(3016,1729.67,TO_DATE('06/Oct/96 13:07','DD/Mon/YY HH24:MI'),2006,1001);


SELECT * FROM ORDERS;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


--1.  List all customers with a rating of 100.

-- Ans:- 01

     SELECT * FROM CUSTOMERS WHERE RATING = 100;
      
-- Ans:- 02      

     SELECT * FROM CUSTOMERS WHERE RATING NOT IN (200,300); 
     
--2.  Find all records in the Customer table with NULL values in the city column.

      SELECT * FROM CUSTOMERS WHERE CITY IS NULL;      

--3.  Find the largest order taken by each salesperson on each date.

-- Ans:- 01
   
      SELECT s.SNAME ,TO_DATE(o.ODATE), MAX(o.AMT) FROM SALESPEOPLE s 
      JOIN ORDERS o ON s.SNUM = o.SNUM
      GROUP BY TO_DATE(ODATE),s.SNAME;

-- Ans:- 02

      SELECT s.SNAME ,TO_DATE(o.ODATE),o.AMT FROM SALESPEOPLE s 
      JOIN ORDERS o ON s.SNUM = o.SNUM
      WHERE o.AMT IN(SELECT MAX(AMT) FROM ORDERS 
      GROUP BY SNUM );
      
--4.  Arrange the Orders table by descending customer number.

      SELECT * FROM ORDERS
      ORDER BY CNUM DESC;
  
--5.  Find which salespeople currently have orders in the Orders table.

     SELECT DISTINCT s.SNUM, s.SNAME, s.CITY, s.COMM FROM SALESPEOPLE s
     JOIN ORDERS o
     ON s.SNUM = o.SNUM
     ORDER BY s.SNUM;

--6.  List names of all customers matched with the salespeople serving them.


      SELECT c.CNAME AS CUSTOMER_NAME,
             s.SNAME AS SALESPERSON_NAME,
             s.CITY AS SALESPERSON_CITY,
             c.CITY AS CUSTOMER_CITY
      FROM CUSTOMERS c
      JOIN SALESPEOPLE s
      ON c.SNUM = s.SNUM
      ORDER BY c.CNAME;


--7.  Find the names and numbers of all salespeople who had more than one customer.

      SELECT s.SNUM,s.SNAME, COUNT(c.CNUM) AS TOTAL_CUSTOMERS FROM SALESPEOPLE s
      JOIN CUSTOMERS c
      ON s.SNUM = c.SNUM
      GROUP BY s.SNUM, s.SNAME
      HAVING COUNT(c.CNUM) > 1
      ORDER BY s.SNUM;

--8.  Count the orders of each of the salespeople and output the results in descending order.

      SELECT s.SNUM, s.SNAME, COUNT(o.ONUM) AS TOTAL_ORDERS FROM SALESPEOPLE s
      JOIN ORDERS o
      ON s.SNUM = o.SNUM
      GROUP BY s.SNUM, s.SNAME
      ORDER BY TOTAL_ORDERS DESC;

--9.  List the Customer table if and only if one or more of the customers in the Customer tables are located in San Jose.

      SELECT * FROM CUSTOMERS WHERE CITY = 'San Jose';
-- OR 

      SELECT CNAME,CITY FROM CUSTOMERS
      GROUP BY CNAME, CITY
      HAVING COUNT(CNUM) >= 1 AND CITY ='San Jose';

      SELECT * FROM CUSTOMERS;
      
--10. Match salespeople to customers according to what city they lived in.

      SELECT s.SNAME AS SALESPERSON_NAME,
             s.CITY AS SALESPERSON_CITY,
             c.CNAME AS CUSTOMER_NAME,
             c.CITY AS CUSTOMER_CITY
      FROM SALESPEOPLE s
      JOIN CUSTOMERS c
      ON  s.SNUM = c.SNUM
      WHERE s.CITY = c.CITY;

--11. Find the largest order taken by each salesperson.

-- Ans:- 01

      SELECT SNUM,MAX(AMT) AS MAX_ORDER_AMOUNT FROM ORDERS
      GROUP BY SNUM
      ORDER BY SNUM;

-- Ans:- 02

      SELECT o.SNUM, MAX(o.AMT) FROM SALESPEOPLE s 
      JOIN ORDERS o ON s.SNUM = o.SNUM
      GROUP BY o.SNUM
      ORDER BY SNUM;
      
--12. Find customers in San Jose who has a rating above 200.

      SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
      WHERE CITY = 'San Jose' AND RATING > 200;

--13. List the names and commissions of all salespeople in London.

      SELECT SNAME AS SALESPERSON_NAME, COMM AS COMMISSION FROM SALESPEOPLE
      WHERE CITY = 'London';

--14. List all the orders of salesperson Monika from the Orders table.

-- Ans:- 01

      SELECT o.ONUM,o.AMT,o.ODATE,o.CNUM,o.SNUM FROM ORDERS o
      JOIN SALESPEOPLE s
      ON o.SNUM = s.SNUM
      WHERE s.SNAME = 'Monika'
      ORDER BY o.ODATE;

-- Ans:- 02

      SELECT * FROM ORDERS 
      WHERE SNUM = ( SELECT SNUM FROM SALESPEOPLE WHERE SNAME = 'Monika');
      
--15. Find all customers with orders on October 3.

      SELECT c.CNUM, c.CNAME, c.CITY, o.ODATE, o.AMT FROM CUSTOMERS c 
      JOIN ORDERS o ON c.CNUM = o.CNUM
      WHERE TO_DATE(ODATE) = '03-Oct-96'
      ORDER BY c.CNUM;
      
--16. Give the sums of the amounts from the orders table, grouped by date, 

     SELECT TO_DATE(ODATE) AS ORDER_DATE, SUM(AMT) AS TOTAL_AMOUNT FROM ORDERS
     GROUP BY TO_DATE(ODATE)
     ORDER BY ORDER_DATE;

--17. Eliminating all those dates where the SUM was not at least 2000.00 above the MAX amount.

     SELECT TO_DATE(ODATE) AS ORDER_DATE, SUM(AMT) AS TOTAL_AMOUNT, ( MAX(AMT) + 2000) FROM ORDERS     
     GROUP BY TO_DATE(ODATE)
     HAVING SUM(AMT) > ( MAX(AMT) + 2000);
    
--18. Select all orders that had amounts that were greater than at least one of the orders from October 6.

-- Ans:- 01

     SELECT * FROM ORDERS 
     WHERE AMT > ANY (SELECT AMT FROM ORDERS WHERE TO_DATE(ODATE) = '06-Oct-96')
     ORDER BY ONUM;
     
-- Ans:- 02
     
     SELECT * FROM ORDERS
     WHERE AMT > ANY ( SELECT AMT FROM ORDERS WHERE TRUNC(ODATE) = TO_DATE('06-Oct-96','DD-Mon-YY')
     )
     ORDER BY ODATE;     
    
--19. Write a query that uses the EXISTS operator to extract all salespeople who have customers with a rating of 300.

-- Ans:- 01    

     SELECT s.SNUM, s.SNAME, s.CITY, s.COMM FROM SALESPEOPLE s
     WHERE EXISTS (SELECT SNUM FROM CUSTOMERS c WHERE c.SNUM = s.SNUM AND RATING = 300);

-- Ans:- 02

     SELECT SNAME FROM SALESPEOPLE 
     WHERE EXISTS (SELECT SNUM FROM CUSTOMERS WHERE SALESPEOPLE.SNUM = CUSTOMERS.SNUM  AND RATING = 300);
     
--20. Find all pairs of customers having the same rating.

    SELECT c1.CNUM AS CUSTOMER1_ID,
           c1.CNAME AS CUSTOMER1_NAME,
           c2.CNUM AS CUSTOMER2_ID,
           c2.CNAME AS CUSTOMER2_NAME,
           c1.RATING
    FROM CUSTOMERS c1
    JOIN CUSTOMERS c2
    ON c1.RATING = c2.RATING
    AND c1.CNUM < c2.CNUM
    ORDER BY c1.RATING, c1.CNUM, c2.CNUM;

--21. Find all customers with CNUM, 1000 above the SNUM of Serres.

-- Ans:- 01
  
    SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
    WHERE CNUM >= ( SELECT SNUM + 1000 FROM SALESPEOPLE WHERE SNAME = 'Serres')
    ORDER BY CNUM;
    
-- Ans:- 02    
    
    SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
    WHERE CNUM >= ( (SELECT SNUM FROM SALESPEOPLE WHERE SNAME = 'Serres') + 1000 )
    ORDER BY CNUM;   

--22. Give the salespeople’s commissions as percentage instead of decimal numbers.

    SELECT SNUM, SNAME AS SALESPERSON_NAME, CITY AS SALESPERSON_CITY,
           COMM * 100 AS COMMISSION_PERCENT FROM SALESPEOPLE
    ORDER BY SNAME;

--23. Find the largest order taken by each salesperson on each date, eliminating those MAX orders, 
--     which are less than $3000.00 in value.

     SELECT SNUM, TO_DATE(ODATE) AS ORDER_DATE,
                  MAX(AMT) AS MAX_ORDER_AMOUNT  FROM ORDERS
     GROUP BY SNUM, TO_DATE(ODATE)
     HAVING MAX(AMT) >= 3000
     ORDER BY SNUM, ORDER_DATE;

--24. List the largest orders on October 3, for each salesperson.

     SELECT s.SNUM, MAX(o.AMT) AS MAX_ORDER_AMOUNT, (TO_DATE (o.ODATE)) FROM ORDERS o
     JOIN SALESPEOPLE s ON o.SNUM = s.Snum
     GROUP BY (TO_DATE (o.ODATE)), s.SNUM, TO_DATE (o.ODATE)
     HAVING TO_DATE (o.ODATE) = '03-Oct-96'
     ORDER BY MAX_ORDER_AMOUNT DESC;

--25. Find all customers located in cities where Serres (SNUM 1002) has customers.

    SELECT CNUM, CNAME, CITY,RATING, SNUM FROM CUSTOMERS
    WHERE SNUM = 1002;
  
--26. Select all customers with a rating above 200.00.

     SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
     WHERE RATING > 200
     ORDER BY RATING DESC, CNUM;

--27. Count the number of salespeople currently listing orders in the Orders table.

-- Ans:- 01 (If without repeating SNUM then answer is 5)

     SELECT COUNT(DISTINCT SNUM) AS NUM_OF_SALESPERSON FROM ORDERS;
     
-- Ans:- 02 (If with repeating SNUM then answer is 15)     
          
     SELECT COUNT( SNUM) AS NUM_OF_SALESPERSON FROM ORDERS;

--28. Write a query that produces all customers serviced by salespeople with a commission above 12%. 
--    Output the customer’s name and the salesperson‘s rate of commission.

-- Ans:- 01

     SELECT c.CNAME AS CUSTOMER_NAME,
            s.COMM * 100 AS SALESPERSON_COMMISSION_PERCENT FROM CUSTOMERS c
     JOIN SALESPEOPLE s ON c.SNUM = s.SNUM
     WHERE s.COMM > 0.12
     ORDER BY c.CNAME;

-- Ans:- 02

     SELECT c.CNAME AS CUSTOMER_NAME,
            s.COMM AS SALESPERSON_COMMISSION_PERCENT FROM SALESPEOPLE s
     JOIN CUSTOMERS c ON s.SNUM = c.SNUM
     WHERE s.COMM*100  > 12
     ORDER BY c.CNAME;

--29. Find salespeople who have multiple customers.

     SELECT s.SNUM,s.SNAME, s.CITY, COUNT(c.CNUM) AS NUM_OF_CUSTOMERS FROM SALESPEOPLE s
     JOIN CUSTOMERS c ON s.SNUM = c.SNUM
     GROUP BY s.SNUM, s.SNAME, s.CITY
     HAVING COUNT(c.CNUM) > 1
     ORDER BY SNUM, NUM_OF_CUSTOMERS DESC;

--30. Find salespeople with customers located in their city.

     SELECT DISTINCT s.SNUM, s.SNAME, s.CITY AS SALESPERSON_CITY,
                                      c.CNAME AS CUSTOMER_NAME,
                                      c.CITY AS CUSTOMER_CITY
                                      FROM SALESPEOPLE s
     JOIN CUSTOMERS c ON s.SNUM = c.SNUM
     WHERE s.CITY = c.CITY
     ORDER BY s.SNUM, c.CNAME;

--31. Find all salespeople whose name starts with ‘P’ and the fourth character is ‘L’.
 
     SELECT SNAME FROM SALESPEOPLE WHERE SNAME LIKE 'P__l';
     
--32. Write a query that uses a sub query to obtain all orders for the customer named ‘Cisneros’. 
--    Assume you do not know his customer number.

     SELECT * FROM ORDERS
     WHERE CNUM = ( SELECT CNUM FROM CUSTOMERS WHERE CNAME = 'Cisneros' );

--33. Find the largest orders for ‘Serres’ and ‘Rifkin’.

   SELECT s.SNAME AS SALESPERSON_NAME,
       MAX(o.AMT) AS MAX_ORDER_AMOUNT  FROM ORDERS o
   JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
   WHERE s.SNAME IN ('Serres', 'Rifkin')
   GROUP BY s.SNAME
   ORDER BY s.SNAME;


--34. Extract the Salespeople table in the following order: SNUM, SNAME, COMMISSION, CITY.

   SELECT SNUM,SNAME,COMM AS COMMISSION, CITY FROM SALESPEOPLE
   ORDER BY SNUM;  
     
--35. Select all customers whose names fall in between ‘A’ and ‘G’ alphabetical range.
  
    SELECT * FROM CUSTOMERS WHERE CNAME BETWEEN 'A%' And 'G%';    

--36. Select all the possible combinations of customers that you can assign.

-- Ans:- 01

    SELECT c1.CNAME AS CUSTOMER1,
           c2.CNAME AS CUSTOMER2
    FROM CUSTOMERS c1
    CROSS JOIN CUSTOMERS c2
    ORDER BY c1.CNAME, c2.CNAME;

-- Ans:- 02

    SELECT s.SNUM,c.CNUM FROM SALESPEOPLE s, CUSTOMERS c;

--37. Select all orders that are greater than the average for October 4.
  
    SELECT * FROM ORDERS
    WHERE AMT > ( SELECT AVG(AMT) FROM ORDERS
    WHERE TO_DATE(ODATE) = '04-Oct-96' )
    ORDER BY ODATE;

--38. Write a select command using a correlated sub query that selects the names and numbers of all customers 
--    with ratings equal to the maximum for their city.

-- Ans:- 01

    SELECT CNAME, CNUM, CITY, RATING FROM CUSTOMERS c1
    WHERE RATING = ( SELECT MAX(RATING) FROM CUSTOMERS c2
    WHERE c2.CITY = c1.CITY )
    ORDER BY RATING DESC;
 
-- Ans:- 02
   
    SELECT CNAME, CNUM, CITY, RATING FROM CUSTOMERS 
    WHERE RATING IN ( SELECT MAX(RATING) FROM CUSTOMERS 
    GROUP BY CITY);

--39. Write a query that totals the orders for each day and places the results in descending order.

   SELECT TO_DATE(ODATE) AS ORDER_DATE, SUM(AMT) AS TOTAL_AMOUNT FROM ORDERS
   GROUP BY TO_DATE(ODATE)
   ORDER BY TOTAL_AMOUNT DESC;

--40. Write a select command that produces the rating followed by the name of each customer in San Jose.

   SELECT RATING, CNAME FROM CUSTOMERS
   WHERE CITY = 'San Jose'
   ORDER BY RATING DESC, CNAME;

--41. Find all orders with amounts smaller than any amount for a customer in San Jose.
 
-- Ans:- 01

   SELECT * FROM ORDERS
   WHERE AMT < ANY ( SELECT AMT FROM ORDERS o
                     JOIN CUSTOMERS c ON o.CNUM = c.CNUM
                     WHERE c.CITY = 'San Jose' );
 
-- Ans:- 02
 
   SELECT * FROM ORDERS
   WHERE AMT  < any ( SELECT AMT FROM ORDERS                   
                      WHERE CNUM IN ( SELECT CNUM FROM CUSTOMERS WHERE CITY = 'San Jose'));

--42. Find all orders with above average amounts for their customers.

-- Ans:- 01

    SELECT * FROM ORDERS o1
    WHERE AMT > (
    SELECT AVG(o2.AMT)
    FROM ORDERS o2
    WHERE o2.CNUM = o1.CNUM
    )
    ORDER BY CNUM, AMT DESC;
    
-- Ans:- 02
    
    SELECT * FROM ORDERS
    WHERE AMT > ALL( SELECT AVG(AMT) FROM ORDERS
                GROUP BY CNUM);

--43. Write a query that selects the highest rating in each city.

    SELECT CITY, MAX(RATING) AS MAX_RATING FROM CUSTOMERS
    GROUP BY CITY
    ORDER BY CITY;

--44. Write a query that calculates the amount of the salesperson’s commission on order by a customer 
--     with a rating above 100.00.

    SELECT o.ONUM AS ORDER_NUMBER,
           c.CNAME AS CUSTOMER_NAME,
           c.RATING AS CUSTOMER_RATING,
           s.SNAME AS SALESPERSON_NAME,
           o.AMT AS ORDER_AMOUNT,
           o.AMT * s.COMM AS COMMISSION_AMOUNT
    FROM ORDERS o
    JOIN CUSTOMERS c ON o.CNUM = c.CNUM
    JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
    WHERE c.RATING > 100
    ORDER BY o.ONUM;

--45. Count the customers with rating above San Jose’s average.

    SELECT COUNT(*) AS NUM_CUSTOMERS_ABOVE_SJ_AVG FROM CUSTOMERS
    WHERE RATING > ( SELECT AVG(RATING) FROM CUSTOMERS WHERE CITY = 'San Jose' );

--46. Write a query that produces all pairs of salespeople with themselves 
--    as well as duplicate rows with the order reversed.
 
     SELECT s1.SNAME AS SALESPERSON1,
            s2.SNAME AS SALESPERSON2
      FROM SALESPEOPLE s1
     CROSS JOIN SALESPEOPLE s2
     ORDER BY s1.SNAME, s2.SNAME;

--47. Find all salespeople that are located in either Barcelona or London.

     SELECT SNUM, SNAME, CITY, COMM FROM SALESPEOPLE
     WHERE CITY IN ('Barcelona', 'London')
     ORDER BY CITY, SNAME;

--48. Find all salespeople with only one customer.

      SELECT s.SNUM, s.SNAME, s.CITY, s.COMM FROM SALESPEOPLE s
      JOIN CUSTOMERS c ON s.SNUM = c.SNUM
      GROUP BY s.SNUM, s.SNAME, s.CITY, s.COMM
      HAVING COUNT(c.CNUM) = 1
      ORDER BY s.SNUM;

--49. Write a query that joins the Customer table to itself to find all pairs of customers 
--    served by a single salesperson.

      SELECT c1.CNAME AS CUSTOMER1,
             c2.CNAME AS CUSTOMER2,
             c1.SNUM AS SALESPERSON_NUMBER FROM CUSTOMERS c1
      JOIN CUSTOMERS c2 ON c1.SNUM = c2.SNUM AND c1.CNUM < c2.CNUM
      ORDER BY c1.SNUM, c1.CNAME, c2.CNAME;

--50. Write a query that will give you all orders for more than $1000.00.

       SELECT * FROM ORDERS
       WHERE AMT > 1000
       ORDER BY AMT DESC;

--51. Write a query that lists each order number followed by the name of the customer who made that order.

       SELECT o.ONUM AS ORDER_NUMBER,
              c.CNAME AS CUSTOMER_NAME
       FROM ORDERS o
       JOIN CUSTOMERS c ON o.CNUM = c.CNUM
       ORDER BY o.ONUM;

--52. Write 2 queries that select all salespeople (by name and number) who have customers in their cities 
--    who they do not service, one using a join and one a correlated subquery. Which solution is more elegant?

-- Ans:- 01

       SELECT DISTINCT s.SNUM, s.SNAME FROM SALESPEOPLE s
       JOIN CUSTOMERS c ON s.CITY = c.CITY
       WHERE c.SNUM <> s.SNUM
       ORDER BY s.SNUM;

-- Ans:- 02     

      SELECT SNUM,SNAME  FROM SALESPEOPLE s 
      WHERE EXISTS (SELECT * FROM CUSTOMERS c 
                     WHERE s.CITY = c.CITY AND s.SNUM <> c.SNUM);
 
-- Ans:- 03

     SELECT SNUM,SNAME  FROM SALESPEOPLE
     WHERE CITY NOT IN ( SELECT c.CITY FROM SALESPEOPLE s 
                         JOIN CUSTOMERS c  ON s.SNUM = c.SNUM );

--53. Write a query that selects all customers whose ratings are equal than ANY (in the SQL sense) of Serres.

      SELECT * FROM CUSTOMERS
      WHERE RATING = ANY ( SELECT RATING FROM CUSTOMERS
                           WHERE SNUM = ( SELECT SNUM FROM SALESPEOPLE
                                          WHERE SNAME = 'Serres' ) 
                          );

--54. Write 2 queries that will produce all orders taken on October 3 or October 4 1996.

-- Ans:- 01

   SELECT * FROM ORDERS
   WHERE TO_DATE(ODATE) = '03-Oct-96' OR TO_DATE(ODATE) = '04-Oct-96';
   
-- Ans:- 02   

   SELECT * FROM ORDERS
   WHERE TO_DATE(ODATE) BETWEEN '03-Oct-96' AND '04-Oct-96';
   
--55. Write a query that produces all pairs of orders by a given customer. 
--    Name that customer and eliminate duplicates.

      SELECT c.CNAME AS CUSTOMER_NAME,
             o1.ONUM AS ORDER1,
             o2.ONUM AS ORDER2
       FROM ORDERS o1
       JOIN ORDERS o2 ON o1.CNUM = o2.CNUM AND o1.ONUM < o2.ONUM
       JOIN CUSTOMERS c ON o1.CNUM = c.CNUM
       ORDER BY c.CNAME, o1.ONUM, o2.ONUM;

--56. Find only those customers whose ratings are higher than every customer in Rome.

      SELECT * FROM CUSTOMERS
      WHERE RATING > ALL ( SELECT RATING FROM CUSTOMERS
                           WHERE CITY = 'Rome' );

--57. Write a query on the customers table whose output will exclude all customers with a rating < = 100.00, 
--    unless they are located in Rome.
   
      SELECT * FROM CUSTOMERS
      WHERE RATING > 100 OR CITY = 'Rome'
      ORDER BY CITY, CNAME;

--58. Find all rows from the Customer table for which the salesperson number is 1001.

      SELECT * FROM CUSTOMERS
      WHERE SNUM = 1001
      ORDER BY CNUM;

--59. Find the total amount in Orders for each salesperson for which this total is greater than the amount 
--     of the largest order in the table.

-- Ans:- 01

      SELECT SNUM, SUM(AMT) AS TOTAL_ORDER_AMOUNT FROM ORDERS 
      GROUP BY SNUM
      HAVING SUM(AMT) > ( SELECT MAX(AMT) FROM ORDERS);

-- Ans:- 02

      SELECT o.SNUM,s.SNAME, SUM(o.AMT) AS TOTAL_ORDER_AMOUNT FROM ORDERS o
      JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
      GROUP BY o.SNUM, s.SNAME
      HAVING SUM(o.AMT) > ( SELECT MAX(AMT) FROM ORDERS )
      ORDER BY TOTAL_ORDER_AMOUNT DESC;

--60. Write a query that selects all orders that have Zeroes or NULL in the Amount field.

      SELECT * FROM ORDERS
      WHERE AMT IS NULL OR AMT LIKE '%0%';

--61. Produce all combinations of salespeople & customer names such that the former precedes the latter alphabetically,
--      and the latter has a rating of less than 200.

      SELECT s.SNAME AS SALESPERSON_NAME,
             c.CNAME AS CUSTOMER_NAME,
             c.RATING FROM SALESPEOPLE s
      CROSS JOIN CUSTOMERS c
      WHERE s.SNAME < c.CNAME AND c.RATING < 200
      ORDER BY s.SNAME, c.CNAME;

--62. List all salespeople’s names and the commission they have earned.

-- Ans:- 01

    SELECT SNAME , COMM FROM SALESPEOPLE ;
    
-- Ans:- 02    
    
      SELECT s.SNAME AS SALESPERSON_NAME, NVL(SUM(o.AMT * s.COMM), 0) AS TOTAL_COMMISSION FROM SALESPEOPLE s
      LEFT JOIN ORDERS o ON s.SNUM = o.SNUM
      GROUP BY s.SNAME
      ORDER BY s.SNAME;

--63. Write a query that produces the names and cities of all customers with the same rating as Hoffman. 
-- Write the query using Hoffman’s CNUM rather than his rating, so that it would still be usable if his rating changed.

      SELECT CNAME, CITY FROM CUSTOMERS
      WHERE RATING = ( SELECT RATING FROM CUSTOMERS
                       WHERE CNAME = 'Hoffman' )
      ORDER BY CNAME;

--64. Find all salespeople for whom there are customers that follow them in alphabetical order.

-- Ans:- 01

     SELECT s.SNUM, s.SNAME FROM SALESPEOPLE s
     WHERE EXISTS (
                   SELECT 1 FROM CUSTOMERS c
                   WHERE c.SNUM = s.SNUM AND c.CNAME > s.SNAME
                   ) 
     ORDER BY s.SNAME;

-- Ans:- 02
     
     SELECT s.SNAME, c.CNAME FROM SALESPEOPLE s 
     JOIN CUSTOMERS c ON s.SNUM = c.SNUM
     ORDER BY s.SNAME;

--65. Write a query that produces the names and ratings of all customers of all who have above average orders.

     SELECT DISTINCT c.CNAME, c.RATING FROM CUSTOMERS c
     JOIN ORDERS o ON c.CNUM = o.CNUM
     WHERE o.AMT > ( SELECT AVG(AMT) FROM ORDERS )
     ORDER BY c.CNAME;

--66. Find the sum of all purchases from the Orders table.

    SELECT SUM(AMT) AS TOTAL_ORDERS_AMOUNT FROM ORDERS;

--67. Write a select command that produces the order number, amount, and date for all rows in the Order table.

    SELECT ONUM, AMT, ODATE FROM ORDERS
    ORDER BY ODATE;

--68. Count the number of not null rating fields in the Customer table including duplicates.

    SELECT COUNT(RATING) AS NOT_NULL_RATING_COUNT FROM CUSTOMERS;

--69. Write a query that gives the names of both the salesperson and the customer for each order after the order number.

    SELECT o.ONUM AS ORDER_NUMBER,
           s.SNAME AS SALESPERSON_NAME,
           c.CNAME AS CUSTOMER_NAME
    FROM ORDERS o
    JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
    JOIN CUSTOMERS c   ON o.CNUM = c.CNUM
    ORDER BY o.ONUM;

--70. List the commissions of all salespeople servicing customers in London.

-- Ans:- 01

   SELECT SNAME,COMM FROM SALESPEOPLE 
   WHERE SNUM IN ( SELECT SNUM FROM CUSTOMERS 
                   WHERE CITY = 'London');

-- Ans:- 02

   SELECT DISTINCT s.SNAME AS SALESPERSON_NAME,
                   s.COMM * 100 AS COMMISSION_PERCENT FROM SALESPEOPLE s
   JOIN CUSTOMERS c ON s.SNUM = c.SNUM
   WHERE c.CITY = 'London'
   ORDER BY s.SNAME;

--71. Write a query using ANY or ALL that will find all salespeople who have no customers located in their city.

      SELECT * FROM SALESPEOPLE s
      WHERE s.CITY <> ALL ( SELECT c.CITY FROM CUSTOMERS c
                            WHERE c.SNUM = s.SNUM );

--72. Write a query using the EXISTS operator that selects all salespeople with customers located in their cities 
--    who are not assigned to them.

-- Ans:- 01

      SELECT s.SNUM, s.SNAME, s.CITY FROM SALESPEOPLE s
      WHERE EXISTS ( SELECT 1 FROM CUSTOMERS c
                     WHERE c.CITY = s.CITY AND c.SNUM <> s.SNUM )
      ORDER BY s.SNAME;

-- Ans:- 02

      SELECT a.SNAME, a.CITY, b.CNAME, b.CITY AS CUS_CITY FROM SALESPEOPLE a,CUSTOMERS b 
      WHERE a.SNUM = b.SNUM AND a.CITY! = b.CITY;

--73. Write a query that selects all customers serviced by Peel or Monika.

-- Ans:- 01

     SELECT c.CNAME AS CUSTOMER_NAME,
            s.SNAME AS SALESPERSON_NAME,
            c.CITY, c.RATING FROM CUSTOMERS c
     JOIN SALESPEOPLE s ON c.SNUM = s.SNUM
     WHERE s.SNAME IN ('Peel', 'Monika')
     ORDER BY c.CNAME;

-- Ans:- 02
     
     SELECT * FROM CUSTOMERS 
     WHERE SNUM IN ( SELECT SNUM FROM SALESPEOPLE 
                     WHERE SNAME IN ( 'Peel','Motika'));

--74. Count the number of salespeople registering orders for each day. 
--    (If a salesperson has more than one order on a given day, he or she should be counted only once.).

-- Ans:- 01

     SELECT ODATE AS ORDER_DATE,
            COUNT(DISTINCT SNUM) AS NUM_SALESPEOPLE FROM ORDERS
     GROUP BY ODATE
     ORDER BY ODATE;

-- Ans:- 02

     SELECT TO_DATE(ODATE), COUNT( DISTINCT SNUM) FROM ORDERS
     GROUP BY TO_DATE(ODATE);
     
--75. Find all orders attributed to salespeople in London.

-- Ans:- 01

     SELECT o.ONUM AS ORDER_NUMBER,
            o.AMT AS AMOUNT,
            o.ODATE AS ORDER_DATE,
            s.SNAME AS SALESPERSON_NAME,
            s.CITY AS SALESPERSON_CITY
     FROM ORDERS o
     JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
     WHERE s.CITY = 'London'
     ORDER BY o.ODATE;

-- Ans:- 02

    SELECT * FROM ORDERS 
    WHERE SNUM IN (SELECT SNUM FROM SALESPEOPLE WHERE CITY = 'London');
    
--76. Find all orders by customers not located in the same cities as their salespeople.

-- Ans:- 01

     SELECT o.ONUM AS ORDER_NUMBER,
            c.CNAME AS CUSTOMER_NAME,
            c.CITY AS CUSTOMER_CITY,
            s.SNAME AS SALESPERSON_NAME,
            s.CITY AS SALESPERSON_CITY,
            o.AMT AS ORDER_AMOUNT,
            o.ODATE AS ORDER_DATE
     FROM ORDERS o
     JOIN CUSTOMERS c ON o.CNUM = c.CNUM
     JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
     WHERE c.CITY <> s.CITY
     ORDER BY o.ODATE;

-- Ans:- 02

    SELECT * FROM ORDERS 
    WHERE CNUM IN (SELECT CNUM FROM CUSTOMERS 
                   WHERE CITY <> ALL (SELECT CITY FROM SALESPEOPLE));
                   
--77. Find all salespeople who have customers with more than one current order.

-- Ans:- 01

     SELECT DISTINCT s.SNUM, s.SNAME FROM SALESPEOPLE s
     JOIN ORDERS o ON s.SNUM = o.SNUM
     GROUP BY s.SNUM, s.SNAME, o.CNUM
     HAVING COUNT(o.ONUM) > 1
     ORDER BY s.SNAME;

-- Ans:- 02

     SELECT SNUM ,COUNT(CNUM) FROM ORDERS
     GROUP BY SNUM
     HAVING COUNT(CNUM) > 1;
  
--78. Write a query that extracts from the Customer table every customer assigned to a salesperson 
-- who currently has at least one other customer (besides the customer being selected) with orders in the Orders table.

-- Ans:- 01

     SELECT c1.CNUM, c1.CNAME, c1.CITY, c1.RATING, c1.SNUM FROM CUSTOMERS c1
     WHERE EXISTS ( SELECT 1 FROM CUSTOMERS c2
                    JOIN ORDERS o ON c2.CNUM = o.CNUM
                    WHERE c2.SNUM = c1.SNUM       -- same salesperson
                    AND c2.CNUM <> c1.CNUM      -- different customer
                   )
     ORDER BY c1.CNUM;

-- Ans:- 02

   SELECT o.SNUM, count(o.CNUM) FROM ORDERS o
   GROUP BY o.SNUM
   HAVING COUNT(CNUM) >= 1;

--79. Write a query that selects all customers whose name begins with ‘C’.

     SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
     WHERE CNAME LIKE 'C%'
     ORDER BY CNUM;

--80. Write a query on the Customers table that will find the highest rating in each city. 
--    Put the output in this form:  for the city (city) the highest rating is : (rating).

     SELECT 'For the city ' || CITY || ' the highest rating is: ' || MAX(RATING) AS MESSAGE FROM CUSTOMERS
     GROUP BY CITY
     ORDER BY CITY;

--81. Write a query that will produce the Snum values of all salespeople with orders currently in the Orders table 
--    without any repeats.

     SELECT DISTINCT SNUM FROM ORDERS
     ORDER BY SNUM;
 
--82. Write a query that lists customers in descending order of rating. Output the rating field first, 
--    followed by the customers’ names and numbers.

     SELECT RATING, CNAME, CNUM FROM CUSTOMERS
     ORDER BY RATING DESC;

--83. Find the average commission for salespeople in London.
    
     SELECT AVG(COMM) AS AVG_COMMISSION FROM SALESPEOPLE
     WHERE CITY = 'London';

--84. Find all orders credited to the same salesperson that services Hoffman.

-- Ans:- 01

     SELECT o.ONUM AS ORDER_NUMBER,
            o.AMT AS AMOUNT,
            o.ODATE AS ORDER_DATE,
            c.CNAME AS CUSTOMER_NAME,
            s.SNAME AS SALESPERSON_NAME
      FROM ORDERS o
      JOIN CUSTOMERS c ON o.CNUM = c.CNUM
      JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
      WHERE o.SNUM = ( SELECT SNUM FROM CUSTOMERS
                       WHERE CNAME = 'Hoffman' )
      ORDER BY o.ODATE;
      
-- Ans:- 02
      
      SELECT * FROM ORDERS
      WHERE SNUM IN (SELECT SNUM FROM ORDERS
                     WHERE CNUM IN ( SELECT CNUM FROM CUSTOMERS
                                     WHERE CNAME = 'Hoffman'));

--85. Find all salespeople whose commission is in between 0.10 and 0.12 both inclusive.

      SELECT SNUM, SNAME, CITY, COMM FROM SALESPEOPLE 
      WHERE COMM BETWEEN 0.10 AND 0.12
      ORDER BY SNUM;

--86. Write a query that will give you the names and cities of all salespeople in London with commission above 0.10
  
      SELECT SNAME, CITY, COMM FROM SALESPEOPLE
      WHERE CITY = 'London' AND COMM > 0.10
      ORDER BY SNAME;

--87. What will be the output from the following query? 

      SELECT * FROM ORDERS WHERE (AMT < 1000 OR NOT (ODATE = 10/03/1996 AND CNUM > 2003));
         
--88. Write a query that selects each customer’s smallest order.

      SELECT CNUM AS CUSTOMER_NUMBER,
             MIN(AMT) AS SMALLEST_ORDER FROM ORDERS
      GROUP BY CNUM
      ORDER BY CNUM;

--89. Write a query that selects the first customer in alphabetical order whose name begins with ‘G’.

-- Ans:- 01
   
      SELECT * FROM ( SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
                      WHERE CNAME LIKE 'G%'
                      ORDER BY CNAME )
      WHERE ROWNUM = 1;
      
-- Ans:- 02

     SELECT CNAME FROM CUSTOMERS
     WHERE CNAME LIKE 'G%';      
     

--90. Write a query that counts the number of different not NULL city values in the Customers table.

     SELECT COUNT(DISTINCT CITY) AS NUM_DISTINCT_CITIES FROM CUSTOMERS
     WHERE CITY IS NOT NULL;

--91. Find the average amount from the Orders table.

     SELECT AVG(AMT) AS AVERAGE_AMOUNT FROM ORDERS;

--92. What would be the output from the following query?

     SELECT * FROM ORDERS WHERE NOT ( ODATE = '10-03-1996' OR SNUM > 1006) AND AMT >= 1500);

--93. Find all customers who are not located in San Jose & whose rating is above 200.

-- Ans:- 01

     SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
     WHERE CITY <> 'San Jose' AND RATING > 200
     ORDER BY CNAME;

-- Ans:- 02
  
    SELECT * FROM CUSTOMERS
    WHERE CITY != 'San Jose' AND RATING > 200;
    
--94. Give a simpler way to write this query:

    SELECT SNUM, SNAME, CITY, COMM FROM SALESPEOPLE 
    WHERE ( COMM > 0.12 AND COMM < 0.14);

--95. Evaluate the following query:

    SELECT * FROM ORDERS WHERE NOT (( ODATE = '10-03-1996' AND SNUM > 1002) OR AMT > 2000);

--96. Which salespeople attend to customers not in the city they have been assigned to?

    SELECT DISTINCT s.SNUM, s.SNAME, s.CITY AS SALESPERSON_CITY FROM SALESPEOPLE s
    JOIN CUSTOMERS c ON s.SNUM = c.SNUM
    WHERE c.CITY <> s.CITY
    ORDER BY s.SNAME;

--97. Which salespeople get commission greater than 0.11 and serving customers rated less than 250?
   
    SELECT DISTINCT s.SNUM, s.SNAME, s.CITY, s.COMM FROM SALESPEOPLE s
    JOIN CUSTOMERS c ON s.SNUM = c.SNUM
    WHERE s.COMM > 0.11 AND c.RATING < 250
    ORDER BY s.SNAME;

--98. Which salespeople have been assigned to the same city but get different commission percentages?
-- avoids pairing the same salesperson with themselves and duplicates

    SELECT DISTINCT s1.SNUM AS SNUM1, s1.SNAME AS SALESPERSON1, 
                    s2.SNUM AS SNUM2, s2.SNAME AS SALESPERSON2, 
                    s1.CITY, s1.COMM AS COMM1, s2.COMM AS COMM2
    FROM SALESPEOPLE s1
    JOIN SALESPEOPLE s2 
    ON s1.CITY = s2.CITY
    AND s1.SNUM < s2.SNUM  
    WHERE s1.COMM <> s2.COMM
    ORDER BY s1.CITY, s1.SNUM;    
   
--99. Which salesperson has earned the most by way of commission?

    SELECT * FROM SALESPEOPLE 
    WHERE COMM = ( SELECT MAX(COMM) FROM SALESPEOPLE);

--100.  Does the customer who has placed the maximum number of orders have the maximum rating?

     SELECT MAX(RATING) AS MAX_RATING FROM CUSTOMERS;    
    
SELECT o.CNUM, c.CNAME, c.RATING, COUNT(o.CNUM) FROM ORDERS o 
JOIN CUSTOMERS c ON c.CNUM = o.CNUM 
GROUP BY o.CNUM, c.CNAME, c.RATING
ORDER BY c.RATING DESC;

SELECT C.*,
CASE
  WHEN C.RATING = (SELECT MAX(RATING) FROM CUSTOMERS)
    THEN 'YES'
      ELSE 'NO'
        END AS RESULT
FROM CUSTOMERS C
WHERE C.CNUM IN (SELECT C1.CNUM FROM CUSTOMERS C1 INNER JOIN ORDERS O1
ON C1.CNUM = O1.CNUM
GROUP BY C1.CNUM
HAVING SUM(O1.AMT) = (SELECT MAX(TOTAL_AMT) FROM (SELECT SUM(AMT) AS TOTAL_AMT FROM ORDERS GROUP BY CNUM)));


with order_counts as (
select b.cnum,count(*) total_orders,a.rating
from customers a
inner join orders b
on a.cnum=b.cnum
group by b.cnum,a.rating
),
max_orders as (
select *
from order_counts
where total_orders=(select max(total_orders) from order_counts)
),
max_rating as (
select *
from order_counts
where rating=(select max(rating) from order_counts)
)
select case
when exists (
select 1
from max_orders mo
inner join max_rating mr
on mo.cnum=mr.cnum
)
then 'Yes, same customer'
else 'No, different customers'
end answer
from dual;
--101.  Has the customer who has spent the largest amount of money been given the highest rating?

-- Ans:- 01

   SELECT o.CNUM, c.CNAME, c.RATING, SUM(o.AMT) FROM ORDERS o 
   JOIN CUSTOMERS c ON c.CNUM = o.CNUM 
   GROUP BY o.CNUM, c.CNAME, c.RATING
   ORDER BY c.RATING DESC;
   
-- Ans:- 02   

     SELECT CNUM, SUM(AMT) AS TOTAL_SPENT FROM ORDERS
     GROUP BY CNUM;
 
     SELECT MAX(TOTAL_SPENT) AS MAX_SPENT 
     FROM (
           SELECT CNUM, SUM(AMT) AS TOTAL_SPENT
     FROM ORDERS
     GROUP BY CNUM
     );

-- Ans:- 03

     SELECT c.CNAME, c.CNUM, c.RATING, o.TOTAL_SPENT,
       CASE 
           WHEN c.RATING = (SELECT MAX(RATING) FROM CUSTOMERS) THEN 'YES'
                             ELSE 'NO'
           END AS HAS_MAX_RATING
           FROM CUSTOMERS c
       JOIN (
            SELECT CNUM, SUM(AMT) AS TOTAL_SPENT FROM ORDERS
        GROUP BY CNUM
        HAVING SUM(AMT) = (
        SELECT MAX(TOTAL_SPENT) 
        FROM (
               SELECT SUM(AMT) AS TOTAL_SPENT
               FROM ORDERS
               GROUP BY CNUM
             )
            )
         ) o ON c.CNUM = o.CNUM;

--102.  List all customers in descending order of customer rating.

      SELECT CNUM, CNAME, CITY, RATING, SNUM FROM CUSTOMERS
      ORDER BY RATING DESC;

--103.  On which days has Hoffman placed orders?
   
      SELECT DISTINCT TRUNC(o.ODATE) AS ORDER_DATE FROM ORDERS o
      WHERE o.CNUM = ( SELECT CNUM FROM CUSTOMERS
                       WHERE CNAME = 'Hoffman' )
      ORDER BY ORDER_DATE;

--104.  Do all salespeople have different commissions?

-- Ans:- 01

      SELECT
          CASE
              WHEN COUNT(*) = COUNT(DISTINCT COMM)
              THEN 'YES, all salespeople have different commissions'
              ELSE 'NO, some salespeople share the same commission'
          END AS RESULT
          FROM SALESPEOPLE;

-- Ans:- 02

   SELECT DISTINCT(COMM), SNAME FROM SALESPEOPLE;

--105.  Which salespeople have no orders between 10/03/1996 and 10/05/1996?

-- Ans:- 01

     SELECT s.SNUM, s.SNAME FROM SALESPEOPLE s
     WHERE NOT EXISTS ( SELECT 1 FROM ORDERS o
     WHERE o.SNUM = s.SNUM AND o.ODATE BETWEEN TO_DATE('03-10-1996','DD-MM-YYYY')
                                             AND TO_DATE('05-10-1996','DD-MM-YYYY')
                      );

-- Ans:- 02
  
   SELECT SNUM FROM ORDERS
   WHERE SNUM NOT IN (SELECT SNUM FROM ORDERS
                      WHERE ODATE BETWEEN TO_DATE('10-Mar-96') AND TO_DATE('10-May-96');

   SELECT * FROM ORDERS;
 
--106.  How many salespersons have succeeded in getting orders?

     SELECT COUNT(DISTINCT SNUM) AS salespersons_with_orders FROM ORDERS;

--107.  How many customers have placed orders?

     SELECT COUNT(DISTINCT CNUM) AS customers_with_orders FROM ORDERS;

--108.  On which date has each salesperson booked an order of maximum value?

-- Ans:- 01

      SELECT o.SNUM, s.SNAME, o.ODATE,o.AMT FROM ORDERS o
      JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
      WHERE o.AMT = ( SELECT MAX(o2.AMT) FROM ORDERS o2
                      WHERE o2.SNUM = o.SNUM )
      ORDER BY o.SNUM;

-- Ans:- 02

   SELECT SNUM, TO_DATE(ODATE), MAX(AMT) FROM ORDERS 
   GROUP BY TO_DATE(ODATE), SNUM ;
  
--109.  Who is the most successful salesperson?

-- Ans:- 01

      SELECT s.SNUM, s.SNAME, SUM(o.AMT * s.COMM) AS total_commission FROM SALESPEOPLE s
      JOIN ORDERS o ON s.SNUM = o.SNUM
      GROUP BY s.SNUM, s.SNAME
      HAVING SUM(o.AMT * s.COMM) = ( SELECT MAX(SUM(o2.AMT * s2.COMM)) FROM SALESPEOPLE s2
      JOIN ORDERS o2 ON s2.SNUM = o2.SNUM
      GROUP BY s2.SNUM );

-- Ans:- 02

   SELECT * FROM (SELECT SNUM, SUM(AMT), DENSE_RANK() OVER(ORDER BY SUM(AMT))DRN FROM ORDERS 
                   GROUP BY SNUM )
   WHERE DRN = 1;
 
--110.  Who is the worst customer with respect to the company?

-- Ans:- 01

      SELECT c.CNUM, c.CNAME, NVL(SUM(o.AMT),0) AS total_purchase FROM CUSTOMERS c
      LEFT JOIN ORDERS o ON c.CNUM = o.CNUM
      GROUP BY c.CNUM, c.CNAME
      HAVING NVL(SUM(o.AMT),0) = ( SELECT MIN(NVL(SUM(o2.AMT),0)) FROM CUSTOMERS c2
      LEFT JOIN ORDERS o2 ON c2.CNUM = o2.CNUM
      GROUP BY c2.CNUM );
    
-- Ans:- 02
  
      SELECT * FROM (SELECT CNUM, SUM(AMT), RANK() OVER(ORDER BY SUM(AMT))RNK FROM ORDERS GROUP BY CNUM )
      WHERE RNK = 1;

--111.  Are all customers not having placed orders greater than 200 totally been serviced by salesperson Peel or Serres?

      SELECT COUNT(*) AS invalid_customers FROM CUSTOMERS c
      WHERE c.CNUM IN ( SELECT CNUM FROM ORDERS
                        GROUP BY CNUM
                        HAVING SUM(AMT) <= 200 )
       AND c.SNUM NOT IN ( SELECT SNUM FROM SALESPEOPLE WHERE SNAME IN ('Peel', 'Serres') );

--112.  Which customers have the same rating?

       SELECT RATING, CNAME FROM CUSTOMERS
       WHERE RATING IN ( SELECT RATING FROM CUSTOMERS
                         GROUP BY RATING
                         HAVING COUNT(*) > 1 )
       ORDER BY RATING, CNAME;

--113.  Find all orders greater than the average for October 4th.

       SELECT * FROM ORDERS
       WHERE AMT > ( SELECT AVG(AMT) FROM ORDERS
                     WHERE TRUNC(ODATE) = TO_DATE('04-Oct-96','DD-Mon-YY') );                                       

--114.  Which customers have above average orders?

        SELECT DISTINCT c.CNUM, c.CNAME FROM CUSTOMERS c
        JOIN ORDERS o ON c.CNUM = o.CNUM
        WHERE o.AMT > ( SELECT AVG(AMT) FROM ORDERS);
                     
--115.  List all customers with ratings above San Jose’s average.

        SELECT CNUM, CNAME, CITY, RATING FROM CUSTOMERS
        WHERE RATING > ( SELECT AVG(RATING) FROM CUSTOMERS
                         WHERE CITY = 'San Jose' );

--116.  Select the total amount in orders for each salesperson for which the total is greater than 
--      the amount of the largest order in the table.

       SELECT SNUM, SUM(AMT) AS total_sales FROM ORDERS
       GROUP BY SNUM
       HAVING SUM(AMT) > ( SELECT MAX(AMT) FROM ORDERS );

--117.  Give names and numbers of all salesperson that have more than one customer.

       SELECT s.SNUM, s.SNAME FROM SALESPEOPLE s
       JOIN CUSTOMERS c ON s.SNUM = c.SNUM
       GROUP BY s.SNUM, s.SNAME
       HAVING COUNT(c.CNUM) > 1;

--118.  Select all salesperson by name and numbers who have customers in their city whom they don’t the service.

       SELECT s.SNUM, s.SNAME FROM SALESPEOPLE s
       WHERE EXISTS (SELECT 1 FROM CUSTOMERS c
                     WHERE c.CITY = s.CITY AND c.SNUM <> s.SNUM );

--119.  Which customers’ rating should be lowered?

       SELECT c.CNUM, c.CNAME, NVL(SUM(o.AMT),0) AS total_order FROM CUSTOMERS c
       LEFT JOIN ORDERS o
       ON c.CNUM = o.CNUM
       GROUP BY c.CNUM, c.CNAME
       HAVING NVL(SUM(o.AMT),0) < ( SELECT AVG(AMT) FROM ORDERS );

--120.  Is there a case for assigning a salesperson to Berlin?
       
       SELECT a.SNAME, b.CITY FROM SALESPEOPLE a JOIN CUSTOMERS b ON a.SNUM = b.SNUM
       WHERE b.CITY = 'Berlin';

--121.  Is there any evidence linking the performance of a salesperson to commission that he or she is being paid?

-- Ans:- 01

       SELECT s.SNUM, s.SNAME, s.COMM AS COMMISSION, SUM(o.AMT) AS total_sales FROM SALESPEOPLE s
       JOIN ORDERS o ON s.SNUM = o.SNUM
       GROUP BY s.SNUM, s.SNAME, s.COMM
       ORDER BY total_sales DESC;

-- Ans:- 02

   SELECT b.SNUM, c.SNAME, SUM(a.AMT) AS total_sales_by_SP, 
   ROUND( SUM(AMT) * c.COMM ) COMM FROM ORDERS a, CUSTOMERS b, SALESPEOPLE c 
   WHERE a.CNUM = b.CNUM AND b.SNUM = c.SNUM 
   GROUP BY b.SNUM, c.SNAME, c.COMM
   ORDER BY total_sales_by_SP DESC;

--122. Dose the total amount in orders by customer in Rome & London exceeds the commission paid to salesperson 
--      in London and New York by more than 5 times?

-- Ans:- 01

       SELECT SUM(o.AMT) AS total_order_amount FROM ORDERS o
       JOIN CUSTOMERS c ON o.CNUM = c.CNUM
       WHERE c.CITY IN ('Rome','London');

-- Ans:- 02

  SELECT DISTINCT (SELECT SUM(a.AMT * c.COMM) AS total_sales FROM ORDERS a,CUSTOMERS b,SALESPEOPLE c 
  WHERE a.CNUM = b.CNUM AND b.SNUM = c.SNUM AND (c.CITY = 'London' OR c.CITY = 'New York')) AS x,
       ( SELECT SUM(a.AMT) FROM ORDERS a,CUSTOMERS b 
         WHERE a.CNUM = b.CNUM AND (b.CITY = 'Rome' OR b.CITY = 'London')) AS y FROM ORDERS;

    
--123.  Which is the date, order number, amt and city for each salesperson (byname) 
--      for the maximum order he has obtained?

--Ans:- 01

       SELECT s.SNAME, o.ONUM, o.AMT, o.ODATE, c.CITY FROM ORDERS o
       JOIN SALESPEOPLE s ON o.SNUM = s.SNUM
       JOIN CUSTOMERS c ON o.CNUM = c.CNUM
       WHERE o.AMT = ( SELECT MAX(AMT) FROM ORDERS
                       WHERE SNUM = o.SNUM )
       ORDER BY s.SNAME;

-- Ans:- 02
       
       SELECT s.SNAME, o.ODATE, o.ONUM, o.AMT, s.CITY FROM SALESPEOPLE s 
       JOIN ORDERS o ON s.SNUM = o.SNUM
       WHERE o.AMT IN (SELECT MAX(AMT) FROM ORDERS 
       GROUP BY SNUM);
    
--124.  Which salesperson(s) should be fired?

       SELECT s.SNUM, s.SNAME FROM SALESPEOPLE s
       LEFT JOIN ORDERS o ON s.SNUM = o.SNUM
       WHERE o.ONUM IS NULL;

--125.  What is the total income for the company? 

         SELECT SUM(AMT) AS Total_Income FROM ORDERS;
