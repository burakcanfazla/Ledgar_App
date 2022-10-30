import sqlite3

class Payment():
    def __init__(self, product, price, date, type, explanation, user):
        self.product = product
        self.price = price
        self.date = date
        self.type = type
        self.explanation = explanation
        self.user = user
    def __str__(self):
        return "Product: {}\nPrice: {}\nDate: {}\nType: {}\nExplanation: {}\nUser: {}\n".format(self.product, self.price, self.date, self.type, self.explanation, self.user)

class UserInformation():
    def __init__(self, id, password):
        self.id = id
        self.password = password

class Ledgar():

    def __init__(self):
        self.CreateConnection()

    def CreateConnection(self):
        self.connection = sqlite3.connect("accountbook.db")
        self.cursor = self.connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS payments (Product TEXT, Price INT, Date TEXT, Type TEXT, Explanation TEXT, User TEXT)"
        self.cursor.execute(query)
        query1 = "CREATE TABLE IF NOT EXISTS userinfos (Id TEXT, Password TEXT)"
        self.cursor.execute(query1)
        self.connection.commit()

    def Disconnect(self):
        self.connection.close()

    def SignIn(self, userinfo):
        query = "SELECT * FROM userinfos WHERE Id = ?"
        self.cursor.execute(query, (userinfo.id,))
        existID = self.cursor.fetchall()
        if len(existID) != 0:
            return str("ID already exist")
        else:
            if len(userinfo.id) < 4:
                return str("ID too weak.")
            elif len(userinfo.password) < 6:
                return str("Password too weak.")
            else:
                query = "INSERT INTO userinfos VALUES(?,?)"
                self.cursor.execute(query, (userinfo.id, userinfo.password))
                self.connection.commit()
                return str("Account succesfully created.")

    def Login(self, userinfo):
        self.cursor.execute("SELECT * FROM userinfos WHERE Id = ? and Password = ?", (userinfo.id, userinfo.password))
        user = self.cursor.fetchall()
        if len(user) != 0:
            return str("Welcome " + str(user[0][0]))
        else:
            return str("Wrong ID or Password !")

    def ShowPayment(self, user):
        query = "SELECT * FROM payments WHERE User = ?"
        self.cursor.execute(query, (user,))
        payments = self.cursor.fetchall()
        if len(payments) == 0:
            return "Payment doesn't exist for" + user
        else:
            return payments
    def AddNewPayment(self, product, type, price, date, user):
        query = "INSERT INTO payments VALUES(?,?,?,?,?,?)"
        self.cursor.execute(query, (product, price, date, type, "", user))
        self.connection.commit()

    def DailySpend(self, date, user):
        query = "SELECT * FROM payments WHERE Date = ? and User = ?"
        self.cursor.execute(query, (date, user,))
        payments = self.cursor.fetchall()
        if len(payments) == 0:
            return "0"
        else:
            dailySpending = 0
            for i in payments:
                dailySpending = dailySpending + i[1]
            return str(dailySpending)
    def MonthlySpend(self):
        pass