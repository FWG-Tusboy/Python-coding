from tkinter import *
from tkinter import messagebox as mb
import tkinter.scrolledtext as tkst
import track_library as lib
import font_manager as fonts
from tkinter.filedialog import askopenfilename, asksaveasfilename
import csv

def set_text(widget, text):
    widget.config(state="normal") # configure state to normal
    widget.delete("1.0", END) # delete from the beginning
    widget.insert(END, text) # insert in the chosen text
    widget.config(state="disabled") # only allow user to read

class TrackList():
    def __init__(self, parent=None):
        if parent is not None:
            self.window = Toplevel(parent) # Create a new Toplevel window if a parent is provided
        else:
            self.window = Tk() # Create a new Tkinter window if no parent is provided
        self.window.geometry("750x450")
        self.window.title("New Track List")

        # Make a list for playlist
        self.playlist = []

        # Make buttons for "Add Track", "Play", "Reset", "Save" and "Load"
        add_tracks_btn = Button(self.window, text="Add Track", command=self.add_track)
        add_tracks_btn.grid(row=0, column=2, padx=5, pady=5, sticky="W")
        play_playlist_btn = Button(self.window, text="Play", command=self.play_playlist)
        play_playlist_btn.grid(row=0, column=3, padx=10, pady=10, sticky="W")
        reset_playlist_btn = Button(self.window, text="Reset", command=self.reset_playlist)
        reset_playlist_btn.grid(row=0, column=4, padx=5, pady=5, sticky="W")
        save_playlist_btn = Button(self.window, text="Save", command=self.save_playlist_to_csv)
        save_playlist_btn.grid(row=0, column=5, padx=5, pady=5, sticky="W")
        load_playlist_btn = Button(self.window, text="Load", command=self.load_playlist_from_csv)
        load_playlist_btn.grid(row=0, column=6, padx=5, pady=5, sticky="W")

        # Enter track number
        lbl_track_number = Label(self.window, text="Enter Track Number")
        lbl_track_number.grid(row=0, column=0, padx=10, pady=10, sticky="W")
        self.input_txt = Entry(self.window, width=6)
        self.input_txt.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        # Available tracks in the library
        available_track = Label(self.window, text="Available tracks: ")
        available_track.grid(row=4, column=0, padx=5, pady=5, sticky=N)
        self.list_txt = tkst.ScrolledText(self.window, width=55, height=8, wrap="none") 
        self.list_txt.grid(row=4, column=1, columnspan=6, padx=10, pady=10, sticky=W) 
        
        # Playlist
        lbl_playlist = Label(self.window, text="Playlist: ")
        lbl_playlist.grid(row=1, column=0, padx=5, pady=5, sticky="N")
        self.displayed_track_txt = Text(self.window, width=55, height=7, wrap="none", state="disabled")
        self.displayed_track_txt.grid(row=1, column=1, columnspan=6, sticky="NW", padx=10, pady=10) 

        # Status of the interface
        self.status_lbl = Label(self.window, text="", font=("Helvetica", 10)) 
        self.status_lbl.grid(row=3, column=1, columnspan=4, sticky="WS", padx=10, pady=2) 

        self.display_available_tracks() 

    def save_playlist_to_csv(self):
        if not self.playlist:
            self.status_lbl.config(text="Playlist is empty. Cannot save.") # if playlist is empty, status will show a message
            return

        file_path = asksaveasfilename(defaultextension=".csv", # default file extension
                                      filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], # file types and their extensions
                                      title="Save Playlist As") # title of the dialog
        if not file_path:
            self.status_lbl.config(text="Save cancelled.") # if user cancels the save dialog
            return

        try:
            with open(file_path, mode="w", newline='', encoding="utf-8") as file: # open the file in write mode, encoding set to utf-8, which is a common encoding for text files
                writer = csv.writer(file) # create a CSV writer object
                writer.writerow(["No.", "Track Number", "Track Name", "Play Count"]) # write the header row
                for i, num in enumerate(self.playlist, start=1): # enumerate starts counting from 1
                    track = lib.library[num]
                    writer.writerow([i, num, track.name, track.play_count])
            self.status_lbl.config(text=f"Playlist saved to {file_path}") # save is successful, status will show a message
        except Exception as e:
            self.status_lbl.config(text=f"Error saving playlist: {e}") # if there is an error during saving, status will show a message

    def load_playlist_from_csv(self):
        file_path = askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], # ask open file dialog for CSV files
                                    title="Open Playlist File")
        if not file_path:
            self.status_lbl.config(text="Load cancelled.") # if user cancels the load dialog
            return

        try:
            with open(file_path, mode="r", encoding="utf-8") as file: # open the file in read mode, encoding set to utf-8
                reader = csv.reader(file)
                next(reader, None)  # skip header
                new_playlist = []
                for row in reader: # read each row in the CSV file
                    if len(row) >= 2: # check if there are at least two columns, because we need track number and name
                        track_num = row[1] # get the track number from the second column
                        if track_num in lib.library: 
                            if track_num not in new_playlist:
                                new_playlist.append(track_num) # add the track number to the new playlist if it is not already there
                if not new_playlist:
                    self.status_lbl.config(text="No valid tracks found in CSV.") # if no valid tracks found in CSV, status will show a message
                else:
                    self.playlist = new_playlist
                    self.update_playlist_display()
                    self.status_lbl.config(text=f"Playlist loaded from {file_path}") # status will show a message if load is successful
        except Exception as e:
            self.status_lbl.config(text=f"Error loading playlist: {e}") # if there is an error, status will show a message

    def add_track(self):
        self.status_lbl.config(text="")
        track_input = self.input_txt.get().strip() # get the input and clean it, avoiding errors
    # Check if input is empty
        if not track_input:
            self.status_lbl.config(text="Please enter a track number.")
            return
    
        # Check if track exists in library
        if track_input in lib.library:
            if track_input not in self.playlist:
                self.playlist.append(track_input)
                self.update_playlist_display()
                self.input_txt.delete(0, END)  # Clear input after successful add
                self.status_lbl.config(text=f"Track {track_input} added to playlist.")
            else:
                self.status_lbl.config(text="Track already in playlist.")
        else:
            self.status_lbl.config(text="Invalid track number.")

    def display_available_tracks(self):
        self.list_txt.config(state="normal")
        self.list_txt.delete("1.0", END) # clear the text area
        # Display all tracks in the library
        for num, track in lib.library.items():
            self.list_txt.insert(END, f"{num}: {track.name} (Played {track.play_count} times)\n")
        self.list_txt.config(state="disabled") # set the text area to read-only

    def update_playlist_display(self):
        self.displayed_track_txt.config(state="normal")
        self.displayed_track_txt.delete("1.0", END)
        # Display the playlist with track numbers and updated play counts
        for i, num in enumerate(self.playlist, start=1): # enumerate starts counting from 1
            track = lib.library[num] # get the track from the library
            name = track.name
            count = track.play_count
            self.displayed_track_txt.insert(END, f"{i}. {name} (Played {count} times)\n")
        self.displayed_track_txt.config(state="disabled")

    def play_playlist(self):
        # If playlist is empty, status will show a message
        if not self.playlist:
            self.status_lbl.config(text="Playlist is empty.")
            return
        self.status_lbl.config(text="Playlist played!")
        # Increment play count for each track in the playlist
        for num in self.playlist: 
            lib.library[num].play_count += 1
        # Update the display of the playlist to show the new play counts
        self.update_playlist_display()
        self.display_available_tracks()

    def reset_playlist(self):
        # Clear the playlist, reset the displayed area, change state to read-only mode and announce the reset
        self.playlist.clear()
        self.displayed_track_txt.config(state="normal")
        self.displayed_track_txt.delete("1.0", END)
        self.displayed_track_txt.config(state="disabled")
        self.status_lbl.config(text="Playlist reset.")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = TrackList()
    fonts.configure()
    app.run()