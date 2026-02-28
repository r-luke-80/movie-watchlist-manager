import tkinter as tk
from tkinter import ttk

movies = []

# Globals for the watchlist window + table
watch_window = None
tree = None


def load_movies_from_file():
    """Load watchlist.txt into movies (if it exists)."""
    try:
        with open("watchlist.txt", "r") as file:
            movies.clear()
            for line in file:
                line = line.strip()
                if line:
                    movies.append(line)
        return True
    except FileNotFoundError:
        return False


def refresh_table():
    """Refresh the Treeview if the watchlist window is open."""
    global tree, watch_window
    if watch_window is None or not watch_window.winfo_exists() or tree is None:
        return

    tree.delete(*tree.get_children())
    for i, m in enumerate(movies):
        if "|" in m:
            title, genre = m.split("|", 1)
            tree.insert(
                "",
                tk.END,
                values=(title, genre),
                tags=("evenrow",) if i % 2 == 0 else ("oddrow",)
            )


def add_movie():
    title = title_entry.get().strip()
    genre = genre_var.get().strip()

    if title == "" or genre == "":
        status_label.config(text="Please fill in both fields.")
        return

    movies.append(f"{title}|{genre}")
    status_label.config(text="Movie added!")
    title_entry.delete(0, tk.END)

    # If watchlist is open, update it immediately
    refresh_table()


def open_watchlist():
    global watch_window, tree

    # If already open, bring to front and refresh
    if watch_window is not None and watch_window.winfo_exists():
        watch_window.lift()
        refresh_table()
        return

    watch_window = tk.Toplevel(root)
    watch_window.title("Watchlist")
    watch_window.geometry("800x900")

    def on_close():
        global watch_window, tree
        tree = None
        watch_window.destroy()
        watch_window = None

    watch_window.protocol("WM_DELETE_WINDOW", on_close)

    top_frame = tk.Frame(watch_window)
    top_frame.pack(fill="x")

    bottom_frame = tk.Frame(watch_window)
    bottom_frame.pack(fill="both", expand=True)

    banner = tk.PhotoImage(file="MovieWatchlistManager/moviecollage.png")
    banner_label = tk.Label(top_frame, image=banner)
    banner_label.image = banner
    banner_label.pack(padx=10, pady=(10, 0))

    tk.Label(top_frame, text="My Watchlist", font=("Arial", 18, "bold")).pack(pady=10)

    # Treeview
    columns = ("title", "genre")
    tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
    tree.heading("title", text="Title")
    tree.heading("genre", text="Genre")

    tree.column("title", width=500, anchor="w")
    tree.column("genre", width=200, anchor="center")

    tree.tag_configure("evenrow", background="#e6f2ff")
    tree.tag_configure("oddrow", background="#ffffff")

    scrollbar = ttk.Scrollbar(bottom_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(padx=15, pady=10, fill="both", expand=True)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            return

        for item_id in selected:
            title, genre = tree.item(item_id, "values")
            record = f"{title}|{genre}"
            if record in movies:
                movies.remove(record)

        refresh_table()

    def clear_list():
        movies.clear()
        refresh_table()

    btn_frame = tk.Frame(bottom_frame)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Delete Selected", command=delete_selected, width=16).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="Clear List", command=clear_list, width=16).grid(row=0, column=1, padx=8)
    tk.Button(btn_frame, text="Back", command=on_close, width=16).grid(row=0, column=2, padx=8)

    refresh_table()


def watchlist_button():
    # If nothing in memory, try loading from file first
    if not movies:
        load_movies_from_file()
    open_watchlist()


def save_watchlist():
    with open("watchlist.txt", "w") as file:
        for movie in movies:
            file.write(movie + "\n")
    status_label.config(text="Saved to file!")


# MAIN WINDOW
root = tk.Tk()
root.title("Movie Watchlist Manager")

tk.Label(root, text="Movie Title").pack()
title_entry = tk.Entry(root)
title_entry.pack()

tk.Label(root, text="Genre").pack()
genre_var = tk.StringVar(value="Action / Adventure")

genre_options = [
    "Action / Adventure", "Comedy", "Drama", "Horror", "Giallo",
    "Sci-Fi", "Fantasy", "Thriller", "Documentary", "Animation", "Romance"
]
tk.OptionMenu(root, genre_var, *genre_options).pack()

photo = tk.PhotoImage(file="MovieWatchlistManager/movie.png")
image_label = tk.Label(root, image=photo)
image_label.image = photo
image_label.pack()

tk.Button(root, text="Add Movie", command=add_movie).pack()
tk.Button(root, text="Watchlist", command=watchlist_button).pack()
tk.Button(root, text="Save Watchlist", command=save_watchlist).pack()
tk.Button(root, text="Exit", command=root.quit).pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()