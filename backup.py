####Automated Python backup script with optional AWS cloud integration

#Imports
import os
import shutil
import datetime
import schedule
import time
#import boto3 (Uncomment for AWS cloud integration)

SOURCE_DIRECTORY = '/path/to/source'
BACKUP_DIRECTORY = '/path/to/backup'

def backup_files(source_dir, backup_dir):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_folder = os.path.join(backup_dir, f"backup_{current_time}")

    try:
        shutil.copytree(source_dir, backup_folder)
        print(f"Backup successful! Files copied to {backup_folder}")
    except Exception as e:
        print(f"Error: {e}")

def job():
    backup_files(SOURCE_DIRECTORY, BACKUP_DIRECTORY)

# Schedule daily backup
schedule.every().day.at("17:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)


##AWS Cloud Integration, uncomment to use

#def upload_to_s3(local_file, bucket_name, s3_file):
 #   s3 = boto3.client('s3')

  #  try:
   #     s3.upload_file(local_file, bucket_name, s3_file)
    #    print(f"File uploaded to: {s3_file}")
    #except Exception as e:
    #    print(f"Error: {e}")

#local_file = '/path/to/file.txt'
#bucket_name = 'your-s3-bucket'
#s3_file = 'backup/file.txt'
#upload_to_s3(local_file, bucket_name, s3_file)