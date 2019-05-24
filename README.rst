=========================
Docker PostgreSQL Backup
=========================

Docker image that runs a cron job which dumps a Postgres database.

Required environment variables
==============================

* :code:`CRON_SCHEDULE`: The time schedule part of a crontab file (e.g: :code:`15 3 * * *` for every night 03:15)
* :code:`DB_HOST`: Postgres hostname
* :code:`DB_PASS`: Postgres password or `POSTGRES_PASSWORD_FILE=/run/secrets/db_password`
* :code:`DB_USER`: Postgres username
* :code:`DB_NAME`: Name of database

Optional environment variables
==============================

* :code:`WEBHOOK`: If specified, an HTTP request will be sent to this URL
* :code:`WEBHOOK_METHOD`: By default the webhook's HTTP method is GET, but can be changed using this variable
* :code:`KEEP_BACKUP_DAYS`: The number of days to keep backups for when pruning old backups

Restoring a backup
==================

This image can also be run as a one off task to restore one of the backups. 
To do this, we run the container with the command: :code:`/backup/restore.sh [S3-filename]`.

The following environment variables are required:

* :code:`DB_HOST`: Postgres hostname
* :code:`DB_PASS`: Postgres password or `POSTGRES_PASSWORD_FILE=/run/secrets/db_password`
* :code:`DB_USER`: Postgres username
* :code:`DB_NAME`: Name of database

