FROM postgres:14.4-alpine

# Install dependencies
RUN apk update && apk add --no-cache \
    bash make curl openssh git python3

# Cleanup
RUN rm /var/cache/apk/*


VOLUME ["/data/backups"]

ENV BACKUP_DIR /data/backups

ADD . /backup

ENTRYPOINT ["/backup/entrypoint.sh"]

CMD crond -f -d 8
