import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ck
import dataset
import queries
import algorithms
import time
from stopwatch import Stopwatch
import math
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

class App:
    def __init__(self, parent): #configuring preset settings
        self.parent = parent
        self.mistakes = 0
        self.map = "Race Track"
        self.configurePreset()
        self.setMainScreen()

        queries.launchDBconnection() #loads database

    def configurePreset(self):
        settings = queries.getSettings()
        if (settings == None): #loads settings if they exist
            self.difficulty = "Easy"
            self.width = 1066
            self.height = 600
            self.parent.geometry(str(self.width)+"x"+str(self.height))
            self.coins = 0
            queries.unlockCar("car", "selected")
            self.car = "car"
            queries.createUserProfile()
            queries.setSettings(str(self.width)+"x"+str(self.height), self.difficulty)
            queries.updateCoins(self.coins)
        else: #creates settings if they dont exist
            self.difficulty = queries.getSettings()[1]
            self.height = int(queries.getSettings()[2].split("x")[1])
            self.width = int(queries.getSettings()[2].split("x")[0])
            self.parent.geometry(queries.getSettings()[2])
            self.coins = queries.getCoins()[0][1]
            self.car = str(self.getSelectedCar())

    def getSelectedCar(self): #gets the users chosen car
        cars = queries.getInventory()
        for car in cars:
            if (car[2] == "selected"):
                return car[1]

    def setBackground(self, image, frame): #sets background of frame
        img = Image.open(image).resize((self.width,self.height))
        imgObj = ImageTk.PhotoImage(img)
        label1 = tk.Label(frame, image=imgObj)
        label1.image = imgObj
        label1.place(x=0, y=0)

    def clearApp(self): #clears child frames from root, improve performance
        for widget in self.parent.winfo_children():
            widget.destroy()

    def handlePlay(self): #plays selected map
        if (self.map == "Race Track"):
            self.playRaceTrack()
        elif (self.map == "Drag Race"):
            self.playDragRace()

    def createButton(self, frame, text, event): #button constructor
        return ck.CTkButton(master=frame, text=text, font=("ArcadeClassic", 24), height=40, width=200,
            fg_color="#32CD32", hover_color="#78cd32", command=event)

    def setMainScreen(self): #creates main menu frame
        #clear root and create new frame
        self.clearApp()
        frame = Frame(self.parent, bg="#32CD32")
        frame.pack(fill="both", expand=True )
        self.setBackground("assets/newbg.png", frame)

        #setup buttons
        playButton = self.createButton(frame, "Play", lambda: self.handlePlay())
        playButton.place(x=self.width*0.50, y=self.height*0.4, anchor=ck.CENTER)

        shopButton = self.createButton(frame, "Shop", lambda: self.Shop())
        shopButton.place(x=self.width*0.50, y=(self.height*0.4)+45, anchor=ck.CENTER)

        leaderboardsButton = self.createButton(frame, "Leaderboards", lambda: self.Leaderboards())
        leaderboardsButton.place(x=self.width*0.50, y=(self.height*0.4)+90, anchor=ck.CENTER)

        History = self.createButton(frame, "History", lambda: self.History())
        History.place(x=self.width*0.50, y=(self.height*0.4)+135, anchor=ck.CENTER)

        settingsButton = self.createButton(frame, "Settings", lambda: self.Settings())
        settingsButton.place(x=self.width*0.50, y=(self.height*0.4)+180, anchor=ck.CENTER)

        QuitButton = self.createButton(frame, "Quit", lambda: self.Quit())
        QuitButton.place(x=self.width*0.50, y=(self.height*0.4)+225, anchor=ck.CENTER)

        #setup map choice
        img = Image.open("assets/playbg2_preview.png").resize((200,200))
        imgObj = ImageTk.PhotoImage(img)
        mapImage = Label(self.parent, image=imgObj, bg='Black', highlightthickness=2, highlightbackground="#32CD32")
        mapImage.image = imgObj
        mapImage.place(x=self.width*0.90, y=self.height*0.825, anchor=ck.CENTER)

        mapChoiceLabel = Label(master=self.parent, text="Change Map", bg="#32CD32", fg="White", font=("ArcadeClassic", 28))
        mapChoiceLabel.place(x=self.width*0.90, y=(self.height*0.825)-120, anchor=ck.CENTER)

        mapChoiceLabel.bind('<Enter>', self.enterHover)
        mapChoiceLabel.bind('<Leave>', self.exitHover)
        mapChoiceLabel.bind('<Button-1>', lambda event: self.mapClick(event, mapImage))

    def enterHover(self, event):
        event.widget.configure(cursor='hand')

    def exitHover(self, event):
        event.widget.configure(cursor='')

    def mapClick(self, event, label): #updates map when user toggles
        if (self.map == "Race Track"):
            self.map = "Drag Race"
            self.updateImage(label, "assets/drag_race_preview.png")
        else:
            self.map == "Drag Race"
            self.map = "Race Track"
            self.updateImage(label, "assets/playbg2_preview.png")

    def updateImage(self, label, image): #refreshes label image
        img = Image.open(image).resize((200, 200))
        imgObj = ImageTk.PhotoImage(img)
        label.config(image=imgObj)
        label.image = imgObj

    def createFrame(self, frame): #frame constructor
        return Frame(master=frame, width=self.width*0.8, height=30, bg="#32CD32")

    def createLabel(self, frame, text, size): #label constructor
        return Label(master=frame, text=text, bg="#32CD32", fg="White", font=("ArcadeClassic", size))

    def Shop(self): #creates shop screen
        self.clearApp()
        frame = Frame(self.parent, bg="#32CD32")
        frame.pack(fill="both", expand=True )
        self.setBackground("assets/newbg.png", frame)
        itemButtonArray = []

        playersCar = self.getSelectedCar()

        #handles frame design
        coinFrame = Frame(frame, bg="black", height=40, width=200, bd=4, highlightbackground="green", highlightthickness=2)
        coinFrame.place(x=self.width*0.9, y=self.height*0.05, anchor=ck.CENTER)

        img = Image.open("assets/coin.png").resize((32,32))
        imgObj = ImageTk.PhotoImage(img)
        coinImage = Label(coinFrame, image=imgObj, bg="black")
        coinImage.image = imgObj
        coinImage.place(relx=0.1, rely=0.5, anchor=ck.CENTER)

        coinLabel = Label(coinFrame, text=str(int(self.coins))+" coins", bg="black", fg="White", font=("ArcadeClassic", 24))
        coinLabel.place(relx=0.1, rely=0.5, x=20, anchor="w")

        backButton = self.createButton(frame, "Back", lambda: self.setMainScreen())
        backButton.place(x=self.width*0.1, y=self.height*0.05, anchor=ck.CENTER)

        fullCarArray = dataset.getCars()
        yourInv = queries.getInventory()
        newItemBuffer = 0

        nameList = [sub_array[1] for sub_array in yourInv]
        for car in fullCarArray: #displays race cars in the shop
            itemx=self.width*0.3 + newItemBuffer
            itemy=self.height*0.5
            buttonBuffer=100
            paddingGap = 4

            #creates car frame that holds car elements
            carFrame = Frame(frame, bg="Black", height=200, width=200, highlightbackground="#32CD32", highlightthickness=2)
            carFrame.place(x=itemx, y=itemy, anchor=ck.CENTER)

            #fits car image inside frame element that is packed at top
            carImg = Image.open(f"assets/{car[0]}.png").resize((200,150))
            carObj = ImageTk.PhotoImage(carImg)
            carImage = Label(carFrame, image=carObj, bg='Black')
            carImage.image = carObj
            carImage.pack(side="top")

            #fits price elements inside frame element that is packed at bottom
            priceFrame = Frame(carFrame, bg="Black", height=40, width=200)
            priceFrame.pack(side="bottom", fill="both")

            coinImage = Label(priceFrame, image=imgObj, bg="Black")
            coinImage.image = imgObj
            coinImage.place(relx=0.15, rely=0.5, anchor=ck.CENTER)
            if (nameList.count(car[0]) > 0): #if user owns car, display it as inventory item
                priceLabel = Label(priceFrame, text=f"{car[1]} coins", bg="Black", fg="White", font=("ArcadeClassic", 24))
                priceLabel.place(relx=0.15, x=25, rely=0.5, anchor="w")

                padunlock = Image.open("assets/padlock_unlock.png").resize((30,30))
                padunlockObj = ImageTk.PhotoImage(padunlock)
                padunlockImage = Label(carImage, image=padunlockObj, bg='Black')
                padunlockImage.image = padunlockObj
                padunlockImage.place(relx=0.9, rely=0.12, anchor=ck.CENTER)

                if (car[0] == playersCar): #if car is currently selected, display it chosen car
                    carFrame.configure(highlightbackground="Yellow")
                    chosenCar = ck.CTkButton(master=frame, text="Chosen", font=("ArcadeClassic", 24), height=40, width=204,
                        fg_color="Yellow", hover_color="Yellow")
                    chosenCar.place(x=itemx, y=itemy+buttonBuffer-paddingGap, anchor="n")
                else: #if car is not currently selected, display it as regular inventory car
                    unlockedButton = ck.CTkButton(master=frame, text="Select", font=("ArcadeClassic", 24), height=40, width=204,
                        fg_color="#32CD32", hover_color="#78cd32")
                    unlockedButton.configure(command=lambda newCar=car[0]: self.changeSelectedCar(playersCar, newCar))
                    unlockedButton.place(x=itemx, y=itemy+buttonBuffer-paddingGap, anchor="n")
            else: #if user doesnt owns car, display it as shop item
                priceLabel = Label(priceFrame, text=f"{car[1]} coins", bg="Black", fg="Red", font=("ArcadeClassic", 24))
                priceLabel.place(relx=0.15, x=25, rely=0.5, anchor="w")

                padlock = Image.open("assets/padlock_lock.png").resize((24,30))
                padlockObj = ImageTk.PhotoImage(padlock)
                padlockImage = Label(carImage, image=padlockObj, bg='Black')
                padlockImage.image = padlockObj
                padlockImage.place(relx=0.9, rely=0.12, anchor=ck.CENTER)

                buyButton = ck.CTkButton(master=frame, text="Buy", font=("ArcadeClassic", 24), height=40, width=208,
                fg_color="#32CD32", hover_color="#78cd32", corner_radius=0)
                buyButton.configure(command=lambda frame=carFrame, coinLabel=coinLabel, carObj=car, price=priceLabel, lock=padlockImage, button=buyButton: self.buyCar(carObj, price, lock, coinLabel, button, frame))
                buyButton.place(x=itemx, y=itemy+buttonBuffer-paddingGap, anchor="n")
            newItemBuffer += 220

    def changeSelectedCar(self, playersCar, newCar):
        queries.changeSelectedCarInDB(playersCar, newCar)
        self.Shop()

    def buyCar(self, car, price, lock, coinLabel, button, frame):
        if (self.coins >= car[1]): #logic to check if user can afford car
            button.configure(command=None, text="Unlocked", hover_color="#32CD32")
            price.configure(fg="White")
            lock.destroy()
            padunlock = Image.open("assets/padlock_unlock.png").resize((30, 30))
            padunlockObj = ImageTk.PhotoImage(padunlock)
            padunlockImage = Label(frame, image=padunlockObj, bg='Black')
            padunlockImage.image = padunlockObj
            padunlockImage.place(relx=0.9, rely=0.12, anchor=ck.CENTER)
            self.deductCoins(car, coinLabel)
            self.Shop()

        elif (self.coins < car[1]): #logic to handle if car cant afford car
            button.configure(fg_color="Red", hover_color="Red")
            frame.configure(highlightbackground="Red")
            root.after(300, lambda: self.highlightCarItem(button, frame, "#32CD32"))

    def highlightCarItem(self, button, frame, color):
        button.configure(fg_color=color, hover_color=color)
        frame.configure(highlightbackground=color)

    def deductCoins(self, car, coinLabel):
        self.coins -= car[1] #deduct car price from coin balance
        coinLabel.configure(text=str(self.coins)+" coins") #update coins on user in database
        queries.updateCoins(self.coins) #insert new car into users inventory
        queries.unlockCar(car[0], "selected")

    def Leaderboards(self):
        self.clearApp()
        frame = Frame(self.parent, bg="#32CD32")
        frame.pack(fill="both", expand=True )
        self.setBackground("assets/leaderboards.png", frame)

        #creates header labels for leaderboards
        headerFrame = Frame(master=frame, width=self.width*0.8, height=40, bg="#32CD32")
        headerFrame.place(x=self.width*0.5, y=(self.height*0.2)-10, anchor=ck.CENTER)

        rankLabel = self.createLabel(headerFrame, "Rank", 24)
        rankLabel.place(relx=0.07, rely=0.5, anchor="center")
        difficultyLabel = self.createLabel(headerFrame, "Difficulty", 24)
        difficultyLabel.place(relx=0.22, rely=0.5, anchor="center")
        timeLabel = self.createLabel(headerFrame, "Time", 24)
        timeLabel.place(relx=0.38, rely=0.5, anchor="center")
        wpmLabel = self.createLabel(headerFrame, "WPM", 24)
        wpmLabel.place(relx=0.5, rely=0.5, anchor="center")
        mistakesLabel = self.createLabel(headerFrame, "Mistakes", 24)
        mistakesLabel.place(relx=0.64, rely=0.5, anchor="center")
        mapLabel = self.createLabel(headerFrame, "Map", 24)
        mapLabel.place(relx=0.78, rely=0.5, anchor="center")
        dateLabel = self.createLabel(headerFrame, "Date", 24)
        dateLabel.place(relx=0.92, rely=0.5, anchor="center")

        rows = queries.getLeaderboardRows()
        if len(rows) == 0: #displays no results screen if they have 0 games played
            rowFrame = Frame(master=frame, width=self.width*0.7, height=30, bg="#32CD32")
            rowFrame.place(x=self.width*0.5, y=(self.height*0.2)+50, anchor=ck.CENTER)
            rankRowLabel = self.createLabel(rowFrame, "No Results", 22)
            rankRowLabel.place(relx=0.5, rely=0.5, anchor=ck.CENTER)
        else: #display leaderboard results
            count = 0
            for row in rows:
                count += 1
                difficulty = row[1]
                time = row[2]
                wpm = row[3]
                mistakes = row[4]
                map = row[5]
                date = row[6]

                rowFrame = self.createFrame(frame)
                rowFrame.place(x=self.width*0.5, y=(self.height*0.2)+(count*40), anchor=ck.CENTER)

                rankRowLabel = self.createLabel(rowFrame, str(count), 22)
                rankRowLabel.place(relx=0.07, rely=0.5, anchor=ck.CENTER)

                difficultyRowLabel = self.createLabel(rowFrame, str(difficulty), 22)
                difficultyRowLabel.place(relx=0.22, rely=0.5, anchor=ck.CENTER)

                timeRowLabel = self.createLabel(rowFrame, str(time)+" seconds", 20)
                timeRowLabel.place(relx=0.38, rely=0.5, anchor=ck.CENTER)

                wpmRowLabel = self.createLabel(rowFrame, str(wpm), 22)
                wpmRowLabel.place(relx=0.5, rely=0.5, anchor=ck.CENTER)

                mistakesRowLabel = self.createLabel(rowFrame, str(mistakes), 22)
                mistakesRowLabel.place(relx=0.64, rely=0.5, anchor=ck.CENTER)

                mapRowLabel = self.createLabel(rowFrame, str(map), 22)
                mapRowLabel.place(relx=0.78, rely=0.5, anchor=ck.CENTER)

                timeRowLabel = self.createLabel(rowFrame, str(date), 22)
                timeRowLabel.place(relx=0.92, rely=0.5, anchor=ck.CENTER)

        backButton = self.createButton(frame, "Back", lambda: self.setMainScreen())
        backButton.place(x=self.width*0.1, y=self.height*0.05, anchor=ck.CENTER)


    def History(self):
        self.clearApp()
        historyFrame = Frame(self.parent, bg="#32CD32")
        self.setBackground("assets/leaderboards.png", historyFrame)
        historyFrame.pack(fill='both', expand=1)

        performanceButton = self.createButton(historyFrame, "See Performance", lambda: self.setPerformanceScreen())
        performanceButton.place(x=self.width*0.9, y=self.height*0.05, anchor=ck.CENTER)
        backButton = self.createButton(historyFrame, "Back", lambda: self.setMainScreen())
        backButton.place(x=self.width*0.1, y=self.height*0.05, anchor=ck.CENTER)

        #creates header labels for leaderboards
        headerFrame = Frame(master=historyFrame, width=self.width*0.8, height=40, bg="#32CD32")
        headerFrame.place(x=self.width*0.5, y=(self.height*0.2)-10, anchor=ck.CENTER)
        difficultyLabel = self.createLabel(headerFrame, "Difficulty", 24)
        difficultyLabel.place(relx=0.15, rely=0.5, anchor="center")
        timeLabel = self.createLabel(headerFrame, "Time", 24)
        timeLabel.place(relx=0.325, rely=0.5, anchor="center")
        wpmLabel = self.createLabel(headerFrame, "WPM", 24)
        wpmLabel.place(relx=0.47, rely=0.5, anchor="center")
        mistakesLabel = self.createLabel(headerFrame, "Mistakes", 24)
        mistakesLabel.place(relx=0.61, rely=0.5, anchor="center")
        mapLabel = self.createLabel(headerFrame, "Map", 24)
        mapLabel.place(relx=0.77, rely=0.5, anchor="center")
        dateLabel = self.createLabel(headerFrame, "Date", 24)
        dateLabel.place(relx=0.92, rely=0.5, anchor="center")

        rows = queries.getHistoryRows()
        if len(rows) == 0:
            rowFrame = Frame(master=historyFrame, width=self.width*0.7, height=30, bg="#32CD32")
            rowFrame.place(x=self.width*0.5, y=(self.height*0.2)+50, anchor=ck.CENTER)
            noResults = self.createLabel(rowFrame, "No Results", 22)
            noResults.place(relx=0.5, rely=0.5, anchor=ck.CENTER)
        else:
            count = 0
            for row in rows:
                count += 1
                difficulty = row[1]
                time = row[2]
                wpm = row[3]
                mistakes = row[4]
                map = row[5]
                date = row[6]

                rowFrame = self.createFrame(historyFrame)
                rowFrame.place(x=self.width*0.5, y=(self.height*0.2)+(count*40), anchor=ck.CENTER)

                difficultyRowLabel = self.createLabel(rowFrame, str(difficulty), 22)
                difficultyRowLabel.place(relx=0.15, rely=0.5, anchor=ck.CENTER)

                timeRowLabel = self.createLabel(rowFrame, str(time)+" seconds", 20)
                timeRowLabel.place(relx=0.325, rely=0.5, anchor=ck.CENTER)

                wpmRowLabel = self.createLabel(rowFrame, str(wpm), 22)
                wpmRowLabel.place(relx=0.47, rely=0.5, anchor=ck.CENTER)

                mistakesRowLabel = self.createLabel(rowFrame, str(mistakes), 22)
                mistakesRowLabel.place(relx=0.61, rely=0.5, anchor=ck.CENTER)

                mapRowLabel = self.createLabel(rowFrame, str(map), 22)
                mapRowLabel.place(relx=0.77, rely=0.5, anchor=ck.CENTER)

                timeRowLabel = self.createLabel(rowFrame, str(date), 22)
                timeRowLabel.place(relx=0.92, rely=0.5, anchor=ck.CENTER)

    def setPerformanceScreen(self): #sets performance screen
        self.clearApp()
        historyFrame = Frame(self.parent, bg="#32CD32")
        self.setBackground("assets/leaderboards.png", historyFrame)
        historyFrame.pack(fill='both', expand=1)
        backButton = self.createButton(historyFrame, "Back", lambda: self.History())
        backButton.place(x=self.width*0.1, y=self.height*0.05, anchor=ck.CENTER)
        plt.style.use('dark_background')

        rows = queries.getPerformance()
        if (len(rows) == 0):
            noresults = self.createLabel(historyFrame, "No Results", 22)
            noresults.place(relx=0.5, rely=0.5, anchor=ck.CENTER)
        else:
            data = []
            for row in rows:
                obj = {"id": row[0], "wpm": row[3]}
                data.append(obj)
            fig = self.createPerformanceGraph(data)
            canvas = FigureCanvasTkAgg(fig, master=historyFrame)
            canvas.draw()
            canvas.get_tk_widget().place(x=self.width*0.5, y=self.height*0.5, anchor=ck.CENTER)


    def createPerformanceGraph(self, data): #creates performance analytics graph
        fig, ax = plt.subplots()

        x = [entry["id"] for entry in data]
        y = [entry["wpm"] for entry in data]

        ax.plot(x, y, marker='o')
        ax.set_title("WPM Performance Over Past Games")
        ax.set_xlabel('Game')
        ax.set_ylabel('WPM')

        return fig

    def Settings(self): #creates settings screen
        self.clearApp()
        settingsFrame = Frame(self.parent, bg="#32CD32")
        self.setBackground("assets/newbg.png", settingsFrame)
        settingsFrame.pack(fill='both', expand=1)

        backButton = self.createButton(settingsFrame, "Back", lambda: self.setMainScreen())
        backButton.place(x=self.width*0.1, y=self.height*0.05, anchor=ck.CENTER)

        currentDimension = ck.StringVar(value=str(self.width)+"x"+str(self.height))
        displayOptions = self.createOptionMenu(settingsFrame, ["1066x600", "1280x720"], currentDimension)
        displayOptions.place(x=self.width*0.5, y=self.height*0.5, anchor=ck.CENTER)

        currentDifficulty = ck.StringVar(value=self.difficulty)
        difficultyOptions = self.createOptionMenu(settingsFrame, ["Easy", "Mild", "Difficult", "Extreme"], currentDifficulty)
        difficultyOptions.place(x=self.width*0.5, y=(self.height*0.5)+45, anchor=ck.CENTER)

        applyButton = self.createButton(settingsFrame, "Save Changes", lambda: self.saveChanges(settingsFrame, currentDimension, currentDifficulty))
        applyButton.place(x=self.width*0.5, y=(self.height*0.5)+90, anchor=ck.CENTER)

    def createOptionMenu(self, frame, values, variable): #option menu constructor
        return ck.CTkOptionMenu(master=frame,
                                       values=values,
                                       font=("ArcadeClassic", 24),
                                       height=40,
                                       width=200,
                                       fg_color="#32CD32",
                                       button_color="#32CD32",
                                       button_hover_color="#32CD32",
                                       dropdown_fg_color="#32CD32",
                                       variable=variable)

    def saveChanges(self, oldFrame, display, difficulty): #saves all game settings to database
        self.difficulty = str(difficulty.get())
        self.height=int(display.get().split("x")[1])
        self.width=int(display.get().split("x")[0])
        queries.setSettings(str(display.get()), str(difficulty.get()))

        self.clearApp()
        bgFrame = Frame(self.parent, bg="#32CD32")
        bgFrame.pack(fill="both", expand=True )
        self.parent.geometry(str(display.get()))
        self.clearApp()
        self.setMainScreen()

    def playDragRace(self): #sets drag race scene
        self.clearApp()
        self.canvas = Canvas(self.parent, width=self.width, height=self.height)
        self.canvas.place(x=0, y=0)

        bg = Image.open("assets/drag_race.png").resize((self.width,self.height))
        self.bgImage = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bgImage)

        self.createHUD(self.canvas) #creates HUD

        #creates players car
        playerCarX=int(self.width*0.12)
        playerCarY=int(self.height*0.12)
        playerCar = Image.open(f"assets/{self.car}.png").resize((playerCarX,playerCarY))
        self.playercar = ImageTk.PhotoImage(playerCar)
        self.carImage = self.canvas.create_image(self.width*0.07, self.height*0.5, image=self.playercar)

        self.setupGame()

    def createHUD(self, canvas):
        canvas.create_text((self.width*0.81), (self.height*0.03) , fill="White", anchor = "nw", font="ArcadeClassic 20 bold",
                        text="Difficulty: "+ self.difficulty)
        self.timerItem = canvas.create_text((self.width*0.81), (self.height*0.07) , fill="White", anchor = "nw", font="ArcadeClassic 20 bold",
                        text="Time: 0.00")

    def playRaceTrack(self): #sets race track scene
        self.clearApp()
        self.canvas = Canvas(self.parent, width=self.width, height=self.height)
        self.canvas.place(x=0, y=0)

        bg = Image.open("assets/playbg2-min.png").resize((self.width,self.height))
        self.bgImage = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor=NW, image=self.bgImage)

        self.createHUD(self.canvas)

        playerCarX=int(self.width*0.11)
        playerCarY=int(self.height*0.12)
        playerCar = Image.open(f"assets/{self.car}.png").resize((playerCarX,playerCarY))
        self.playercar = ImageTk.PhotoImage(playerCar)
        self.carImage = self.canvas.create_image(self.width*0.88, self.height*0.65, image=self.playercar)
        self.setupGame()

    def setupGame(self):
        self.locked = True
        self.complete = False
        self.textStopwatch = Stopwatch(1)
        self.setupText()
        self.countdown()

    def setupText(self):
        #creates background for text
        w=self.width
        h=self.height
        if (self.map == "Race Track"):
            bgRect = self.canvas.create_rectangle(w*0.17, h*0.526, w*0.83, h*0.715,
            fill='black', outline='green', width='2')
            sentenceRect = self.canvas.create_rectangle(w*0.173, h*0.53, w*0.826, h*0.72,
            fill='black', width='2')
        elif (self.map == "Drag Race"):
            bgRect = self.canvas.create_rectangle(w*0.17, h*0.811, w*0.83, h*1,
            fill='black', outline='green', width='2')
            sentenceRect = self.canvas.create_rectangle(w*0.173, h*0.815, w*0.826, h*1,
            fill='black', width='2')

        validSentence=dataset.returnSentence(self.difficulty) #gets sentence and does prechecks
        self.answer = validSentence
        size=16
        if (h == 600 and w == 1066): #different configuration for different resolutions
            if (self.map == "Race Track"):
                lineStart = 0.5425
            elif (self.map == "Drag Race"):
                lineStart = 0.8275
            lineBuffer = 0.0225
            spacing=10
            limit=60
            size=14
            font=("Telegrama", 14)
        if (h == 720 and w == 1280):
            if (self.map == "Race Track"):
                lineStart = 0.5425
            elif (self.map == "Drag Race"):
                lineStart = 0.8275
            lineBuffer = 0.025
            spacing=12
            limit=60
            size=18
            font=("Telegrama", 17)

        self.chars = []
        count = 1
        carryover = 0
        for i, char in enumerate(validSentence): #loops through answer drawing each character
            if (count > limit and char == " "):
                lineStart += lineBuffer
                count = 0
            x = w*0.17 + count*spacing
            y = h*lineStart
            count += 1
            textObj = self.canvas.create_text(x, y, text=char, font=font, justify=LEFT, fill='white')
            self.chars.append({'char': char, 'charItem': textObj})


        self.entry = ck.CTkEntry(master=self.parent, width=self.width*0.662, height=self.height*0.04,
                            fg_color="white", text_color='green',
                            font=('Arial', size), corner_radius=0)

        if (self.map == "Race Track"):
            self.entry.place(x=self.width*0.5, y=self.height*0.7, anchor="c")
        elif (self.map == "Drag Race"):
            self.entry.place(x=self.width*0.5, y=self.height*0.98, anchor="c")
        self.entry.focus_set()
        self.entry.configure(state="disabled")

    def countdown(self): #commences countdown screen
        self.countdownItem = self.canvas.create_text((self.width*0.5), (self.height*0.425) , fill="White", font=("Arial", 100), text="3")
        text = self.canvas.itemcget(self.countdownItem, "text")
        root.after(1000, self.updateCountdown)

    def updateCountdown(self): #provides the animation for the countdown display that flashes red
        text = self.canvas.itemcget(self.countdownItem, "text")

        if (text == "3"):
            self.canvas.itemconfig(self.countdownItem, fill = "Red")
            root.after(300, self.highlightCountdown)
            root.after(1000, self.updateCountdown)
            self.canvas.itemconfig(self.countdownItem, text = "2")

        if (text == "2"):
            self.canvas.itemconfig(self.countdownItem, fill = "Red")
            root.after(300, self.highlightCountdown)
            root.after(1000, self.updateCountdown)
            self.canvas.itemconfig(self.countdownItem, text = "1")

        if (text == "1"):
            self.canvas.itemconfig(self.countdownItem, fill = "Red")
            root.after(300, self.highlightCountdown)
            root.after(1000, self.updateCountdown)
            self.canvas.itemconfig(self.countdownItem, text = "GO")

        if (text == "GO"):
            self.canvas.itemconfig(self.countdownItem, fill = "Red")
            root.after(300, self.highlightCountdown)
            root.after(1000, self.updateCountdown)
            self.canvas.delete(self.countdownItem)
            self.entry.configure(state="normal")
            self.locked = False
            self.handleTyping()
            self.stopwatch = Stopwatch(1)
            self.updateTimer()

    def highlightCountdown(self):
        self.canvas.itemconfig(self.countdownItem, fill="White")

    def updateTimer(self):
        if (self.complete == False):
            self.canvas.itemconfig(self.timerItem, text="Time: " + str(round(self.stopwatch.duration, 2)))
            root.after(50, self.updateTimer)

    def handleTyping(self): #detects key press event
        self.entry.bind("<Key>", self.keyPress)
        self.usersCharList = []

    def keyPress(self, event): #handles key press event
        inputLength = len(self.usersCharList)
        answerLength = len(self.answer)
        if (event.keysym == "BackSpace" and len(self.usersCharList) > 0):
            self.usersCharList.pop()
            self.removeLetter(event)
        if (len(event.keysym) == 1 or event.char == "," or event.char == "." or event.char == "-"
            or event.char == " " or event.char == "(" or event.char == ")"):
            self.usersCharList.append(event.char)
            self.highlightChar(event.char)
            self.entry.update_idletasks()

    def highlightChar(self, char): #highlights character in the game
        index = len(self.usersCharList) - 1
        inputLength = len(self.usersCharList)
        answerLength = len(self.answer)

        if (index < answerLength):
            answerChar = self.answer[index]
            if (char != answerChar or self.locked == True): #character is wrong
                textObj = self.chars[index]['charItem']
                self.canvas.itemconfig(textObj, fill = "Red")
                self.mistakes += 1
                self.locked = True
            if (char == answerChar and self.locked == False): #character is right
                textObj = self.chars[index]['charItem']
                self.canvas.itemconfig(textObj, fill = "Green")
                self.locked = False
                if (self.map == "Race Track"): #calls each animation method for each map
                    self.handleRaceTrackProgress()
                elif (self.map == "Drag Race"):
                    self.handleDragRaceProgress()

                if (self.answer[-1] == answerChar and answerLength == inputLength): #game complete logic
                    self.stopwatch.stop()
                    self.locked = True
                    self.complete = True
                    self.entry.insert(len(self.entry.get()), char)
                    self.entry.configure(state="disabled")
                    self.rewardCoins()
                    self.popup()

    def removeLetter(self, event): #handles text animation for backspacing a character
        index = len(self.usersCharList)
        inputLen = len(self.chars)
        if (index < inputLen):
            textObj = self.chars[index]['charItem']
            self.canvas.itemconfig(textObj, fill = "White")
            self.locked = False

    def handleDragRaceProgress(self): #drag race animation
        userLen = len(self.usersCharList)
        answerLength = len(self.answer)
        progress = userLen/answerLength

        startX, startY = self.width*0.13, self.height*0.5
        endX, endY = self.width*0.90, self.height*0.5
        newX = startX + int((endX - startX) * (progress)) - int(self.width*0.12) // 2

        self.canvas.coords(self.carImage, newX, startY)


    def handleRaceTrackProgress(self): #race track animation
        canvasWidth = self.canvas.winfo_width()
        canvasHeight = self.canvas.winfo_height()
        turns = dataset.getTurns()
        userLen = len(self.usersCharList)
        answerLength = len(self.answer)
        progressPercent = userLen/answerLength

        trackLength = 0
        for i in range(len(turns) - 1): # calculate the total length of the track
            x1 = turns[i][0] * canvasWidth
            y1 = turns[i][1] * canvasHeight
            x2 = turns[i + 1][0] * canvasWidth
            y2 = turns[i + 1][1] * canvasHeight
            trackLength += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # calculate the current position of the car
        carX = self.canvas.coords(self.carImage)[0]
        carY = self.canvas.coords(self.carImage)[1]
        distanceTraveled = 0
        for i in range(len(turns) - 1): #checks car segment and updates proportionally
            x1 = turns[i][0] * canvasWidth
            y1 = turns[i][1] * canvasHeight
            x2 = turns[i + 1][0] * canvasWidth
            y2 = turns[i + 1][1] * canvasHeight

            #initialises segment start and end and use interpolation to update car x,y
            segmentLength = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            segmentProgress = segmentLength / trackLength
            segmentStartProgress = distanceTraveled
            segmentEndProgress = distanceTraveled + segmentProgress
            if progressPercent >= segmentStartProgress and progressPercent <= segmentEndProgress:
                segmentProgressPercent = (progressPercent - segmentStartProgress) / segmentProgress
                carX = int(x1 + segmentProgressPercent * (x2 - x1))
                carY = int(y1 + segmentProgressPercent * (y2 - y1))
                break
            distanceTraveled += segmentProgress

        self.canvas.coords(self.carImage, carX, carY)


    def popup(self): #popup display on game completion
        time = round(self.stopwatch.duration, 2)
        words = len(self.answer.split(" "))
        minutes = time / 60
        wpm = round(words/minutes, 1)
        queries.insertRecord(self.difficulty, round(self.stopwatch.duration, 2), wpm, self.mistakes, self.map)

        # Create the pop-up frame
        popup = Frame(self.parent, width=self.width*0.35, height=self.height*0.8, bg='Black',
        bd=2, highlightbackground="red", highlightthickness=2)
        popup.place(x=self.width*0.5, y=self.height*0.5, anchor="center")

        img = Image.open("assets/trophy.png").resize((180, 180))
        imgObj = ImageTk.PhotoImage(img)
        trophy = Label(popup, image=imgObj, bg='Black', highlightthickness=0)
        trophy.image = imgObj
        trophy.place(relx=0.5, rely=0.22, anchor="center")

        wpmLabel = tk.Label(popup, text="Words  Per  Minute: " + str(wpm), bg="Black", fg="Yellow", font=("ArcadeClassic", 18), wraplength=self.width*0.3)
        wpmLabel.place(relx=0.5, rely=0.45, anchor="center")

        img = Image.open("assets/GameOver.png")
        imgObj = ImageTk.PhotoImage(img)
        gameOver = Label(popup, image=imgObj, bg='Black', highlightthickness=0)
        gameOver.image = imgObj
        gameOver.place(relx=0.5, rely=0.55, anchor="center")

        winnerLabel = tk.Label(popup, text="You   Win!", bg="Black", fg="#00fd0e", font=("ArcadeClassic", 26), wraplength=self.width*0.3)
        winnerLabel.place(relx=0.5, rely=0.65, anchor="center")

        descLabel = tk.Label(popup, text="You  completed  the  "+str(self.difficulty)+"  difficulty  in  "+str(time)+"  seconds.", bg="Black", fg="White", font=("ArcadeClassic", 19), wraplength=self.width*0.3)
        descLabel.place(relx=0.5, rely=0.75, anchor="center")

        closePopupButton = ck.CTkButton(master=popup,
                              text="Continue",
                              font=("ArcadeClassic", 20),
                              height=35,
                              width=180,
                              fg_color="#32CD32",
                              hover_color="#78cd32",
                              command= lambda: self.setMainScreen())
        closePopupButton.place(relx=0.5, rely=0.9, anchor=ck.CENTER)

    def rewardCoins(self):
        speedScore = algorithms.calcSpeedScore(len(self.answer), round(self.stopwatch.duration, 2))
        bonusScore = algorithms.calcBonusScore(self.mistakes)
        accuracyMultiplier = algorithms.getAccuracyMultiplier(len(self.answer), self.mistakes)
        difficultyMultiplier = algorithms.getDifficultyMultiplier(self.difficulty)
        #calculates coins and rewards user
        coins = algorithms.calculateCoins(speedScore, bonusScore, accuracyMultiplier, difficultyMultiplier)

        dimensions = str(self.width)+"x"+str(self.height)
        totalCoins = round(self.coins, 0) + round(coins, 0)
        self.coins = totalCoins
        queries.updateCoins(totalCoins)

    def Quit(self):
        self.parent.quit()

    def start(self):
        self.parent.mainloop()

root = ck.CTk()
root.geometry("1066x600")
root.resizable(False, False)
root.title("Keyboard Typing Racer")
app = App(root)
app.start()
