from os import access
from tkinter import *
from tkinter import filedialog
from pygame import *
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
################################################################################
# Global variables
global current_song # string directory of file
current_song = None

global paused 
paused = False

global current_song_length # make it an int
current_song_length = None

global current_song_position # keep as int
current_song_position = None

global hasAlteredPlayPosition
hasAlteredPlayPosition = False

################################################################################

# setup window
root = Tk()
root.title("MP3 Player")
root.iconbitmap("images/melody.ico")
root.geometry("500x400")
pygame.mixer.init()

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
# Add/Remove Songs

def addSong(): 
    song = filedialog.askopenfilename(initialdir='Audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    playlist.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='Audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        playlist.insert(END, song)

def remove_song():
    if current_song == playlist.get(ACTIVE):
        pygame.mixer.music.stop()
    playlist.delete(ANCHOR)


def remove_all_song():
    playlist.delete(0, END)
    pygame.mixer.music.stop()

################################################################################
# support functions for below - control global variables better

def reset_current_song_position(): #reset current song position
    global current_song_position
    current_song_position = int(0)
    return

def set_currently_playing_song(song_currently_playing): # change global currently playing
    global current_song
    current_song = song_currently_playing
    get_current_song_length()
    return

def get_current_song_length(): # get length of current song - calculate and set its length
    song = playlist.get(current_song)
    mutagen_song = MP3(song)

    global current_song_length     
    current_song_length = int(mutagen_song.info.length)

    return current_song_length

def set_slider_length():
    # set slider values
    slider.config(to=current_song_length, value=0)

def increment_current_time():
    global current_song_position
    current_song_position  = int(current_song_position + 1)
    return

def get_play_time():
    global hasAlteredPlayPosition
    global current_song_position    

    # keep incrementing time
    if hasAlteredPlayPosition == False: # increments as normal if its just play
        current_song_position = int(pygame.mixer.music.get_post()/1000)
    else:
        increment_current_time()
        hasAlteredPlayPosition = True
    
    # Display times
    time_formatted = time.strftime('%M:%S', time.gmtime(current_song_position))
    song_length_formatted = time.strftime('%M:%S', time.gmtime(current_song_length))
    play_status.config(text="Time Elapsed: " + time_formatted + " of " + song_length_formatted + "     ")
    
    # if it reaches the end stop function
    if current_song_length > current_song_position:
        return

    # alter slider and keep calling itself
    if current_song != None:
        slider.config(value=int(current_song_position))
        play_status.after(1000, get_play_time) # keep calling itself every second
    



################################################################################
# button functions
def play():
    # will play whatever is highlight
    song = playlist.get(ACTIVE) 
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    # set current song and length
    set_currently_playing_song(song)
    get_current_song_length()

    # resets position of current position to 0
    reset_current_song_position()
    
    # call play time
    get_play_time() 

    # set slider length
    set_slider_length()

def play_next(next_song):
    song = next_song

    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    set_currently_playing_song(song)
    get_current_song_length()
    
    # call play time
    get_play_time() 

    # set slider length
    set_slider_length()
    
def stop():
    pygame.mixer.music.stop()
    playlist.select_clear(ACTIVE)
    global current_song
    current_song = None
    reset_current_song_position()


def pause(x):
    global paused
    if paused == False :
        
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False

def next():
    #select the next song
    current = playlist.curselection()
    next_song = (current[0] + 1,) # gets next song
    toPlay = playlist.get(next_song)
    # play it
    play_next(toPlay)

    # Highlight right song
    playlist.selection_clear(0, END)
    playlist.activate(next_song)
    playlist.selection_set(next_song, last=None)

def back():
    # select the previous song
    current = playlist.curselection()
    next_song = (current[0] - 1,) # gets next song
    toPlay = playlist.get(next_song)
    # play it
    play_next(toPlay)

    # Highlight right song
    playlist.selection_clear(0, END)
    playlist.activate(next_song)
    playlist.selection_set(next_song, last=None)

def slide():
    global hasAlteredPlayPosition
    global current_time

    hasAlteredPlayPosition = True
    current_time = slider.get()
    song = current_song

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(start=int(slider.get()))



################################################################################



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


################################################################################
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