#!/usr/bin/python

import os
import subprocess
import sys
from datetime import datetime

# Read secret from file
def read_secret(secret_name):
    try:
        f = open('/run/secrets/' + secret_name, 'r')
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
WEBHOOK = os.environ.get("WEBHOOK")
WEBHOOK_METHOD = os.environ.get("WEBHOOK_METHOD") or "GET"
KEEP_BACKUP_DAYS = int(os.environ.get("KEEP_BACKUP_DAYS", 30))

dt = datetime.now()
file_name = DB_NAME + "_" + dt.strftime("%Y-%m-%d")
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

def take_backup():
    #if backup_exists():
    #    sys.stderr.write("Backup file already exists!\n")
    #    sys.exit(1)
    
    # trigger postgres-backup
    cmd("env PGPASSWORD=%s pg_dump -Fc -h %s -U %s %s > %s" % (DB_PASS, DB_HOST, DB_USER, DB_NAME, backup_file))

def prune_local_backup_files():
    cmd("find %s -type f -prune -mtime +%i -exec rm -f {} \;" % (BACKUP_DIR, KEEP_BACKUP_DAYS))

def log(msg):
    print "[%s]: %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)

def main():
    start_time = datetime.now()
    log("Dumping database")
    take_backup()
    log("Pruning local backup copies")
    prune_local_backup_files()
    
    if WEBHOOK:
        log("Making HTTP %s request to webhook: %s" % (WEBHOOK_METHOD, WEBHOOK))
        cmd("curl -X %s %s" % (WEBHOOK_METHOD, WEBHOOK))
    
    log("Backup complete, took %.2f seconds" % (datetime.now() - start_time).total_seconds())


if __name__ == "__main__":
    main()
