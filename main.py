from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from pygame import mixer

def formTime(seconds):
    minute = int(seconds / 60)
    seconds = int(seconds % 60)
    return f"{minute}:{seconds:02d}"

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
        settingsWindow.geometry(f"{windowWidth}x{settingsHeight}+{rootX}+{rootY - settingsHeight - 5}")
        settingsWindow.deiconify()
    else:
        settingsWindow.withdraw()

def addMusic():
    global playlist, musicFrame

    musicPath = filedialog.askopenfilename(title="Добавить музыку", filetypes=[("Audio files", ("*.mp3", "*.wav", "*.ogg"))])

    if musicPath not in playlist:
        playlist.append(musicPath)

        musicName = musicPath.split("/")[-1].split(".")[0]
        indexTrack = len(playlist) - 1
        label = Label(musicFrame, text=musicName, anchor=W)
        label.pack(fill=X, padx=5, pady=2)

        label.bind("<Button-1>", lambda e,indexTrack=indexTrack:playLabelTrack(indexTrack))

def playLabelTrack(indexTrack):
    global currentTrack, played
    currentTrack = indexTrack

    fullTime.config(text=formTime(mixer.Sound(playlist[currentTrack]).get_length()))
    musicName = playlist[currentTrack].split("/")[-1].split(".")[0]
    trackName.config(text=musicName)
    mixer.music.load(playlist[currentTrack])
    mixer.music.play()
    played = True
    playButton.config(text="Pause")
    timeRegul.config(to=mixer.Sound(playlist[currentTrack]).get_length())
    root.after(1000, updateTime)

def move(event, windowHeight, windowWidth):
    rootX = root.winfo_x()
    rootY = root.winfo_y()
    x, y = root.winfo_pointerxy()

    root.geometry(f"+{x}+{y}")

    settingsHeight = int(windowHeight * 0.2)
    settingsWindow.geometry(f"{windowWidth}x{settingsHeight}+{rootX}+{rootY - settingsHeight - 5}")

    musicWidth = int(windowWidth * 0.4)
    listMusicWindow.geometry(f"{musicWidth}x{windowHeight}+{rootX - musicWidth - 5}+{rootY}")

def playMusic():
    global currentTrack, played
    if played == False:
        mixer.music.load(playlist[currentTrack])
        mixer.music.unpause()
        playButton.config(text="Pause")
    else:
        mixer.music.pause()
        playButton.config(text="Play")
    played = not played
    root.after(1000, updateTime)

def nextMusic():
    global currentTrack
    currentTrack = (currentTrack + 1) % len(playlist)
    fullTime.config(text=formTime(mixer.Sound(playlist[currentTrack]).get_length()))
    musicName = playlist[currentTrack].split("/")[-1].split(".")[0]
    trackName.config(text=musicName)
    timeRegul.config(to=mixer.Sound(playlist[currentTrack]).get_length())
    mixer.music.load(playlist[currentTrack])
    mixer.music.play()

def backMusic():
    global currentTrack
    currentTrack = (currentTrack - 1) % len(playlist)
    fullTime.config(text=formTime(mixer.Sound(playlist[currentTrack]).get_length()))
    musicName = playlist[currentTrack].split("/")[-1].split(".")[0]
    trackName.config(text=musicName)
    timeRegul.config(to=mixer.Sound(playlist[currentTrack]).get_length())
    mixer.music.load(playlist[currentTrack])
    mixer.music.play()

def updateTime():
    global currentTrack
    seconds = mixer.music.get_pos() / 1000
    nowTime.config(text=formTime(seconds))
    timeRegul.set(seconds)
    root.after(1000, updateTime)
    


if __name__ == "__main__":
    mixer.init()

    root = Tk()
    root.title("AudioPlayer")
    root.resizable(False, False)

    screnHeight = root.winfo_screenheight()
    screenWidth = root.winfo_screenwidth()

    windowWidth = int(screenWidth * 0.4)
    windowHeight = int(windowWidth * 8 / 10)
    root.geometry(f"{windowWidth}x{windowHeight}")
    root.overrideredirect(True)
    root.call('source', 'azure.tcl')
    root.call("set_theme", "dark")
    style = Style()

    upFrame = Frame(root)
    upFrame.pack(side=TOP, fill=X)

    settingButton = Button(upFrame, text="Settings", command=lambda: showSettings(windowHeight, windowWidth))
    settingButton.pack(side=RIGHT, padx=10, pady=10)

    img = PhotoImage(file="default.png")
    canvasImage = Canvas(width=200, height=200)
    canvasImage.create_image(1, 1, anchor=NW, image=img)
    canvasImage.pack(side=TOP)


    timeAndNameFrame = Frame(root)
    timeAndNameFrame.pack(pady=10, fill=X)

    trackName = Label(timeAndNameFrame, text="default")
    trackName.pack(pady=5)
    timeFrame = Frame(timeAndNameFrame)
    timeFrame.pack(side=TOP, padx=5, pady=20)
    nowTime = Label(timeFrame, text="00:00")
    timeRegul = Scale(timeFrame, from_=0, to=1000, orient=HORIZONTAL, length=200)
    fullTime = Label(timeFrame, text="00:00")
    nowTime.pack(side=LEFT)
    timeRegul.pack(side=LEFT, padx=5)
    fullTime.pack(side=LEFT)



    buttonFrame = Frame(root)
    buttonFrame.pack(expand=True)

    playButton = Button(buttonFrame, text="Play", command=playMusic)
    nextButton = Button(buttonFrame, text="Next", command=nextMusic)
    backButton = Button(buttonFrame, text="Back", command=backMusic)
    pinButton = Button(buttonFrame, text="Pin", command=pinApp)
    listButton = Button(buttonFrame, text="List", command=lambda: showListMusic(windowHeight, windowWidth))
    listButton.pack(side=LEFT, padx=10)
    backButton.pack(side=LEFT, padx=10)
    playButton.pack(side=LEFT, padx=10)
    nextButton.pack(side=LEFT, padx=10)
    pinButton.pack(side=LEFT, padx=10)




    listMusicWindow = Toplevel()
    listMusicWindow.resizable(True, False)
    addMusicButton = Button(listMusicWindow, text="Add music", command=addMusic)
    addMusicButton.pack(anchor=N, pady=10)
    musicFrame = Frame(listMusicWindow)
    musicFrame.pack(fill=BOTH, expand=True)
    listMusicWindow.overrideredirect(True)
    listMusicWindow.withdraw()


    settingsWindow = Toplevel()
    settingsWindow.resizable(False, True)
    transparencyRegul = Scale(settingsWindow, from_=0.3, to=1, value=1, orient=HORIZONTAL, command=updateTransparency)
    transparencyRegul.pack(pady=10)
    settingsWindow.overrideredirect(True)
    settingsWindow.withdraw()


    playlist = []
    played = False
    showedSettings = False
    showedList = False
    pinned = False
    currentTrack = 0

    root.bind("<B1-Motion>", lambda event: move(event, windowHeight, windowWidth))
    root.mainloop()