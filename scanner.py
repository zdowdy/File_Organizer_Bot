from pathlib import Path
from datetime import datetime
import config

def folder_scan(folder_path):
    folder=Path(folder_path)
    if not folder.exists():
        print(f'{folder_path} not found')
        return
    print(f'\nScanning {folder_path}\n{'='*50}')

    for item in folder.iterdir():                                  #This for loop finds the files in the folder and pulls info on them using item.stat then prints info
        if item.is_file():
            mod_time=datetime.fromtimestamp(item.stat().st_mtime)  
            print(f'Name: {item.name}')
            print(f'   File Type   : {item.suffix or 'None'}')
            print(f'   Modified on : {mod_time.strftime("%m-%d-%Y")}\n')

if __name__ == '__main__':
    folder_scan(config.TARGET_FOLDER)                               #Pulls TARGET_FOLDER as the folder_path
