# File_organization_bot

A Python bot that organizes files/folders in a specified path by moving them into categorized folders based on file types, keywords, and date.

#Features

- Classifies files by extension, keyword, and modified date
- Organizes subfolders based on their contents
- Real-time watching with automatic organization on new downloads
- Dry run mode to preview changes before moving anything
- Conflict handling for duplicate filenames
- Full logging to terminal and organizer.log

#Project Structure

file_organization_bot/
- ├── config.py          # Target folder setting
- ├── scanner.py         # Scans and displays folder contents
- ├── classifier.py      # Classification engine (Keywords and File types)
- ├── actions.py         # Movement logic and conflict handling
- ├── logger.py          # Logging to terminal and file
- ├── watcher.py         # Real-time folder watcher
- ├── organizer.log      # Auto-generated log file
- ├── requirements.txt   # Project dependencies
- └── tests/
- ├───── test_classifier.py
- └───── test_actions.py

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Setup

**1. Clone or download the project**

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows
source venv/bin/activate          # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set your target folder in `config.py`:**
```python
TARGET_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
#To move the bot to a different folder on a separate drive, use r'(path)'
#EX TARGET_FOLDER=r'Z:\Games'
```

---

## Usage

**Preview what would be organized (safe - nothing moves):**
```bash
python actions.py
```
Set `dry_run=True` at the bottom of `actions.py`.

**Run a full organization:**
```bash
python actions.py
```
Set `dry_run=False` at the bottom of `actions.py`.

**Start the real-time watcher:**
```bash
python watcher.py
```
Press `Ctrl+C` to stop.

**Run tests:**
```bash
python -m unittest tests.test_classifier -v
python -m unittest tests.test_actions -v
```

---

## Category Folders

| Folder | Contents |
|---|---|
| Apps | .exe, .msi installers |
| Archives | .zip, .rar, .7z |
| Career | Resumes, cover letters, LORs |
| Code | .py, .js, .html, .m, .css |
| Documents | .pdf, .docx, .xlsx, .pptx, .txt |
| Finance | Tax, receipts, credit reports |
| Game Files | .ini, .gi, .dll, game archives |
| Health | Immunization, medical, patient files |
| Images | .jpg, .png, .gif, .bmp, .svg |
| Unsorted files | Unrecognized files sorted by year |

---

## Dependencies
- Python 3.12+
- watchdog==6.0.0

---

## Author
Zy Dowdy
