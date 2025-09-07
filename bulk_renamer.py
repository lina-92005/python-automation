import os
import datetime
import json

# Folder path to rename files
folder_path = r"C:\Users\LENOVO\Desktop\test"

# Prefix pattern for renamed files
pattern = "File"

# Allowed file types for renaming
allowed_extensions = [".jpg", ".png", ".pdf", ".txt", ".docx", ".mp4", ".zip", ".rar" ,".mp3" ,".psd",".py" ,".mkv" ,".wav"]

# Backup mapping file to store original → renamed filenames
backup_file = os.path.join(folder_path, "name_map.json")
name_map = {}

# Load existing backup map if available
if os.path.exists(backup_file):
    with open(backup_file, "r", encoding="utf-8") as f:
        name_map = json.load(f)

# Get list of files in folder, sorted by last modified date
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))  # chronological order

# Renaming process
for index, filename in enumerate(files, start=1):
    old_path = os.path.join(folder_path, filename)
    ext = os.path.splitext(filename)[1].lower()

    # Only process allowed file types and skip already renamed files
    if ext in allowed_extensions and not filename.startswith(pattern + "_"):
        # Get the file's last modified date
        timestamp = os.path.getmtime(old_path)
        file_date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

        # Build new filename with date and index
        new_name = f"{pattern}_{file_date}_{index}{ext}"
        new_path = os.path.join(folder_path, new_name)

        # Handle potential name collisions
        counter = 1
        while os.path.exists(new_path):
            new_name = f"{pattern}_{file_date}_{index}_{counter}{ext}"
            new_path = os.path.join(folder_path, new_name)
            counter += 1

        # Rename the file and update backup mapping
        os.rename(old_path, new_path)
        name_map[new_name] = filename  # store original → renamed mapping
        print(f"Renamed: {filename} → {new_name}")

# Save backup mapping for potential restoration
with open(backup_file, "w", encoding="utf-8") as f:
    json.dump(name_map, f, indent=4)

print("Renaming finished and backup mapping saved.")
