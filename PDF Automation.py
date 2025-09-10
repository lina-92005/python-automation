"""
PDF Automation Master Script - Day 5
Features:
1. Extract text from PDFs
2. Merge PDFs (manual or folder)
3. Extract tables into Excel
4. Combine freely (choose multiple options)
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfMerger
import tabula
import pandas as pd
import os

# ---------------- Functions ---------------- #

def extract_text():
    pdf_path = input("Enter PDF path for text extraction: ").strip('"')
    output_txt = Path(pdf_path).with_suffix(".txt")

    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

    with open(output_txt, "w", encoding="utf-8") as out:
        out.write(text)

    print(f"✅ Text extracted to {output_txt}")


def merge_pdfs():
    choice = input("Do you want manual merge or folder merge? (m/f): ").lower()
    merger = PdfMerger()

    if choice == "m":
        files = input("Enter PDF file paths separated by space: ").split()
        for pdf in files:
            merger.append(pdf.strip('"'))
    elif choice == "f":
        folder = input("Enter folder path: ").strip('"')
        for pdf in sorted(Path(folder).glob("*.pdf")):
            merger.append(str(pdf))

    output_file = input("Enter output PDF file path: ").strip('"')
    merger.write(output_file)
    merger.close()
    print(f"✅ PDFs merged into {output_file}")


def extract_tables():
    pdf_path = input("Enter PDF path for table extraction: ").strip('"')
    output_excel = Path(pdf_path).with_suffix(".xlsx")

    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

    with pd.ExcelWriter(output_excel) as writer:
        for i, table in enumerate(tables):
            table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)

    print(f"✅ {len(tables)} tables extracted to {output_excel}")


# ---------------- Menu ---------------- #

print("\n📌 PDF Automation Master Script - Choose what you want to do")
print("1. Extract text")
print("2. Merge PDFs")
print("3. Extract tables")
print("4. All")

choices = input("👉 Enter your choices (e.g., 1 3): ").split()

if "4" in choices:
    extract_text()
    merge_pdfs()
    extract_tables()
else:
    if "1" in choices: extract_text()
    if "2" in choices: merge_pdfs()
    if "3" in choices: extract_tables()

print("\n🎉 All selected tasks are complete!")
