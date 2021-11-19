import sqlite3


class SQLite:
    def __init__(self):
        self.con = sqlite3.connect('Database/My_DataBase.db')
        self.c = self.con.cursor()

    def Close(self):
        self.con.close()

    def CreateTable(self, query):
        self.c.execute(query)
        self.con.commit()

    def Insert(self, tableName, val1, val2):
        self.c.execute("INSERT INTO {} VALUES (:val1, :val2)".format(tableName), {'val1': val1, 'val2': val2})
        self.con.commit()

    def InsertPlayer(self, username, score, nickname):
        self.c.execute("INSERT INTO Player VALUES (:username, :score, :nickname)", {'username': username, 'score': score, 'nickname': nickname})
        self.con.commit()

    def Select(self, query):
        self.c.execute(query)
        return self.c.fetchall()

    def SelectPlayer(self, username):
        self.c.execute("SELECT * FROM Player Where Username = '{}'".format(username))

        for row in self.c.fetchall():
            if row[0] == username:
                return row[2]

    def ValueExist(self, tableName, val1, val2):
        temp = False
        self.c.execute("SELECT * FROM {} WHERE Username='{}' AND Password='{}';".format(tableName, val1, val2))

        for row in self.c.fetchall():
            if row[0] == val1 and row[1] == val2:
                temp = True
            else:
                temp = False

        return temp

    def UsernameNotTaken(self, tableName, val1):
        temp = True
        self.c.execute("SELECT * FROM {} WHERE Username='{}';".format(tableName, val1))

        for row in self.c.fetchall():
            if row[0] == val1:
                temp = False
            else:
                temp = True

        return temp

    def NicknameNotTaken(self, new_nickname, nickname):
        temp = True
        if new_nickname != nickname:
            self.c.execute("SELECT * FROM Player WHERE Nickname='{}';".format(new_nickname))

            for row in self.c.fetchall():
                if row[3] == new_nickname:
                    temp = False
                else:
                    temp = True

            return temp

    def GetPlayerScore(self, name):
        self.c.execute("SELECT * FROM Player WHERE Username = '{}'".format(name))

        for row in self.c.fetchall():
            if row[0] == name:
                return row[1]
            else:
                print("ERROR: I could not find this Name in the Database!")

    def UpdateScore(self, name, score):
        self.c.execute("UPDATE Player SET Score = '{}' WHERE Username ='{}'".format(score, name))
        self.con.commit()

    def UpdateNickname(self, old_name, new_name):
        self.c.execute("UPDATE Player SET Nickname = '{}' WHERE Nickname ='{}'".format(new_name, old_name))
        self.con.commit()

    def DeleteWithName(self, tableName, name):
        self.c.execute("DELETE FROM {} WHERE Username ='{}'".format(tableName, name))
        self.con.commit()

    def DeletePlayerByScore(self, score):
        self.c.execute("DELETE FROM Player WHERE Score ='{}'".format(score))
        self.con.commit()