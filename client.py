import ftplib
import ntpath
import os
import socket
import time
from ftplib import FTP
from pathlib import Path
from threading import Thread
from tkinter import *
from tkinter import filedialog, ttk

import pygame
from playsound import playsound
from pygame import mixer

PORT = 8080
IP_ADDRESS = "127.0.0.1"
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox = None
filePathLabel = None
song_counter = 0
infoLabel = None


def browseFiles():
    global listbox
    global song_counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd("shared_files")
        fname = ntpath.basename(filename)
        with open(filename, "rb") as file:
            ftp_server.storbinary(f"STOR {fname}", file)

        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter, fname)
        song_counter = song_counter + 1

    except FileNotFoundError:
        print("Cancel Button Pressed")


def download():
    global infoLabel
    song_to_download = listbox.get(ANCHOR)
    infoLabel.configure(text="Downloading " + song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home())
    download_path = home + "/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd("shared_files")
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, "wb")
    ftp_server.retrbinary("RETR " + song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text="Download Complete")
    time.sleep(1)
    if song_selected != "":
        infoLabel.configure(text="Now Playing: " + song_selected)
    else:
        infoLabel.configure(text="")


def play():
    global song_selected
    global listbox
    song_selected = listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load("shared_files/" + song_selected)
    mixer.music.play()
    if song_selected != "":
        infoLabel.configure(
            text="Now Playing: " + song_selected,
            fg="white",
            bg="LightSkyBlue",
            font=("Calibri", 15),
        )
    else:
        infoLabel.configure(text="")


def stop():
    global song_selected

    pygame
    mixer.init()
    mixer.music.load("shared_files/" + song_selected)
    mixer.music.pause()
    infoLabel.configure(text="")


def pause():
    global song_selected

    pygame
    mixer.init()
    mixer.music.load("shared_files/" + song_selected)
    mixer.music.pause()


def resume():
    global song_selected

    mixer.init()
    mixer.music.load("shared_files/" + song_selected)
    mixer.music.play()


def musicWindow():
    global song_counter
    global listbox
    global infoLabel

    window = Tk()

    window.title("Music Sharing")
    window.geometry("320x350")
    window.configure(bg="LightSkyBlue")

    selectLabel = Label(
        window, text="Select Song", bg="LightSkyBlue", font=("Calibri", 10), fg="black"
    )
    selectLabel.place(x=2, y=1)

    listbox = Listbox(
        window,
        height=10,
        width=39,
        activestyle="dotbox",
        bg="LightSkyBlue",
        borderwidth=2,
        font=("Calibri", 10),
    )
    listbox.place(x=10, y=20)
    for file in os.listdir("shared_files"):
        filename = os.fsdecode(file)
        listbox.insert(song_counter, filename)
        song_counter = song_counter + 1

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight=1, relx=1)
    scrollbar1.config(command=listbox.yview)

    playButton = Button(
        window,
        text="Play",
        width=10,
        bg="LightSkyBlue",
        font=("Calibri", 10),
        command=play,
    )
    playButton.place(x=30, y=200)

    stopButton = Button(
        window,
        text="Stop",
        bd=1,
        width=10,
        bg="LightSkyBlue",
        font=("Calibri", 10),
        command=stop,
    )
    stopButton.place(x=200, y=200)

    upload = Button(
        window,
        text="Upload",
        width=10,
        bd=1,
        bg="LightSkyBlue",
        font=("Calibri", 10),
        command=browseFiles,
    )
    upload.place(x=30, y=250)

    download = Button(
        window, text="Download", width=10, bd=1, bg="LightSkyBlue", font=("Calibri", 10)
    )
    download.place(x=200, y=250)

    resumeButton = Button(
        window,
        text="Resume",
        width=10,
        bd=1,
        bg="SkyBlue",
        font=("Calibri", 10),
        command=resume,
    )
    resumeButton.place(x=30, y=300)

    pauseButton = Button(
        window,
        text="Pause",
        width=10,
        bd=1,
        bg="SkyBlue",
        font=("Calibri", 10),
        command=pause,
    )
    pauseButton.place(x=200, y=300)

    infoLabel = Label(window, text="", fg="blue", font=("Calibri", 8))
    infoLabel.place(x=4, y=330)

    window.mainloop()


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()


setup()
