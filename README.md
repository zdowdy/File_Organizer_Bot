# File Organizer Bot

A Python bot that automatically organizes files and folders in a specified directory by moving them into categorized folders based on file type, keywords, and modified date. Includes real-time watching, weekly email reports, and full Windows automation via Task Scheduler.

---

## Features

- Classifies files by extension, keyword, and modified date
- Organizes subfolders based on their contents
- Real-time watching with automatic organization on new downloads
- Dry run mode to safely preview changes before moving anything
- Conflict handling for duplicate filenames
- Weekly email report summarizing moves and errors
- Full logging to terminal and `organizer.log`
- Fully automated via Windows Task Scheduler

---

## Project Structure
file_organization_bot/
├── config.py               # Target folder setting
├── scanner.py              # Scans and displays folder contents
├── classifier.py           # Classification engine (keywords and file types)
├── actions.py              # Move logic and conflict handling
├── logger.py               # Logging to terminal and file
├── watcher.py              # Real-time folder watcher
├── email_alerts.py         # Weekly email report
├── run_watcher.bat         # Bat file for Task Scheduler automation
├── run_actions.bat         # Bat file for Task Scheduler automation
├── requirements.txt        # Project dependencies
└── tests/
├── test_classifier.py
└── test_actions.py

---

## Setup

**1. Clone the repository:**
```bash
git clone https://github.com/zdowdy/file_organizer_bot.git
cd file_organizer_bot
```

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
# Default - uses your system Downloads folder
TARGET_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# To target a folder on a separate drive use a raw string
TARGET_FOLDER = r"Z:\Games"
```

**5. Set up email alerts (optional):**

Create a `.env` file in the project root:
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your@gmail.com

> **Note:** Gmail requires an [App Password](https://myaccount.google.com/apppasswords) — do not use your regular Gmail password. Never commit your `.env` file to GitHub.

---

## Usage

**Preview what would be organized — nothing moves:**
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

> **Note:** `Ctrl+C` only works when running `watcher.py` manually in a terminal. When running via Task Scheduler use `pythonw.exe` (see Automation section) — to stop it right-click the task in Task Scheduler and select **End**, or kill `pythonw.exe` in Task Manager.

**Send a weekly email report manually:**
```bash
python email_alerts.py
```

**Run tests:**
```bash
python -m unittest tests.test_classifier -v
python -m unittest tests.test_actions -v
```

---

## Automation (Windows Task Scheduler)

The bot runs fully automatically using Windows Task Scheduler:

| Task | Trigger | Script |
|---|---|---|
| Real-time watcher | At log on | `run_watcher.bat` |
| Weekly folder organization | Weekly (e.g. Monday 8:30 AM) | `run_actions.bat` |
| Weekly email report | Weekly (e.g. Monday 9:00 AM) | `email_alerts.py` |

### Task Scheduler Settings
For the watcher task set the following under Properties:

**General tab:**
- Run only when user is logged on
- Leave **Run with highest privileges unchecked** — enabling it causes the task to fail by running in a different security context that cannot access user profile paths

**Trigger:**
- Set to At log on — not At startup, which runs before Python is accessible

**Action tab:**

Point Task Scheduler directly at your venv Python executable for all three tasks:

**Watcher Task:**
| Field | Value |
|---|---|
| Program/script | `C:\path\to\your\venv\Scripts\pythonw.exe` |
| Add arguments | `watcher.py` |
| Start in | `C:\path\to\your\project\file_organization_bot` |

**Actions Task:**
| Field | Value |
|---|---|
| Program/script | `C:\path\to\your\venv\Scripts\python.exe` |
| Add arguments | `run_actions.bat` |
| Start in | `C:\path\to\your\project\file_organization_bot` |

**Email Alerts Task:**
| Field | Value |
|---|---|
| Program/script | `C:\path\to\your\venv\Scripts\python.exe` |
| Add arguments | `email_alerts.py` |
| Start in | `C:\path\to\your\project\file_organization_bot` |

> **`python.exe` vs `pythonw.exe`:**
> - Use `pythonw.exe` for the watcher — runs silently in the background with no console window, no Ctrl+C required
> - Use `python.exe` for actions and email tasks — they run, complete, and exit on their own so no console suppression is needed
> - To stop a `pythonw.exe` task: right-click it in Task Scheduler → **End**, or kill `pythonw.exe` in Task Manager

**Settings tab:**
- Allow task to run on demand
- Restart every 1 minute, up to 3 times
- Uncheck "Stop the task if it runs longer than"

---

## Category Folders

| Folder | Contents |
|---|---|
| Apps | `.exe`, `.msi` installers |
| Archives | `.zip`, `.rar`, `.7z` |
| Career | Resumes, cover letters, letters of recommendation |
| Code | `.py`, `.js`, `.html`, `.m`, `.css` |
| Documents | `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt` |
| Finance | Tax documents, receipts, credit reports |
| Game Files | `.ini`, `.gi`, `.dll`, game archives |
| Health | Immunization records, medical documents |
| Images | `.jpg`, `.png`, `.gif`, `.bmp`, `.svg` |
| Unsorted files | Unrecognized files sorted by year modified |

---

## How Classification Works

Files are classified using three rules checked in this order:

1. **Keyword match** — filename contains words like `resume`, `tax`, `immunization`
2. **Extension match** — file type maps to a category (`.pdf` → Documents)
3. **Date fallback** — unrecognized files are sorted into `Unsorted files/YEAR`

Keywords are checked before extensions so that a file like `resume.pdf` correctly routes to `Career` instead of `Documents`.

---

## Dependencies

- Python 3.12+
- `watchdog==6.0.0`
- `python-dotenv==1.2.2`

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Author

Zy Dowdy