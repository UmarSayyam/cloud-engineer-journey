# Linux Notes

## Commands learned
- pwd, ls, cd, mkdir, touch, rm, cp, mv
- chmod, chown — file permissions
- ps, top, kill — process management
- ssh, scp — remote access
- grep, cat, less — file reading
- curl, wget — HTTP requests

## Key concepts
- Everything is a file in Linux
- Permissions: rwx for owner, group, others
- chmod 755 = rwxr-xr-x (standard for scripts)
- chmod 600 = rw------- (private files like SSH keys)
- SSH uses key pairs — private key stays local

## Scripts written
- healthcheck.sh — server health monitoring
- backup.sh — automated dated backups
- myscript.sh — first ever shell script
