import tkinter as tk
import tkinter.scrolledtext as tkst


import track_library as lib
import font_manager as fonts


def set_text(text_area, content):
    text_area.delete("1.0", tk.END) # Clear the text area
    text_area.insert(1.0, content) # Insert new content at the beginning (1.0 means start at the first line, first character)


class TrackViewer():
    def __init__(self, window):
        window.geometry("750x350") # Set the window as a 750x350
        window.title("View Tracks") # Set the title of the window as "View Tracks"

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked) # Button to list all tracks
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10) # Align the button to a specific row and column

        enter_lbl = tk.Label(window, text="Enter Track Number") # Label for track number input
        enter_lbl.grid(row=0, column=1, padx=10, pady=10) # Align the label to a specific row and column

        self.input_txt = tk.Entry(window, width=3) # Entry field for track number input
        self.input_txt.grid(row=0, column=2, padx=10, pady=10) # Align the entry to a specific row and column

        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked) # Button to view specific track details
        check_track_btn.grid(row=0, column=3, padx=10, pady=10) # Align the button to a specific row and column

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none") # ScrolledText widget to display the list of tracks
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10) # Align the scrolledtext to a specific row, column and columnspan

        self.track_txt = tk.Text(window, width=24, height=4, wrap="none") # Text widget to display details of a specific track
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10) # Align the text to a specific row and column

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10)) # Label to display status messages
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10) # Align the label to a specific row, column and columnspan

        self.list_tracks_clicked() # Call to list all tracks initially

    def view_tracks_clicked(self):
        key = self.input_txt.get() # Get the track number from the input field
        name = lib.get_name(key) # Retrieve the track name using the key
        if name is not None: # Check if the track exists ( not None = existed track )
            artist = lib.get_artist(key) # Retrieve the artist name using the key
            rating = lib.get_rating(key) # Retrieve the rating using the key
            play_count = lib.get_play_count(key) # Retrieve the play count using the key
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}" # Format the track details
            set_text(self.track_txt, track_details) # Put the contents in order
        else:
            set_text(self.track_txt, f"Track {key} not found") # If track not found, display a message
        self.status_lbl.configure(text="View Track button was clicked!") # Update status label

    def list_tracks_clicked(self):
        track_list = lib.list_all() # Get the list of all tracks from the library
        set_text(self.list_txt, track_list) # Set the text in the list text area
        self.status_lbl.configure(text="List Tracks button was clicked!") # Configure the status to the text 

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    TrackViewer(window)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
