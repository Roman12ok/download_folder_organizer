import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sources_dir = "/Users/romanenglishahmadu/Downloads/"

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

app_extensions = [".dmg", ".exe"]

# Define a dictionary to map file extensions to categories
categories = {
    'Images': image_extensions,
    'Videos': video_extensions,
    'Audios': audio_extensions,
    'Documents': document_extensions,
    'App': app_extensions
}

# Create folders if they don't exist
for category in categories.keys():
    folder_path = os.path.join(sources_dir, category)
    os.makedirs(folder_path, exist_ok=True)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        # Wait a moment to ensure the file is fully written
        time.sleep(1)
        # Call your organizing logic here
        self.organize_files()

    def organize_files(self):
        with os.scandir(sources_dir) as entries:
            for entry in entries:
                if entry.is_file() and not entry.name.startswith('.'):  # Skip system files
                    # Get file extension
                    _, file_extension = os.path.splitext(entry.name)

                    # Find category for the file
                    file_category = next((category for category, extensions in categories.items() if file_extension.lower() in extensions), 'Other')

                    # Construct the destination path
                    dest_path = os.path.join(sources_dir, file_category, entry.name)

                    # Move the file to the appropriate folder
                    shutil.move(entry.path, dest_path)

                    print(f"Moved {entry.name} to {file_category} folder")

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=sources_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    

