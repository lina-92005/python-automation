
from pathlib import Path

p = Path(r'C:\Users\LENOVO\Desktop\test_folder')
(p / "photo1.jpg").write_text("duplicate file")  # creates a second photo1.jpg
