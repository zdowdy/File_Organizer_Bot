import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()                                                           #Load info from .env
SENDER=os.getenv('EMAIL_SENDER')
PASSWORD=os.getenv('EMAIL_PASSWORD')
RECEIVER=os.getenv('EMAIL_RECEIVER')
LOG_FILE=Path(__file__).parent/'organizer.log'

def parse_log(days=7):                                                  #Reads organizer logs from the last 7 days
    if not LOG_FILE.exists():
        return [], []
    
    cutoff=datetime.now()-timedelta(days=days)                          #Sets a time range for the parse
    moves=[]
    errors=[]

    with open(LOG_FILE,'r', encoding='utf-8') as f:
        for line in f:
            try:
                timestamp_str=line[1:20]                                #timestamp format
                timestamp=datetime.strptime(timestamp_str, '%m-%d-%Y %H:%M:%S')
                
                if timestamp<cutoff:                                    #Skips entries older than the cutoff time
                    continue

                if 'INFO' in line and 'Moved:' in line:
                    moves.append(line.strip())
                elif 'ERROR' in line:
                    errors.append(line.strip())
            except ValueError:                                          #Skips lines that dont match the format
                continue                                                
    return moves, errors

def build_email_body(moves,errors):
    now=datetime.now().strftime('%B %d, %Y')
    week_ago=(datetime.now()-timedelta(days=7)).strftime('%B %d,%Y')
                                                                        #Email format
    email_body=f'''                                                     
File Organizer Bot - Weekly Report
Period: {week_ago} to {now}
{'='*50}

Summary
-------
Files moved   : {len(moves)}
Errors found  : {len(errors)}

'''
    if errors:                                                          #displays if there are any errors and what they are
        email_body+= 'ERRORS (require attention)\n'
        email_body+= '-'*50 + '\n'
        for error in errors:
            email_body+=f'  {error}\n'
        email_body+='\n'
    else:
        email_body+='ERRORS\n'
        email_body+='-'*30 + '\n'
        email_body+='  No errors this week.\n\n'

    if moves:                                                           #Displays how many files were moved if any at all
        email_body+='FILES MOVED THIS WEEK\n'
        email_body+='-'*30 + '\n'
        for move in moves[-20:]:                                        #show last 20 moves max
            email_body+=f'  {move}\n'
        if len(moves)>20:
            email_body+=f'  ... and {len(moves)-20} more.\n'
    else:
        email_body+='FILES MOVED THIS WEEK\n'
        email_body+='-'*30 + '\n'
        email_body+='  No files moved this week.\n'

    return email_body

def send_weekly_report():
    if not all([SENDER, PASSWORD, RECEIVER]):                           #Checks for email credentials
        print('ERROR: Missing email credentials in .env file')
        return
    
    moves, errors=parse_log(days=7)                                     #imports moves and errors as well as the email_body from functions
    email_body=build_email_body(moves, errors)

    msg=MIMEMultipart()                                                 #import credentials and email_body in
    msg['From']=SENDER
    msg['To']=RECEIVER
    msg['Subject']=f'File Organizer Bot - Weekly Report ({datetime.now().strftime('%b %d')})'

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()          # upgrades to encrypted connection
            server.ehlo()
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())
            print(f'[Email Sent] Weekly report sent to {RECEIVER}')
    except smtplib.SMTPAuthenticationError:
        print('ERROR: Authentication failed - check your App Password in .env')
    except smtplib.SMTPException as e:
        print(f'ERROR: Failed to send email - {e}')
    except Exception as e:
        print(f'ERROR: Unexpected error - {e}')

if __name__=='__main__':
    send_weekly_report()