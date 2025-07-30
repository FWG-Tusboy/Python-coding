from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import track_library as lib
import font_manager as fonts

def set_text(text_area, content):
    text_area.delete("1.0", tk.END) # clear the text area
    text_area.insert("1.0", content) # set the content

class UpdateTracks:
    def __init__(self, parent=None):
        if parent is not None:
            self.window = Toplevel(parent)
        else:
            self.window = Tk()
        self.window.geometry("700x300")
        self.window.title("Update Tracks")

        # Track Number input
        lbl_track_number = Label(self.window, text="Track Number:")
        lbl_track_number.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.track_input = tk.Entry(self.window, width=10)
        self.track_input.grid(row=0, column=1, padx=5, pady=5, sticky="W")

        # New Rating input
        lbl_new_rating = Label(self.window, text="New Rating (1-5):")
        lbl_new_rating.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.rating_input = tk.Entry(self.window, width=10)
        self.rating_input.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        # Update Track button
        update_btn = tk.Button(self.window, text="Update Track", command=self.update_track)
        update_btn.grid(row=0, column=2, padx=5, pady=5, sticky="W")

        # ScrolledText widget to display the list of tracks (always visible)
        lbl_available_tracks = Label(self.window, text="Available Tracks: ")
        lbl_available_tracks.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.list_txt = tkst.ScrolledText(self.window, width=50, height=8, wrap="none",
                                          selectbackground="#0078d4", selectforeground="white")
        self.list_txt.grid(row=3, column=1, columnspan=3, sticky="W", padx=5, pady=5)
        self.display_all_tracks()

        # Status label
        self.status_lbl = tk.Label(self.window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="W")

    def display_all_tracks(self):
        # Display all tracks in the library
        self.list_txt.config(state="normal")
        track_list = lib.list_all()
        set_text(self.list_txt, track_list)
        self.list_txt.config(state="disabled")

    def update_track(self):
        # Update the track rating based on user input of track key number
        track_key = self.track_input.get().strip()
        new_rating = self.rating_input.get().strip()

        # Check if track_key and new_rating are digits
        if not track_key.isdigit() or not new_rating.isdigit():
            # if not digits, clear the input fields and show an error message
            self.track_input.delete(0, tk.END)
            self.rating_input.delete(0, tk.END)
            self.status_lbl.config(text="Please enter valid digit for both track number and rating.")
            return

        if not track_key or not new_rating:
            # if not input is put in completely, status will remind for user to input in both fields
            self.status_lbl.config(text="Please enter both track number and new rating.")
            return

        # Check if the track exists in the library, if not show an message
        name = lib.get_name(track_key)
        if name is None:
            self.status_lbl.config(text=f"Track {track_key} not found in the library.")
            return

        # Check if the rating is valid by using try-except, if not valid, show an error message
        try:
            rating_value = int(new_rating)
            if rating_value < 1 or rating_value > 5:
                self.status_lbl.config(text="Rating must be between 1 and 5.")
                return
        # If valid, set the rating
        except ValueError:
            self.status_lbl.config(text="Rating must be a number between 1 and 5.")
            return

        # Set the new rating for the track
        lib.set_rating(track_key, rating_value)
        self.display_all_tracks()
        # Show a success message
        self.status_lbl.config(
            text=f"Rating has been changed at {track_key} ({name})"
        )
        # Clear the input fields after the update
        self.track_input.delete(0, tk.END)
        self.rating_input.delete(0, tk.END)

    def run(self):
        self.window.mainloop()
if __name__ == "__main__":
    app = UpdateTracks
    fonts.configure()
    app()