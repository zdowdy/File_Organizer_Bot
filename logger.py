import logging
from pathlib import Path
from datetime import datetime

LOG_FILE=Path(__file__).parent / 'organizer.log'                #Where the log file will be saved (path)

def setup_logger():
    global logger
    logger= logging.getLogger('file_organizer')                 #Creates a name for the logger
    logger.setLevel(logging.DEBUG)                              #Captures all movemnet of files

    if logger.handlers:                                         #preventing duclicate entries from being made
        return logger
    
    formatter=logging.Formatter(                                #Format of the log entry
        fmt='[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S'
    )
                                                                #Use handlers to control where log entries are sent 
    file_handler=logging.FileHandler(LOG_FILE, encoding='utf-8')#Writes to LOG_FILE path set to DEBUG so it captures everything in format
    file_handler.setLevel(logging.DEBUG)                    
    file_handler.setFormatter(formatter)

    console_handler= logging.StreamHandler()                    #Prints to the terminal and it is set to INFO so it only shows movement and errors in format
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)                             # adds both handlers to logger ready for use
    logger.addHandler(console_handler)
    return logger

logger=setup_logger()

def log_move(source, destination):                              #Logs successful movement of files or folders
    logger.info(f'Moved: {source} -> {destination}')

def log_skip(file_path, reason):                                #Logs skipped files or foldrs and the reason
    logger.debug(f'Skipped: {file_path} ({reason})')

def log_error(file_path, error):                                #Logs errors that occur during processing
    logger.error(f'Error: {file_path} - {error}')

def log_startup(target_folder):                                 #Shows when and where the bot is active
    logger.info(f'{'='*50}')
    logger.info(f'File Organizer Bot Active')
    logger.info(f'Active in {target_folder}')
    logger.info(f'{'='*50}')