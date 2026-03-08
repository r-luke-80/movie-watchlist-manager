# Author: Russ Lukaszewski
# Program: My Movie Watchlist
# Course: SDEV 140
# Assignment: Final Project
# Date: March 5, 2026
#
# GUI program for managing a personal movie watchlist using
# Tkinter. Movies can be added, viewed in a table, deleted,
# cleared, and saved to a file.

# Github Repository:
# https://gitbuh.com/r-luke-80/movie-watchlist-manager 

import tkinter as tk
from tkinter import ttk

# Store movie entries in memory as strings formatted like "Title|Genre" 
movies = []

# Reference to the watchlist window when it is open
watch_window = None

# Reference to the Treeview table used in the watchlist window
tree = None


def load_movies_from_file():
    """Load watchlist.txt into the movies list if the file exists."""
    try:
        # Open the saved watchlist file for reading
        with open("watchlist.txt", "r") as file:
            # Clear the current in-memory list before loading saved data
            movies.clear()
            
            # Read each line from the file
            for line in file:
                line = line.strip()

                # Only add non-empty lines to the movies list
                if line:
                    movies.append(line)
                    
        # Return True if the file was loaded successfully
        return True
    except FileNotFoundError:
        # Return False if the file does not exit yet
        return False


def refresh_table():
    """Refresh the Treeview table with the current movies list if the watchlist is open."""
    global tree, watch_window

    # Stop if the watchlist window or Treeview does not currently exist
    if watch_window is None or not watch_window.winfo_exists() or tree is None:
        return
    
    # Remove all current rows from the Treeview before rebuilding the table
    tree.delete(*tree.get_children())

    # Loop through each movie in the movies list
    for i, m in enumerate(movies):

        # Make sure the store movie string contains the separator (|)
        if "|" in m:
            # Split the movie string into title and genre
            title, genre = m.split("|", 1)

            # Insert the movie into the table with alternating row colors
            tree.insert(
                "",
                tk.END,
                values=(title, genre),
                tags=("evenrow",) if i % 2 == 0 else ("oddrow",)
            )


def add_movie():
    """Add a movie title and genre to the watchlist."""
    # Get the movie title from the Entry widget and remove extra spaces
    title = title_entry.get().strip()

    # Get the selected genre from the dropdown menu
    genre = genre_var.get().strip()

    # Validation: both field must contain data
    if title == "" or genre == "":
        status_label.config(text="Please fill in both fields.")
        return
    
    # Add the movie to the in-memory list using "Title|Genre" format
    movies.append(f"{title}|{genre}")

    # Show a confirmation message to the user letting them it worked
    status_label.config(text="Movie added!")

    # Clear the title entry box for the next movie
    title_entry.delete(0, tk.END)

    # If watchlist is open, update it immediately
    refresh_table()


def open_watchlist():
    """Open the watchlist window and display all movies in a table."""
    global watch_window, tree

    # If the watchlist is already open, show it and refesh the table
    if watch_window is not None and watch_window.winfo_exists():
        watch_window.lift()
        refresh_table()
        return

    # Creates a second window separate from the main window.
    watch_window = tk.Toplevel(root)
    watch_window.title("Watchlist")
    watch_window.geometry("800x900")

    def on_close():
        """Close the watchlist window and reset related variables."""
        global watch_window, tree

        # Reset the Treeview reference
        tree = None

        # Close the watchlist window
        watch_window.destroy()

        # Reset the watchlist window reference
        watch_window = None
    
    # If the user clicks the window's X button, run the on_close() function
    watch_window.protocol("WM_DELETE_WINDOW", on_close)

    #Create a frame for the banner image and heading
    top_frame = tk.Frame(watch_window)
    top_frame.pack(fill="x")

    # Create a frame for the table, scrollbar, and buttons
    bottom_frame = tk.Frame(watch_window)
    bottom_frame.pack(fill="both", expand=True)

    # Load and display the banner image in the top frame
    banner = tk.PhotoImage(file="moviecollage.png")
    banner_label = tk.Label(top_frame, image=banner)
    banner_label.image = banner
    banner_label.pack(padx=10, pady=(10, 0))

    # Display the main heading for the watchlist window
    tk.Label(top_frame, text="My Watchlist", font=("Arial", 18, "bold")).pack(pady=10)

    # Create the columns for the Treeview table
    columns = ("title", "genre")

    # Create the Treeview widget to display the watchlist as a table
    tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")

    # Create the column headings shown at the top of the table
    tree.heading("title", text="Title")
    tree.heading("genre", text="Genre")

    # Set the width and alignment of each column
    tree.column("title", width=500, anchor="w")
    tree.column("genre", width=200, anchor="center")

    # Creates alternating row colors for a zebra striping effect
    tree.tag_configure("evenrow", background="#e6f2ff")
    tree.tag_configure("oddrow", background="#ffffff")

    # Create a vertical scrollbar for the Treeview table
    scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=tree.yview)

    # Link the scrollbar to the Treeview table
    tree.configure(yscrollcommand=scrollbar.set)

    # Places the scrollbar on the right side 
    scrollbar.pack(side="right", fill="y")

    # Places the Treeview table in the window
    tree.pack(padx=15, pady=10, fill="both", expand=True)

    def delete_selected():
        """Remove the selected movie entry from the watchlist."""
        # Get the currently selected row(s)
        selected = tree.selection()

        # Stop if there is nothing selected
        if not selected:
            return
        
        # Remove each selected movie from the movies list
        for item_id in selected:
            title, genre = tree.item(item_id, "values")
            record = f"{title}|{genre}"

            if record in movies:
                movies.remove(record)
        
        # Refresh the table after deletion
        refresh_table()

    def clear_list():
        """Remove all movies from the watchlist and refresh the table."""
        # Remove all tables from the in-memory list
        movies.clear()

        # Refresh the table so it looks empty
        refresh_table()

    #Create a frame to organize the watchlist buttons
    btn_frame = tk.Frame(bottom_frame)
    btn_frame.pack(pady=10)

    # Create the buttons used to manage the watchlist
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected, width=16).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="Clear List", command=clear_list, width=16).grid(row=0, column=1, padx=8)
    tk.Button(btn_frame, text="Back", command=on_close, width=16).grid(row=0, column=2, padx=8)

    # Fill the Treeview table with the current movies when the window opens
    refresh_table()


def watchlist_button():
    """Open the watchlist window when the Watchlist button is clicked."""
    open_watchlist()    


def save_watchlist():
    """Save the current movies list to watchlist.txt and display a confirmation message."""
    # Open watchlist.txt in write mode; create it if does not exist
    with open("watchlist.txt", "w") as file:

        # Write each movie entry to the file on its own line
        for movie in movies:
            file.write(movie + "\n")

    # Show a confirmation message after saving the watchlist
    status_label.config(text="Saved to file!")


# Create the main window
root = tk.Tk()
root.title("My Movie Watchlist")

# Load previously saved movies when the program starts
load_movies_from_file()

# Label for the movie title entry field
tk.Label(root, text="Movie Title").pack()

# Entry widget for typing a movie title
title_entry = tk.Entry(root)
title_entry.pack()

# Label for the genre dropdown menu
tk.Label(root, text="Genre").pack()

# Default genre shown in the dropdown menu when the program starts
genre_var = tk.StringVar(value="Action / Adventure")

# List of genre choices displayed in the dropdown menu
genre_options = [
    "Action / Adventure", "Comedy", "Drama", "Crime Drama", "Horror", "Giallo",
    "Sci-Fi", "Fantasy", "Thriller", "Documentary", "Animation", "Romance"
]

# Dropdown menu used to select a movie genre
tk.OptionMenu(root, genre_var, *genre_options).pack()

# Loads and displays the main window picture
photo = tk.PhotoImage(file="movie.png")
image_label = tk.Label(root, image=photo)
image_label.image = photo
image_label.pack()

# Buttons for adding, viewing, saving, and exiting the program
tk.Button(root, text="Add Movie", command=add_movie).pack()
tk.Button(root, text="Watchlist", command=watchlist_button).pack()
tk.Button(root, text="Save Watchlist", command=save_watchlist).pack()
tk.Button(root, text="Exit", command=root.quit).pack()

# Label used to display status and validation messages 
status_label = tk.Label(root, text="")
status_label.pack()

# Starts the GUI so the window stays open and responsive
root.mainloop()