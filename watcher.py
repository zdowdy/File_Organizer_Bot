import time 
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from actions import organize_file
from logger import log_startup, log_error
import config

class OrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):                                            #on_created:triggers every time a new file or folder appears and event conatins inf on what happened
        if event.is_directory:                                              #Checks if item is a folder if it is it gets skiped since we only monitor files
            return
        
        file_path=Path(event.src_path)                                      #Full path of the new file in the watched folder for the first time
        
        if file_path.suffix in ('.part','.crdownload','.tmp'):              #Skips partial down load and temp files clear terminal and log noise
            return
        
        time.sleep(4)                                                       #Updated the sleep time to [reduce errors in the email report]

        if not file_path.exists():                                          #Updated to skip if file has already been moved or deleted[reduces errors in the email report]
            return

        try:                                                                #Try/except prevents the bot from crashing if an error where to occur it logs it and continues
            organize_file(file_path, config.TARGET_FOLDER, dry_run=False)
        except Exception as e:
            log_error(file_path, f'Watcher error- {e}')
    
    def on_moved(self, event):                                              #on_moved:triggers when a file is renamed or dragged to watched folder
        if event.is_directory:                                              #Checks if item is a folder if it is it gets skiped since we only monitor files
            return
        
        file_path=Path(event.dest_path)                                     #Uses event.dest_path since we want new location of file not where it came from
        
        if file_path.suffix in ('.part','.crdownload','.tmp'):              #Skips partial down load and temp files clear terminal and log noise
            return
        
        time.sleep(4)                                                       #Updated the sleep time to [reduce errors in the email report]

        if not file_path.exists():                                          #Updated to skip if file has already been moved or deleted[reduces errors in the email report]
            return

        try:                                                                #Try/except prevents the bot from crashing if an error where to occur it logs it and continues
            organize_file(file_path, config.TARGET_FOLDER, dry_run=False)
        except Exception as e:
            log_error(file_path, f'Watcher error- {e}')
    
def start_watcher():
        target=config.TARGET_FOLDER
        if not Path(target).exists():                                       #Checks if the TARGET_FOLDER exists if it does not it returns early and says folder not found
            print(f'Folder not found {target}')
            return
        log_startup(target)                                                 #Shows what is being watched and how to stop it from watching
        print(f'Watching: {target}')
        print('Press Crtl+C to stop\n')

        event_handler=OrganizerHandler()
        observer=Observer()
        observer.schedule(event_handler, target, recursive=False)           #Connects observer and event_handler to watch target and trigger event_handler when anything happens     recursive=False is to only watch the top level(files) in the Downloads not subfolders
        observer.start()                                                    #Runs the observer in the backgroud alongside the main code

        try:                                                                #Try keeps the watcher running indefinitely 
            while True:
                time.sleep(1)
        except KeyboardInterrupt:                                           #Except shuts down the backgrough thread when Ctrl+C is pressed
            observer.stop()
            print('\nWatcher stopped.')
        observer.join()                                                     #Waits for the observer thread to fully finish before the script exits

if __name__ =='__main__':
    start_watcher()