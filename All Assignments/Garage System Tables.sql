
------------------------Assignments on Garage Data Questions----------------------------------------------------------------------------------

CREATE TABLE Customer_table
(
  CID           NUMBER PRIMARY KEY,
  CNAME         VARCHAR2(100),
  CADD          VARCHAR2(100),
  C_CONTACT     NUMBER,
  C_CREDITDAYS  NUMBER,
  CJ_DATE       DATE,
  SEX           VARCHAR2(50)
);

SELECT * FROM Customer_table;

INSERT INTO Customer_table VALUES(1001,'Cyona blake','NEW YORK',1235684,20,TO_DATE('20-Jan-11','DD-MM-YY'),'FEMALE');
INSERT INTO Customer_table VALUES(1002,'JOHN SMITH','NEW JERSI',1341684,20,TO_DATE('21-Feb-11','DD-MM-YY'),'MALE');
INSERT INTO Customer_table VALUES(1003,'JORDAN WOOD','PRAG',1805184,20,TO_DATE('22-Mar-11','DD-MM-YY'),'MALE');
INSERT INTO Customer_table VALUES(1004,'CHRISTNA','MANHATTON',1125684,31,TO_DATE('23-Apr-13','DD-MM-YY'),'FEMALE');
INSERT INTO Customer_table VALUES(1005,'TOM HILL','LONDON',1239284,10,TO_DATE('25-Jun-15','DD-MM-YY'),'MALE');
INSERT INTO Customer_table VALUES(1006,'KAMILA JOSEF','PARISE',124568,9,TO_DATE('28-Jul-11','DD-MM-YY'),'FEMALE');
INSERT INTO Customer_table VALUES(1007,'ANDRU SYMON','TAXES',125654,15,TO_DATE('01-Apr-16','DD-MM-YY'),'MALE');
INSERT INTO Customer_table VALUES(1008,'SANJU SAMSUNG','NEW YORK',12346341,4,TO_DATE('20-Jan-16','DD-MM-YY'),'MALE');

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE TABLE Vendors_Table
(
 VID           NUMBER PRIMARY KEY,
 VNAME         VARCHAR2(100),
 VADD          VARCHAR2(100),
 VCONTACT      NUMBER,
 VCREDITDAYS   NUMBER,
 VJ_DATE       DATE       
);

SELECT * FROM Vendors_Table;

INSERT INTO Vendors_Table VALUES(2001,'KIRAN PATIL','PUNE',20535535,20,TO_DATE('20-Jan-10','DD-MM-YY'));
INSERT INTO Vendors_Table VALUES(2002,'PRAKASH JAIN','MUMBAI',2063564,10,TO_DATE('05-Nov-11','DD-MM-YY'));
INSERT INTO Vendors_Table VALUES(2003,'SWAPNIL THETE','NASHIK',25355352,15,TO_DATE('18-Mar-10','DD-MM-YY'));
INSERT INTO Vendors_Table VALUES(2004,'AMOL SHENDE','SATARA',23674776,18,TO_DATE('07-Apr-15','DD-MM-YY'));
INSERT INTO Vendors_Table VALUES(2005,'KARAN SINTRE','BULDHANA',256756,30,TO_DATE('22-Apr-09','DD-MM-YY'));
INSERT INTO Vendors_Table VALUES(2006,'RAM KULKARNI','OSMANABAD',20367454,21,TO_DATE('09-Jul-10','DD-MM-YY'));


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE Employee_Table
(
 EID           NUMBER PRIMARY KEY,
 ENAME         VARCHAR2(100),
 EJOB          VARCHAR2(100),
 EADD          VARCHAR2(100),
 ECONTACT      NUMBER,
 ESAL          NUMBER,      
 EDOJ          DATE,
 EDOL          DATE       
);

SELECT * FROM Employee_Table;

INSERT INTO Employee_Table VALUES(3001,'STEVEN KING','PAINTER','NEW YORK',10367454,1200,TO_DATE('09-Jul-10','DD-MM-YY'),NULL);
INSERT INTO Employee_Table VALUES(3002,'DAVID AUSTIN','FITTER','MANHATON',10367434,1100,TO_DATE('09-Aug-10','DD-MM-YY'),NULL);
INSERT INTO Employee_Table VALUES(3003,'BRUCE ERNST','MECHANIC','NEW JERCY',10367264,2200,TO_DATE('08-Sep-10','DD-MM-YY'),NULL);
INSERT INTO Employee_Table VALUES(3004,'LUIS POPP','MECHANIC','NEW JERCY',10367264,1700,TO_DATE('19-Oct-09','DD-MM-YY'),TO_DATE('06-Sep-10','DD-MM-YY'));
INSERT INTO Employee_Table VALUES(3005,'SHERI GOMES','FITTER','PARIS',10327264,1000,TO_DATE('19-Oct-09','DD-MM-YY'),TO_DATE('01-Aug-10','DD-MM-YY'));
INSERT INTO Employee_Table VALUES(3000,'JAMES PHILLIP','FITTER','PARIS',10322264,NULL,TO_DATE('01-Jan-08','DD-MM-YY'),NULL);

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE Sparepart_Table
(
 SPID           NUMBER PRIMARY KEY,
 SPNAME         VARCHAR2(250),
 SPRATE         NUMBER,
 SPUNIT         VARCHAR2(100)              
);

SELECT * FROM Sparepart_Table;


INSERT INTO Sparepart_Table VALUES(4001,'TWO WHEELER TUBE',250,'NOS');
INSERT INTO Sparepart_Table VALUES(4002,'TWO WHEELER ENGINE OIL',400,'LTRS');
INSERT INTO Sparepart_Table VALUES(4003,'FOUR WHEELER ENGINE OIL',5000,'LTRS');
INSERT INTO Sparepart_Table VALUES(4004,'TWO WHEELER CARBORATOR',680,'NOS');
INSERT INTO Sparepart_Table VALUES(4005,'TWO WHEELER CLUTCH WIRE',129,'MTRS');
INSERT INTO Sparepart_Table VALUES(4006,'TWO WHEELER TAIL LIGHT',100,'NOS');
INSERT INTO Sparepart_Table VALUES(4007,'TWO WHEELER INDICATORS',150,'NOS');
INSERT INTO Sparepart_Table VALUES(4008,'FOUR WHEELER GASKIT',1340,'NOS');
INSERT INTO Sparepart_Table VALUES(4009,'WHITE COLOUR',340,'LTRS');
INSERT INTO Sparepart_Table VALUES(4010,'BLACK COLOUR',240,'LTRS');
INSERT INTO Sparepart_Table VALUES(4011,'TWO WHEELER SIDE MIRROR',250,'NOS');
INSERT INTO Sparepart_Table VALUES(4012,'FOUR WHEELER SIDE MIRROR',450,'NOS');
INSERT INTO Sparepart_Table VALUES(4013,'TWO WHEELER SHOCKUP',1320,'PAIR');
INSERT INTO Sparepart_Table VALUES(4014,'FOUR WHEELER BUMPER',6000,'NOS');
INSERT INTO Sparepart_Table VALUES(4015,'FOUR WHEELER FRONT GLASS',7000,'PCS');



------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE Purchase_Table
(
 PID           NUMBER PRIMARY KEY,
 VID           NUMBER,
 SPID          NUMBER,
 PQTY          NUMBER,
 SPRATE        NUMBER,
 SPGST         DECIMAL(10,2),
 PDATE         DATE,
 TRANCOST      NUMBER,
 TOTAL         DECIMAL(10,2),
 RCV_EID       NUMBER,
 FOREIGN KEY(VID) REFERENCES Vendors_Table(VID),
 FOREIGN KEY(SPID) REFERENCES Sparepart_Table(SPID),      
 FOREIGN KEY(RCV_EID) REFERENCES Employee_Table(EID)                   
);

SELECT * FROM Purchase_Table;

INSERT INTO Purchase_Table VALUES(5001,2001,4001,10,250,350,TO_DATE('01-Jan-11','DD-MM-YY'),1300,4150,3001);
INSERT INTO Purchase_Table VALUES(5002,2002,4002,4,400,288,TO_DATE('02-Mar-11','DD-MM-YY'),100,1988,3001);
INSERT INTO Purchase_Table VALUES(5003,2003,4004,8,680,761.6,TO_DATE('12-Jun-11','DD-MM-YY'),50,6251.6,3003);
INSERT INTO Purchase_Table VALUES(5004,2004,4005,10,129,154.8,TO_DATE('22-Aug-11','DD-MM-YY'),125,1569.8,3004);
INSERT INTO Purchase_Table VALUES(5005,2005,4006,20,100,300,TO_DATE('07-Sep-11','DD-MM-YY'),20,2320,3003);
INSERT INTO Purchase_Table VALUES(5006,2006,4007,30,150,630,TO_DATE('12-Oct-11','DD-MM-YY'),60,5190,3000);
INSERT INTO Purchase_Table VALUES(5007,2001,4003,20,5000,14000,TO_DATE('07-Sep-11','DD-MM-YY'),1000,115000,3000);
INSERT INTO Purchase_Table VALUES(5008,2006,4005,1,129,15.48,TO_DATE('12-Oct-11','DD-MM-YY'),50,194.48,3005);
INSERT INTO Purchase_Table VALUES(5009,2006,4005,1,129,15.48,TO_DATE('15-Oct-11','DD-MM-YY'),50,194.48,3005);
INSERT INTO Purchase_Table VALUES(5010,2006,4009,5,340,238,TO_DATE('20-Oct-11','DD-MM-YY'),0,2938,3005);

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CREATE TABLE SER_DET_Table
(
 SID        NUMBER PRIMARY KEY,       
 CID        NUMBER,
 EID        NUMBER,
 SPID       NUMBER,
 TYP_VEH    VARCHAR2(50),
 VEH_NO     VARCHAR2(50),
 TYP_SER    VARCHAR2(100),
 SER_DATE   DATE,
 QTY        DECIMAL(5,1),
 SP_RATE    DECIMAL(10,1),
 SP_AMT     DECIMAL(10,1),
 SP_GST     DECIMAL(10,1),
 SER_AMT    DECIMAL(10,1),
 COMM       DECIMAL(10,1),
 TOTAL      DECIMAL(10,1),
 FOREIGN KEY(CID) REFERENCES Customer_table(CID),
 FOREIGN KEY(EID) REFERENCES Employee_Table(EID),       
 FOREIGN KEY(SPID) REFERENCES Sparepart_Table(SPID)                                  
);

SELECT * FROM SER_DET_Table;

INSERT INTO SER_DET_Table VALUES(6001,1001,3001,4001,'TWO WHEELER','MH15CA3228','TUBE DAMAGED',TO_DATE('02-Jan-11','DD-MM-YY'),1,250,250,35,50,0,335);
INSERT INTO SER_DET_Table VALUES(6002,1002,3002,4002,'TWO WHEELER','MH16US713','FULL SERVICING',TO_DATE('04-Mar-11','DD-MM-YY'),1,400,400,52,300,50,752);
INSERT INTO SER_DET_Table VALUES(6003,1003,3004,4005,'TWO WHEELER','MH12PQ1313','CLUTCH WIRE',TO_DATE('22-Aug-11','DD-MM-YY'),1,129,129,0,10,0,139);
INSERT INTO SER_DET_Table VALUES(6004,1002,3002,4002,'TWO WHEELER','MH16US713','FULL SERVICING',TO_DATE('05-May-11','DD-MM-YY'),1,400,400,52,300,50,752);
INSERT INTO SER_DET_Table VALUES(6005,1004,3001,4009,'TWO WHEELER','MH14PA335','COLOR',TO_DATE('21-Oct-11','DD-MM-YY'),2.5,340,850,119,500,150,1469);
INSERT INTO SER_DET_Table VALUES(6006,1006,3001,4009,'TWO WHEELER','MH12WE334','COLOR',TO_DATE('01-Dec-11','DD-MM-YY'),2.5,340,850,119,500,150,1469);
INSERT INTO SER_DET_Table VALUES(6007,1007,3001,4001,'FOUR WHEELER','MH17BB1345','TUBE DAMAGED',TO_DATE('01-Jan-12','DD-MM-YY'),1,250,250,35,150,0,435);

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Q.1 List all the customers serviced.

-- Ans:- 01

     SELECT DISTINCT  c.CID, c.CNAME, c.CADD, c.C_CONTACT FROM Customer_table c
     JOIN SER_DET_Table s
     ON c.CID = s.CID;

-- Ans:- 02

     SELECT * FROM Customer_table
     WHERE CID IN (SELECT CID FROM SER_DET_Table);

     SELECT s.CID,c.CNAME FROM SER_DET_Table s 
     JOIN Customer_table c on s.CID = c.CID;


-- Q.2 Customers who are not serviced.

-- Ans:- 01

     SELECT * FROM Customer_table
     WHERE CID NOT IN (SELECT CID FROM SER_DET_Table);

-- Ans:- 02

     SELECT  c.CID, c.CNAME, c.CADD, c.C_CONTACT FROM Customer_table c
     WHERE NOT EXISTS (
                       SELECT 1
                       FROM SER_DET_Table s
                       WHERE s.CID = c.CID
                       );
                                           
                       
-- Q.3 Employees who have not received the commission.

-- Ans:- 01

     SELECT * FROM Employee_Table
     WHERE EID IN (SELECT EID FROM SER_DET_Table
                    WHERE COMM=0);

-- Ans:- 02
  
     SELECT DISTINCT  e.EID, e.ENAME, e.EJOB FROM Employee_Table e
     LEFT JOIN SER_DET_Table s     
     ON e.EID = s.EID          
     WHERE s.COMM = 0;
    
     
-- Q.4 Name the employee who have maximum Commission.

     SELECT e.EID, e.ENAME, s.COMM FROM Employee_Table e
     JOIN SER_DET_Table s
     ON e.EID = s.EID
     WHERE s.COMM = (
                     SELECT MAX(COMM)
                     FROM SER_DET_Table
                     );

-- Q.5 Show employee name and minimum commission amount received by an employee.

     SELECT  e.ENAME, s.COMM AS MIN_COMMISSION FROM Employee_Table e
     JOIN SER_DET_Table s
     ON e.EID = s.EID
     WHERE s.COMM = (
                     SELECT MIN(COMM)
                     FROM SER_DET_Table
                     );
                     
-- Q.6 Display the Middle record from any table.

      SELECT * FROM (
                SELECT t.*, ROW_NUMBER() OVER (ORDER BY ROWID) rn,
                COUNT(*)    OVER () cnt
                FROM ORDERS t
                )
      WHERE rn = CEIL(cnt / 2);
      
-- Q.7 Display last 4 records of any table. (--NOT Working)

      SELECT * FROM(SELECT c.*, ROW_NUMBER()OVER(ORDER BY ROWNUM) rn FROM Customer_table c)
      WHERE rn > (SELECT COUNT(*) FROM Customer_table) - 4;
      
      SELECT * FROM Customer_table;      
      
-- Q.8 Count the number of records without count function from any table.

      SELECT MAX(ROWNUM) AS total_records FROM ORDERS;
      
-- Q.9 Delete duplicate records from "Ser_det" table on cid.(note Please rollback after execution).
  
      DELETE FROM SER_DET_Table 
      WHERE ROWID NOT IN (
                          SELECT MIN(ROWID)
                          FROM SER_DET_Table
                          GROUP BY CID
                          );

-- Q.10 Show the name of Customer who have paid maximum amount 

      SELECT c.CNAME, s.TOTAL FROM Customer_table c
      JOIN SER_DET_Table s
      ON c.CID = s.CID
      WHERE s.TOTAL = (
                       SELECT MAX(TOTAL)
                       FROM SER_DET_Table
                       );
                       
-- Q.11 Display Employees who are not currently working.
     
      SELECT EID, ENAME, EJOB, EDOJ, EDOL FROM Employee_Table
      WHERE EDOL IS NOT NULL;

      
-- Q.12 How many customers serviced their two wheelers.

-- Note:- If you want only different employee without repeating ID then answer is 5.   
      
      SELECT COUNT(DISTINCT CID) AS two_wheeler_customers FROM SER_DET_Table
      WHERE TYP_VEH = 'TWO WHEELER';
    
-- Note:- If you want all employee with repeating ID then answer is 6.
   
      SELECT COUNT(CID) AS two_wheeler_customers FROM SER_DET_Table
      WHERE TYP_VEH = 'TWO WHEELER';
      
-- Q.13 List the Purchased Items which are used for Customer Service with Unit of that Item.
   
      SELECT DISTINCT sp.SPNAME, sp.SPUNIT FROM Sparepart_Table sp
      JOIN SER_DET_Table s
      ON sp.SPID = s.SPID;
      
-- Q.14 Customers who have Colored their vehicles.

      SELECT DISTINCT c.CID, c.CNAME, c.CADD, c.C_CONTACT FROM Customer_table c
      JOIN SER_DET_Table s
      ON c.CID = s.CID
      WHERE s.TYP_SER = 'COLOR';
      
-- Q.15 Find the annual income of each employee inclusive of Commission

      SELECT  e.EID, e.ENAME, (NVL(e.ESAL,0) * 12 + NVL(SUM(s.COMM),0)) AS ANNUAL_INCOME FROM Employee_Table e
      LEFT JOIN SER_DET_Table s
      ON e.EID = s.EID
      GROUP BY e.EID, e.ENAME, e.ESAL
      ORDER BY ANNUAL_INCOME DESC;
      
-- Q.16 Vendor Names who provides the engine oil.

      SELECT DISTINCT v.VNAME FROM Vendors_Table v
      JOIN Purchase_Table p
      ON v.VID = p.VID
      JOIN Sparepart_Table sp
      ON p.SPID = sp.SPID
      WHERE sp.SPNAME LIKE '%ENGINE OIL%';
      
-- Q.17 Total Cost to purchase the Color and name the color purchased.

      SELECT sp.SPNAME AS COLOR_NAME,
      SUM(p.PQTY * p.SPRATE + NVL(p.SPGST,0) + NVL(p.TRANCOST,0)) AS TOTAL_PURCHASE_COST
      FROM Sparepart_Table sp
      JOIN Purchase_Table p
      ON sp.SPID = p.SPID
      WHERE sp.SPNAME LIKE '%COLOUR%' OR sp.SPNAME LIKE '%COLOR%'
      GROUP BY sp.SPNAME;
      
-- Q.18 Purchased Items which are not used in "Ser_det".

      SELECT DISTINCT sp.SPNAME, sp.SPUNIT FROM Sparepart_Table sp
      JOIN Purchase_Table p
      ON sp.SPID = p.SPID
      WHERE sp.SPID NOT IN (
                            SELECT DISTINCT SPID
                            FROM SER_DET_Table
                            );
                            
-- Q.19 Spare Parts Not Purchased but existing in Sparepart

      SELECT SPID, SPNAME, SPUNIT FROM Sparepart_Table sp
      WHERE SPID NOT IN (
                         SELECT DISTINCT SPID
                         FROM Purchase_Table
                         );
                         
-- Q.20 Calculate the Profit/Loss of the Firm. consider one month salary of each employee for Calculation.

-- Ans:- 01 (Note: this join is not really needed if summing all purchases separately)

     SELECT  NVL(SUM(s.TOTAL),0) - (NVL(SUM(e.ESAL),0) 
                                 + NVL(SUM(p.PQTY * p.SPRATE + NVL(p.SPGST,0) + NVL(p.TRANCOST,0)),0)) AS PROFIT_OR_LOSS
     FROM Employee_Table e
     CROSS JOIN SER_DET_Table s
     LEFT JOIN Purchase_Table p
     ON p.SPID = p.SPID;  
     
-- Ans:- 02

     SELECT SUM(s.TOTAL)- SUM(e.ESAL) 
     FROM Employee_Table e 
     JOIN SER_DET_Table s ON e.EID = s.EID; 
     
-- Q.21 Specify the names of customers who have serviced their vehicles more than one time.

     SELECT c.CID, c.CNAME, c.CADD, c.C_CONTACT, COUNT(s.SID) AS SERVICE_COUNT FROM Customer_table c
     JOIN SER_DET_Table s
     ON c.CID = s.CID
     GROUP BY c.CID, c.CNAME, c.CADD, c.C_CONTACT
     HAVING COUNT(s.SID) > 1;

-- Q.22 List the Items purchased from vendors location-wise.
    
     SELECT v.VADD AS VENDOR_LOCATION,
            v.VNAME AS VENDOR_NAME,
            sp.SPNAME AS ITEM_NAME,
            p.PQTY,p.SPRATE,(p.PQTY * p.SPRATE + NVL(p.SPGST,0) + NVL(p.TRANCOST,0)) AS TOTAL_COST
     FROM Purchase_Table p
     JOIN Vendors_Table v
     ON p.VID = v.VID
     JOIN Sparepart_Table sp
     ON p.SPID = sp.SPID
     ORDER BY v.VADD, v.VNAME, sp.SPNAME;

-- Q.23 Display count of two wheeler and four wheeler from ser_details

-- Ans:- 01

     SELECT TYP_VEH, COUNT(*) AS VEHICLE_COUNT FROM SER_DET_Table
     GROUP BY TYP_VEH;

-- Ans:- 02

     SELECT TYP_VEH, COUNT(*) AS VEHICLE_COUNT FROM SER_DET_Table
     WHERE TYP_VEH ='TWO WHEELER'
     GROUP BY TYP_VEH
     
     UNION ALL
     
     SELECT TYP_VEH, COUNT(*) FROM SER_DET_Table
     WHERE TYP_VEH ='FOUR WHEELER'
     GROUP BY TYP_VEH;
     
-- Q.24 Display name of customers who paid highest SPGST and for which item?

     SELECT c.CNAME AS CUSTOMER_NAME, sp.SPNAME AS ITEM_NAME, s.SP_GST FROM SER_DET_Table s
     JOIN Customer_table c
     ON s.CID = c.CID
     JOIN Sparepart_Table sp
     ON s.SPID = sp.SPID
     WHERE s.SP_GST = (
                       SELECT MAX(SP_GST)
                       FROM SER_DET_Table
                       );

-- Q.25 Display vendors name who have charged highest SPGST rate for which item?

     SELECT v.VNAME AS VENDOR_NAME, sp.SPNAME AS ITEM_NAME, p.SPGST AS SPGST_CHARGED
     FROM Purchase_Table p
     JOIN Vendors_Table v
     ON p.VID = v.VID
     JOIN Sparepart_Table sp
     ON p.SPID = sp.SPID
     WHERE p.SPGST = (
                      SELECT MAX(SPGST)
                      FROM Purchase_Table
                      );

-- Q.26   list name of item and employee name who have received item 

-- Ans:- 01

     SELECT sp.SPNAME AS ITEM_NAME, e.ENAME AS EMPLOYEE_NAME FROM Employee_Table e 
     JOIN Purchase_Table p ON e.EID = p.RCV_EID 
     JOIN Sparepart_Table sp on p.SPID = sp.SPID;

-- Ans:- 02

     SELECT sp.SPNAME AS ITEM_NAME, e.ENAME AS EMPLOYEE_NAME FROM Purchase_Table p
     JOIN Sparepart_Table sp ON p.SPID = sp.SPID
     JOIN Employee_Table e ON p.RCV_EID = e.EID;

-- Q.27 Display the Name and Vehicle Number of Customer who serviced his vehicle, And Name the Item used for Service, 
-- And specify the purchase date of that Item with his vendor and Item Unit and Location, 
-- And employee Name who serviced the vehicle. for Vehicle NUMBER "MH-14PA335".'

     SELECT c.CNAME AS CUSTOMER_NAME,
            s.VEH_NO AS VEHICLE_NUMBER,
            sp.SPNAME AS ITEM_USED,
            sp.SPUNIT AS ITEM_UNIT,
            p.PDATE AS PURCHASE_DATE,
            v.VNAME AS VENDOR_NAME,
            v.VADD AS VENDOR_LOCATION,
            e.ENAME AS EMPLOYEE_NAME
     FROM SER_DET_Table s 
     JOIN Customer_table c ON s.CID = c.CID
     JOIN Employee_Table e ON s.EID = e.EID
     JOIN Sparepart_Table sp ON s.SPID = sp.SPID
     JOIN Purchase_Table p ON sp.SPID = p.SPID
     JOIN Vendors_Table v ON p.VID = v.VID
     WHERE s.VEH_NO = 'MH-14PA335';

---OR 

     SELECT c.CNAME AS CUSTOMER_NAME,
            s.VEH_NO AS VEHICLE_NUMBER,
            sp.SPNAME AS ITEM_USED,
            sp.SPUNIT AS ITEM_UNIT,
            p.PDATE AS PURCHASE_DATE,
            v.VNAME AS VENDOR_NAME,
            v.VADD AS VENDOR_LOCATION,
            e.ENAME AS EMPLOYEE_NAME
     FROM Customer_table c 
     JOIN SER_DET_Table s ON c.CID = s.CID 
     JOIN Sparepart_Table sp ON s.SPID = sp.SPID 
     JOIN Purchase_Table p ON sp.SPID = p.SPID
     JOIN Vendors_Table v ON v.VID = p.VID
     JOIN Employee_Table e ON e.EID = s.EID
     WHERE VEH_NO = 'MH-14PA335';

-- Q.28 who belong this vehicle  MH-14PA335" Display the customer name 

     SELECT DISTINCT c.CNAME AS CUSTOMER_NAME
     FROM SER_DET_Table s
     JOIN Customer_table c ON s.CID = c.CID
     WHERE s.VEH_NO = 'MH-14PA335';
-- OR

     SELECT c.CNAME AS CUSTOMER_NAME, s.VEH_NO FROM Customer_table c 
     JOIN SER_DET_Table s ON c.CID = s.CID
     WHERE s.VEH_NO = 'MH-14PA335';

-- Q.29 Display the name of customer who belongs to New York and when he /she service their  vehicle on which date   

     SELECT c.CNAME AS CUSTOMER_NAME,
            c.CADD AS ADDRESS,
            s.VEH_NO AS VEHICLE_NUMBER,
            s.SER_DATE AS SERVICE_DATE
     FROM Customer_table c
     JOIN SER_DET_Table s ON c.CID = s.CID
     WHERE c.CADD = 'NEW YORK'
     ORDER BY s.SER_DATE;

-- Q.30 from whom we have purchased items having maximum cost?

     SELECT * FROM ( 
                    SELECT v.VNAME AS VENDOR_NAME,p.TOTAL, 
                    DENSE_RANK() OVER( ORDER BY p.TOTAL DESC) DRN 
              FROM Vendors_Table v JOIN Purchase_Table p ON v.VID = p.VID)
              WHERE DRN = 1;

-- Q.31 Display the names of employees who are not working as Mechanic and that employee done services   .
   
     SELECT DISTINCT e.ENAME AS EMPLOYEE_NAME, e.EJOB FROM Employee_Table e
     JOIN SER_DET_Table s
     ON e.EID = s.EID
     WHERE e.EJOB <> 'MECHANIC';
 

-- Q.32 Display the various jobs along with total number of employees in each job. The output should contain 
--       only those jobs with more than two employees.

     SELECT EJOB AS JOB, 
            COUNT(*) AS TOTAL_EMPLOYEES
     FROM Employee_Table
     GROUP BY EJOB
     HAVING COUNT(*) > 2;

-- Q.33 Display the details of employees who done service  and give them rank according to their no. of services .

     SELECT e.EID, e.ENAME, e.EJOB, COUNT(s.SID) AS NO_OF_SERVICES,
        RANK() OVER (ORDER BY COUNT(s.SID) DESC) AS SERVICE_RANK
     FROM Employee_Table e
     JOIN SER_DET_Table s
     ON e.EID = s.EID
     GROUP BY e.EID, e.ENAME, e.EJOB
     ORDER BY SERVICE_RANK;

-- Q.34 Display those employees who are working as Painter and fitter and who provide service 
--      and total count of service done by fitter and painter  
     
     SELECT e.ENAME AS EMPLOYEE_NAME,
            e.EJOB AS JOB,
           COUNT(s.SID) AS TOTAL_SERVICES
     FROM Employee_Table e
     JOIN SER_DET_Table s
     ON e.EID = s.EID
     WHERE e.EJOB IN ('PAINTER', 'FITTER')
     GROUP BY e.ENAME, e.EJOB  
     ORDER BY e.EJOB, TOTAL_SERVICES DESC;

-- Q.35 Display employee salary and as per highest salary provide Grade to employee 

-- Ans:- 01

    SELECT f.* ,
    CASE 
        DRN WHEN 1 THEN 'A' ELSE 'B' END GRADE
    FROM( SELECT e.ENAME, NVL(e.ESAL,0)SAL , DENSE_RANK() OVER( ORDER BY NVL(e.ESAL,0) DESC) DRN
    FROM Employee_Table e) f;
    
-- Ans:- 02
    
     SELECT ENAME AS EMPLOYEE_NAME,
            ESAL AS SALARY,
     CASE 
        WHEN RANK() OVER (ORDER BY ESAL DESC) = 1 THEN 'A'
        WHEN RANK() OVER (ORDER BY ESAL DESC) = 2 THEN 'B'
        WHEN RANK() OVER (ORDER BY ESAL DESC) = 3 THEN 'C'        
        ELSE 'D'        
    END AS GRADE
    FROM Employee_Table
    ORDER BY ESAL DESC;

-- Q.36  display the 4th record of emp table without using group by and rowid

-- Ans:- 01 (As per EID sequence then answer is 3003)

    SELECT * FROM (
                   SELECT e.*, ROW_NUMBER() OVER (ORDER BY EID) AS RN
                   FROM Employee_Table e
                   ) 
    WHERE RN = 4;

-- Ans:- 02 (As per row number then answer is 3004)

    SELECT * FROM (
                   SELECT e.*, ROW_NUMBER() OVER (ORDER BY ROWNUM) AS RN
                   FROM Employee_Table e
                   ) 
    WHERE RN = 4;

-- Q.37 Provide a commission 100 to employees who are not earning any commission.

    UPDATE SER_DET_Table
    SET COMM = 100
    WHERE COMM IS NULL OR COMM = 0;
    
    SELECT * FROM SER_DET_Table;
    
    Rollback;

-- Q.38 write a query that totals no. of services  for each day and place the results in descending order

-- Ans:- 01
   
    SELECT SER_DATE, COUNT(*) AS TOTAL_SERVICES FROM SER_DET_Table
    GROUP BY SER_DATE
    ORDER BY TOTAL_SERVICES DESC;

-- Ans:- 02

    SELECT SER_DATE, COUNT(SID) AS TOTAL_SERVICES FROM SER_DET_Table
    GROUP BY SER_DATE
    ORDER BY TOTAL_SERVICES DESC;

-- Q.39 Display the service details of those customer who belong from same city 

    SELECT s.* FROM SER_DET_Table s
    JOIN Customer_table c
    ON s.CID = c.CID
    WHERE c.CADD IN (
                     SELECT CADD FROM Customer_table
                     GROUP BY CADD
                     HAVING COUNT(*) > 1
                     )
    ORDER BY c.CADD, s.SER_DATE;

-- Q.40 write a query join customers table to itself to find all pairs of customers service by a single employee

-- Ans:- 01
    
     SELECT DISTINCT c1.CID, c1.CNAME AS CUSTOMER_1, 
                     c2.CID, c2.CNAME AS CUSTOMER_2, 
                     e.EID AS EMPLOYEE_ID, 
                     e.EName AS EMPLOYEE_Name
     FROM Customer_table c1 JOIN SER_DET_Table s1
     ON c1.CID = s1.CID JOIN Employee_Table e 
     ON s1.EID = e.EID JOIN SER_DET_Table s2 
     ON e.EID = s2.EID JOIN Customer_table c2 
     ON s2.CID = c2.CID
     WHERE c1.CID < c2.CID;

-- Ans:- 02  

    SELECT DISTINCT c1.CNAME AS CUSTOMER_1,
                    c2.CNAME AS CUSTOMER_2,
                    s1.EID AS EMPLOYEE_ID
    FROM SER_DET_Table s1
    JOIN SER_DET_Table s2
    ON s1.EID = s2.EID
    AND s1.CID < s2.CID   -- avoid self-pairing and duplicates
    JOIN Customer_table c1
    ON s1.CID = c1.CID
    JOIN Customer_table c2
    ON s2.CID = c2.CID
    ORDER BY s1.EID, c1.CNAME, c2.CNAME;

-- Q.41 List each service number follow by name of the customer who made  that service
   
    SELECT s.SID AS SERVICE_NUMBER,
           c.CNAME AS CUSTOMER_NAME
    FROM SER_DET_Table s
    JOIN Customer_table c
    ON s.CID = c.CID
    ORDER BY s.SID;

-- Q.42 Write a query to get details of employee and provide rating on basis of  maximum services provide by employee.  
--      Note (rating should be like A,B,C,D)

    SELECT e.EID, e.ENAME AS EMPLOYEE_NAME, 
           e.EJOB AS JOB,
           COUNT(s.SID) AS TOTAL_SERVICES,
    CASE 
        WHEN RANK() OVER (ORDER BY COUNT(s.SID) DESC) = 1 THEN 'A'
        WHEN RANK() OVER (ORDER BY COUNT(s.SID) DESC) = 2 THEN 'B'
        WHEN RANK() OVER (ORDER BY COUNT(s.SID) DESC) = 3 THEN 'C'
        ELSE 'D'
    END AS RATING
    FROM Employee_Table e
    JOIN SER_DET_Table s
    ON e.EID = s.EID
    GROUP BY e.EID, e.ENAME, e.EJOB
    ORDER BY TOTAL_SERVICES DESC;

-- Q.43 Write a query to get maximum service amount of each customer with their customer details ?

    SELECT c.CID, c.CNAME, c.CADD, c.C_CONTACT, c.C_CREDITDAYS, c.CJ_DATE, c.SEX,
    MAX(s.SER_AMT) AS MAX_SERVICE_AMOUNT
    FROM Customer_table c
    JOIN SER_DET_Table s
    ON c.CID = s.CID
    GROUP BY c.CID, c.CNAME, c.CADD, c.C_CONTACT, c.C_CREDITDAYS, c.CJ_DATE, c.SEX
    ORDER BY MAX_SERVICE_AMOUNT DESC;

-- Q.44 Get the details of customers with his total no of services ?

    SELECT c.CID, c.CNAME, c.CADD,c.C_CONTACT,c.C_CREDITDAYS,c.CJ_DATE,c.SEX,
    COUNT(s.SID) AS TOTAL_SERVICES
    FROM Customer_table c
    LEFT JOIN SER_DET_Table s
    ON c.CID = s.CID
    GROUP BY c.CID, c.CNAME, c.CADD, c.C_CONTACT, c.C_CREDITDAYS, c.CJ_DATE, c.SEX
    ORDER BY TOTAL_SERVICES DESC;

-- Q.45 From which location spare part purchased  with highest cost ?

    SELECT v.VADD AS VENDOR_LOCATION,
           sp.SPNAME AS ITEM_NAME,
           (p.PQTY * p.SPRATE + NVL(p.SPGST,0) + NVL(p.TRANCOST,0)) AS TOTAL_COST
    FROM Purchase_Table p
    JOIN Vendors_Table v
    ON p.VID = v.VID
    JOIN Sparepart_Table sp
    ON p.SPID = sp.SPID
    WHERE (p.PQTY * p.SPRATE + NVL(p.SPGST,0) + NVL(p.TRANCOST,0)) = (
    SELECT MAX(PQTY*SPRATE + NVL(SPGST,0) + NVL(TRANCOST,0))
    FROM Purchase_Table
    );

-- Q.46 Get the details of employee with their service details who has salary is null

-- Ans:- 01

    SELECT e.*,s.* FROM Employee_Table e JOIN SER_DET_Table s 
    ON e.EID = s.EID
    WHERE e.ESAL IS NULL;  

-- Ans:- 02

    SELECT e.EID,e.ENAME AS EMPLOYEE_NAME,
                 e.EJOB AS JOB,
                 e.EADD AS ADDRESS,
                 e.ECONTACT AS CONTACT,
                 e.ESAL AS SALARY,
                 e.EDOJ AS DATE_OF_JOINING,
                 e.EDOL AS DATE_OF_LEAVING,
                 s.SID AS SERVICE_ID,
                 s.VEH_NO AS VEHICLE_NUMBER,
                 s.TYP_VEH AS VEHICLE_TYPE,
                 s.TYP_SER AS SERVICE_TYPE,
                 s.SER_DATE AS SERVICE_DATE,
                 s.QTY AS ITEM_QTY,                 
                 s.SER_AMT AS SERVICE_AMOUNT
     FROM Employee_Table e JOIN SER_DET_Table s
     ON e.EID = s.EID
     WHERE e.ESAL IS NULL;

-- Q.47 find the sum of purchase location wise 

-- Ans:- 01
    
    SELECT v.VADD , SUM(p.total) 
    FROM Vendors_Table v 
    JOIN Purchase_Table p 
    ON v.VID = p.VID 
    GROUP BY v.VADD
    ORDER BY SUM(p.total) DESC;
    
-- Ans:- 02    
    
    SELECT v.VADD AS VENDOR_LOCATION,
           SUM(p.PQTY * p.SPRATE + NVL(p.SPGST,0) + NVL(p.TRANCOST,0)) AS TOTAL_PURCHASE_AMOUNT
    FROM Purchase_Table p
    JOIN Vendors_Table v
    ON p.VID = v.VID
    GROUP BY v.VADD
    ORDER BY TOTAL_PURCHASE_AMOUNT DESC;
    
-- Q.48 write a query sum of purchase amount in word location wise ?
         
    SELECT ESAL, TO_CHAR(TO_DATE(ESAL,'J'),'JSP') FROM Employee_Table;
    
       
    SELECT v.VADD , SUM(p.total) AS TOTAL, TO_CHAR(TO_DATE(TOTAL,'J'),'JSP') FROM Vendors_Table v 
    JOIN Purchase_Table p 
    ON v.VID = p.VID 
    GROUP BY v.VADD
    ORDER BY SUM(p.total) DESC;
    

-- Q.49 Has the customer who has spent the largest amount money has been give highest rating

    SELECT c.CNAME,s.total, DENSE_RANK() OVER(ORDER BY s.total DESC) AS RATING 
    FROM Customer_table c 
    JOIN SER_DET_Table s ON c.CID = s.CID ;

-- Q.50 select the total amount in service for each customer for which the total is greater than
--      the amount of the largest service amount in the table

      SELECT c.CID, c.CNAME,
      SUM(s.SER_AMT) AS TOTAL_SERVICE_AMOUNT
      FROM Customer_table c
      JOIN SER_DET_Table s
      ON c.CID = s.CID
      GROUP BY c.CID, c.CNAME
      HAVING SUM(s.SER_AMT) > (SELECT MAX(SER_AMT) FROM SER_DET_Table)   
      ORDER BY TOTAL_SERVICE_AMOUNT DESC;

-- Q.51  List the customer name and sparepart name used for their vehicle and  vehicle type

    SELECT  c.CNAME AS CUSTOMER_NAME,
            sp.SPNAME AS SPAREPART_NAME,
            s.TYP_VEH AS VEHICLE_TYPE
    FROM SER_DET_Table s
    JOIN Customer_table c
    ON s.CID = c.CID
    JOIN Sparepart_Table sp
    ON s.SPID = sp.SPID
    ORDER BY c.CNAME;

-- Q.52 Write a query to get spname ,ename,cname quantity ,rate ,service amount for record exist in service table 

    SELECT sp.SPNAME AS SPAREPART_NAME,
           e.ENAME AS EMPLOYEE_NAME,
           c.CNAME AS CUSTOMER_NAME,
           s.QTY AS QUANTITY,
           s.SP_RATE AS RATE,
           s.SER_AMT AS SERVICE_AMOUNT
    FROM SER_DET_Table s
    JOIN Sparepart_Table sp
    ON s.SPID = sp.SPID
    JOIN Employee_Table e
    ON s.EID = e.EID
    JOIN Customer_table c
    ON s.CID = c.CID
    ORDER BY s.SID;

-- Q.53 specify the vehicles owners who is tube damaged.

    SELECT c.CNAME AS CUSTOMER_NAME,
           s.VEH_NO AS VEHICLE_NUMBER,
           s.TYP_VEH AS VEHICLE_TYPE,
           s.TYP_SER AS SERVICE_TYPE
    FROM SER_DET_Table s
    JOIN Customer_table c
    ON s.CID = c.CID
    WHERE s.TYP_SER = 'TUBE DAMAGED';

-- Q.54 Specify the details who have taken full service.
  
    SELECT s.SID AS SERVICE_ID,
           c.CNAME AS CUSTOMER_NAME,
           s.VEH_NO AS VEHICLE_NUMBER,
           s.TYP_VEH AS VEHICLE_TYPE,
           s.TYP_SER AS SERVICE_TYPE,
           s.SER_DATE AS SERVICE_DATE,
           e.ENAME AS EMPLOYEE_NAME,
           s.QTY AS QUANTITY,
           s.SP_RATE AS RATE,
           s.SER_AMT AS SERVICE_AMOUNT
    FROM SER_DET_Table s
    JOIN Customer_table c    
    ON s.CID = c.CID   
    JOIN Employee_Table e
    ON s.EID = e.EID
    WHERE s.TYP_SER = 'FULL SERVICING'
    ORDER BY s.SER_DATE;

-- Q.55 Select the employees who have not worked yet and left the job.

    SELECT * FROM Employee_Table e
    WHERE e.EDOL IS NOT NULL
    AND e.EID NOT IN (SELECT DISTINCT EID FROM SER_DET_Table);

-- Q.56  Select employee who have worked first ever.

    SELECT e.EID,e.ENAME AS EMPLOYEE_NAME,
           e.EJOB AS JOB,
           e.EADD AS ADDRESS,
           e.ECONTACT AS CONTACT,
           e.ESAL AS SALARY,
           e.EDOJ AS DATE_OF_JOINING,
           e.EDOL AS DATE_OF_LEAVING,
           s.SID AS SERVICE_ID,
           s.VEH_NO AS VEHICLE_NUMBER,
           s.TYP_VEH AS VEHICLE_TYPE,
           s.TYP_SER AS SERVICE_TYPE,
           s.SER_DATE AS SERVICE_DATE
    FROM Employee_Table e
    JOIN SER_DET_Table s
    ON e.EID = s.EID
    WHERE s.SER_DATE = (SELECT MIN(SER_DATE) FROM SER_DET_Table);

-- Q.57 Display all records falling in odd date

    SELECT * FROM SER_DET_Table
    WHERE MOD(TO_NUMBER(TO_CHAR(SER_DATE, 'DD')), 2) = 1
    ORDER BY SER_DATE;

-- Q.58 Display all records falling in even date

    SELECT * FROM SER_DET_Table
    WHERE MOD(TO_NUMBER(TO_CHAR(SER_DATE, 'DD')), 2) = 0
    ORDER BY SER_DATE;

-- Q.59 Display the vendors whose material is not yet used.

    SELECT DISTINCT v.VID, v.VNAME AS VENDOR_NAME,
                           v.VADD AS LOCATION,
                           v.VCONTACT AS CONTACT
    FROM Vendors_Table v
    JOIN Purchase_Table p
    ON v.VID = p.VID
    WHERE p.SPID NOT IN (SELECT DISTINCT SPID FROM SER_DET_Table);

-- Q.60 Difference between purchase date and used date of spare part.

    SELECT sp.SPNAME AS SPAREPART_NAME,
           v.VNAME AS VENDOR_NAME,
           p.PDATE AS PURCHASE_DATE,
           s.SER_DATE AS USED_DATE,
           (s.SER_DATE - p.PDATE) AS DAYS_DIFF
    FROM Purchase_Table p
    JOIN SER_DET_Table s
    ON p.SPID = s.SPID
    JOIN Sparepart_Table sp
    ON p.SPID = sp.SPID
    JOIN Vendors_Table v
    ON p.VID = v.VID
    ORDER BY DAYS_DIFF;


