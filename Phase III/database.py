import sqlite3
import getopt, sys, os

conn = sqlite3.connect('ApartmentRentalSystem.db')

conn.execute('pragma foreign_keys = ON')
conn.row_factory = sqlite3.Row
c = conn.cursor()

#Create the tables for Apartment Rental System
def create_tables(): 	
    c.execute('''
        CREATE TABLE USER (
            Username            VARCHAR(9) PRIMARY KEY,
            Password            VARCHAR(30) NOT NULL)
    ''')

    c.execute('''
        CREATE TABLE MANAGEMENT (
            Username            VARCHAR(50),
            Password            VARCHAR(50),
            FOREIGN KEY (Username)
                    REFERENCES USER (Username))
    ''')

    c.execute('''
        CREATE TABLE PROSPECTIVE_RESIDENT(
            Username            VARCHAR(50)     UNIQUE,
            Pref_date           DATE,
            Pref_lease          INT(2),
            Gender              VARCHAR(6),
            Name                VARCHAR(255),
            DOB                 DATE,
            Month_income        REAL(20, 2),
            Min_rate            REAL(7, 2),
            Max_rate            REAL(7, 2),
            Prev_add            VARCHAR(255),
            Req_category        VARCHAR(11),
            PRIMARY KEY (Name, DOB),
            FOREIGN KEY (Username)
                    REFERENCES USER (Username))
    ''')

    c.execute('''
        CREATE TABLE APARTMENT(
            Apt_number          INT(4),
            Category            VARCHAR(30),
            Lease_term          INT(2),
            Sq_ft               VARCHAR(30),
            Available_on        DATE,
            Rent                REAL(7, 2),
            PRIMARY KEY (Apt_number))
    ''')

    c.execute('''
        CREATE TABLE RESIDENT(
            Ano                 INT(4),
            Name                VARCHAR(255),
            DOB                 DATE,
            PRIMARY KEY (Name, DOB),
            FOREIGN KEY (Ano)
                REFERENCES APARTMENT (Apt_number),
            FOREIGN KEY (Name, DOB)
                REFERENCES PROSPECTIVE_RESIDENT (Name, DOB))
    ''')

    c.execute('''
        CREATE TABLE PAYMENT_INFOMATION(
            Card_no             INT(16),
            Exp_date            DATE,
            CVV                 INT(4),
            Card_name           VARCHAR(30),
            Rname               VARCHAR(30),
            Rbdate              DATE,
            PRIMARY KEY (Card_no),
            FOREIGN KEY (Rname, Rbdate)
                REFERENCES RESIDENT (Name, DOB))
    ''')

    c.execute('''
        CREATE TABLE DATE(
            Month              VARCHAR(10),
            Year               YEAR,
            PRIMARY KEY (Month,Year))
    ''')

    c.execute('''
        CREATE TABLE ISSUE(
            Issue_type          VARCHAR(20),
            PRIMARY KEY (Issue_type))
    ''')

    c.execute('''
        CREATE TABLE MAINTENACE_REQUEST(
            Ano                INT(4),
            Req_date           DATE,
            I_type             VARCHAR(20),
            Res_date           DATE,
            PRIMARY KEY (Ano, I_Type, Req_date),
            FOREIGN KEY (Ano)
                REFERENCES APARTMENT (Apt_number),
            FOREIGN KEY (I_type)
                REFERENCES ISSUE (Issue_type))
    ''')

    c.execute('''
        CREATE TABLE REMINDER(
            Ano                INT(4),
            Rdate              DATE,
            Status             VARCHAR(13),
            Message            VARCHAR(500),
            PRIMARY KEY (Rdate, Ano),
            FOREIGN KEY (Ano)
                REFERENCES APARTMENT (Apt_number))
    ''')
    
    c.execute('''
        CREATE TABLE PAY_RENT(
            Ano                INT(4),
            D_month            VARCHAR(10),
            D_year             YEAR,
            Payment_date       DATE,
            Amount             REAL(7, 2),
            Cno                INT(16),
            FOREIGN KEY(D_month, D_year)
                REFERENCES DATE (Month, Year),
            FOREIGN KEY(Ano)
                REFERENCES APARTMENT (Apt_number))
    ''')


def execute_insert(query, param):
	if param == None: 
		c.execute(query)
	else: 
		c.execute(query, param)
	conn.commit()

def execute_select(query, param): 
	if param == None: 
		c.execute(query)
	else: 
		c.execute(query, param)
	# return c.fetchall()
	origin_res = c.fetchall()
	res = []
	for i in origin_res: 
		res.append(dict(zip(i.keys(), i)))
	return res


def create_data_populations():
	
	# ----------------------------- Creating USERS (Regular and Management -------------------------------------
	# There should be at least 15 prospective residents out	of which 10 should be in the resident table


	execute_insert('''insert into USER values (?,?)''', ('NormalUser01', '1234')) #Apartment 1001
	execute_insert('''insert into USER values (?,?)''', ('NormalUser02', '1234')) #Apartment 1002
	execute_insert('''insert into USER values (?,?)''', ('NormalUser03', '1234')) #Apartment 1003
	execute_insert('''insert into USER values (?,?)''', ('NormalUser04', '1234')) #Apartment 1004
	execute_insert('''insert into USER values (?,?)''', ('NormalUser05', '1234')) #Apartment 1005
	execute_insert('''insert into USER values (?,?)''', ('NormalUser06', '1234')) #Apartment 2001
	execute_insert('''insert into USER values (?,?)''', ('NormalUser07', '1234')) #Apartment 2002
	execute_insert('''insert into USER values (?,?)''', ('NormalUser08', '1234')) #Apartment 2003
	execute_insert('''insert into USER values (?,?)''', ('NormalUser09', '1234')) #Apartment 2004
	execute_insert('''insert into USER values (?,?)''', ('NormalUser10', '1234')) #Apartment 2005
	execute_insert('''insert into USER values (?,?)''', ('NormalUser11', '1234')) 
	execute_insert('''insert into USER values (?,?)''', ('NormalUser12', '1234')) 
	execute_insert('''insert into USER values (?,?)''', ('NormalUser13', '1234')) 
	execute_insert('''insert into USER values (?,?)''', ('NormalUser14', '1234')) 
	execute_insert('''insert into USER values (?,?)''', ('NormalUser15', '1234'))
	execute_insert('''insert into USER values (?,?)''', ('NormalUser16', 'Password16'))
	execute_insert('''insert into USER values (?,?)''', ('NormalUser17', 'Password17'))
	execute_insert('''insert into USER values (?,?)''', ('NormalUser18', 'Password16')) #Apartment 1006
	execute_insert('''insert into USER values (?,?)''', ('NormalUser19', 'Password17')) #Apartment 1007
	execute_insert('''insert into USER values (?,?)''', ('NormalUser20', 'Password16'))
	execute_insert('''insert into USER values (?,?)''', ('NormalUser21', 'Password17'))
	execute_insert('''insert into USER values (?,?)''', ('ManagementUser16', '1234'))
	execute_insert('''insert into USER values (?,?)''', ('ManagementUser17', '1234'))

	# ----------------------- Creating MANAGEMENT Details (10 out of 15) ------------------------------------------
	# There should be at least 2 Managers
	execute_insert('''insert into MANAGEMENT values (?,?)''', ('ManagementUser16', '1234'))
	execute_insert('''insert into MANAGEMENT values (?,?)''', ('ManagementUser17', '1234'))

	# ---------------------- Creating PROSPECTIVE_RESIDENT Details (15 applied) --------------------------------
	# Date is YYYY-MM-DD
	
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser01', '2014-07-25', 12, 'Male', 'Male01', '1980-01-01', 2000.99, 1000.50, 2000.50, '217 01st St NW APT 01', '1bdr-1bth')) #Apartment 1001
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser02', '2014-07-25',  6, 'Male', 'Male02', '1981-01-01', 2500.99, 1000.50, 2000.50, '217 02nd St NW APT 02', '1bdr-1bth')) #Apartment 1002
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser03', '2014-07-25', 12, 'Male', 'Male03', '1982-01-01', 3000.99, 1000.50, 2000.50, '217 03rd St NW APT 03', '1bdr-1bth')) #Apartment 1003
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser04', '2014-07-25', 12, 'Male', 'Male04', '1983-01-01', 3500.99, 1000.50, 2000.50, '217 04th St NW APT 04', '1bdr-1bth')) #Apartment 1004
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser05', '2014-07-25',  6, 'Male', 'Male05', '1984-01-01', 4000.99, 1000.50, 2000.50, '217 05th St NW APT 05', '1bdr-1bth')) #Apartment 1005
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser18', '2014-07-25', 12, 'Male', 'Male18', '1973-01-01', 3500.99, 1000.50, 2000.50, '217 18th St NW APT 18', '1bdr-1bth')) #Apartment 1006
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser19', '2014-07-25', 12, 'Male', 'Male19', '1974-01-01', 4000.99, 1000.50, 2000.50, '217 19th St NW APT 19', '1bdr-1bth')) #Apartment 1007
	
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser06', '2014-07-25',  6, 'Female', 'Female01', '1985-01-01', 4500.99, 1000.50, 2000.50, '217 06th St NW APT 06', '2bdr-1bth')) #Apartment 2001
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser07', '2014-07-25', 12, 'Female', 'Female02', '1986-01-01', 5000.99, 1000.50, 2000.50, '217 07th St NW APT 07', '2bdr-1bth')) #Apartment 2002
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser08', '2014-07-25',  3, 'Female', 'Female03', '1987-01-01', 5500.99, 1000.50, 2000.50, '217 08th St NW APT 08', '2bdr-1bth')) #Apartment 2003
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser09', '2014-07-25',  6, 'Female', 'Female04', '1988-01-01', 6000.99, 1000.50, 2000.50, '217 09th St NW APT 09', '2bdr-1bth')) #Apartment 2004
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser10', '2014-07-25', 12, 'Female', 'Female05', '1989-01-01', 6500.99, 1000.50, 2000.50, '217 10th St NW APT 10', '2bdr-1bth')) #Apartment 2005
	
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser11', '2015-01-25',  3, 'Male', 'Male06', '1990-01-01', 7000.99, 1000.50, 2000.50, '217 11th St NW APT 11', '2bdr-2bth'))
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser12', '2015-01-25',  6, 'Male', 'Male07', '1991-01-01', 7500.99, 1000.50, 2000.50, '217 12th St NW APT 12', '2bdr-2bth'))
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser13', '2015-01-25', 12, 'Male', 'Male08', '1992-01-01', 8000.99, 1000.50, 2000.50, '217 13th St NW APT 13', '2bdr-2bth'))
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser14', '2015-01-25',  3, 'Male', 'Male09', '1993-01-01', 8500.99, 1000.50, 2000.50, '217 14th St NW APT 14', '2bdr-2bth'))
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser15', '2014-07-25',  3, 'Male', 'Male10', '1994-01-01', 9000.99, 1000.50, 2000.50, '217 15th St NW APT 15', '2bdr-2bth'))

	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser21', '2015-07-26',  3, 'Male', 'Male21', '1976-01-01', 4000.99, 1000.50, 2000.50, '217 21th St NW APT 21', '2bdr-1bth'))

	# Denied
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser16', '2014-07-25',  6, 'Male', 'Male11', '1988-01-01', 1000.99, 1000.50, 2000.50, '217 11th St NW APT 11', '1bdr-1bth')) #DeniedRent
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser17', '2014-07-25',  3, 'Male', 'Male12', '1988-02-01', 2000.99, 1000.50, 2000.50, '217 12th St NW APT 12', '2bdr-1bth')) #DeniedRent
    
	execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''', ('NormalUser20', '2015-07-26', 12, 'Male', 'Male20', '1975-01-01', 3500.99, 1000.50, 2000.50, '217 20th St NW APT 20', '1bdr-1bth')) #DeniedFull
	

        
    # ----------------------- Creating APARTMENT Details (21 Apartments) ------------------------------------------
	# Available catergories     1bdr-1bth,	2bdr- 1bth, 2bdr-2bth
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1001,'1bdr-1bth',  12, '1200 Sqft.', None,'400.99')) #Available on will be populate at startup
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1002,'1bdr-1bth',   6, '1200 Sqft.', None,'430.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1003,'1bdr-1bth',  12, '1200 Sqft.', None,'420.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1004,'1bdr-1bth',  12, '1200 Sqft.', None,'450.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1005,'1bdr-1bth',   6, '1200 Sqft.', None,'440.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1006,'1bdr-1bth',  12, '1200 Sqft.', None,'460.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (1007,'1bdr-1bth',  12, '1200 Sqft.', None,'465.99'))
	

	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2001,'2bdr-1bth',    6, '2200 Sqft.', None,'710.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2002,'2bdr-1bth',   12, '2200 Sqft.', None,'730.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2003,'2bdr-1bth',    3, '2200 Sqft.', None,'750.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2004,'2bdr-1bth',    6, '2200 Sqft.', None,'740.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2005,'2bdr-1bth',   12, '2200 Sqft.', None,'770.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2006,'2bdr-1bth', None, '2200 Sqft.', None,'760.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2007,'2bdr-1bth', None, '2200 Sqft.', None,'780.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2008,'2bdr-1bth', None, '2200 Sqft.', None,'710.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2009,'2bdr-1bth', None, '2200 Sqft.', None,'735.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2010,'2bdr-1bth', None, '2200 Sqft.', None,'755.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2011,'2bdr-1bth', None, '2200 Sqft.', None,'745.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (2012,'2bdr-1bth', None, '2200 Sqft.', None,'775.99'))

	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3001,'2bdr-2bth', None, '3200 Sqft.', None,'1210.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3002,'2bdr-2bth', None, '3200 Sqft.', None,'1230.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3003,'2bdr-2bth', None, '3200 Sqft.', None,'1240.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3004,'2bdr-2bth', None, '3200 Sqft.', None,'1220.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3005,'2bdr-2bth', None, '3200 Sqft.', None,'1250.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3006,'2bdr-2bth', None, '3200 Sqft.', None,'1270.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3007,'2bdr-2bth', None, '3200 Sqft.', None,'1260.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3008,'2bdr-2bth', None, '3200 Sqft.', None,'1220.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3009,'2bdr-2bth', None, '3200 Sqft.', None,'1250.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3010,'2bdr-2bth', None, '3200 Sqft.', None,'1270.99'))
	execute_insert('''insert into APARTMENT values (?,?,?,?,?,?)''', (3011,'2bdr-2bth', None, '3200 Sqft.', None,'1260.99'))
	
    # ----------------------- Creating RESIDENT Details (10 out of 15) ------------------------------------------
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1001, 'Male01', '1980-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1002, 'Male02', '1981-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1003, 'Male03', '1982-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1004, 'Male04', '1983-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1005, 'Male05', '1984-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1006, 'Male18', '1973-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (1007, 'Male19', '1974-01-01'))
	
	execute_insert('''insert into RESIDENT values (?,?,?)''', (2001, 'Female01', '1985-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (2002, 'Female02', '1986-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (2003, 'Female03', '1987-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (2004, 'Female04', '1988-01-01'))
	execute_insert('''insert into RESIDENT values (?,?,?)''', (2005, 'Female05', '1989-01-01'))

	

	# ----------------------- Creating PAYMENT_INFOMATION Details  ------------------------------------------
	# For every resident there should be at least one credit card.	
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999901, '2020-01-25', 150, 'Bank of America', 'Male01', '1980-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997101, '2022-01-25', 130, 'Wells Fargo',     'Male01', '1980-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999902, '2020-02-25', 151, 'Bank of America', 'Male02', '1981-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997102, '2022-02-25', 131, 'Wells Fargo',     'Male02', '1981-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999903, '2020-03-25', 152, 'Bank of America', 'Male03', '1982-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997103, '2022-03-25', 132, 'Wells Fargo',     'Male03', '1982-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999904, '2020-04-25', 153, 'Bank of America', 'Male04', '1983-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997104, '2022-04-25', 133, 'Wells Fargo',     'Male04', '1983-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999905, '2020-05-25', 154, 'Bank of America', 'Male05', '1984-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997105, '2022-05-25', 134, 'Wells Fargo',     'Male05', '1984-01-01'))

	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999918, '2020-05-25', 118, 'Bank of America', 'Male18', '1973-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997118, '2022-05-25', 118, 'Wells Fargo',     'Male18', '1973-01-01'))

	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999919, '2020-05-25', 119, 'Bank of America', 'Male19', '1974-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997119, '2022-05-25', 119, 'Wells Fargo',     'Male19', '1974-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999906, '2020-06-25', 155, 'Bank of America', 'Female01', '1985-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997106, '2022-06-25', 135, 'Wells Fargo',     'Female01', '1985-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999907, '2020-07-25', 156, 'Bank of America', 'Female02', '1986-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997107, '2022-07-25', 136, 'Wells Fargo',     'Female02', '1986-01-01'))
    
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999908, '2020-08-25', 157, 'Bank of America', 'Female03', '1987-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997108, '2022-08-25', 137, 'Wells Fargo',     'Female03', '1987-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999909, '2020-09-25', 158, 'Bank of America', 'Female04', '1988-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997109, '2022-09-25', 138, 'Wells Fargo',     'Female04', '1988-01-01'))
	
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (99990000999910, '2020-10-25', 159, 'Bank of America', 'Female05', '1989-01-01'))
	execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (77770000997110, '2022-10-25', 139, 'Wells Fargo',     'Female05', '1989-01-01'))

    # ----------------------- Creating DATE Details  --------------------------------
	# ??????????????????????????????????????????????????
	execute_insert('''insert into DATE values (?,?)''', ('JULY', 2014))
	execute_insert('''insert into DATE values (?,?)''', ('AUGUST', 2014))
	execute_insert('''insert into DATE values (?,?)''', ('SEPTEMBER', 2014))
	execute_insert('''insert into DATE values (?,?)''', ('OCTOBER', 2014))
	execute_insert('''insert into DATE values (?,?)''', ('NOVEMBER', 2014))
	
	
	# ----------------------- Creating ISSUES Details  ------------------------------------------
	# There should be at least 3 types of issues, which could be reported.	
	execute_insert('''insert into ISSUE values (?)''', ('Air Conditioner(s) Problems',))
	execute_insert('''insert into ISSUE values (?)''', ('Light(s) Problems',))
	execute_insert('''insert into ISSUE values (?)''', ('Water/Pipes Problems',))
	execute_insert('''insert into ISSUE values (?)''', ('Garbage Disposal Problems',))
	execute_insert('''insert into ISSUE values (?)''', ('Other Problems',))

	# ----------------------- Creating REMINDER Details  --------------------------------
	# The reminder table should have details about at least 3 apartments who have defaulted for the month of August and 3 for the month of September
	# August
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1001, '2014-08-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1002, '2014-08-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1003, '2014-08-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1005, '2014-08-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	# September
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1001, '2014-09-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1002, '2014-09-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1003, '2014-09-04', 'Read', 'Your payment is past due. Please pay immediately.'))
	execute_insert('''insert into REMINDER values (?,?,?,?)''', (1005, '2014-09-04', 'Read', 'Your payment is past due. Please pay immediately.'))
        
	# ----------------------- Creating MAINTENACE_REQUEST Details  --------------------------------
	# The Maintenance request table should have at least 4 resolved requests for each of the 3 months mentioned in the 'Service Request Resolution Report'.	
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1001, '2014-08-01','Air Conditioner(s) Problems',      '2014-08-05'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1001, '2014-08-10','Light(s) Problems',                '2014-08-11'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1001, '2014-08-15','Water/Pipes Problems',             '2014-08-16'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1003, '2014-08-16','Garbage Disposal Problems',        '2014-08-17'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1003, '2014-09-17','Air Conditioner(s) Problems',      '2014-09-18'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1004, '2014-09-18','Light(s) Problems',                '2014-09-19'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1004, '2014-09-21','Water/Pipes Problems',             '2014-09-24'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1005, '2014-09-22','Garbage Disposal Problems',        '2014-09-23'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (2001, '2014-10-03','Air Conditioner(s) Problems',      '2014-10-06'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (2001, '2014-10-05','Light(s) Problems',                '2014-10-06'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (2001, '2014-10-06','Water/Pipes Problems',             '2014-10-06'))
	execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (1001, '2014-10-07','Air Conditioner(s) Problems',      '2014-10-09'))
	
        # ----------------------- Creating PAY_RENT Details  --------------------------------
	# The 'pays rent' table should have appropriate data for those apartments based on when they were allotted.
	# Date is YYYY-MM-DD
	
	# 12 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1001, 'JULY',      2014, '2014-07-01', None, 99990000999901)) 
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1001, 'AUGUST',    2014, '2014-08-01', None, 99990000999901)) #Late
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1001, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999901)) #Late
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1001, 'OCTOBER',   2014, '2014-10-01', None, 99990000999901))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1001, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999901))
	
        # 6 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1002, 'JULY',      2014, '2014-07-01', None, 99990000999902))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1002, 'AUGUST',    2014, '2014-08-09', None, 99990000999902)) #Late
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1002, 'SEPTEMBER', 2014, '2014-09-10', None, 99990000999902)) #Late
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1002, 'OCTOBER',   2014, '2014-10-01', None, 99990000999902))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1002, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999902))

	
        # 12 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1003, 'JULY',      2014, '2014-07-01', None, 99990000999903))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1003, 'AUGUST',    2014, '2014-08-11', None, 99990000999903)) #Late
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1003, 'SEPTEMBER', 2014, '2014-09-12', None, 99990000999903)) #Late 
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1003, 'OCTOBER',   2014, '2014-10-01', None, 99990000999903))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1003, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999903))


        # 12 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1004, 'JULY',      2014, '2014-07-01', None, 99990000999904)) 
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1004, 'AUGUST',    2014, '2014-08-01', None, 99990000999904)) 
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1004, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999904))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1004, 'OCTOBER',   2014, '2014-10-01', None, 99990000999904))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1004, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999904))
	
        # 6 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1005, 'JULY',      2014, '2014-07-01', None, 99990000999905))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1005, 'AUGUST',    2014, '2014-08-13', None, 99990000999905)) #Late
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1005, 'SEPTEMBER', 2014, '2014-09-14', None, 99990000999905)) #Late 
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1005, 'OCTOBER',   2014, '2014-10-01', None, 99990000999905))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1005, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999905)) 
	
        # 12 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1006, 'JULY',      2014, '2014-07-01', None, 99990000999918))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1006, 'AUGUST',    2014, '2014-08-01', None, 99990000999918))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1006, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999918))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1006, 'OCTOBER',   2014, '2014-10-01', None, 99990000999918))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1006, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999918)) 

	# 3 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1007, 'JULY',      2014, '2014-07-01', None, 99990000999919))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1007, 'AUGUST',    2014, '2014-08-01', None, 99990000999919))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1007, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999919))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1007, 'OCTOBER',   2014, '2014-10-01', None, 99990000999919))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (1007, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999919))

	
	# 6 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2001, 'JULY',      2014, '2014-07-01', None, 99990000999906))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2001, 'AUGUST',    2014, '2014-08-01', None, 99990000999906))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2001, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999906))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2001, 'OCTOBER',   2014, '2014-10-01', None, 99990000999906))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2001, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999906))
	
        # 12 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2002, 'JULY',      2014, '2014-07-01', None, 99990000999907))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2002, 'AUGUST',    2014, '2014-08-01', None, 99990000999907))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2002, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999907))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2002, 'OCTOBER',   2014, '2014-10-01', None, 99990000999907))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2002, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999907))

	# 3 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2003, 'JULY',      2014, '2014-07-01', None, 99990000999908))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2003, 'AUGUST',    2014, '2014-08-01', None, 99990000999908))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2003, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999908))

	# 6 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2004, 'JULY',      2014, '2014-07-01', None, 99990000999909))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2004, 'AUGUST',    2014, '2014-08-01', None, 99990000999909))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2004, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999909))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2004, 'OCTOBER',   2014, '2014-10-01', None, 99990000999909))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2004, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999909))

	# 12 Month Lease
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2005, 'JULY',      2014, '2014-07-01', None, 99990000999910))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2005, 'AUGUST',    2014, '2014-08-01', None, 99990000999910))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2005, 'SEPTEMBER', 2014, '2014-09-01', None, 99990000999910))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2005, 'OCTOBER',   2014, '2014-10-01', None, 99990000999910))
	execute_insert('''insert into PAY_RENT values (?,?,?,?,?,?)''', (2005, 'NOVEMBER',  2014, '2014-11-01', None, 99990000999910))


def print_all_data():
	c.execute('''select * from USER''')
	res = c.fetchall()
	print('USER')
	if len(res) == 0: 
		print("Empty")
	else: 
		print(res[0].keys())
		for i in res: 
			print(tuple(i))
	print('')

	c.execute('''select * from MANAGEMENT''')
	res = c.fetchall()
	print('MANAGEMENT')
	if len(res) == 0: 
		print("Empty")
	else: 
		print(res[0].keys())
		for i in res: 
			print(tuple(i))
	print('')

	c.execute('''select * from PROSPECTIVE_RESIDENT''')
	res = c.fetchall()
	print('PROSPECTIVE_RESIDENT')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
        
	c.execute('''select * from APARTMENT''')
	res = c.fetchall()
	print('APARTMENT')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')        

	c.execute('''select * from RESIDENT''')
	res = c.fetchall()
	print('RESIDENT')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
		
	c.execute('''select * from PAYMENT_INFOMATION''')
	res = c.fetchall()
	print('PAYMENT_INFOMATION')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
	
	c.execute('''select * from DATE''')
	res = c.fetchall()
	print('DATE')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
	
	c.execute('''select * from ISSUE''')
	res = c.fetchall()
	print('ISSUE')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
	
	c.execute('''select * from MAINTENACE_REQUEST''')
	res = c.fetchall()
	print('MAINTENACE_REQUEST')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
		
	c.execute('''select * from REMINDER''')
	res = c.fetchall()
	print('REMINDER')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')	
	
	c.execute('''select * from PAY_RENT''')
	res = c.fetchall()
	print('PAY_RENT')
	if len(res) == 0:
		print("Empty")
	else:
		print(res[0].keys())
		for i in res:
			print(tuple(i))
	print('')
		
def setup():
	create_tables()
	create_data_populations()

def reset():
	c.execute('delete from MANAGEMENT')
	c.execute('delete from PROSPECTIVE_RESIDENT')
	c.execute('delete from USER')
	c.execute('delete from APARTMENT')
	c.execute('delete from RESIDENT')
	c.execute('delete from PAYMENT_INFOMATION')
	c.execute('delete from DATE')
	c.execute('delete from ISSUE')
	c.execute('delete from MAINTENACE_REQUEST')
	c.execute('delete from REMINDER')
	c.execute('delete from PAY_RENT')

	conn.commit()
	create_data_populations()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "prc", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-p":
            print_all_data()
        elif o == "-c":
            setup()
        elif o == "-r":
            reset()
main()

