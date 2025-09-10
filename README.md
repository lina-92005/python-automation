# Python Automation
20-day Python automation journey (file handling, automation scripts, freelancing-ready projects).

## Day 1: File Creation and Organizer
**Scripts:**  
- `creat empty files.py`  
- `organize_files.py`  
- `organizer_dryrun.py`  

**Features:**  
- Creates empty files for testing.  
- Organizes files into folders by type (images, documents, videos, etc.).  
- Includes a dry-run version to preview changes safely.

---

## Day 2: Date-Based Bulk File Renamer
**Script:**  
- `bulk_renamer.py`  

**Features:**  
- Renames files based on last modified date.  
- Adds sequential numbering to prevent collisions.  
- Supports multiple file types.  
- Saves a backup mapping (`name_map.json`) for easy restoration.
## Day 3: File Organizer (Automation Tool)
**Script:**
- `file_organizer.py`

**Features:**
- Scans a folder and organizes files into categories (images, documents, videos, music, others).
- Handles duplicate filenames with smart renaming (no overwrites).
- Easy to customize file categories.
- Provides clear logs for each moved file.
## Day 4: Web Scraper → Save to CSV/Excel
**Script:**
- `WebScraper.py`

**Features:**
- Scrapes quotes, authors, and tags from http://quotes.toscrape.com (or any website via URL change).
- Supports scraping all pages or a custom number of pages or quotes.
- Optionally shows a live progress bar while scraping.
- Saves results into CSV and Excel files (quotes_final.csv / quotes_final_progress.xlsx).
- Includes a small helper to preview the first 10 quotes directly in Python.

## Day 5: PDF Automation Master Script
**Script:**
- `pdf_automation.py`

**Features:**
- Extract Text → Converts PDF content into a .txt file (per page text extraction).
- Merge PDFs → Supports two modes:
    Manual → Select specific PDF files in a custom order.
    Folder → Merge all PDFs inside a folder automatically.
- Extract Tables → Detects tables in a PDF and exports them into an Excel file, with each table saved on a separate sheet.
- Flexible Menu → Choose to run one, two, or all tasks in a single execution.
- Simple & Interactive → User-friendly menu prompts guide you step by step.
