from tkinter import*
import database
from tkinter import messagebox
import copy
import tkinter.font as tkFont
from datetime import date
import datetime
import calendar
from dateutil.relativedelta import relativedelta

import time

class myGUI:
    def __init__(self, aWin):
        today = datetime.date.today()
        
        #Update database with correct available_on for each apartment
        database.execute_insert('''UPDATE APARTMENT SET Available_on = ? WHERE Lease_term is NULL''', (today,))
        residingResidentList = database.execute_select('''SELECT Pref_date, Ano, Name, Pref_lease FROM RESIDENT NATURAL JOIN PROSPECTIVE_RESIDENT''', None)

        for eachDict in residingResidentList:
            apartmentNumber = eachDict["Ano"]
            residentName = eachDict["Name"]
            moveInDate = eachDict["Pref_date"]
            leaseTerm = eachDict["Pref_lease"]

            d1 = date(int(moveInDate[0:4]), int(moveInDate[5:7]), int(moveInDate[8:10]));
            newDate = d1 + relativedelta(months = leaseTerm)
            database.execute_insert('''UPDATE APARTMENT SET Available_on = ? WHERE Apt_number = ?''', (newDate,apartmentNumber))

        #Update expired apartment
        expiredApartmentList = database.execute_select('''SELECT Apt_number FROM APARTMENT WHERE Available_on < ?''', (today,))
        
        for eachDict in expiredApartmentList:
            expiredApartment = eachDict["Apt_number"]
            database.execute_insert('''UPDATE APARTMENT SET Lease_term = ? WHERE Apt_number = ?''', (None, expiredApartment))
            database.execute_insert('''DELETE FROM MAINTENACE_REQUEST WHERE Ano = ?''', (expiredApartment,))
            database.execute_insert('''DELETE FROM REMINDER WHERE Ano = ?''', (expiredApartment,))
            database.execute_insert('''DELETE FROM PAY_RENT WHERE Ano = ?''', (expiredApartment,))
            expiredUserList = database.execute_select('''SELECT * FROM RESIDENT WHERE Ano = ? ''', (expiredApartment,))
      
            for eachDict in expiredUserList:
                expiredName = eachDict["Name"]
                expiredDOB = eachDict["DOB"]
                database.execute_insert('''DELETE FROM PAYMENT_INFOMATION WHERE Rname = ? AND Rbdate = ?''', (expiredName, expiredDOB))
                database.execute_insert('''DELETE FROM RESIDENT WHERE Ano = ?''', (expiredApartment,))
                expiredProsList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT WHERE Name = ? AND DOB = ? ''', (expiredName, expiredDOB))
                expiredPros = expiredProsList[0]["Username"]
                database.execute_insert('''DELETE FROM PROSPECTIVE_RESIDENT WHERE Username = ? ''', (expiredPros,))
                database.execute_insert('''DELETE FROM USER WHERE Username = ? ''', (expiredPros,))

        #Update rent information

        
        currentMonth = time.strftime("%B").upper()
        currentYear = today.year
        dateInfo = database.execute_select('''SELECT * FROM DATE WHERE Month = ? AND Year = ?''', (currentMonth,currentYear))
        residentPay = database.execute_select('''SELECT * FROM RESIDENT''', None)
        if dateInfo == []:
            database.execute_insert('''INSERT INTO DATE VALUES (?,?)''', (currentMonth, currentYear))
            for eachDict in residentPay:
                aptNumber = eachDict["Ano"]
                database.execute_insert('''INSERT INTO PAY_RENT VALUES (?,?,?,?,?,?)''', (aptNumber, currentMonth, currentYear , None,None,None))

        rentInfoList = database.execute_select('''SELECT Apt_number, Rent FROM APARTMENT ''', None)

        for eachDict in rentInfoList:
            aptNo = eachDict["Apt_number"]
            aptRent = eachDict["Rent"]
            database.execute_insert('''UPDATE PAY_RENT SET Amount = ? WHERE Ano = ?''', (aptRent,aptNo))
            
        payrentInfoList = database.execute_select('''SELECT * FROM PAY_RENT''', None)

        for eachDict in payrentInfoList:
            aptNo = eachDict["Ano"]
            theMonth = eachDict["D_month"]
            theYear = eachDict["D_year"]
            tempDate = eachDict["Payment_date"]
            currentAmount = eachDict["Amount"]
            if tempDate is None:
                payDay = today.day
            else:
                payDay = int(tempDate[8:10])
            if payDay > 3 :
                extraPay = (payDay - 3) * 50
                newAmount = extraPay + currentAmount
                database.execute_insert('''UPDATE PAY_RENT SET Amount = ? WHERE Ano = ? AND D_month = ? AND D_year = ?''', (newAmount, aptNo, theMonth, theYear))

            




        
        #Font Customizations
        self.checkboxDict = dict()
        self.customFont = tkFont.Font(family="Helvetica", size=20)
        self.customFont6 = tkFont.Font(family="Helvetica", size=17)
        self.customFont1 = tkFont.Font(family="Helvetica", size=15)

        self.customFont20 = tkFont.Font(family="Calibri", size=20)
        self.customFont17 = tkFont.Font(family="Calibri", size=17)
        self.customFont13 = tkFont.Font(family="Calibri", size=13)

        self.customFont13B = tkFont.Font(family="Calibri", size=13, weight="bold")


        self.headingFont = tkFont.Font(family="Calibri", size=18, weight="bold")

        #Screen Size
        verticalPixel = 400
        horizontalPixel = 800

        #Init
        self.window=aWin
        self.window.title("Apartment Rental System")   
        self.window.minsize(horizontalPixel, verticalPixel)
        self.window.maxsize(horizontalPixel, verticalPixel)
        
        #Login (Figure 1)
        self.LoginPage()
        self.lastState = "Login"
        
        
        #New User Registration (Figure 2)
        self.userRegistration = Toplevel()
        self.userRegistration.title("New User Registration")
        self.userRegistration.minsize(horizontalPixel, verticalPixel)
        self.userRegistration.maxsize(horizontalPixel, verticalPixel)        
        self.userRegistration.withdraw()

        #Prospective Resident Application Form (Figure 3)
        self.applicationForm = Toplevel()
        self.applicationForm.title("Prospective Resident Application Form")
        self.applicationForm.minsize(1600, 800)
        self.applicationForm.maxsize(1600, 800)
        self.applicationForm.withdraw()

        #Homepage (Figure 4)
        self.residentHomepage = Toplevel()
        self.residentHomepage.title("Resident Homepage")
        self.residentHomepage.minsize(horizontalPixel, verticalPixel)
        self.residentHomepage.maxsize(horizontalPixel, verticalPixel)
        self.residentHomepage.withdraw()

        self.managementHomepage = Toplevel()
        self.managementHomepage.title("Management Homepage")
        self.managementHomepage.minsize(horizontalPixel, verticalPixel)
        self.managementHomepage.maxsize(horizontalPixel, verticalPixel)
        self.managementHomepage.withdraw()

        #Rent (Figure 5)
        self.rent = Toplevel()
        self.rent.title("Rent")
        self.rent.minsize(horizontalPixel, verticalPixel)
        self.rent.maxsize(horizontalPixel, verticalPixel) 
        self.rent.withdraw()

        #Request Maintenance (Figure 6)
        self.requestMaintenance = Toplevel()
        self.requestMaintenance.title("Request Maintenance")
        self.requestMaintenance.minsize(horizontalPixel, verticalPixel)
        self.requestMaintenance.maxsize(horizontalPixel, verticalPixel)
        self.requestMaintenance.withdraw()

        #Payment Information (Figure 7)
        self.paymentInformation = Toplevel()
        self.paymentInformation.title("Payment Information")
        self.paymentInformation.minsize(horizontalPixel, verticalPixel)
        self.paymentInformation.maxsize(horizontalPixel, verticalPixel)
        self.paymentInformation.withdraw()

        #Application Review (Figure 8)
        self.applicationReview = Toplevel()
        self.applicationReview.title("Application Review")
        self.applicationReview.minsize(1600, 800)
        self.applicationReview.maxsize(1600, 800)
        self.applicationReview.withdraw()

        #Apartment Allotment (Figure 9)
        self.apartmentAllotment = Toplevel()
        self.apartmentAllotment.title("Apartment Allotment")
        self.apartmentAllotment.minsize(960, 480)
        self.apartmentAllotment.maxsize(960, 1600)
        self.apartmentAllotment.withdraw()

        #View Maintenance Requests (Figure 10)
        self.viewRequests = Toplevel()
        self.viewRequests.title("View Maintenance Requests")
        self.viewRequests.minsize(horizontalPixel, verticalPixel)
        self.viewRequests.maxsize(horizontalPixel, 1600)
        self.viewRequests.withdraw()

        #Reminder (Figure 11)
        self.reminder = Toplevel()
        self.reminder.title("Reminder")
        self.reminder.minsize(horizontalPixel, verticalPixel)
        self.reminder.maxsize(horizontalPixel, verticalPixel)
        self.reminder.withdraw()

        #Leasing Report (Figure 12)
        self.leasingReport = Toplevel()
        self.leasingReport.title("Leasing Report")
        self.leasingReport.minsize(horizontalPixel, verticalPixel)
        self.leasingReport.maxsize(horizontalPixel, 1600)
        self.leasingReport.withdraw()

        #Service Request Resolution Report(Figure 13)
        self.serviceReport = Toplevel()
        self.serviceReport.title("Service Request Resolution Report")
        self.serviceReport.minsize(horizontalPixel, verticalPixel)
        self.serviceReport.maxsize(horizontalPixel, 1600)
        self.serviceReport.withdraw()

        #Rent Defaulters Report(Figure 14)
        self.rentDefaulters = Toplevel()
        self.rentDefaulters.title("Rent Defaulters Report")
        self.rentDefaulters.minsize(horizontalPixel, verticalPixel)
        self.rentDefaulters.maxsize(horizontalPixel, 1600)
        self.rentDefaulters.withdraw()




    
        
        
    #-------------------------------------------------------------- Login (Figure 1) ---------------------------------------------------------
    #GUI
    def GoBack(self):
        if self.lastState == "Registration":
            self.userRegistration.withdraw()
            self.window.deiconify()
            
        if self.lastState == "Resident Homepage":
            self.username.set("")
            self.password.set("")
            self.residentHomepage.withdraw()
            self.window.deiconify()
            
        if self.lastState == "Management Homepage":
            self.username.set("")
            self.password.set("")
            self.managementHomepage.withdraw()
            self.window.deiconify()
            
        if self.lastState == "Application Form":
            self.userList = database.execute_select('''SELECT * FROM USER''', None)
            residentList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT NATURAL JOIN RESIDENT''', None)
            prospectiveList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT as a WHERE NOT EXISTS (SELECT * FROM RESIDENT as b WHERE a.Name = b.Name)''', None)
            managerList = database.execute_select("SELECT * FROM MANAGEMENT", None)

            allUsernames = {x["Username"] for x in self.userList}
            residentUsernames = {x["Username"] for x in residentList}
            managerUsernames = {x["Username"] for x in managerList}
            prospectiveUsernames = {x["Username"] for x in prospectiveList}

            stranger = allUsernames - residentUsernames - managerUsernames - prospectiveUsernames
            for eachStranger in stranger:
                database.execute_insert('''DELETE FROM USER WHERE Username = ?''', (eachStranger,))
            
            self.applicationForm.withdraw()
            self.UserRegistrationPage()
            
        if self.lastState == "Pay Rent":
            self.rent.withdraw()
            self.ResidentHomepage()
            
        if self.lastState == "Request Maintenance":
            self.requestMaintenance.withdraw()
            self.ResidentHomepage()
                
        if self.lastState == "Payment Information":
            self.paymentInformation.withdraw()
            self.ResidentHomepage()

        if self.lastState == "Application Review":
            self.applicationReview.withdraw()
            self.ManagementHomepage()

        if self.lastState == "Leasing Report":
            self.leasingReport.withdraw()
            self.ManagementHomepage()
            
        if self.lastState == "Service Report":
            self.serviceReport.withdraw()
            self.ManagementHomepage()
            
        if self.lastState == "Rent Defaulters":
            self.rentDefaulters.withdraw()
            self.ManagementHomepage()

        if self.lastState == "Reminder":
            self.reminder.withdraw()
            self.ManagementHomepage()

        if self.lastState == "View Maintenance":
            self.viewRequests.withdraw()
            self.ManagementHomepage()

        if self.lastState == "Apartment Allotment":
            self.apartmentAllotment.withdraw()
            self.ApplicationReview()
            
            
    def LoginPage(self):
        self.lastState = "Login"
        self.lastStateFlag = "None"
        
        Label(self.window,text = "Login", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 375, pady = 18).grid(column = 0, columnspan = 2, row = 0, sticky = W)
        Label(self.window,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 18).grid(column = 0, columnspan = 2, row = 1, sticky = W)
        Label(self.window,text = "Username:", font = self.customFont13, background = '#E9EAED').grid(column = 0,row = 2,sticky = E)
        Label(self.window,text = "Password:", font = self.customFont13, background = '#E9EAED').grid(column = 0,row = 3,sticky = E)
        
        self.window.configure(background='#E9EAED')

        self.username = StringVar()
        self.password = StringVar()
        
        username = Entry(self.window,width = 20, textvariable=self.username)
        password = Entry(self.window,width = 20, show="*", textvariable=self.password)
        username.grid(column = 1, row = 2, sticky = W)
        password.grid(column = 1, row = 3, sticky = W)

        Label(self.window,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground = '#E9EAED', padx = 375, pady= 18).grid(column = 0, columnspan = 2, row = 4, sticky = W)

        Button(self.window,text = "Login", font = self.customFont13, background = '#DADADA',command = self.LoginCheck,padx = 20).grid(column = 0,row = 5,sticky = E)
        Button(self.window,text = "Create Account", font = self.customFont13, background = '#DADADA',command = self.UserRegistrationPage,padx = 20).grid(column = 1,row = 5,sticky = W)

        self.window.bind("<Return>",self.LoginCheck)

    #Logic
    def LoginCheck(self, event=None):
        
        username = self.username.get()
        password = self.password.get()
        self.userList = database.execute_select('''SELECT * FROM USER''', None)
        residentList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT NATURAL JOIN RESIDENT''', None)
        prospectiveList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT as a WHERE NOT EXISTS (SELECT * FROM RESIDENT as b WHERE a.Name = b.Name)''', None)
        managerList = database.execute_select("SELECT * FROM MANAGEMENT", None) #[{"Username":"potato", "Password":"test"}, {"Username":"Carrot", "Password":"Banana"}]

        allUsernames = {x["Username"] for x in self.userList}
        residentUsernames = {x["Username"] for x in residentList}
        managerUsernames = {x["Username"] for x in managerList}
        prospectiveUsernames = {x["Username"] for x in prospectiveList}
 
        

        #Check if username already exists
        if username not in allUsernames:
            messagebox.showinfo("Error","Username Invalid")
            return None

        #Check for correct password
        flag = False
        for eachClass in [self.userList, managerList]:
            for eachDict in eachClass:
                if eachDict["Username"] == username and eachDict["Password"] == password:
                    flag = True
        if not flag:
            messagebox.showinfo("Error","Incorrect Password")
            return None


        #Redirect to correct window
        if username in managerUsernames:
            self.userType = "Manager"
            self.ManagementHomepage()
        elif username in residentUsernames:
            self.userType = "Resident"
            self.ResidentHomepage()
        elif username in prospectiveUsernames:
            self.userType = "Prospective Resident"
            messagebox.showinfo("Welcome!","Your Application is under review!")
        else:
            print("Who is this?")
    
      
    #-------------------------------------------------------------- New User Registration (Figure 2) ---------------------------------------------------------
    #GUI
    def UserRegistrationPage(self):
        if self.lastState != "Application Form":
            self.window.withdraw()
            self.userRegistration.deiconify()
        else:
            self.userRegistration.deiconify()
        
        Label(self.userRegistration,text = "Create Account Page", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 300, pady = 18).grid(column = 0, columnspan = 2, row = 0, sticky = W)
        Label(self.userRegistration,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 18).grid(column = 0, columnspan = 2, row = 1, sticky = W)
        Label(self.userRegistration,text = "Username:", font = self.customFont13, background = '#E9EAED').grid(column = 0,row = 2, sticky = E)
        Label(self.userRegistration,text = "Password:", font = self.customFont13, background = '#E9EAED').grid(column = 0,row = 3, sticky = E)
        Label(self.userRegistration,text = "Confirm Password:", font = self.customFont13, background = '#E9EAED').grid(column = 0, row = 4, sticky = E)
        Button(self.userRegistration,text = "Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        
        self.userRegistration.configure(background='#E9EAED')
        
        self.newUsername = Entry(self.userRegistration,width = 20)
        self.newPassword = Entry(self.userRegistration,width = 20)
        self.confirmPassword = Entry(self.userRegistration,width = 20)
        
        self.newUsername.grid(column = 1, row = 2, sticky = W)
        self.newPassword.grid(column = 1, row = 3, sticky = W)
        self.confirmPassword.grid(column = 1, row = 4, sticky = W)
    

        Label(self.userRegistration,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground = '#E9EAED', padx = 375, pady = 18).grid(column = 0, columnspan = 2, row = 5, sticky = W)

        Button(self.userRegistration,text = "Register", font = self.customFont13, background = '#DADADA', command = self.CreateAccountCheck, padx = 20).grid(column = 1, row = 6, sticky = W)

        self.lastState = "Registration"

    #Logic
    def CreateAccountCheck(self):
        newUsername = self.newUsername.get()
        newPassword = self.newPassword.get() 
        confirmPassword = self.confirmPassword.get()

        if (newUsername, newPassword, confirmPassword) == ("", "", ""):
            messagebox.showerror("Invalid Information", "Please enter a username and a password.")
            return None

        if newUsername == "":            
            messagebox.showerror("No Username", "Please enter a username.")
            return None

        if newPassword == "":
            messagebox.showerror("No Password", "Please enter a password.")
            return None

        if confirmPassword == "":
            messagebox.showerror("No Password Confirmation", "Please re-enter your password in the confirmation box.")
            return None

        if newPassword != confirmPassword:
            messagebox.showerror("Password Mismatch", "The two entered passwords do not match. Please re-enter your password in the confirmation box and try again.")
            return None


        self.userList = database.execute_select('''SELECT * FROM USER''', None)
        for eachDict in self.userList:
            if newUsername == eachDict["Username"]: #username already taken
                messagebox.showinfo("Error", "Sorry. This username is taken, please select another username.")
                return None

        database.execute_insert('''insert into USER values (?,?)''', (newUsername, newPassword))

        self.username.set(newUsername)

        self.ApplicationFormPage()


    #-------------------------------------------------------------- Prospective Resident Application Form (Figure 3) ---------------------------------------------------------
    def handler(self):
        if messagebox.askokcancel("Quit?", "Are you sure you want to quit? Your username won't be saved."):
            self.userList = database.execute_select('''SELECT * FROM USER''', None)
            residentList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT NATURAL JOIN RESIDENT''', None)
            prospectiveList = database.execute_select('''SELECT Username FROM PROSPECTIVE_RESIDENT as a WHERE NOT EXISTS (SELECT * FROM RESIDENT as b WHERE a.Name = b.Name)''', None)
            managerList = database.execute_select("SELECT * FROM MANAGEMENT", None)
        
            allUsernames = {x["Username"] for x in self.userList}
            residentUsernames = {x["Username"] for x in residentList}
            managerUsernames = {x["Username"] for x in managerList}
            prospectiveUsernames = {x["Username"] for x in prospectiveList}
            print(allUsernames);
            print(residentUsernames);
            print(managerUsernames);
            print(prospectiveUsernames);
                
            stranger = allUsernames - residentUsernames - managerUsernames - prospectiveUsernames
            print(allUsernames - residentUsernames - managerUsernames - prospectiveUsernames)
            for eachStranger in stranger:
                print(eachStranger)
                database.execute_insert('''DELETE FROM USER WHERE Username = ?''', (eachStranger,))            
            self.applicationForm.destroy()
            print ("Destoy root window.")
            
    def ApplicationFormPage(self):
        self.applicationForm.protocol("WM_DELETE_WINDOW", self.handler)
   
        self.userRegistration.withdraw()
        self.applicationForm.deiconify()
            
        for child in self.applicationForm.winfo_children():
            child.destroy()
        Label(self.applicationForm,text = "Prospective Resident Application Form ", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 600, pady = 18).grid(column = 0, columnspan = 50, row = 0, sticky = W)
        Label(self.applicationForm,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 10).grid(column = 0, columnspan = 50, row = 1, sticky = W)

    
        Button(self.applicationForm,text = "Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)

        self.lastState = "Application Form"
        self.applicationForm.configure(background='#E9EAED')
        
        Label(self.applicationForm,text = "Name:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 2, sticky = W)
        Label(self.applicationForm,text = "Date of Birth:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 3, sticky = W)
        Label(self.applicationForm,text = "Gender:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 4, sticky = W)
        Label(self.applicationForm,text = "Monthly Income ($):", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 5, sticky = W)
        Label(self.applicationForm,text = "Category of Apartment:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 6, sticky = W)
        Label(self.applicationForm,text = "Monthly Rent ($):", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 7, sticky = W)
        Label(self.applicationForm,text = "Preferred Move-in Date:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 8, sticky = W)
        Label(self.applicationForm,text = "Lease Term:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 9, sticky = W)
        Label(self.applicationForm,text = "Prev Residence:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 10, sticky = W)

        self.applicationName = Entry(self.applicationForm, width = 60)
        self.monthlyIncome = Entry(self.applicationForm, width = 20)
        
        self.bullet1 = IntVar()
        self.bullet2 = IntVar()
        uncheck1 = lambda: [self.bullet1.set(1), self.bullet2.set(0)] if self.bullet1.get() == 1 else [self.bullet1.set(0), self.bullet2.set(0)]
        uncheck2 = lambda: [self.bullet2.set(1), self.bullet1.set(0)] if self.bullet2.get() == 1 else [self.bullet2.set(0), self.bullet1.set(0)]
        self.check1 = Checkbutton(self.applicationForm, text = "Male", variable = self.bullet1, onvalue = 1, offvalue = 0, font = self.customFont13, background='#E9EAED', command=uncheck1)
        self.check2 = Checkbutton(self.applicationForm, text = "Female", variable = self.bullet2, onvalue = 1, offvalue = 0, font = self.customFont13, background='#E9EAED', command=uncheck2)
        
        self.years = list()
        self.months = list()
        self.days = list()
        self.min = list()
        self.max = list()
        self.category = list()
        self.leaseTerms = list()
                                     
        yearsList = range(1900,2014)
        monthsList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        daysList = range(1, 32)
        daysListSoft = range(1, 31)
        daysListFebNoLeap = range(1, 29)
        daysListFebLeap = range(1, 30)
        minList = []
        maxsList = []
        for x in range(500, 1001, 100):
            minList.append(x)
        for x in range(1000, 2001, 100):
            maxsList.append(x)
        categoryList = ["1bdr-1bth", "2bdr-1bth", "2bdr-2bth"]
        leaseTermsList = ["3 months", "6 months", "12 months"]
        datesList =[]
        i = 0
        today = datetime.date.today().toordinal()
        while i <= 180:
            d = date.fromordinal(today + i)
            datesList.append(d.isoformat())
            i = i + 1
            
        self.dropDownYear = IntVar()
        self.dropDownMonth = StringVar()
        self.dropDownDay = IntVar()
        self.dropDownMin = IntVar()
        self.dropDownMax = IntVar()
        self.dropDownCategory = StringVar()
        self.dropDownLeaseTerms = StringVar()
        self.dropDownMoveIn = StringVar()
        
        self.dropDownYear.set(1900)
        self.dropDownMonth.set("January")
        self.dropDownDay.set(1)
        self.dropDownMin.set(1000)
        self.dropDownMax.set(1700)
        self.dropDownCategory.set("1bdr-1bth")
        self.dropDownLeaseTerms.set("12 months")
        self.dropDownMoveIn.set(datesList[0])

        dropDownYearMenu = OptionMenu(self.applicationForm, self.dropDownYear, *yearsList)
        dropDownMonthMenu = OptionMenu(self.applicationForm, self.dropDownMonth, *monthsList)
        
        dropDownDayMenu = OptionMenu(self.applicationForm, self.dropDownDay, *daysList)
        
        dropDownMinMenu = OptionMenu(self.applicationForm, self.dropDownMin, *minList)
        dropDownMaxMenu = OptionMenu(self.applicationForm, self.dropDownMax, *maxsList)
        dropDownCategoryMenu = OptionMenu(self.applicationForm, self.dropDownCategory, *categoryList)
        dropDownLeaseTermsMenu = OptionMenu(self.applicationForm, self.dropDownLeaseTerms, *leaseTermsList)
        dropDownMoveInMenu = OptionMenu(self.applicationForm, self.dropDownMoveIn, *datesList)


        self.applicationName.grid(column = 2, columnspan = 3, row = 2, sticky = W)
        dropDownYearMenu.grid(column = 2, row = 3, sticky = W)
        dropDownMonthMenu.grid(column = 3, row = 3, sticky = W)
        dropDownDayMenu.grid(column = 4, row = 3, sticky = W)
        self.check1.grid(column = 2,row = 4, sticky = W)
        self.check2.grid(column = 3,row = 4, sticky = W)
        self.monthlyIncome.grid(column = 2, columnspan = 3, row = 5, sticky = W)
        dropDownCategoryMenu.grid(column=2, columnspan = 3, row = 6, sticky = W)
        Label(self.applicationForm,text = "Min:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2, row = 7, sticky = W)
        Label(self.applicationForm,text = "Max:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 4, row = 7, sticky = W)
        dropDownMinMenu.grid(column = 3, row = 7, sticky = W)
        dropDownMaxMenu.grid(column = 5, row = 7, sticky = W)
        dropDownMoveInMenu.grid(column = 2, row = 8, sticky = W)
        dropDownLeaseTermsMenu.grid(column = 2, row = 9, sticky = W)
        self.prevResidence = Text(self.applicationForm,width = 40,height = 8, background='#FFFFFF')
        self.prevResidence.grid(column = 2, row = 10, columnspan = 10, sticky = SW)
        Label(self.applicationForm,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 175, pady = 10).grid(column = 0, row = 11, sticky = W)

            
        submitButton = Button(self.applicationForm, text="Submit", command = self.SubmitApplicationCheck) #bind the function that inserts this user's data to database (or whatever)
        submitButton.grid(row=11, column=5, columnspan=10, sticky=S) #change column number if necessary


    def SubmitApplicationCheck(self):
        self.lastState = "Application Finished"
        self.buttonNotPressed = False
        if self.bullet1.get() is 0 and self.bullet2.get() is 0:
            messagebox.showerror("Invalid gender", "Please enter your gender")
            return None

        gender = "Male" if self.bullet1.get() is 1 else "Female"
        Username = self.username.get()
        applicationName = self.applicationName.get()
        monthlyIncome = self.monthlyIncome.get()
        DOByear = self.dropDownYear.get()
        DOBmonth = self.dropDownMonth.get()
        DOBday = str(self.dropDownDay.get())
        minMonthlyRent = self.dropDownMin.get()
        maxMonthlyRent = self.dropDownMax.get()
        aptCategory = self.dropDownCategory.get()
        leaseTerm = self.dropDownLeaseTerms.get()
        moveInDate = self.dropDownMoveIn.get()
        prevResidence = self.prevResidence.get("1.0", END)

        #sanity check

        if Username == "":
            messagebox.showerror("Invalid login", "Please register again")
            return None

        if applicationName == "":
            messagebox.showerror("Invalid name entry", "Please enter a name")
            return None
            
        if monthlyIncome == "":
            messagebox.showerror("Invalid monthly income", "Please enter a monthly income")
            return None

        if monthlyIncome.isdigit() == False:
            print(monthlyIncome.isdigit())
            messagebox.showerror("Invalid monthly income", "Please enter a value")
            return None

        if prevResidence == "":
            messagebox.showerror("Invalid previous residence", "Please enter a previous residence")
            return None

        if leaseTerm == "12 months":
            leaseTerm = 12
        elif leaseTerm == "6 months":
            leaseTerm = 6
        else:
            leaseTerm = 3

        def monthToNum(date):
            return{
                    'January' : '01',
                    'February' : '02',
                    'March' : '03',
                    'April' : '04',
                    'May' : '05',
                    'June' : '06',
                    'July' : '07',
                    'August' : '08',
                    'September' : '09', 
                    'October' : '10',
                    'November' : '11',
                    'December' : '12'
            }[date]

        def dayFormat(day):
            return {
                    '1' : '01',
                    '2' : '02',
                    '3' : '03',
                    '4' : '04',
                    '5' : '05',
                    '6' : '06',
                    '7' : '07',
                    '8' : '08',
                    '9' : '09'
            }[day]
                    

        DOBmonth = monthToNum(DOBmonth)
        if self.dropDownDay.get() < 10:
            DOBday = dayFormat(DOBday)

        DOB = str(DOByear) + "-" + DOBmonth + "-" + DOBday

        leapYearFlag = False
        
        if self.dropDownYear.get() % 4 == 0:
            if self.dropDownYear.get() % 100 == 0:
                if self.dropDownYear.get() % 400 == 0:
                    leapYearFlag = True
                else:
                    leapYearFlag = False
            else:
                leapYearFlag = True      
        else:
            leapYearFlag = False
            
        if leapYearFlag == False and self.dropDownMonth.get() == "February":
            if self.dropDownDay.get() == 29 or self.dropDownDay.get() == 30 or self.dropDownDay.get() == 31:
                messagebox.showerror("Invalid", "Please enter a valid date! This month and this year has only 28 days! (No Leap)")
                return None
        elif leapYearFlag == True and self.dropDownMonth.get() == "February":
            if self.dropDownDay.get() == 30 or self.dropDownDay.get() == 31:
                messagebox.showerror("Invalid", "Please enter a valid date! This month and this year has only 29 days! (Leap)")
                return None
        elif self.dropDownMonth.get() == "April" or self.dropDownMonth.get() == "June" or self.dropDownMonth.get() == "September" or self.dropDownMonth.get() == "November":
            if self.dropDownDay.get() == 31:
                messagebox.showerror("Invalid", "Please enter a valid date! This month has only 30 days!")
                return None
        
        database.execute_insert('''insert into PROSPECTIVE_RESIDENT values (?,?,?,?,?,?,?,?,?,?,?)''',
                                (Username, moveInDate, leaseTerm, gender, applicationName, DOB, monthlyIncome, minMonthlyRent, maxMonthlyRent, prevResidence, aptCategory))
        messagebox.showinfo("Welcome", "Thank you for your application! Please kindly wait for our feedback!")
        self.applicationForm.withdraw()
        self.window.deiconify()

        
    #-------------------------------------------------------------- Homepage (Figure 4) ---------------------------------------------------------
    def ResidentHomepage(self):
        if self.lastState != "Pay Rent" or self.lastState != "Request Maintenance" or self.lastState != "Payment Information" :
            self.window.withdraw()
            self.residentHomepage.deiconify()
        else:
            self.residentHomepage.deiconify()

        for child in self.residentHomepage.winfo_children():
            child.destroy()
        self.residentHomepage.configure(background='#E9EAED')       
        Label(self.residentHomepage,text = "Homepage", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 360, pady = 18).grid(column = 0, columnspan = 3, row = 0, sticky = W)
        Label(self.residentHomepage,text = "Hello Resident! (" + self.username.get() +")", font = self.customFont13B, background = '#E9EAED', pady = 10, padx = 15).grid(column = 0, columnspan = 3, row = 1, sticky = W)
    
        Label(self.residentHomepage,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 20).grid(column = 0, columnspan = 3, row = 2, sticky = W)
        
        Button(self.residentHomepage,text = "Log Out", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        
   
        Button(self.residentHomepage, text = "Pay Rent", command = self.PayRent, font = self.customFont13B, background = '#FF0000', foreground = '#FFFFFF').grid(column = 0, row = 3)
        Button(self.residentHomepage, text = "Request Maintenance", command = self.RequestMaintenance, font = self.customFont13).grid(column = 1, row = 3)
        Button(self.residentHomepage, text = "Payment Information", command = self.PaymentInformation, font = self.customFont13).grid(column = 2, row = 3)
        self.residentHomepage.configure(background='#E9EAED')

        getResidentList = database.execute_select('''SELECT Ano FROM RESIDENT NATURAL JOIN PROSPECTIVE_RESIDENT WHERE Username = ?''', (self.username.get(),))
        self.getResident = getResidentList[0]["Ano"]

        
        messageCount = database.execute_select('''SELECT count(*) FROM REMINDER WHERE Status = ? AND Ano = ?''',("Unread",self.getResident))[0]["count(*)"]
        if messageCount > 0:
            Button(self.residentHomepage,text = "You have " + str(messageCount) + " message from the department", font = self.customFont13B, command = self.ViewMessage,background = '#E9EAED',foreground = '#FF0000').grid(column = 2, row = 1, sticky = W)
        
  
        self.lastState = "Resident Homepage"
    def ViewMessage(self):
        actualMessageList = database.execute_select('''SELECT * FROM REMINDER WHERE Status = ? AND Ano = ? ORDER BY Rdate ASC''',("Unread",self.getResident))
        x = 1
        for eachDict in actualMessageList:
            actualMessage = eachDict["Message"]
            date = eachDict["Rdate"]
            messagebox.showinfo("Message " + str(x), date + " " + actualMessage )
            x = x + 1
        database.execute_insert('''UPDATE REMINDER SET Status = ? WHERE Ano = ?''', ("Read", self.getResident))
        self.residentHomepage.withdraw()
        self.ResidentHomepage()

    def ManagementHomepage(self):
        if self.lastState != "Application Review" or self.lastState != "Leasing Report" or self.lastState != "Service Report" or self.lastState != "Rent Defaulters" or self.lastState != "Reminder" or self.lastState != "Application Review" :
            self.window.withdraw()
            self.managementHomepage.deiconify()
        else:
            self.managementHomepage.deiconify()

        for child in self.managementHomepage.winfo_children():
            child.destroy()
        self.lastState = "Management Homepage"
        self.managementHomepage.configure(background='#E9EAED')
        
        Label(self.managementHomepage,text = "Homepage", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 360, pady = 18).grid(column = 0, columnspan = 3, row = 0, sticky = W)
        Label(self.managementHomepage,text = "Hello Manager! (" + self.username.get() +")", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 0, columnspan = 3,row = 1, sticky = W)
        Label(self.managementHomepage,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 20).grid(column = 0, columnspan = 3, row = 2, sticky = W)
        Button(self.managementHomepage,text = "Log Out", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        
   
        Button(self.managementHomepage, text = "Application Review", command = self.ApplicationReview, font = self.customFont13).grid(column = 0, row = 3)
        Button(self.managementHomepage, text = "Maintenance Results", command = self.ViewMaintenanceRequest, font = self.customFont13).grid(column = 1, row = 3)
        Button(self.managementHomepage, text = "Rent Reminder", command = self.Reminder, font = self.customFont13).grid(column = 2, row = 3)
        self.managementHomepage.configure(background='#E9EAED')

        reportList = ["Rent Defaulters Report", "3 Months Leasing Report", "Service Resolution Report"]
     
        self.dropDownReports = StringVar()
        self.dropDownReports.set("Rent Defaulters Report")
        dropDownReportsMenu = OptionMenu(self.managementHomepage, self.dropDownReports, *reportList)
        Label(self.managementHomepage,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 20).grid(column = 0, columnspan = 3, row = 4, sticky = W)
        Label(self.managementHomepage,text = "Select Reports:", font = self.customFont13B, background = '#E9EAED').grid(column = 0,row = 5, sticky = E)
        dropDownReportsMenu.grid(column = 1, row = 5, sticky = W)
        
        Button(self.managementHomepage, text = "View", command = self.chooseReport, font = self.customFont13).grid(column = 2, row = 5)

    def chooseReport(self):
        if str(self.dropDownReports.get()) == "Rent Defaulters Report":
            self.RentDefaulters()
        if str(self.dropDownReports.get()) == "3 Months Leasing Report":
            self.LeasingReport()
        if str(self.dropDownReports.get()) == "Service Resolution Report":
            self.ServiceReport()
        
   #-------------------------------------------------------------- Rent (Figure 5) ---------------------------------------------------------
    #GUI
    def PayRent(self):
        
        self.residentHomepage.withdraw()
        self.rent.deiconify()
        for child in self.rent.winfo_children():
            child.destroy()
        self.rent.configure(background='#E9EAED')

        Label(self.rent,text = "Rent", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 375, pady = 18).grid(column = 0, columnspan = 50, row = 0, sticky = W)

        Label(self.rent,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 10).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        
        Button(self.rent,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        

        Label(self.rent,text = "Date:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 2, sticky = W)
        Label(self.rent,text = "Apartment No:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 3, sticky = W)
        Label(self.rent,text = "Rent for Month:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 4, sticky = W)
        Label(self.rent,text = "Amount Due ($):", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 5, sticky = W)
        Label(self.rent,text = "Use Card", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 6, sticky = W)

        apartmentDict = database.execute_select('''SELECT Ano FROM RESIDENT NATURAL JOIN PROSPECTIVE_RESIDENT WHERE Username = ?''', (self.username.get(),))

        self.apartmentNumber = apartmentDict[0]["Ano"]


        cardListofDict = database.execute_select('''SELECT Card_no FROM PAYMENT_INFOMATION NATURAL JOIN RESIDENT WHERE Ano = ? AND Rname = Name AND Rbdate = DOB''', (self.apartmentNumber,))
        cardList = [];
        for eachDict in cardListofDict:
                cardList.append(eachDict["Card_no"])
        todayDate = datetime.date.today()

        monthsList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    
              
        self.years = list()
        self.months = list()
        self.dates = list()
        

                                     
        yearsList = range(2014, 2015)
        
        datesList =[]
        i = 0
        today = datetime.date.today().toordinal()
        
        while i <= 180:
            d = date.fromordinal(today + i)
            datesList.append(d.isoformat())
            i = i + 1

        self.dropDownYear = IntVar()
        self.dropDownMonth = StringVar()
        self.dropDownDate = StringVar()
        self.dropDownCard = IntVar()
        
          
        self.dropDownDate.set(datesList[0])
        self.dropDownYear.set(2014)

        self.dropDownMonth.set(monthsList[todayDate.month - 1])
        self.selectedMonthUpper = monthsList[todayDate.month - 1].upper()
        self.dropDownMonth.trace('w', self.monthChange)
        self.dropDownDate.trace('w', self.dateChange)

        self.dropDownCard.set(cardList[0])
        

        dropDownDateMenu = OptionMenu(self.rent, self.dropDownDate, *datesList)
        dropDownYearMenu = OptionMenu(self.rent, self.dropDownYear, *yearsList)
        self.dropDownMonthMenu = OptionMenu(self.rent, self.dropDownMonth, *monthsList)
        dropDownCardMenu = OptionMenu(self.rent, self.dropDownCard, *cardList)

        
       

        
        
        dropDownDateMenu.grid(column = 2, row = 2, sticky = W)
        Label(self.rent,text = self.apartmentNumber, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 3, sticky = W)
        self.dropDownMonthMenu.grid(column = 2, row = 4, sticky = W)
        dropDownYearMenu.grid(column = 3, row = 4, sticky = W)
        #Label(self.rent,text = self.amountDue, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
        dropDownCardMenu.grid(column = 2, row = 6, sticky = W)
        self.lastState = "Pay Rent"

        PayButton = Button(self.rent, text="Pay Rent", command = self.PayRentCheck) #bind correct function
        PayButton.grid(row=7, column=3, sticky=S) #change column # to move button left/right
 

    def monthChange(self, *args):
        self.lastStateFlag = "setting"
        self.selectedMonth = self.dropDownMonth.get()
        self.selectedMonthUpper = self.dropDownMonth.get().upper()

       
        amountDueDict = database.execute_select('''SELECT * FROM PAY_RENT WHERE Ano  = ? AND D_month = ? AND Payment_date IS NULL''', (self.apartmentNumber, self.selectedMonthUpper))
        print(amountDueDict)
        if amountDueDict != []:
            self.amountDue = amountDueDict[0]["Amount"]
            Label(self.rent,text = "XXXXXX", font = self.customFont13, background = '#E9EAED', foreground = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
            Label(self.rent,text = self.amountDue, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
        else:
            self.amountDue = 0
            Label(self.rent,text = "XXXXXX", font = self.customFont13, background = '#E9EAED', foreground = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
            Label(self.rent,text = self.amountDue, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)

    def dateChange(self, *args):
        todayDate = datetime.date.today()

        getDate = self.dropDownDate.get()

        d1 =  date(int(getDate[0:4]), int(getDate[5:7]), int(getDate[8:10]));
        if int(getDate[8:10]) > 3:
            datedifference = (d1 - todayDate).days
            amountDueDict = database.execute_select('''SELECT Amount FROM PAY_RENT WHERE Ano  = ? AND D_month = ? AND Payment_date IS NULL''', (self.apartmentNumber, self.selectedMonthUpper))
            if amountDueDict != []:
                self.amountDue = amountDueDict[0]["Amount"]
                self.amountDue = self.amountDue + datedifference * 50
                Label(self.rent,text = "XXXXXX", font = self.customFont13, background = '#E9EAED', foreground = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
                Label(self.rent,text = self.amountDue, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
            else:
                self.amountDue = 0
                Label(self.rent,text = "XXXXXX", font = self.customFont13, background = '#E9EAED', foreground = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)
                Label(self.rent,text = self.amountDue, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 5, sticky = W)


            
            

    
    

        


    def PayRentCheck(self):
        payYear = self.dropDownYear.get()
        payMonth = self.dropDownMonth.get()
        payDate = self.dropDownDate.get()
        amountDue = self.amountDue
        cardNo = self.dropDownCard.get()
        apartmentNumber = self.apartmentNumber
        payMonth = payMonth.upper()
        
        paymentListDict = database.execute_select('''SELECT Payment_date FROM PAY_RENT WHERE Ano = ? AND D_month = ? AND D_year = ?''', (apartmentNumber, payMonth, payYear))
        if self.amountDue == 0 :
            messagebox.showinfo("Payment error", "You have already payed for this month.")
            return None

        database.execute_insert('''UPDATE PAY_RENT SET Payment_date = ?, Amount = ?, Cno = ? WHERE Ano = ? AND D_month = ? AND D_year = ?''', (payDate, amountDue, cardNo, apartmentNumber,  payMonth, payYear ))

   

        messagebox.showinfo("Payment successful", "Thank you for your payment")

        self.ResidentHomepage()
        
    def RequestMaintenance(self):
        self.residentHomepage.withdraw()
        self.requestMaintenance.deiconify()
        for child in self.requestMaintenance.winfo_children():
            child.destroy()
        self.requestMaintenance.configure(background = '#E9EAED')

        Label(self.requestMaintenance,text = "Request Maintenance", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 290, pady = 18).grid(column = 0, columnspan = 5, row = 0, sticky = W)
        Label(self.requestMaintenance,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 10).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        
        Button(self.requestMaintenance,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)

        self.today = datetime.date.today().toordinal()
        self.d = date.fromordinal(self.today)
        Label(self.requestMaintenance, text = "Date of Request (yyyy/mm/dd):", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 2,row = 2, sticky = E)
        Label(self.requestMaintenance, text = self.d, font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 3,row = 2, sticky = W)

        apartmentDict = database.execute_select('''SELECT Ano FROM RESIDENT NATURAL JOIN PROSPECTIVE_RESIDENT WHERE Username = ?''', (self.username.get(),))
        self.apartmentNumber = apartmentDict[0]["Ano"]

        Label(self.requestMaintenance,text = "Apartment No:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1,row = 3, sticky = W)
        Label(self.requestMaintenance,text = self.apartmentNumber, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2,row = 3, sticky = W)

        issueListofDict = database.execute_select('''SELECT * FROM ISSUE''', None)
        issueList = [];
        for eachDict in issueListofDict:
                issueList.append(eachDict["Issue_type"])
        self.dropDownIssue = StringVar()
        self.dropDownIssue.set(issueList[0])
        dropDownIssueMenu = OptionMenu(self.requestMaintenance, self.dropDownIssue, *issueList)
        Label(self.requestMaintenance,text = "Issue", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, row = 4, sticky = W)
        dropDownIssueMenu.grid(column = 2, row = 4, sticky = W)
        self.lastState = "Request Maintenance"

        MaintenanceButton = Button(self.requestMaintenance, text="Request Maintenance", command = self.RequestMaintenanceInsert) #bind correct function
        MaintenanceButton.grid(row=5, column=3, sticky=S) #change column # to move button left/right

    def RequestMaintenanceInsert(self):
        date = str(self.d)
        ApartmentNo = self.apartmentNumber
        issue = self.dropDownIssue.get()
        date = date.replace("-", ",")
        checkOccurence = database.execute_select('''SELECT * FROM MAINTENACE_REQUEST WHERE Ano = ? AND Req_date = ? AND I_type = ? ''', (ApartmentNo,date,issue))
        print(checkOccurence)
        if checkOccurence == []:
            database.execute_insert('''insert into MAINTENACE_REQUEST values (?,?,?,?)''', (ApartmentNo, date, issue, None))
            messagebox.showinfo("Maintenance Request Success", "Thank you for your request, we will fix it as soon as possible.")
        else:
            messagebox.showerror("Duplicate", "You have already submitted this issue today")
            
        
        self.requestMaintenance.withdraw()
        self.ResidentHomepage()
        
    def PaymentInformation(self):
        self.residentHomepage.withdraw()
        self.paymentInformation.deiconify()
        self.paymentInformation.configure(background = '#E9EAED')

        Label(self.paymentInformation,text = "Payment Information", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 290, pady = 18).grid(column = 0, columnspan = 8, row = 0, sticky = W)
        Label(self.paymentInformation,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        
        Button(self.paymentInformation,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)

        Label(self.paymentInformation,text = "Add Card", font = self.customFont13B, background = '#E9EAED', pady = -50).grid(column = 2,row = 2, sticky = W)
        Label(self.paymentInformation,text = "Delete Card Information", font = self.customFont13B, background = '#E9EAED', pady = -50).grid(column = 4, row = 2, sticky = E)
        Label(self.paymentInformation,text = "Card Number:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = 4, sticky = W)
        Label(self.paymentInformation,text = "Expiration Date:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = 5, sticky = W)
        Label(self.paymentInformation,text = "CVV:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = 6, sticky = W)
        Label(self.paymentInformation,text = "Bank:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = 7, sticky = W)  
        Label(self.paymentInformation,text = "Select Card:", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 3, padx = 15, row = 4, sticky = E)

        datesList =[]
        i = 0
        today = datetime.date.today().toordinal()
        while i <= 180:
            d = date.fromordinal(today + i)
            datesList.append(d.isoformat())
            i = i + 1
        datesList = sorted({"-".join(x.split("-")[:2]) for x in datesList})
        self.dropDownDate = StringVar()
        self.dropDownDate.set(datesList[0])
        dropDownDateMenu = OptionMenu(self.paymentInformation, self.dropDownDate, *datesList)

        apartmentDict = database.execute_select('''SELECT Ano FROM RESIDENT NATURAL JOIN PROSPECTIVE_RESIDENT WHERE Username = ?''', (self.username.get(),))
        self.apartmentNumber = apartmentDict[0]["Ano"]

        self.cardListofDict = database.execute_select('''SELECT SUBSTR(Card_no,(length(Card_no)-3),4) FROM PAYMENT_INFOMATION NATURAL JOIN RESIDENT WHERE Ano = ? AND Rname = Name AND Rbdate = DOB''', (self.apartmentNumber,))
        cardList = [];
        #print(cardListofDict)
        for eachDict in self.cardListofDict:
            cardList.append(eachDict["SUBSTR(Card_no,(length(Card_no)-3),4)"])
                
        self.dropDownCard = IntVar()
        self.dropDownCard.set(cardList[0])
        dropDownCardMenu = OptionMenu(self.paymentInformation, self.dropDownCard, *cardList)
        dropDownCardMenu.grid(column = 4, columnspan = 2, row = 4, sticky = W)

        self.newCardNumber = Entry(self.paymentInformation,width = 20)
        self.newCVV = Entry(self.paymentInformation,width = 20)
        self.newBank = Entry(self.paymentInformation, width = 20)

        self.newCardNumber.grid(column = 1, columnspan = 2, row = 4, sticky = W)
        dropDownDateMenu.grid(column = 1, columnspan = 2, row = 5, sticky = W)
        self.newCVV.grid(column = 1, columnspan = 2, row = 6, sticky = W)
        self.newBank.grid(column = 1, columnspan = 2, row = 7, sticky = W)

        Button(self.paymentInformation, text = "Save", command = self.SaveCard, font = self.customFont13).grid(column = 2, row = 8)
        Button(self.paymentInformation, text = "Delete", command = self.DeletCard, font = self.customFont13).grid(column = 4, row = 8)
        self.lastState = "Payment Information"

    def SaveCard(self):
        cardNum = self.newCardNumber.get()
        expDate = self.dropDownDate.get()
        CVV = self.newCVV.get()
        bank = self.newBank.get()
        DOBdict = database.execute_select('''SELECT DOB FROM RESIDENT NATURAL JOIN PAYMENT_INFOMATION WHERE Ano = ? AND Rname = Name''', (self.apartmentNumber,))
        DOB = DOBdict[0]["DOB"]
        RnameDict = database.execute_select('''SELECT Name FROM RESIDENT WHERE Ano = ? AND DOB = ?''', (self.apartmentNumber, DOB))
        name = RnameDict[0]["Name"]
        
        if bank == "":
            messagebox.showerror("Bank error", "Please enter a bank")
            return None

        if len(CVV) is not 3:
            messagebox.showerror("CVV Error", "Length of CVV must be 3")
            return None

        if len(cardNum) < 10 or len(cardNum) > 16:
            messagebox.showerror("Card Error", "Length of Card number must be between 10 and 16, inclusive")
            return None

        try:
            CVV = int(CVV)
        except:
            messagebox.showerror("CVV Error", "Please enter a number value for CVV")
            return None

        try:
            cardNum = int(cardNum)
        except:
            messagebox.showerror("Card Number Error", "Please enter a number value for card number")
            return None
        
        database.execute_insert('''insert into PAYMENT_INFOMATION values (?,?,?,?,?,?)''', (cardNum, expDate, CVV, bank, name, DOB))
        messagebox.showinfo("Card Add Success", "Card added successfully")

        self.paymentInformation.withdraw()
        self.ResidentHomepage()
        
    def DeletCard(self):
        if len(self.cardListofDict) is 1:
            messagebox.showerror("Delete card error", "Cannot delete last card, we must have one on file")
            return None

        database.execute_insert('''DELETE FROM PAYMENT_INFOMATION WHERE SUBSTR(Card_no,(length(Card_no)-3),4) = ?''', (str(self.dropDownCard.get()),))
        messagebox.showinfo("Delete card success", "Card deleted successfully")
        self.paymentInformation.withdraw()
        self.ResidentHomepage()
        
    def ApplicationReview(self):
        if self.lastState != "Apartment Allotment":
            self.managementHomepage.withdraw()
            self.applicationReview.deiconify()
	    
        else:
            self.applicationReview.deiconify()

        for child in self.applicationReview.winfo_children():
            child.destroy()

        self.applicationReview.configure(background = '#E9EAED')

        Label(self.applicationReview,text = "Application Review", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 710, pady = 18).grid(column = 0, columnspan = 9, row = 0, sticky = W)
        Label(self.applicationReview,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        Button(self.applicationReview,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        
        Label(self.applicationReview,text = "Name", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "DOB", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 1, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "(yyyy,mm,dd)", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 1, padx = 15, row = 3, sticky = W)
        Label(self.applicationReview,text = "Gender", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 2, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "Monthly Income ($)", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 3, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "Request Cat.", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 4, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "Pref. Move Date", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 5, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "(yyyy,mm,dd)", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 5, padx = 15, row = 3, sticky = W)
        Label(self.applicationReview,text = "Lease Term", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 6, padx = 15, row = 2, sticky = W)
        Label(self.applicationReview,text = "Accept/Reject", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 7, padx = 15, row = 2, sticky = W)
        prospectiveResidentList = database.execute_select('''SELECT Name, DOB,  Gender, Month_income, Req_category, Pref_date, Pref_lease FROM PROSPECTIVE_RESIDENT AS a WHERE NOT EXISTS (SELECT * FROM RESIDENT AS b WHERE a.Name = b.Name) ''', None)
        rowIndex = 4
        
        self.bullets = dict()
        self.Name = dict()
        today = datetime.date.today()
        for eachDict in prospectiveResidentList:
            monthlyIncome = eachDict["Month_income"]
            reqeustedCat = eachDict["Req_category"]
            namePros = eachDict["Name"]
            preferDate = eachDict["Pref_date"]
            
            Label(self.applicationReview,text = namePros, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = rowIndex, sticky = W)
            Label(self.applicationReview,text = eachDict["DOB"], font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 1, padx = 15, row = rowIndex, sticky = W)
            Label(self.applicationReview,text = eachDict["Gender"], font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 2, padx = 15, row = rowIndex, sticky = W)
            Label(self.applicationReview,text = monthlyIncome, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 3, padx = 15, row = rowIndex, sticky = W)
            Label(self.applicationReview,text = reqeustedCat, font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 4, padx = 15, row = rowIndex, sticky = W)
            Label(self.applicationReview,text = eachDict["Pref_date"], font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 5, padx = 15, row = rowIndex, sticky = W)
            if eachDict["Pref_lease"] == 3:
                Label(self.applicationReview,text = "3 months", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 6, padx = 15, row = rowIndex, sticky = W)
            if eachDict["Pref_lease"] == 6:
                Label(self.applicationReview,text = "6 months", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 6, padx = 15, row = rowIndex, sticky = W)
            if eachDict["Pref_lease"] == 12:
                Label(self.applicationReview,text = "12 months", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 6, padx = 15, row = rowIndex, sticky = W)
            availableApartmentRent = database.execute_select('''SELECT MIN(Rent) FROM APARTMENT WHERE Lease_term is NULL AND Category = ? AND Available_on <= ?''', (eachDict["Req_category"], preferDate))

            minRentList = []

            for eachDict in availableApartmentRent:
                minRentList.append(eachDict["MIN(Rent)"])

            if minRentList[0] is None:
                Label(self.applicationReview,text = "Reject", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 7, row = rowIndex, sticky = W)
                self.bullet1 = IntVar()
                self.bullets[rowIndex - 3] = self.bullet1
                self.check1 = Checkbutton(self.applicationReview, variable = self.bullets[rowIndex -3], onvalue = 0, offvalue = 0, font = self.customFont13, background='#E9EAED', command=self.uncheckEverything(rowIndex - 3))
                #self.check1.grid(column = 8,row = rowIndex, sticky = W)
                #self.checkboxDict[rowIndex - 3] = self.bullet1
                self.Name[rowIndex - 4] = namePros
            else:
                if monthlyIncome <= (minRentList[0] * 3):
                    Label(self.applicationReview,text = "Reject", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 7, row = rowIndex, sticky = W)
                    self.bullet1 = IntVar()
                    self.bullets[rowIndex - 3] = self.bullet1
                    self.check1 = Checkbutton(self.applicationReview, variable = self.bullets[rowIndex -3], onvalue = 0, offvalue = 0, font = self.customFont13, background='#E9EAED', command=self.uncheckEverything(rowIndex - 3))
                    #self.check1.grid(column = 8,row = rowIndex, sticky = W)
                    #self.checkboxDict[rowIndex - 3] = self.bullet1
                    self.Name[rowIndex - 4] = namePros

                else:
                    Label(self.applicationReview,text = "Accept", font = self.customFont13, background = '#E9EAED', pady = 10).grid(column = 7, row = rowIndex, sticky = W)
                    self.bullet1 = IntVar()
                    self.bullets[rowIndex - 3] = self.bullet1
                    self.check1 = Checkbutton(self.applicationReview, variable = self.bullets[rowIndex -3], onvalue = rowIndex - 3, offvalue = 0, font = self.customFont13, background='#E9EAED', command=self.uncheckEverything(rowIndex - 3))
                    self.check1.grid(column = 8,row = rowIndex, sticky = W)
                    self.checkboxDict[rowIndex - 3] = self.bullet1
                    self.Name[rowIndex - 4] = namePros

                    

            rowIndex = rowIndex + 1
        
        Button(self.applicationReview, text = "Next", command = self.ApartmentAllotment, font = self.customFont13B, padx = 15, pady = 15).grid(column = 7, row = rowIndex+1)
            
        self.lastState = "Application Review"
        


    def uncheckEverything(self, index):
        def uncheck():
            for (x,y) in self.checkboxDict.items():
                if x == index:
                    pass
                else:
                    y.set(0)
        return uncheck

    def ApartmentAllotment(self):
        self.lastState = "Apartment Allotment"
        self.applicationReview.withdraw()
        self.apartmentAllotment.deiconify()

        for child in self.apartmentAllotment.winfo_children():
            child.destroy()

            
        self.apartmentAllotment.configure(background = '#E9EAED')
        

        x = 1
        y = 0
        for eachBullet in self.bullets:
            y = y + self.bullets[x].get()
            x = x + 1

        bulletChecked = y - 1

        prospectiveResidentList = database.execute_select('''SELECT * FROM PROSPECTIVE_RESIDENT as b WHERE NOT EXISTS (SELECT * FROM RESIDENT as c WHERE b.Name = c.Name) AND Name = ?''', (self.Name[bulletChecked],))
        for eachDict in prospectiveResidentList:
            self.requestedByPros = eachDict["Req_category"]
            self.nameofPros = eachDict["Name"]

        Label(self.apartmentAllotment,text = "Apartment Allotment", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 375, pady = 18).grid(column = 0, columnspan = 9, row = 0, sticky = W)
        Label(self.apartmentAllotment,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 6, row = 1, sticky = W)
        Label(self.apartmentAllotment,text = "Application Name: " + self.nameofPros , font = self.customFont13B, background = '#E9EAED', pady = 10, padx = 15).grid(column = 0, columnspan = 3, row = 1, sticky = W)

        Label(self.apartmentAllotment,text = "Apartment No", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 0, padx = 15, row = 2, sticky = W)
        Label(self.apartmentAllotment,text = "Category", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 1, padx = 15, row = 2, sticky = W)
        Label(self.apartmentAllotment,text = "Monthly Rent ($)", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 2, padx = 15, row = 2, sticky = W)
        Label(self.apartmentAllotment,text = "Sq Ft.", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 3, padx = 15, row = 2, sticky = W)
        Label(self.apartmentAllotment,text = "Available From ", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 4, padx = 15, row = 2, sticky = W)
        Label(self.apartmentAllotment,text = "Select", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 5, padx = 15, row = 2, sticky = W)

        availability = database.execute_select('''SELECT Apt_number, Category, Rent, Sq_ft, Available_on FROM APARTMENT as a WHERE NOT EXISTS (SELECT * FROM RESIDENT as b WHERE a.Apt_number = b.Ano) AND Category = ? ORDER BY Rent DESC''', (self.requestedByPros,))
        self.i = 3
        self.selectApartment = dict()
        self.checkboxApartmentDict = dict()
        self.Apt = dict()
        
        for eachDict in availability:
            self.Apt_number = eachDict["Apt_number"]
            self.Category = eachDict["Category"]
            self.Rent = eachDict["Rent"]
            self.Sq_ft = eachDict["Sq_ft"]
            self.Available_on = eachDict["Available_on"]
            
            Label(self.apartmentAllotment,text = self.Apt_number, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = self.i, sticky = W)
            Label(self.apartmentAllotment,text = self.Category, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 1, padx = 15, row = self.i, sticky = W)
            Label(self.apartmentAllotment,text = self.Rent, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = self.i, sticky = W)
            Label(self.apartmentAllotment,text = self.Sq_ft, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = self.i, sticky = W)
            Label(self.apartmentAllotment,text = self.Available_on, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = self.i, sticky = W)
            
            self.selectApartmentBullet = IntVar()
            self.selectApartment[self.i - 2] = self.selectApartmentBullet
            self.check1 = Checkbutton(self.apartmentAllotment, variable = self.selectApartment[self.i -2], onvalue = self.i - 2, offvalue = 0, font = self.customFont13, background='#E9EAED', command = self.uncheckEverything(self.i - 2))
            self.check1.grid(column = 5,row = self.i, sticky = W)
            self.checkboxDict[self.i - 2] = self.selectApartmentBullet
            self.Apt[self.i - 3] = self.Apt_number
            self.i = self.i + 1
           

        


        Label(self.apartmentAllotment,text = "Apartment Availability", font = self.customFont13B, background = '#E9EAED', pady = 10).grid(column = 3, row = 2, sticky = W)
        Button(self.apartmentAllotment,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        Button(self.apartmentAllotment,text = "Assign Apartment", font = self.customFont13B, background = '#DADADA', command = self.AssignApartment, padx = 20).grid(column = 5, row = self.i, sticky = W)
        
    def AssignApartment(self):
        x = 1
        y = 0
        for eachBullet in self.selectApartment:
            y = y + self.selectApartment[x].get()
            x = x + 1

        bulletChecked = y - 1
        print(bulletChecked)

        apartmentSelected = database.execute_select('''SELECT Apt_number FROM APARTMENT WHERE Apt_number = ?''', (self.Apt[bulletChecked],))
        prospectiveConcerned = database.execute_select('''SELECT Name, DOB, Pref_lease, Pref_date FROM PROSPECTIVE_RESIDENT WHERE Name = ?''', (self.nameofPros,))
        for eachDict in prospectiveConcerned:
            pName = eachDict["Name"]
            pDOB = eachDict["DOB"]
            pLease = eachDict["Pref_lease"]
            pMove = eachDict["Pref_date"]
        for eachDict in apartmentSelected:
            sApt = eachDict["Apt_number"]
            
        d1 = date(int(pMove[0:4]), int(pMove[5:7]), int(pMove[8:10]));
        newAvailable = d1 + relativedelta(months = pLease)
        messagebox.showinfo("Success","Apartment Assigned")
        database.execute_insert('''INSERT INTO RESIDENT VALUES (?,?,?)''', (sApt, pName, pDOB))
        database.execute_insert('''UPDATE APARTMENT SET Lease_term = ?, Available_on = ? WHERE Apt_number = ?''', (pLease,newAvailable, sApt))
        self.GoBack()
        

        
    def ViewMaintenanceRequest(self):
        self.managementHomepage.withdraw()
        self.viewRequests.deiconify()
        self.lastState = "View Maintenance"


        for child in self.viewRequests.winfo_children():
            child.destroy()
        self.viewRequests.configure(background = '#E9EAED')

        Label(self.viewRequests,text = "View Maintenance Request", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 290, pady = 18).grid(column = 0, columnspan = 8, row = 0, sticky = W)
        Label(self.viewRequests,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        Button(self.viewRequests,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        

        Label(self.viewRequests,text = "Date of Request", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = 2, sticky = W)
        Label(self.viewRequests,text ="Apt No", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 1, padx = 15, row = 2, sticky = W)
        Label(self.viewRequests,text = "Description", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 2, sticky = W)
        Label(self.viewRequests,text = "Select", font = self.customFont13B ,background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 2, sticky = W)

        Label(self.viewRequests,text = "(yyyy/mm/dd)", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = 3, sticky = W)

        pendingRequest = database.execute_select('''SELECT * FROM MAINTENACE_REQUEST WHERE Res_date IS NULL ORDER BY Req_date ASC''', None)
        resolvedRequest = database.execute_select('''SELECT * FROM MAINTENACE_REQUEST WHERE Res_date IS NOT NULL ORDER BY Res_date ASC''', None)

        rowIndex = 4
        self.selectResolve = dict()
        self.checkboxResolveDict = dict()
        self.reqdateList = dict()
        self.reqAptList = dict()
        self.iTypeList = dict()
        if pendingRequest != []:
            for eachDict in pendingRequest:
                self.reqdate = eachDict["Req_date"]
                self.reqApt = eachDict["Ano"]
                self.iType = eachDict["I_type"]
                Label(self.viewRequests,text = self.reqdate, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = rowIndex, sticky = W)
                Label(self.viewRequests,text = self.reqApt, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 1, padx = 15, row = rowIndex, sticky = W)
                Label(self.viewRequests,text = self.iType, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = rowIndex, sticky = W)

                self.selectResolveBullet = IntVar()
                self.selectResolve[rowIndex - 3] = self.selectResolveBullet
                self.check1 = Checkbutton(self.viewRequests, variable = self.selectResolve[rowIndex -3], onvalue = rowIndex - 3, offvalue = 0, font = self.customFont13, background='#E9EAED', command = self.uncheckEverything(rowIndex - 3))
                self.check1.grid(column = 3,row = rowIndex, sticky = W)
                self.checkboxDict[rowIndex - 3] = self.selectResolveBullet
                
                self.reqdateList[rowIndex - 4] = self.reqdate
                self.reqAptList[rowIndex - 4] = self.reqApt
                self.iTypeList[rowIndex - 4] = self.iType
                
                rowIndex = rowIndex + 1
            ResolveButton = Button(self.viewRequests, text="Resolved", command = self.ResolveIssue) #bind correct function
            ResolveButton.grid(row=rowIndex, column=3, sticky=S) #change column # to move button left/right
            rowIndex = rowIndex + 1
        Label(self.viewRequests,text = "Resolved Issues", font = self.customFont13B ,background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = rowIndex, sticky = W)
        rowIndex = rowIndex + 1
    
        Label(self.viewRequests,text = "Date of Request", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = rowIndex, sticky = W)
        Label(self.viewRequests,text = "Apt No", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 1, padx = 15, row = rowIndex, sticky = W)
        Label(self.viewRequests,text = "Description", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = rowIndex, sticky = W)
        Label(self.viewRequests,text = "Resolved on", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = rowIndex, sticky = W)

        rowIndex = rowIndex + 1

        Label(self.viewRequests,text = "(yyyy/mm/dd)", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = rowIndex, sticky = W)
        Label(self.viewRequests,text = "(yyyy/mm/dd)", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = rowIndex, sticky = W)

        rowIndex = rowIndex + 1
        for eachDict in resolvedRequest:
            self.reqdate2 = eachDict["Req_date"]
            self.reqApt2 = eachDict["Ano"]
            self.iType2 = eachDict["I_type"]
            self.resdate2 = eachDict["Res_date"]
            Label(self.viewRequests,text = self.reqdate2, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 0, padx = 15, row = rowIndex, sticky = W)
            Label(self.viewRequests,text = self.reqApt2, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 1, padx = 15, row = rowIndex, sticky = W)
            Label(self.viewRequests,text = self.iType2, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = rowIndex, sticky = W)
            Label(self.viewRequests,text = self.resdate2, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = rowIndex, sticky = W)

            rowIndex = rowIndex + 1
                
        

        allRequest = {x["Username"] for x in self.userList}
    def ResolveIssue(self):
        x = 1
        y = 0
        for eachBullet in self.selectResolve:
            y = y + self.selectResolve[x].get()
            x = x + 1

        bulletChecked = y - 1
        print(self.reqdateList[bulletChecked])
        print(self.reqAptList[bulletChecked])
        print(self.iTypeList[bulletChecked])

        self.today = datetime.date.today().toordinal()
        self.d = str(date.fromordinal(self.today))
        formattedDate= self.d.replace("-", ",")

        
        database.execute_insert('''UPDATE MAINTENACE_REQUEST SET Res_date = ? WHERE Ano = ? AND Req_date = ? AND I_type = ? ''', (formattedDate, self.reqAptList[bulletChecked], self.reqdateList[bulletChecked], self.iTypeList[bulletChecked]))
        messagebox.showinfo("Success","Resolved")
        
        self.viewRequests.withdraw()
        self.ViewMaintenanceRequest()
        

    def Reminder(self):
        self.managementHomepage.withdraw()
        self.lastState = "Reminder"
        self.reminder.deiconify()
        self.reminder.configure(background = '#E9EAED')

        month = datetime.datetime.now().strftime("%B")
        Month = month.upper()
        
        Label(self.reminder,text = "Reminder", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 375, pady = 18).grid(column = 0, columnspan = 2, row = 0, sticky = W)
        Label(self.reminder,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 18).grid(column = 0, columnspan = 2, row = 1, sticky = W)
        Button(self.reminder,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)

        Label(self.reminder,text = "Apartment No:  ", font = self.customFont13, background = '#E9EAED').grid(column = 0,row = 2,sticky = 'ew')
        Label(self.reminder,text = "Message:   ", font = self.customFont13, background = '#E9EAED').grid(column = 0,row = 3,sticky = 'ew')

        Label(self.reminder,text= "Date:  " + str(datetime.date.today()), background = '#E9EAED').grid(column=1,row=1,sticky="ew")
        self.message = "Your payment is past due. Please pay immediately."
        Label(self.reminder,text = self.message, background = '#E9EAED').grid(column=1,row=3,sticky= "w")
        self.ano = IntVar()
        self.date = datetime.date.today()

        dueDate = date(self.date.year, self.date.month, 3)
        if self.date > dueDate:
            anoDict = database.execute_select('''SELECT Ano FROM PAY_RENT WHERE Payment_date is NULL AND D_Month = ? ''', (Month,))
            anoList=[]
            for item in anoDict:
                ano = item["Ano"]
                anoList.append(int(ano))
            self.ano.set(anoList[0])
            self.dropDownAnoMenu = OptionMenu(self.reminder,self.ano,*anoList).grid(column=1,row=2,sticky="w")
        else:
            Label(self.reminder,text= "No Apartment", background = '#E9EAED').grid(column=1,row=2,sticky = W)
        
        
            

        
        

        Button(self.reminder,text ="Send",command=self.remind).grid(column=1,row=4)
        
        
        

    def remind(self):

        checkOccurence = database.execute_select('''SELECT * FROM REMINDER WHERE Ano = ? AND Rdate = ? ''', (self.ano.get(),self.date))
        if checkOccurence == []:
            database.execute_insert('''INSERT INTO REMINDER VALUES (?,?,?,?)''',(self.ano.get(),self.date,"Unread",self.message))
            messagebox.showinfo("Sent","Reminder Sent.")
        else:
            messagebox.showerror("Duplicate", "You have already submitted this reminder today")
            

 
        
    def LeasingReport(self):
        self.managementHomepage.withdraw()
        self.leasingReport.deiconify()
        self.leasingReport.configure(background = '#E9EAED')
        self.lastState = "Leasing Report"

        Label(self.leasingReport,text = "3 Month Leasing Report", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 290, pady = 18).grid(column = 0, columnspan = 8, row = 0, sticky = W)
        Label(self.leasingReport,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        Button(self.leasingReport,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
         
        Label(self.leasingReport,text = "Month", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 2, sticky = W)
        Label(self.leasingReport,text = "Category", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 2, sticky = W)
        Label(self.leasingReport,text = "No. of Apartments", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 4 , padx = 15, row = 2, sticky = W)

        Label(self.leasingReport,text = "August", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 3, sticky = W)
        Label(self.leasingReport,text = "1bdr-1bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 3, sticky = W)
        Label(self.leasingReport,text = "2bdr-1bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 4, sticky = W)
        Label(self.leasingReport,text = "2bdr-2bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 5, sticky = W)

        Label(self.leasingReport,text = "September", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 6, sticky = W)
        Label(self.leasingReport,text = "1bdr-1bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 6, sticky = W)
        Label(self.leasingReport,text = "2bdr-1bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 7, sticky = W)
        Label(self.leasingReport,text = "2bdr-2bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 8, sticky = W)

        Label(self.leasingReport,text = "October", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 9, sticky = W)
        Label(self.leasingReport,text = "1bdr-1bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 9, sticky = W)
        Label(self.leasingReport,text = "2bdr-1bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 10, sticky = W)
        Label(self.leasingReport,text = "2bdr-2bth", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 11, sticky = W)


        today = datetime.date.today()
        augustDate = date(today.year, 8, 1);
        septemberDate = date(today.year, 9, 1);
        octoberDate = date(today.year, 10, 1);

        numOfAptAug1bdr1bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '1bdr-1bth' AND Available_on > ? AND Lease_term IS NOT NULL ''', (augustDate,))
        Label(self.leasingReport,text = numOfAptAug1bdr1bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 3, sticky = W)
        numOfAptAug2bdr1bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '2bdr-1bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (augustDate,))
        Label(self.leasingReport,text = numOfAptAug2bdr1bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 4, sticky = W)
        numOfAptAug2bdr2bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '2bdr-2bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (augustDate,))
        Label(self.leasingReport,text = numOfAptAug2bdr2bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 5, sticky = W)
        
        numOfAptSep1bdr1bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '1bdr-1bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (septemberDate,))
        Label(self.leasingReport,text = numOfAptSep1bdr1bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 6, sticky = W)
        numOfAptSep2bdr1bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '2bdr-1bth' AND Available_on > ? AND Lease_term IS NOT NULL''',  (septemberDate,))
        Label(self.leasingReport,text = numOfAptSep2bdr1bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 7, sticky = W)
        numOfAptSep2bdr2bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '2bdr-2bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (septemberDate,))
        Label(self.leasingReport,text = numOfAptSep2bdr2bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 8, sticky = W)

        numOfAptOct1bdr1bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '1bdr-1bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (octoberDate,))
        Label(self.leasingReport,text = numOfAptOct1bdr1bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 9, sticky = W)
        numOfAptOct2bdr1bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '2bdr-1bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (octoberDate,))
        Label(self.leasingReport,text = numOfAptOct2bdr1bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 10, sticky = W)
        numOfAptOct2bdr2bth= database.execute_select('''SELECT count(*) FROM APARTMENT WHERE Category = '2bdr-2bth' AND Available_on > ? AND Lease_term IS NOT NULL''', (octoberDate,))
        Label(self.leasingReport,text = numOfAptOct2bdr2bth[0]["count(*)"], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 11, sticky = W)
        

        

        





        self.window.withdraw()
    def ServiceReport(self):
        self.managementHomepage.withdraw()
        self.serviceReport.deiconify()
        self.serviceReport.configure(background = '#E9EAED')

        requestsDict = database.execute_select('''SELECT * FROM MAINTENACE_REQUEST WHERE Res_date IS NOT NULL''', None)
        months = []
        for request in requestsDict:
            if request["Req_date"][5:7] not in months:
                months.append(request["Req_date"][5:7])

        month1IType = []
        month2IType = []
        month3IType = []
        
        for month in months:
            for request in requestsDict:
                if month in request["Req_date"][5:7]:
                    if month == "08":
                        if request["I_type"] not in month1IType:
                            month1IType.append(request["I_type"])
                    if month == "09":
                        if request["I_type"] not in month2IType:
                            month2IType.append(request["I_type"])
                    if month == "10":
                        if request["I_type"] not in month3IType:
                            month3IType.append(request["I_type"])

        avgDaysForMonth1 = []
        avgDaysForMonth2 = []
        avgDaysForMonth3 = []

        for iType in month1IType:
            count = 0
            avg = 0
            for request in requestsDict:
                if iType in request["I_type"] and "08" in request["Req_date"][5:7]:
                    if int(request["Res_date"][8:10]) - int(request["Req_date"][8:10]) is 0:
                        count = count + 1
                        avg = avg + 1
                    else:
                        avg = avg + int(request["Res_date"][8:10]) - int(request["Req_date"][8:10])
                        count = count + 1
            avgDaysForMonth1.append(int(avg / count))

        for iType in month2IType:
            count = 0
            avg = 0
            for request in requestsDict:
                if iType in request["I_type"] and "09" in request["Req_date"][5:7]:
                    if int(request["Res_date"][8:10]) - int(request["Req_date"][8:10]) is 0:
                        count = count + 1
                        avg = avg + 1
                    else:
                        avg = avg + int(request["Res_date"][8:10]) - int(request["Req_date"][8:10])
                        count = count + 1
            avgDaysForMonth2.append(int(avg / count))

        for iType in month3IType:
            count = 0
            avg = 0
            for request in requestsDict:
                if iType in request["I_type"] and "10" in request["Req_date"][5:7]:
                    if int(request["Res_date"][8:10]) - int(request["Req_date"][8:10]) is 0:
                        count = count + 1
                        avg = avg + 1
                    else:
                        avg = avg + int(request["Res_date"][8:10]) - int(request["Req_date"][8:10])
                        count = count + 1
            avgDaysForMonth3.append(int(avg / count))



        Label(self.serviceReport,text = "Service Request Resolution Report", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 290, pady = 18).grid(column = 0, columnspan = 8, row = 0, sticky = W)
        Label(self.serviceReport,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        Button(self.serviceReport,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        
        Label(self.serviceReport,text = "Month", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 2, sticky = W)
        Label(self.serviceReport,text = "Type of Request", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 2, sticky = W)
        Label(self.serviceReport,text = "Average No of Days", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 4 , padx = 15, row = 2, sticky = W)

        Label(self.serviceReport,text = "August", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 3, sticky = W)
        try:
            Label(self.serviceReport,text = month1IType[0], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 3, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth1[0], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 3, sticky = W)
        except:
            None
        try:
            Label(self.serviceReport,text = month1IType[1], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 4, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth1[1], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 4, sticky = W)
        except:
            None
        try:
            Label(self.serviceReport,text = month1IType[2], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 5, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth1[2], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 5, sticky = W)
        except:
            None

        Label(self.serviceReport,text = "September", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 6, sticky = W)
        try:
            Label(self.serviceReport,text = month2IType[0], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 6, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth2[0], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 6, sticky = W)
        except:
            None
        try:
            Label(self.serviceReport,text = month2IType[1], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 7, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth2[1], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 7, sticky = W)
        except:
            None
        try:
            Label(self.serviceReport,text = month2IType[2], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 8, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth2[2], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 8, sticky = W)
        except:
            None

        Label(self.serviceReport,text = "October", font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, padx = 15, row = 9, sticky = W)
        try:
            Label(self.serviceReport,text = month3IType[0], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 9, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth3[0], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 9, sticky = W)
        except:
            None
        try:
            Label(self.serviceReport,text = month3IType[1], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 10, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth3[1], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 10, sticky = W)
        except:
            None
        try:
            Label(self.serviceReport,text = month3IType[2], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 11, sticky = W)
            Label(self.serviceReport,text = avgDaysForMonth3[2], font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4, padx = 15, row = 11, sticky = W)
        except:
            None

        self.lastState = "Service Report"


    def RentDefaulters(self):
        
        self.managementHomepage.withdraw()
        self.rentDefaulters.deiconify()
        self.lastrowIndex = 4
        
        self.rentDefaulters.configure(background = '#E9EAED')

        monthsList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.dropDownMonth2 = StringVar()
        self.dropDownMonth2.set("January")
        dropDownMonthMenu = OptionMenu(self.rentDefaulters, self.dropDownMonth2, *monthsList)
        

        Label(self.rentDefaulters,text = "Rent Defaulters", font = self.headingFont, background = '#3C5A99', foreground='#FFFFFF', padx = 320, pady = 18).grid(column = 0, columnspan = 8, row = 0, sticky = W)
        Button(self.rentDefaulters,text = "Go Back", font = self.customFont13B, background = '#DADADA', command = self.GoBack, padx = 20).grid(column = 0, row = 0, sticky = W)
        
        Label(self.rentDefaulters,text = "Blank", font = self.headingFont, background = '#E9EAED', foreground='#E9EAED', padx = 375, pady = 5).grid(column = 0, columnspan = 50, row = 1, sticky = W)
        dropDownMonthMenu.grid(column = 3, row = 2, sticky = E)
        Label(self.rentDefaulters,text = "Apartment", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 2, row = 3, sticky = W)
        Label(self.rentDefaulters,text = "Extra Amount Paid($)", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = 3, sticky = W)
        Label(self.rentDefaulters,text = "Defaulted By", font = self.customFont13B, background = '#E9EAED', pady = 5).grid(column = 4 , padx = 15, row = 3, sticky = W)
        Button(self.rentDefaulters,text = "Select", font = self.customFont13, command = self.RentDefaultersView).grid(column = 4, row = 2, sticky = W)

        self.lastState = "Rent Defaulters"

    def RentDefaultersView(self):
        today = datetime.date.today()
        

        if self.lastrowIndex > 4 :

            for x in range(4, self.lastrowIndex):
                Label(self.rentDefaulters,text = "XXXX", font = self.customFont13, background = '#E9EAED', foreground='#E9EAED', pady = 5).grid(column = 2, row = x, sticky = W)
                Label(self.rentDefaulters,text = "XXXX", font = self.customFont13, background = '#E9EAED', foreground='#E9EAED', pady = 5).grid(column = 3, padx = 15, row = x, sticky = W)
                Label(self.rentDefaulters,text = "XXXX", font = self.customFont13, background = '#E9EAED', foreground='#E9EAED', pady = 5).grid(column = 4 , padx = 15, row = x, sticky = W)
                


        def monthToNum(int):
            return{
                    'January' : '01',
                    'February' : '02',
                    'March' : '03',
                    'April' : '04',
                    'May' : '05',
                    'June' : '06',
                    'July' : '07',
                    'August' : '08',
                    'September' : '09', 
                    'October' : '10',
                    'November' : '11',
                    'December' : '12'
            }[int]
        intMonth = monthToNum(self.dropDownMonth2.get())
   
        payrentInfoList = database.execute_select('''SELECT * FROM PAY_RENT WHERE D_Month = ? ''', (self.dropDownMonth2.get().upper(),))
        rowIndex = 4
        for eachDict in payrentInfoList:
            aptNo = eachDict["Ano"]
            theMonth = eachDict["D_month"]
            theYear = eachDict["D_year"]
            tempDate = eachDict["Payment_date"]
 
            if tempDate is None:
                payDay = today.day
            else:
                payDay = int(tempDate[8:10])
            if payDay > 3 :
                defaulted = (payDay - 3)
                extraPay =  defaulted * 50
                
                Label(self.rentDefaulters,text = aptNo, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 2, row = rowIndex, sticky = W)
                Label(self.rentDefaulters,text = extraPay, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 3, padx = 15, row = rowIndex, sticky = W)
                Label(self.rentDefaulters,text = defaulted, font = self.customFont13, background = '#E9EAED', pady = 5).grid(column = 4 , padx = 15, row = rowIndex, sticky = W)
                rowIndex = rowIndex + 1

        self.lastrowIndex = rowIndex
        
            


               
     
 



rootWin = Tk()
myGUI(rootWin)
rootWin.mainloop()
