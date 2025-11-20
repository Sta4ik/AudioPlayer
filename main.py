from tkinter import *
from tkinter.ttk import *
# from pygame import mixer

def pinApp():
    global pinned
    pinned = not pinned
    root.attributes("-topmost", pinned)

def showListMusic(windowHeight, windowWidth):
    global showedList, listMusicWindow
    showedList = not showedList


    rootX = root.winfo_x()
    rootY = root.winfo_y()
    musicWidth = int(windowWidth * 0.4)

    if showedList:
        listMusicWindow.geometry(f"{musicWidth}x{windowHeight}+{rootX - musicWidth - 5}+{rootY}")
        listMusicWindow.deiconify()
    else:
        listMusicWindow.withdraw()

def updateTransparency(valueAlpha):
    root.attributes("-alpha", valueAlpha)
    settingsWindow.attributes("-alpha", valueAlpha)
    listMusicWindow.attributes("-alpha", valueAlpha)

def showSettings(windowHeight, windowWidth):
    global showedSettings, settingsWindow
    showedSettings = not showedSettings

    rootX = root.winfo_x()
    rootY = root.winfo_y()
    settingsHeight = int(windowHeight * 0.2)

    if showedSettings:
        settingsWindow.geometry(f"{windowWidth}x{settingsHeight}+{rootX}+{rootY - settingsHeight - 35}")
        settingsWindow.deiconify()
    else:
        settingsWindow.withdraw()


if __name__ == "__main__":
    # mixer.init()

    root = Tk()
    root.title("AudioPlayer")
    root.resizable(False, False)

    screnHeight = root.winfo_screenheight()
    screenWidth = root.winfo_screenwidth()

    windowWidth = int(screenWidth * 0.4)
    windowHeight = int(windowWidth * 8 / 10)
    root.geometry(f"{windowWidth}x{windowHeight}")
    root.call('source', 'azure.tcl')
    root.call("set_theme", "dark")
    style = Style()

    upFrame = Frame(root)
    upFrame.pack(side=TOP, fill=X)

    settingButton = Button(upFrame, text="Settings", command=lambda: showSettings(windowHeight, windowWidth))
    settingButton.pack(side=RIGHT, padx=10, pady=10)

    timeFrame = Frame(root)
    timeFrame.pack()

    nowTime = Label(timeFrame)
    timeRegul = Scale(timeFrame, orient=HORIZONTAL)
    fullTime = Label(timeFrame)
    nowTime.pack()
    timeRegul.pack()
    fullTime.pack()


    buttonFrame = Frame(root)
    buttonFrame.pack(expand=True)

    playButton = Button(buttonFrame, text="Play")
    nextButton = Button(buttonFrame, text="Next")
    backButton = Button(buttonFrame, text="Back")
    pinButton = Button(buttonFrame, text="Pin", command=pinApp)
    listButton = Button(buttonFrame, text="List", command=lambda: showListMusic(windowHeight, windowWidth))
    listButton.pack(side=LEFT, padx=10)
    backButton.pack(side=LEFT, padx=10)
    playButton.pack(side=LEFT, padx=10)
    nextButton.pack(side=LEFT, padx=10)
    pinButton.pack(side=LEFT, padx=10)




    listMusicWindow = Toplevel()
    listMusicWindow.resizable(True, False)
    addMusicButton = Button(listMusicWindow, text="Add music")
    addMusicButton.pack(anchor=N, pady=10)
    listMusicWindow.withdraw()


    settingsWindow = Toplevel()
    settingsWindow.resizable(False, True)
    transparencyRegul = Scale(settingsWindow, from_=0.3, to=1, value=1, orient=HORIZONTAL, command=updateTransparency)
    transparencyRegul.pack(pady=10)
    settingsWindow.withdraw()

    showedSettings = False
    showedList = False
    pinned = False
    root.mainloop()