from tkinter import *
import tkinter as tk
from tkinter import messagebox as mb
import track_library as lib
from library_item import LibraryItem
import font_manager as fonts
import tkinter.scrolledtext as tkst

class AddTrackGUI:
    def __init__(self, parent=None):
        # create window
        self._create_window(parent)
        # create widgets
        self._create_widgets()

    def _create_window(self, parent=None):
        if parent is not None:
            self.window = Toplevel(parent)
        else:
            self.window = Tk()
        self.window.title("Add Track")
        self.window.geometry("630x500")

    def _create_widgets(self):
        # create a label
        lbl_info = Label(self.window, text="Create your own track here!", font = ("Arial", 15))
        lbl_info.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        lbl_info = Label(self.window, text="Current track: ", font = ("Arial", 12))
        lbl_info.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        lbl_name = Label(self.window, text="Track Name: ")
        lbl_name.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        lbl_artist = Label(self.window, text="Artist: ")
        lbl_artist.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        lbl_rating = Label(self.window, text="Rating: ")
        lbl_rating.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        lbl_play_count = Label(self.window, text="Play Count: ")
        lbl_play_count.grid(row=5, column=1, padx=5, pady=5, sticky=W)
        # create a text box
        txt_track_list = tkst.ScrolledText(self.window, width=30, height=10)
        txt_track_list.grid(row=2, rowspan=4, column=0, padx=5, pady=5, sticky=W)
        # create an entry
        self.track_var = StringVar()
        txt_name = Entry(self.window, width=20, textvariable=self.track_var)
        txt_name.grid(row=2, column=2, padx=5, pady=5, sticky=W)

        self.artist_var = StringVar()
        txt_artist = Entry(self.window, width=20, textvariable=self.artist_var)
        txt_artist.grid(row=3, column=2, padx=5, pady=5, sticky=W)

        self.rating_var = StringVar()
        txt_rating = Entry(self.window, width=20, textvariable=self.rating_var)
        txt_rating.grid(row=4, column=2, padx=5, pady=5, sticky=W)

        self.play_count_var = IntVar()
        txt_play_count = Entry(self.window, width=20, textvariable=self.play_count_var)
        txt_play_count.grid(row=5, column=2, padx=5, pady=5, sticky=W)

        btn_add = Button(self.window, text="Add Track", command=self.add_new_track)
        btn_add.grid(row=6, column=1, padx=5, pady=5, sticky=W)
    
    def add_new_track(self):
        track = self.track_var.get()
        artist = self.artist_var.get()
        rating = self.rating_var.get()
        play_count = self.play_count_var.get()
        # Validate input
        if not track or not artist or not rating.isdigit():
            mb.showerror("Input Error", "Please enter valid track name, artist, and rating (number).")
            return
    
        # Very simple: next key is count + 1 as string
        new_key = str(len(lib.library) + 1) # Set new key as the next number in the library
        lib.library[new_key] = LibraryItem(track, artist, int(rating)) # Create a new LibraryItem
        lib.library[new_key].play_count = play_count # Set play count for the new track
        mb.showinfo("Track Added", f"Track '{track}' added to library as track {new_key}.")
    
        # Clear fields
        self.track_var.set("")
        self.artist_var.set("")
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = AddTrackGUI()
    app.run()