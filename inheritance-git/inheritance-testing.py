import sqlite3
from tkinter import *
from tkinter import ttk
import os


class Welcome:
    def __init__(self, master):
        self.master = master

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screen_width, screen_height))  # size of window then offset
        self.master.title('Main Menu')

        Label(self.master, text='Welcome', font=("Times New Roman", "24", "bold")).pack()

        Button(self.master, text="Im A Carer", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.openCarer).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Im A Client", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.openClient).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Im An Admin", width=20, pady=5, padx=5,relief='sunken',bd=8,command=self.openAdmin).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Quit", width=20, pady=5, padx=5, relief='sunken', bd=8, command=self.Quit).pack(
            fill=BOTH)

    def openCarer(self):
        root = Toplevel(self.master)
        ImACarer(root)
        # CarerWindows(root)
    def openClient(self):
        root = Toplevel(self.master)
        ImAClient(root)
        # ClientWindows(root)

    def openAdmin(self):
        root = Toplevel(self.master)
        ImAnAdmin(root)
        # AdminWindows(root)

    def Quit(self):
        self.master.destroy()
        exit()
    # ============================================================================Carer Account Windows========================================================================


class LoginAccountWindow:
    def __init__(self, master):
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screen_width, screen_height))  # size of window then offset
        self.master.title('Account Window')

        self.Username = StringVar()
        self.Password = StringVar()

        Label(self.master, text="Login", font=("Times New Roman", "24", "bold"), pady=10, ).pack()

        Label(self.master, text='Username:', padx=5, fg='black').place(x=643, y=58)
        Label(self.master, text='Password:', padx=5, fg='black').place(x=646, y=77)

        username = Entry(self.master, textvariable=self.Username, highlightthickness=1)
        username.config( highlightcolor= "dark green")
        username.pack()

        password = Entry(self.master, textvariable=self.Password, show='*', highlightthickness=1)
        password.config( highlightcolor= "dark green")
        password.pack()


        Button(self.master, text="Login", width=20, pady=5, padx=5, relief='sunken', bd=8, command=self.Login).pack(fill=BOTH, pady = 2)
        Button(self.master, text="I Dont Have An Account", width=20, pady=5 , padx=5, relief='sunken', bd=8, command = self.Register).pack(fill=BOTH)



    def Register(self): #todo fix labels

        self.Username = StringVar()
        self.Password = StringVar()
        self.text = StringVar()
        self.text.set("")

        Label(self.master, text="Create An Account", font=("Times New Roman", "24", "bold"), pady=10, ).pack()

        Label(self.master, text='Username:', padx=5, fg='black').place(x=642, y=258)
        Label(self.master, text='Password:', padx=5, fg='black').place(x=645, y=280)

        Entry(self.master, textvariable=self.Username, highlightthickness=1).pack()

        Entry(self.master, textvariable=self.Password, show='*').pack()

        Button(self.master, text="Register", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.Save_Register).pack(fill=BOTH, pady=5)

    def CheckPassword(self):
        Password = self.Password.get().strip()
        regex = '^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,12})\S$'
        if re.search(regex, Password):
            return Password
        else:
            self.label_1 = Label(self.master, text="Password Invalid, Please Check Again"
                                                   "\n*6-12 Characters\n*1 Capital Letter\n*1 Special Character\nE.g Alexander19!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)


class ImACarer(LoginAccountWindow):
    def __init__(self, master):
        LoginAccountWindow.__init__(self, master)

    def Login(self):
        Username = self.Username.get().strip()
        Password = self.Password.get().strip()

        db = sqlite3.connect("Rota.db")
        cursor = db.cursor()
        sql = "SELECT * FROM Carer_Logins WHERE Username=? AND Password=?"
        cursor.execute(sql, (Username, Password))
        results = cursor.fetchall()
        # print(results)

        if results:
            self.label_1 = Label(self.master, text="You Have Successfully Logged In!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)
            root = Toplevel(self.master)
            CarerWindows(root)  # random class for testing purpose
        else:
            self.label_2 = Label(self.master, text="Username Or Password Doesn't Exist!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_2.pack()
            self.master.after(5000, self.label_2.destroy)

    def Save_Register(self):
        Username = self.Username.get()
        Password = self.CheckPassword()
        print("PASS", Password)  # 1 print
        if Password is None:
            pass
        elif Username == "":
            self.label_1 = Label(self.master, text="Username Invalid, It Cannot Be Blank!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)
        else:

            db = sqlite3.connect("Rota.db")
            cursor = db.cursor()
            sql = "SELECT * from Carer_Logins"  # select usernames
            cursor.execute(sql)
            rows = cursor.fetchall()
            data = []
            for row in rows:
                data.append(row[0])
            print(data)
            if Username in data:
                self.text.set("Username Or Password Already Exists!")
                Label(self.master, textvariable=self.text, font=("Times New Roman", "12", "bold"),
                      pady=10, ).pack()  # if it does exist then error
            else:
                self.text.set("You Have Been Successfuly Registered!")
                sql = "INSERT INTO Carer_Logins (Username, Password) values (?,?)"  # else insert into carer_login table
                data = (Username, Password)
                cursor.execute(sql, data)
                db.commit()
                Label(self.master, textvariable=self.text, font=("Times New Roman", "12", "bold"), pady=10, ).pack()
                root = Toplevel(self.master)
                CarerWindows(root)

class CarerWindows:
    def __init__(self, master):
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screen_width, screen_height))  # size of window then offset
        self.master.title('Carer Window')

        Label(self.master, text='What Would You Like To Do?', font=("Times New Roman", "24", "bold")).pack()

        Button(self.master, text="Add Carer", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.AddCarer).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Delete Carer", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.DeleteEditCarer).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Visits", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.Visits).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Client Plans", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.Client_Plans).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Quit", width=20, pady=5, padx=5, relief='sunken', bd=8, command=self.Quit).pack(fill=BOTH, pady = 2)

    def AddCarer (self):
        root = Toplevel(self.master)
        # CarerZ(root)
        # AddCarerWindow(root)

    def DeleteEditCarer(self):
        root = Toplevel(self.master)
        # DeleteEditCarerWindow(root)

    def Visits(self):
        root = Toplevel(self.master)
        # VisitsWindow(root)

    def Client_Plans(self):
        root = Toplevel(self.master)
        # ClientPlansWindow(root)

    def Quit(self):
        self.master.destroy()
        exit()

class ImAClient (LoginAccountWindow):
    def __init__(self, master):
        LoginAccountWindow.__init__(self, master)

    def Login(self):
        Username = self.Username.get().strip()
        Password = self.Password.get().strip()

        db = sqlite3.connect("Rota.db")
        cursor = db.cursor()
        sql = "SELECT * FROM Client_Logins WHERE Username=? AND Password=?"
        cursor.execute(sql, (Username, Password))
        results = cursor.fetchall()
        # print(results)

        if results:
            self.label_1 = Label(self.master, text="You Have Successfully Logged In!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)
            root = Toplevel(self.master)
            ClientWindows(root)
        else:
            self.label_2 = Label(self.master, text="Username Or Password Doesn't Exist!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_2.pack()
            self.master.after(5000, self.label_2.destroy)
    def Save_Register(self):
        Username = self.Username.get()
        Password = self.CheckPassword()
        print("PASS", Password)  # 1 print
        if Password is None:
            pass
        elif Username == "":
            self.label_1 = Label(self.master, text="Username Invalid, It Cannot Be Blank!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)
        else:

            db = sqlite3.connect("Rota.db")
            cursor = db.cursor()
            sql = "SELECT * from Client_Logins"  # select usernames
            cursor.execute(sql)
            rows = cursor.fetchall()
            data = []
            for row in rows:
                data.append(row[0])
            print(data)
            if Username in data:
                self.text.set("Username Or Password Already Exists!")
                Label(self.master, textvariable=self.text, font=("Times New Roman", "12", "bold"),
                      pady=10, ).pack()  # if it does exist then error
            else:
                self.text.set("You Have Been Successfuly Registered!")
                sql = "INSERT INTO Client_Logins (Username, Password) values (?,?)"  # else insert into carer_login table
                data = (Username, Password)
                cursor.execute(sql, data)
                db.commit()
                Label(self.master, textvariable=self.text, font=("Times New Roman", "12", "bold"), pady=10, ).pack()
                root = Toplevel(self.master)
                ClientWindows(root)

class ClientWindows:
    def __init__(self, master):
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screen_width, screen_height)) # size of window then offset
        self.master.title('Client Window')

        Label(self.master, text='What Would You Like To Do?', font=("Times New Roman", "24", "bold")).pack()

        Button(self.master, text="Add Client", width=20, pady=5, padx=5,relief='sunken',bd=8,command=self.AddClient).pack(fill=BOTH, pady = 2)
        Button(self.master, text="Delete / Edit Clients", width=20, pady=5, padx=5,relief='sunken',bd=8,command=self.DeleteEditClient).pack(fill=BOTH, pady = 2)
        Button(self.master, text="Add Client Plan", width=20, pady=5, padx=5,relief='sunken',bd=8,command=self.AddClientPlan).pack(fill=BOTH, pady = 2)
        Button(self.master, text="Quit", width=20, pady=5, padx=5,relief='sunken',bd=8,command=self.Quit).pack(fill=BOTH, pady = 2)

    def AddClient(self):
        root = Toplevel(self.master)
        # Client(root)
        # AddClientWindow(root)
    def DeleteEditClient(self):
        root = Toplevel(self.master)
        # DeleteEditClientWindow(root)

    def AddClientPlan(self):
        root = Toplevel(self.master)
        # AddClientPlanWindow(root)

    def Quit(self):
        self.master.destroy()
        exit()

class ImAnAdmin(LoginAccountWindow):
    def __init__(self, master):
        LoginAccountWindow.__init__(self, master)

    def Login(self):
        Username = self.Username.get().strip()
        Password = self.Password.get().strip()

        db = sqlite3.connect("Rota.db")
        cursor = db.cursor()
        sql = "SELECT * FROM Admin_Logins WHERE Username=? AND Password=?"
        cursor.execute(sql, (Username, Password))
        results = cursor.fetchall()
        # print(results)

        if results:
            self.label_1 = Label(self.master, text="You Have Successfully Logged In!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)
            root = Toplevel(self.master)
            AdminWindows(root)
        else:
            self.label_2 = Label(self.master, text="Username Or Password Doesn't Exist!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_2.pack()
            self.master.after(5000, self.label_2.destroy)

    def Save_Register(self):
        Username = self.Username.get()
        Password = self.CheckPassword()
        print("PASS", Password)  # 1 print
        if Password is None:
            pass
        elif Username == "":
            self.label_1 = Label(self.master, text="Username Invalid, It Cannot Be Blank!",
                                 font=("Times New Roman", "12", "bold"), pady=10, )
            self.label_1.pack()
            self.master.after(5000, self.label_1.destroy)
        else:

            db = sqlite3.connect("Rota.db")
            cursor = db.cursor()
            sql = "SELECT * from Admin_Logins"  # select usernames
            cursor.execute(sql)
            rows = cursor.fetchall()
            data = []
            for row in rows:
                data.append(row[0])
            print(data)
            if Username in data:
                self.text.set("Username Or Password Already Exists!")
                Label(self.master, textvariable=self.text, font=("Times New Roman", "12", "bold"),
                      pady=10, ).pack()  # if it does exist then error
            else:
                self.text.set("You Have Been Successfuly Registered!")
                sql = "INSERT INTO Admin_Logins (Username, Password) values (?,?)"  # else insert into carer_login table
                data = (Username, Password)
                cursor.execute(sql, data)
                db.commit()
                Label(self.master, textvariable=self.text, font=("Times New Roman", "12", "bold"), pady=10, ).pack()
                root = Toplevel(self.master)
                AdminWindows(root)

class AdminWindows:
    def __init__(self, master):
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screen_width, screen_height))  # size of window then offset
        self.master.title('Admin Window')

        Label(self.master, text='What Would You Like To Do?', font=("Times New Roman", "24", "bold")).pack()
        Button(self.master, text="Add Visit", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.AddVisit).pack(fill=BOTH, pady = 2)
        Button(self.master, text="Cancel Visit", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.CancelVisit).pack(fill=BOTH, pady = 2)
        Button(self.master, text="View Carers", width=20, pady=5, padx=5, relief='sunken', bd=8,command=self.ViewCarers).pack(fill=BOTH, pady = 2)

        Button(self.master, text="Quit", width=20, pady=5, padx=5, relief='sunken', bd=8, command=self.Quit).pack(fill=BOTH, pady = 2)

    def AddVisit(self):
        root = Toplevel(self.master)
        # AddVisitWindow(root)

    def ViewCarers (self):
        root = Toplevel(self.master)
        # ViewCarersWindow(root)

    def CancelVisit(self):
        root = Toplevel(self.master)
        # CancelVisitWindow(root)

    def Quit(self):
        self.master.destroy()
        exit()


if __name__ == '__main__':
    root = Tk()
    myGUIWelcome = Welcome(root)
    root.mainloop()