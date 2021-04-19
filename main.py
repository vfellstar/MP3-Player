# imports
from os import access
from tkinter import *
from tkinter import filedialog
from pygame import *
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

################################################################################

# setup window
root = Tk()
root.title("MP3 Player")
root.iconbitmap("images/melody.ico")
root.geometry("500x400")
pygame.mixer.init()

# global variables
global paused 
paused = False

global current_song
current_song = None

global current_song_length
current_song_length = None

global current_time
current_time = None

global hasAlteredPlayPosition
hasAlteredPlayPosition = False

################################################################################################################################################################

# create playlist <--- will add songs to it
playlist = Listbox(root, bg="grey", fg="black", width=70, selectbackground="orange")
playlist.pack(pady=10)

# Control buttons images
back_image = PhotoImage(file="Images/back.png")
forward_image = PhotoImage(file="Images/forward.png")
play_image = PhotoImage(file="Images/play.png")
pause_image = PhotoImage(file="Images/pause.png")
stop_image = PhotoImage(file="Images/stop.png")

# Control frames
controlFrame = Frame(root)
controlFrame.pack()

################################################################################
# playtime functions


def get_song_length():

    currently_playing = playlist.curselection()
    song = playlist.get(currently_playing)

    mutagen_song = MP3(song)
    global current_song_length
    song_length = mutagen_song.info.length # returns length in seconds
    current_song_length = song_length
    return current_song_length


def get_play_time():
    global current_time
    if hasAlteredPlayPosition == False:
        current_play_time = pygame.mixer.music.get_pos()/1000
        current_time = current_play_time


    # convert above into time format rather than seconds
    time_formatted = time.strftime('%M:%S', time.gmtime(current_time))

    if current_song != None:
        # after 1 sec itll call itself
        slider.config(value=int(current_time))
        play_status.after(1000, get_play_time) 

    # song length and shit
    song_length = get_song_length()

    song_length_formatted = time.strftime('%M:%S', time.gmtime(song_length))

    # put text in
    play_status.config(text="Time Elapsed: " + time_formatted + " of " + song_length_formatted + "     ")
    slider.config(to=int(song_length))



# add song(s) function
def addSong(): 
    song = filedialog.askopenfilename(initialdir='Audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    playlist.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='Audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        playlist.insert(END, song)

def play():
    song = playlist.get(ACTIVE) # will play whatever is highlight
    global current_song 
    current_song = song

    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    

    
    get_play_time() # call play time
    song = playlist.get(current_song)


def playNext(songToPlay):
    song = songToPlay 
    global current_song_length
    current_song_length = 0
    current_song_length = get_song_length()
    global current_song 
    current_song = song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()


    get_play_time() # call play time

def stop():
    pygame.mixer.music.stop()
    playlist.select_clear(ACTIVE)
    global current_song
    current_song = None

def pause(is_paused):
    global paused
    paused = is_paused
    if paused == False :
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False
    
def next():
    current = playlist.curselection()
    next_song = (current[0] + 1,) # gets next song
    toPlay = playlist.get(next_song)
    playNext(toPlay)

    # Highlight right song
    playlist.selection_clear(0, END)
    playlist.activate(next_song)
    playlist.selection_set(next_song, last=None)


def back():
    current = playlist.curselection()
    next_song = (current[0] - 1,) # gets next song
    toPlay = playlist.get(next_song)
    playNext(toPlay)

    # Highlight right song
    playlist.selection_clear(0, END)
    playlist.activate(next_song)
    playlist.selection_set(next_song, last=None)

def remove_song():
    if current_song == playlist.get(ACTIVE):
        pygame.mixer.music.stop()
    playlist.delete(ANCHOR)


def remove_all_song():
    playlist.delete(0, END)
    pygame.mixer.music.stop()

def slide(y):
    global hasAlteredPlayPosition
    global current_time

    hasAlteredPlayPosition = True
    current_time = slider.get()

    song = playlist.get(ACTIVE)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(slider.get()))


# Create control buttons
back_btn = Button (controlFrame, image=back_image, borderwidth=0, padx=15, command=back)
forward_btn = Button (controlFrame, image=forward_image, borderwidth=0, padx=15, command=next)
play_btn = Button (controlFrame, image=play_image, borderwidth=0, padx=15, command=play)
pause_btn = Button (controlFrame, image=pause_image, borderwidth=0, padx=15, command=lambda: pause(paused))
stop_btn = Button (controlFrame, image=stop_image, borderwidth=0, padx=15, command=stop)
back_btn.grid(row=0 ,column=0)
forward_btn.grid(row=0 ,column=1)
play_btn.grid(row=0 ,column=2)
pause_btn.grid(row=0 ,column=3)
stop_btn.grid(row=0 ,column=4)

# menu
my_menu = Menu(root)
root.config(menu=my_menu)

# song menus
addSongMenu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=addSongMenu)
deleteSongMenu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=deleteSongMenu)

# commands in the top left
addSongMenu.add_command(label="Add A Song To The Playlist", command=addSong)
addSongMenu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)
deleteSongMenu.add_command(label="Remove A Song From The Playlist", command=remove_song)
deleteSongMenu.add_command(label="Remove All Songs From Playlist", command=remove_all_song)

# play status
play_status = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
play_status.pack(fill=X, side=BOTTOM, ipady=2)

# music slider
slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=400)
slider.pack(pady=35)

#temp

root.mainloop()