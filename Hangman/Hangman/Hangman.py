import sys
import random
import codecs
import pygame
from pygame import mixer
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from sqlite import SQLite

username = "Player0000"
difficulty = 1
category = 1
isGameOver = 0


class SignIn(QDialog):
    def __init__(self):
        super(SignIn, self).__init__()
        loadUi("Qt_Design/login.ui", self)
        self.loginButton.clicked.connect(self.SignInFunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signUpButton.clicked.connect(self.GoToSignUp)
        self.error_invalid.setVisible(False)

    def SignInFunction(self):
        global username
        username = self.username.text()
        password = self.password.text()

        if sql.ValueExist("Login", username, password):
            self.error_invalid.setVisible(False)
            client = Client()
            widget.addWidget(client)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            print("Invalid Username or Password!")
            self.error_invalid.setVisible(True)

    def GoToSignUp(self):
        signUp = SignUp()
        widget.addWidget(signUp)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SignUp(QDialog):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi("Qt_Design/signup.ui", self)
        self.createAccountButton.clicked.connect(self.SignUpFunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signInButton.clicked.connect(self.GoToSignIn)
        self.error_usernametaken.setVisible(False)
        self.error_password.setVisible(False)

    def SignUpFunction(self):
        username = self.username.text()

        if self.password.text() == self.confirmPassword.text():
            self.error_password.setVisible(False)
            password = self.password.text()
            if sql.UsernameNotTaken("Login", username):
                self.error_usernametaken.setVisible(False)

                sql.Insert("Login", username, password)
                sql.InsertPlayer(username, 0, username)

                signIn = SignIn()
                widget.addWidget(signIn)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.error_usernametaken.setVisible(True)
        else:
            self.error_password.setVisible(True)

    def GoToSignIn(self):
        signIn = SignIn()
        widget.addWidget(signIn)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Client(QDialog):
    def __init__(self):
        super(Client, self).__init__()
        loadUi("Qt_Design/client.ui", self)
        mixer.music.load('Sound/sound.wav')
        mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.newWordButton.clicked.connect(self.GoToGameSettings)
        self.viewPlayersButton.clicked.connect(self.GoToViewPlayers)
        self.settingsButton.clicked.connect(self.GoToSettings)
        self.signOutButton.clicked.connect(self.GoToSignIn)
        self.exitButton.clicked.connect(self.ExitGameFunction)

        widget.setFixedWidth(1100)
        widget.setFixedHeight(600)

    def GoToGameSettings(self):
        gamesettings = GameSettings()
        widget.addWidget(gamesettings)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToViewPlayers(self):
        rank = Rank()
        widget.addWidget(rank)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToSettings(self):
        settings = Settings()
        widget.addWidget(settings)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToSignIn(self):
        signIn = SignIn()
        widget.addWidget(signIn)
        widget.setCurrentIndex(widget.currentIndex() + 1)

        widget.setFixedWidth(500)
        widget.setFixedHeight(600)

    def ExitGameFunction(self):
        sys.exit()


class Rank(QDialog):
    def __init__(self):
        super(Rank, self).__init__()
        loadUi("Qt_Design/rank.ui", self)

        self.tableWidget.setColumnWidth(0, 300)
        self.tableWidget.setColumnWidth(1, 100)
        self.LoadData()
        self.backButton.clicked.connect(self.GoToMainMenu)
        # sql.UpdateScore('b', 50)

    def LoadData(self):
        self.tableWidget.setRowCount(50)
        tableRow = 0
        for row in sql.Select("SELECT * FROM Player ORDER BY Score DESC"):
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(str(row[1])))

            tableRow += 1

    def GoToMainMenu(self):
        client = Client()
        widget.addWidget(client)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Settings(QDialog):
    def __init__(self):
        global username
        super(Settings, self).__init__()
        loadUi("Qt_Design/settings.ui", self)

        self.label_nickname.setText(sql.SelectPlayer(username))

        self.changeNameButton.clicked.connect(self.ChangeNickname)
        self.okButton.clicked.connect(self.GoToMainMenu)

        self.changeNameButton.setVisible(True)
        self.label_newNickname.setVisible(False)
        self.newNickname_txt.setVisible(False)
        self.error_usernametaken.setVisible(False)
        self.submitButton.setVisible(False)

    def ChangeNickname(self):
        self.changeNameButton.setVisible(False)
        self.label_newNickname.setVisible(True)
        self.newNickname_txt.setVisible(True)
        self.error_usernametaken.setVisible(False)
        self.submitButton.setVisible(True)
        self.submitButton.clicked.connect(self.Submit)

    def Submit(self):
        global username
        nickname = sql.SelectPlayer(username)
        new_nickname = self.newNickname_txt.text()
        if sql.NicknameNotTaken(new_nickname, nickname):
            sql.UpdateNickname(nickname, new_nickname)
            self.label_nickname.setText(new_nickname)
            self.changeNameButton.setVisible(True)
            self.label_newNickname.setVisible(False)
            self.newNickname_txt.setVisible(False)
            self.submitButton.setVisible(False)
            self.error_usernametaken.setVisible(False)
        else:
            self.error_usernametaken.setVisible(True)

    def GoToMainMenu(self):
        client = Client()
        widget.addWidget(client)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class GameSettings(QDialog):
    def __init__(self):
        super(GameSettings, self).__init__()
        loadUi("Qt_Design/gamesettings.ui", self)
        self.difficulty = 2  # medium difficulty
        self.category = 1  # 1st option
        self.start_Button.clicked.connect(self.GoToStartGame)
        self.back_Button.clicked.connect(self.GoToMainMenu)
        self.medium_radioButton.setChecked(True)

    def GameSettings(self):
        global difficulty, category
        if self.easy_radioButton.isChecked():
            self.difficulty = 1
        elif self.medium_radioButton.isChecked():
            self.difficulty = 2
        elif self.hard_radioButton.isChecked():
            self.difficulty = 3
        else:
            print("ERROR: not a Valid radioButton Input...")

        if self.comboBox.currentText() == "ΓΕΩΓΡΑΦΙΑ":
            self.category = 1
        elif self.comboBox.currentText() == "ΤΕΧΝΟΛΟΓΙΑ":
            self.category = 2
        elif self.comboBox.currentText() == "ΑΘΛΗΤΙΣΜΟΣ":
            self.category = 3
        elif self.comboBox.currentText() == "ΜΟΥΣΙΚΗ":
            self.category = 4
        elif self.comboBox.currentText() == "ΖΩΑ":
            self.category = 5
        else:
            print("ERROR: not a Valid CheckBox Input...")

        difficulty = self.difficulty
        category = self.category

    def GoToStartGame(self):
        global isGameOver
        isGameOver = 0
        self.GameSettings()
        game = MainGame()
        widget.addWidget(game)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToMainMenu(self):
        client = Client()
        widget.addWidget(client)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainGame(QDialog):
    def __init__(self):
        global difficulty

        super(MainGame, self).__init__()
        loadUi("Qt_Design/game.ui", self)
        self.lives = 6
        self.victory = 0
        self.img = 1
        self.correctWords = 0

        self.selected_word = ""
        self.temp = ""

        lives = self.lives / difficulty
        self.lives = int(lives)

        self.setPhoto(str(self.img))
        self.label_GameOver.setVisible(False)
        self.label_Won.setVisible(False)
        self.label_Lost.setVisible(False)
        self.playAgain_Button.setVisible(False)
        self.mainMenu_Button.setVisible(False)
        self.exitGame_Button.setVisible(False)
        self.label_.setVisible(True)
        self.label_OnWin.setVisible(False)
        self.label_OnLose.setVisible(False)
        self.label_lives.setText(str(self.lives))

        self.playAgain_Button.clicked.connect(self.GoToGameSettings)
        self.mainMenu_Button.clicked.connect(self.GoToMainMenu)
        self.exitGame_Button.clicked.connect(self.ExitGame)
        self.A_Button.clicked.connect(self.A_Clicked)
        self.B_Button.clicked.connect(self.B_Clicked)
        self.G_Button.clicked.connect(self.G_Clicked)
        self.D_Button.clicked.connect(self.D_Clicked)
        self.E_Button.clicked.connect(self.E_Clicked)
        self.Z_Button.clicked.connect(self.Z_Clicked)
        self.H_Button.clicked.connect(self.H_Clicked)
        self.U_Button.clicked.connect(self.U_Clicked)
        self.I_Button.clicked.connect(self.I_Clicked)
        self.K_Button.clicked.connect(self.K_Clicked)
        self.L_Button.clicked.connect(self.L_Clicked)
        self.M_Button.clicked.connect(self.M_Clicked)
        self.N_Button.clicked.connect(self.N_Clicked)
        self.J_Button.clicked.connect(self.J_Clicked)
        self.O_Button.clicked.connect(self.O_Clicked)
        self.P_Button.clicked.connect(self.P_Clicked)
        self.R_Button.clicked.connect(self.R_Clicked)
        self.S_Button.clicked.connect(self.S_Clicked)
        self.T_Button.clicked.connect(self.T_Clicked)
        self.Y_Button.clicked.connect(self.Y_Clicked)
        self.F_Button.clicked.connect(self.F_Clicked)
        self.X_Button.clicked.connect(self.X_Clicked)
        self.Q_Button.clicked.connect(self.Q_Clicked)
        self.W_Button.clicked.connect(self.W_Clicked)
        self.ChooseWord()

    def ChooseWord(self):
        global category

        if category == 1:
            txt = 'TextFiles/geography.txt'
        elif category == 2:
            txt = 'TextFiles/technology.txt'
        elif category == 3:
            txt = 'TextFiles/sport.txt'
        elif category == 4:
            txt = 'TextFiles/music.txt'
        elif category == 5:
            txt = 'TextFiles/animals.txt'

        index = random.randint(0, 9)
        file = codecs.open(txt, 'r', 'utf-8')
        line = file.readlines()
        self.selected_word = line[index].strip('/n')

        self.label_OnWin.setText(self.selected_word)
        self.label_OnLose.setText(self.selected_word)

        self.victory = len(self.selected_word) - 2
        temp = ""
        for i in range(0, len(self.selected_word) - 2):
            if self.selected_word[i] != " ":
                temp += "_ "
            else:
                temp += "  "
                self.victory -= 1

        self.temp = temp
        self.label_.setText(temp)

        file.close()

    def isCorrect(self, x):
        global username, difficulty, isGameOver
        tempScore = 0
        temp = self.victory
        for i in range(0, len(self.selected_word) - 2):
            if self.selected_word[i] == x:
                self.temp = list(self.temp)
                self.temp[2 * i] = x
                self.temp = "".join(self.temp)
                self.victory -= 1
                self.correctWords += 1

        if difficulty == 1:
            tempScore += (1 * self.correctWords) * difficulty
        elif difficulty == 2:
            tempScore += (5 * self.correctWords) * difficulty
        elif difficulty == 3:
            tempScore += (10 * self.correctWords) * difficulty

        if self.victory == temp:
            self.UpdateLives()
        elif self.victory == 0:
            isGameOver = 1
            self.label_OnWin.setVisible(True)
            self.label_.setVisible(False)
            if difficulty == 1:
                tempScore = (1 * self.correctWords * (self.lives + 1) * difficulty)
                score = (sql.GetPlayerScore(username) + (1 * self.correctWords * ((self.lives + 1) * difficulty)))
                sql.UpdateScore(username, score)
            elif difficulty == 2:
                tempScore = (5 * self.correctWords * (self.lives + 1) * difficulty)
                score = (sql.GetPlayerScore(username) + (5 * self.correctWords * ((self.lives + 1) * difficulty)))
                sql.UpdateScore(username, score)
            elif difficulty == 3:
                tempScore = (10 * self.correctWords * (self.lives + 1) * difficulty)
                score = (sql.GetPlayerScore(username) + (10 * self.correctWords * ((self.lives + 1) * difficulty)))
                sql.UpdateScore(username, score)

            self.label_Won.setVisible(True)
            self.label_GameOver.setVisible(True)
            self.playAgain_Button.setVisible(True)
            self.mainMenu_Button.setVisible(True)
            self.exitGame_Button.setVisible(True)

        self.label_.setText(self.temp)
        self.label_Score.setText(str(tempScore))

    def ExitGame(self):
        sys.exit()

    def GoToMainMenu(self):
        client = Client()
        widget.addWidget(client)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToGameSettings(self):
        gamesettings = GameSettings()
        widget.addWidget(gamesettings)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def UpdateLives(self):
        global difficulty, username, isGameOver

        if self.lives >= 1:

            self.lives -= 1
            self.img += difficulty

            self.setPhoto(str(self.img))
            self.label_lives.setText(str(self.lives))
        else:
            self.setPhoto('GameOver')
            isGameOver = 1
            self.label_OnLose.setVisible(True)
            self.label_.setVisible(False)
            if difficulty == 1:
                sql.UpdateScore(username, (sql.GetPlayerScore(username) - 500))
            elif difficulty == 2:
                sql.UpdateScore(username, (sql.GetPlayerScore(username) - 250))
            elif difficulty == 3:
                sql.UpdateScore(username, (sql.GetPlayerScore(username) - 100))
            self.label_Lost.setVisible(True)
            self.label_GameOver.setVisible(True)
            self.playAgain_Button.setVisible(True)
            self.mainMenu_Button.setVisible(True)
            self.exitGame_Button.setVisible(True)

    def A_Clicked(self):
        global isGameOver
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.A_Button.setVisible(False)
            self.isCorrect("Α")

    def B_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.B_Button.setVisible(False)
            self.isCorrect("Β")

    def G_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.G_Button.setVisible(False)
            self.isCorrect("Γ")

    def D_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.D_Button.setVisible(False)
            self.isCorrect("Δ")

    def E_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.E_Button.setVisible(False)
            self.isCorrect("Ε")

    def Z_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.Z_Button.setVisible(False)
            self.isCorrect("Ζ")

    def H_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.H_Button.setVisible(False)
            self.isCorrect("Η")

    def U_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.U_Button.setVisible(False)
            self.isCorrect("Θ")

    def I_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.I_Button.setVisible(False)
            self.isCorrect("Ι")

    def K_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.K_Button.setVisible(False)
            self.isCorrect("Κ")

    def L_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.L_Button.setVisible(False)
            self.isCorrect("Λ")

    def M_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.M_Button.setVisible(False)
            self.isCorrect("Μ")

    def N_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.N_Button.setVisible(False)
            self.isCorrect("Ν")

    def J_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.J_Button.setVisible(False)
            self.isCorrect("Ξ")

    def O_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.O_Button.setVisible(False)
            self.isCorrect("Ο")

    def P_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.P_Button.setVisible(False)
            self.isCorrect("Π")

    def R_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.R_Button.setVisible(False)
            self.isCorrect("Ρ")

    def S_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.S_Button.setVisible(False)
            self.isCorrect("Σ")

    def T_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.T_Button.setVisible(False)
            self.isCorrect("Τ")

    def Y_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.Y_Button.setVisible(False)
            self.isCorrect("Υ")

    def F_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.F_Button.setVisible(False)
            self.isCorrect("Φ")

    def X_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.X_Button.setVisible(False)
            self.isCorrect("Χ")

    def Q_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.Q_Button.setVisible(False)
            self.isCorrect("Ψ")

    def W_Clicked(self):
        if isGameOver == 1:
            self.A_Button.setEnabled(False)
        else:
            self.W_Button.setVisible(False)
            self.isCorrect("Ω")

    def setPhoto(self, x):
        self.photo.setPixmap(QtGui.QPixmap("Images/Kremala_{}.png".format(x)))


sql = SQLite()

try:
    # CREATE TABLE Login
    ctl = """CREATE TABLE "Login" (
                "Username"	TEXT NOT NULL UNIQUE,
                "Password"	TEXT NOT NULL,
                PRIMARY KEY("Username")
            ); """

    sql.CreateTable(ctl)
except:
    print("Table Login Already exists!")
try:
    # CREATE TABLE Player
    ctp = """CREATE TABLE "Player" (
	            "Username"	TEXT NOT NULL UNIQUE,
	            "Score"	INTEGER,
	            "Nickname"	TEXT NOT NULL UNIQUE,
	            PRIMARY KEY("Username")
	        );"""

    sql.CreateTable(ctp)
except:
    print("Table Player Already exists!")
try:
    # CREATE TABLE Word
    ctw = """CREATE TABLE "Word" (
	            "Word"	TEXT NOT NULL UNIQUE,
	            "Category"	TEXT NOT NULL,
	            PRIMARY KEY("Word")
            );"""

    sql.CreateTable(ctw)
except:
    print("Table Word Already exists!")

pygame.mixer.init()
app = QApplication(sys.argv)
mainwindow = SignIn()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(600)
widget.show()
app.exec_()