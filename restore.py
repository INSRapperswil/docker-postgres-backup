#!/usr/bin/python

import os
import subprocess
import sys
from datetime import datetime

# Read secret from file
def read_secret(secret_name):
    try:
        f = open('/run/secrets/' + secret_name, 'r', encoding='utf-8')
    except EnvironmentError:
        return ''
    else:
        with f:
            return f.readline().strip()

BACKUP_DIR = os.environ["BACKUP_DIR"]
DB_NAME = os.environ["DB_NAME"]
DB_PASS = os.environ.get("DB_PASS", read_secret('db_password'))
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]

file_name = sys.argv[1]
backup_file = os.path.join(BACKUP_DIR, file_name)

def cmd(command):
    try:
        subprocess.check_output([command], shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        sys.stderr.write("\n".join([
            "Command execution failed. Output:",
            "-"*80,
            e.output,
            "-"*80,
            ""
        ]))
        raise

def backup_exists():
    return os.path.exists(backup_file)

def restore_backup():
    if not backup_exists():
        sys.stderr.write("Backup file doesn't exists!\n")
        sys.exit(1)
    
    # restore postgres-backup
    cmd("env PGPASSWORD=%s pg_restore -Fc -h %s -U %s -d %s %s" % (
        DB_PASS, 
        DB_HOST, 
        DB_USER, 
        DB_NAME, 
        backup_file,
    ))

def log(msg):
    print "[%s]: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)

def main():
    start_time = datetime.now()
    if backup_exists():
        log("Backup file already exists in filesystem %s" % backup_file)
        log("Restoring database")
        restore_backup()   
        log("Restore complete, took %.2f seconds" % (datetime.now() - start_time).total_seconds())
    else:
        log("Backup does not exist")
        exit 1


if __name__ == "__main__":
    main()
