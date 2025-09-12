import os
import hashlib
import shutil

# ====== Default folder (can be changed here) ======
DEFAULT_FOLDER = r'C:\Users\LENOVO\Desktop\test'
DUPLICATE_FOLDER = "duplicates"  # where to move duplicates if user selects 'move'


def hash_file(path, blocksize=65536):
    """Return SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        buf = f.read(blocksize)
        while buf:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()


def find_duplicates(folder):
    """Find duplicate files by hashing every file (100% accurate), keep oldest file as original."""
    hash_map = {}
    duplicates = []

    for root, _, files in os.walk(folder):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                filesize = os.path.getsize(filepath)
                if filesize == 0:  # skip empty files
                    continue

                filehash = hash_file(filepath)
            except Exception:
                continue

            if filehash in hash_map:
                # Compare creation times to decide which one to keep
                original = hash_map[filehash]
                if os.path.getctime(filepath) < os.path.getctime(original):
                    # current file is older → keep it, mark previous as duplicate
                    duplicates.append((filepath, original))
                    hash_map[filehash] = filepath
                else:
                    # current file is newer → mark it as duplicate
                    duplicates.append((original, filepath))
            else:
                hash_map[filehash] = filepath

    return duplicates


def main():
    # Step 1: Ask for folder path or use default
    choice = input(f"Use default folder '{DEFAULT_FOLDER}'? (y/n): ").strip().lower()
    if choice == "y":
        folder = DEFAULT_FOLDER
    else:
        folder = input("Enter the folder path: ").strip()

    if not os.path.isdir(folder):
        print("❌ Invalid folder path.")
        return

    # Step 2: Ask for action
    print("\nChoose an action:")
    print("1. Report only")
    print("2. Delete duplicates")
    print("3. Move duplicates to 'duplicates/' folder")
    action = input("Enter 1/2/3: ").strip()

    # Step 3: Find duplicates
    duplicates = find_duplicates(folder)

    if not duplicates:
        print("\n✅ No duplicates found.")
        return

    # Save report
    report_file = "duplicates_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        for dup in duplicates:
            f.write(f"{dup[0]} == {dup[1]}\n")

    print(f"\n📄 Found {len(duplicates)} duplicate files.")
    print(f"Report saved to {report_file}\n")

    # Dry run confirmation
    confirm = input("Proceed with the chosen action? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("🔎 Dry run only. No changes made.")
        return

    # Step 4: Execute action
    if action == "2":  # Delete
        for _, dup in duplicates:
            try:
                os.remove(dup)
                print(f"🗑️ Deleted: {dup}")
            except Exception as e:
                print(f"⚠️ Error deleting {dup}: {e}")

    elif action == "3":  # Move
        os.makedirs(DUPLICATE_FOLDER, exist_ok=True)
        for _, dup in duplicates:
            try:
                shutil.move(dup, os.path.join(DUPLICATE_FOLDER, os.path.basename(dup)))
                print(f"📦 Moved: {dup}")
            except Exception as e:
                print(f"⚠️ Error moving {dup}: {e}")

    else:
        print("📊 Report only mode. No files were changed.")

    print("\n✅ Task completed.")


if __name__ == "__main__":
    main()
