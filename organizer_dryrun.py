import os

# Your folder path
folder_path = r"C:\Users\LENOVO\Desktop\test"

# File categories
file_types = {
    "Images": [".jpg", ".png", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3", ".wav"]
}

# Dry-run check
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    if os.path.isfile(file_path):
        for folder, extensions in file_types.items():
            if file.lower().endswith(tuple(extensions)):
                print(f"Would move: {file} → {folder}")
                break
        else:
            print(f"No category for: {file} → stays in test_folder")
