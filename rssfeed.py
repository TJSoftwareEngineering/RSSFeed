import feedparser
import tkinter as tk
from tkinter import font
import webbrowser
import os

# Read RSS URLs from txt
def read_feed_urls(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    else:
        return []

# Save URLs to file
def save_feed_urls(file_path, feed_urls):
    with open(file_path, 'w') as file:
        file.write('\n'.join(feed_urls))

# Update feed list
def update_feed_list():
    feed_list.delete(0, tk.END)
    feed_urls = read_feed_urls('rss_feeds.txt')
    for url in feed_urls:
        feed_list.insert(tk.END, url)

# Fetch and display
def fetch_feed():
    feed_entries.config(state=tk.NORMAL) 
    feed_entries.delete(1.0, tk.END)

    feed_urls = read_feed_urls('rss_feeds.txt')

    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            feed_entries.insert(tk.END, title + '\n', ('title',))
            feed_entries.insert(tk.END, f"Link: {link}\n\n", ('link',))

    feed_entries.config(state=tk.DISABLED)

# Add RSS URL
def add_feed_url():
    new_url = feed_url_entry.get()
    if new_url:
        feed_urls = read_feed_urls('rss_feeds.txt')
        feed_urls.append(new_url)
        save_feed_urls('rss_feeds.txt', feed_urls)
        feed_url_entry.delete(0, tk.END)
        update_feed_list()

def open_link(event):
    selected_text = feed_entries.tag_prevrange('link', feed_entries.index(tk.SEL_FIRST))
    if selected_text:
        link = feed_entries.get(selected_text[0], selected_text[1])
        webbrowser.open(link)

# Create main window
window = tk.Tk()
window.title("RSS Feed Reader")

text_font = font.nametofont("TkDefaultFont")
text_font.configure(size=12)

# Listbox for feed URLs
feed_list = tk.Listbox(window, selectmode=tk.SINGLE)
feed_list.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
feed_list.bind("<ButtonRelease-1>", fetch_feed)  # Fetch the selected feed on click

# Scrollbar
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
feed_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=feed_list.yview)

# Input field
feed_url_entry = tk.Entry(window, font=text_font)
feed_url_entry.pack(fill=tk.BOTH, padx=10, pady=10)

# Add button
add_feed_button = tk.Button(window, text="Add Feed", command=add_feed_url)
add_feed_button.pack(fill=tk.BOTH)

# Fetch button
fetch_button = tk.Button(window, text="Fetch Feed", command=fetch_feed)
fetch_button.pack(fill=tk.BOTH)

# Display feed entries
feed_entries = tk.Text(window, wrap=tk.WORD, font=text_font)
feed_entries.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create tags for formatting
feed_entries.tag_configure('title', font=text_font, underline=1)
feed_entries.tag_configure('link', font=text_font, foreground='blue')
feed_entries.tag_bind('link', '<Button-1>', open_link)

# Update feed
update_feed_list()

# Run GUI
window.mainloop()
