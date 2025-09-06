import os #interact with the file system (paths, listing files, checking if something is a file/folder).
import shutil # has higher-level operations like moving or copying files.

# Your folder path
folder_path = r"C:\Users\LENOVO\Desktop\test_folder"
other_folder = os.path.join(folder_path, "Other")
# File categories
file_types = {
    "Images": [".jpg", ".png", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3", ".wav"]
}

# Create category folders if not exist
for folder in file_types.keys():
    folder_dir = os.path.join(folder_path, folder)
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)
    if not os.path.exists(other_folder):
        os.makedirs(other_folder)

# Function to safely move files with collision handling
# def safe_move(src_path, dest_folder):
#     base_name = os.path.basename(src_path)
#     target_path = os.path.join(dest_folder, base_name)
#     count = 1
#     # If file exists, add (1), (2), etc.
#     while os.path.exists(target_path):
#         name, ext = os.path.splitext(base_name)
#         target_path = os.path.join(dest_folder, f"{name} ({count}){ext}")
#         count += 1
#     shutil.move(src_path, target_path)
#     return os.path.basename(target_path)

# Organize files
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if os.path.isfile(file_path):
        moved = False
        for folder, extensions in file_types.items():
            if file.lower().endswith(tuple(extensions)):
                target = os.path.join(folder_path, folder, file)
                shutil.move(file_path, target)
                print(f"Moved: {file} → {folder}")
                moved = True
                break
        if not moved:
            shutil.move(file_path, os.path.join(other_folder, file))
            print(f"Moved: {file} → Other")
