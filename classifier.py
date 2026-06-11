from datetime import datetime
from collections import Counter

EXTENSION_MAP = {                                                                                   #The dict the classifing for the file types
    # Documents
    '.pdf': 'Documents', '.docx': 'Documents', '.doc': 'Documents',
    '.txt': 'Documents', '.xlsx': 'Documents', '.csv': 'Documents',
    '.pptx': 'Documents',
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
    '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images',
    # Videos
    '.mp4': 'Videos', '.mov': 'Videos', '.avi': 'Videos',
    '.mkv': 'Videos',
    # Audio
    '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
    # Code
    '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code','.m': 'Code', '.ino': 'Code',
    #Apps
    '.exe': 'Apps',  '.jar': 'Archives',
    #Game files
    '.ini': 'Game Files', 'dll': 'Game Files', '.gi':'Game Files', '.dll': 'Game Files'
}

KEYWORD_MAP = {                                                                                     #The dict for keywords in the file name
    'invoice': 'Finance',
    'budget':  'Finance',
    'receipt': 'Finance',
    'trip-receipt': 'Finance',
    'tax':      'Finance',
    'budget':   'Finance',
    'credit': 'Finance',

    'resume':  'Career',
    'cv':      'Career',
    'cover':   'Career',
    'career':     'Career',
    'coverletter': 'Career',
    'lor': 'Career',
    'internship': 'Career',

    'immunization': 'Health',
    'discharge':    'Health',
    'ultrasound':   'Health',
    'medical':      'Health',
    'patient':      'Health',

    'elden':  'Game Files',
    'nioh':   'Game Files',
    'steamrip': 'Game Files',
    'onlinefix': 'Game Files',
}

def classify_file(file_path):
    SKIP_NAMES = ('desktop.ini', 'thumbs.db')

    if file_path.name.lower() in SKIP_NAMES:                                                        #files to skip
        return None
    
    name_sort=file_path.stem.lower()
    ext_sort=file_path.suffix.lower()

    for keyword,category in KEYWORD_MAP.items():                                                    #Sorted by keyword (more specific)
        if keyword in name_sort:
            return category

    if ext_sort in EXTENSION_MAP:                                                                   #Sorted by extension (generalized)
        return EXTENSION_MAP[ext_sort]
        
    year_mod=datetime.fromtimestamp(file_path.stat().st_mtime).year                                 #If the file does not fall into either of these categories sort by year modified
    return (f'Unsorted files/{year_mod}')

def classify_folder(folder_path):
    counts=Counter()

    for item in folder_path.iterdir():
        if item.is_file():
            category=classify_file(item)
            if category:
                top_level_sort=category.split('/')[0]
                counts[top_level_sort] += 1
    
    if counts:
        return counts.most_common(1)[0][0]
    
    name = folder_path.name.lower()
    for keyword, category in KEYWORD_MAP.items():
        if keyword in name:
            return category
        
    CODE_HINTS = ('project','arduino', 'python', 'code')
    GAME_HINTS = ('fix', 'repair', 'steam', 'game')

    if any(hint in name for hint in CODE_HINTS):
        return 'Code'
    if any(hint in name for hint in GAME_HINTS):
        return 'Game Files'

    return 'Unsorted files'

if __name__ == '__main__':                                                                          #test to print the category for every file in downloads
    import config
    from pathlib import Path

    folder=Path(config.TARGET_FOLDER)

    print('\n=====FILES=====')
    for item in folder.iterdir():
        if item.is_file:
            category=classify_file(item)
            print(f'{item.name:50} -> {category}')
    print('\n=====Folders=====')
    for item in folder.iterdir():
        if item.is_dir():
            category=classify_folder(item)
            print(f'{item.name:50} -> {category}')