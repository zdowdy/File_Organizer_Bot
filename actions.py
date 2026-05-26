import shutil
from pathlib import Path
from classifier import classify_file, classify_folder
from logger import log_move, log_skip, log_error

def organize_file(file_path, target_folder, dry_run=True):
    category = classify_file(file_path)
    
    if category is None:                                         #Skips temp Files
        return
    
    destination_folder=Path(target_folder) / category            #Pathlib has a feature called operator overloading where '/' is used to join the path with the next part
    destination=destination_folder / file_path.name

    if destination.exists():                                     #Checks if a file with the same name exists and if it does assigns it the the handle_conflict function
        destination=handle_conflict(destination)

    if dry_run:                                                  #A preview to see what would happen w/o moving anything while dry_run=True
        print(f'[DRY RUN] Would move:')
        print(f'   FROM: {file_path}')
        print(f'   TO  : {destination}\n')
    else:
        try:
            destination_folder.mkdir(parents=True, exist_ok=True)    #Creates new folder if category does not already exist
            shutil.move(str(file_path), str(destination))            #This line is what acctualy moves the file to the destination folder
            print(f'[MOVED] {file_path.name}')
            print(f'   TO : {destination}\n')
            log_move(file_path, destination)                         #Logs the movement of files in organize.log
        except PermissionError as e:
            log_error(file_path, f'Permission denied - {e}')
        except Exception as e:
            log_error(file_path, e)

def organize_subfolders(target_folder, dry_run=True):            #Organizes the folders in the downloads folder
    folder=Path(target_folder)
    subfolders=[item for item in folder.iterdir() if item.is_dir()]

    SKIP_FOLDERS={                                               #subfolders that are already organized 
        'Documents', 'Images', 'Videos', 'Audio', 'Archives',
        'Apps', 'Code', 'Game Files', 'Career', 'Finance',
        'Health', 'Unsorted files'
    }
                                                                 #headers
    print(f'\nFound {len(subfolders)} subfolders in {target_folder}')                                   
    print(f'Mode: {"DRY RUN - no folders will be moved" if dry_run else "LIVE - folders will be moved"}\n')
    print('=' * 50)

    for subfolder in subfolders:
        if subfolder.name in SKIP_FOLDERS:                       #Skips folders that are organized
            continue

        category = classify_folder(subfolder)                    #Setting destination path
        destination_folder = folder / category
        destination = destination_folder /subfolder.name
        
        if destination.exists():                          #Passes destinatuion to handle confilict
            destination=handle_conflict(destination)
        
        if dry_run:                                              #A preview to see what would happen w/o moving anything while dry_run=True
            print(f'[DRY RUN] Would move folder:')
            print(f'   FROM: {subfolder}')
            print(f'   TO  : {destination}\n')
        else:
            try:
                destination_folder.mkdir(parents=True, exist_ok=True)#Creates new folder if category does not already exist
                shutil.move(str(subfolder), str(destination))        #This line is what moves the subfolder to the destination folder
                print(f'[MOVED FOLDER] {subfolder.name}')
                print(f'   TO : {destination}\n')
                log_move(subfolder, destination)                     #Logs the movement of files in organize.log
            except PermissionError as e:
                log_error(subfolder, f'Permission denied - {e}')
            except Exception as e:
                log_error(subfolder, e)

def handle_conflict(destination):                                # handles duplicate files
    counter = 2
    stem=destination.stem                                        #filename (resume)
    suffix=destination.suffix                                    #file type (.pdf)
    parent=destination.parent                                    #folder path ()

    while destination.exists():                                  #changes the name of duplicate file to _{counter} EX resume_1 and resume_2
        destination=parent/f'{stem}_{counter}{suffix}'
        counter+=1
    return destination

def organize_folder(target_folder, dry_run=True):                #Headers and output text 
    folder=Path(target_folder)

    if not folder.exists():
        print(f'Folder not found: {target_folder}')
        return
    
    files=[item for item in folder.iterdir() if item.is_file()]
    print(f'\nFound {len(files)} files in {target_folder}')
    print(f'Mode: {"DRY RUN - no files will be moved" if dry_run else "LIVE - files will be moved"}\n')
    print('='*100)

    for file_path in files:
        organize_file(file_path, target_folder, dry_run=dry_run)

if __name__ == '__main__':
    import config
    
    organize_folder(config.TARGET_FOLDER, dry_run=False)            #change dry_run to True or Flase from here to toggle would move on if True and vice versa
    organize_subfolders(config.TARGET_FOLDER, dry_run=False)            #change dry_run to True or Flase from here to toggle would move on if True and vice versa