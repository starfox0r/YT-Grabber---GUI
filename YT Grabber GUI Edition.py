import pytube
import requests
import ssl
import tkinter as tk
from tkinter import ttk

# Disable SSL verification for requests library
requests.packages.urllib3.disable_warnings()
s = requests.Session()
s.verify = False

# Disable SSL verification for pytube
ssl._create_default_https_context = ssl._create_unverified_context

# Define the function to download the selected video stream
def download_video():
    # Get the selected resolution
    selection = resolution_combobox.current()
    selected_stream = streams[selection]

    # Create a YouTube object from the URL
    youtube = pytube.YouTube(url_entry.get())

    # Download the video and audio streams or just the audio
    if download_type_var.get() == 1:
        selected_stream.download()
        status_label.config(text=f"Download complete! Filename: {selected_stream.default_filename}")
    elif download_type_var.get() == 2:
        audio_stream = youtube.streams.get_audio_only()
        audio_stream.download()
        status_label.config(text=f"Download complete! Filename: {audio_stream.default_filename}")





# Define the function to update the available resolutions when the user enters a video URL
def update_resolutions(event=None):
    # Create a YouTube object from the URL
    youtube = pytube.YouTube(url_entry.get())

    # Get the available streams
    global streams
    streams = youtube.streams.filter(progressive=True)

    # Update the resolution combobox
    resolution_combobox.config(values=[stream.resolution for stream in streams])

    # Enable the resolution combobox
    resolution_combobox.config(state="readonly")

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")

# Create the URL entry field
url_label = ttk.Label(window, text="Enter the URL of the video you want to download:")
url_label.grid(row=0, column=0, padx=10, pady=10)
url_entry = ttk.Entry(window, width=40)
url_entry.grid(row=0, column=1, padx=10, pady=10)
url_entry.bind("<Return>", update_resolutions)

# Create the apply URL button
apply_url_button = ttk.Button(window, text="Apply URL", command=update_resolutions)
apply_url_button.grid(row=0, column=2, padx=10, pady=10)

# Create the download type radio buttons
download_type_var = tk.IntVar()
download_type_var.set(1)
download_type_label = ttk.Label(window, text="Select download type:")
download_type_label.grid(row=1, column=0, padx=10, pady=10)
video_radio = ttk.Radiobutton(window, text="Video and audio", variable=download_type_var, value=1)
video_radio.grid(row=1, column=1, padx=10, pady=10)
audio_radio = ttk.Radiobutton(window, text="Audio only", variable=download_type_var, value=2)
audio_radio.grid(row=1, column=2, padx=10, pady=10)

# Create the resolution combobox
resolution_label = ttk.Label(window, text="Select resolution:")
resolution_label.grid(row=2, column=0, padx=10, pady=10)
resolution_combobox = ttk.Combobox(window, state="disabled", width=20)
resolution_combobox.grid(row=2, column=1, padx=10, pady=10)

# Create the download button
download_button = ttk.Button(window, text="Download", command=download_video)
download_button.grid(row=3, column=1, padx=10, pady=10)

# Create the status label
status_label = ttk.Label(window, text="")
status_label.grid(row=4, column=1, padx=10, pady=10)

# Start the main loop
window.mainloop()
