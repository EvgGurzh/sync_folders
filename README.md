# Sync.py
Sync.py is a Python script for one way directories synchronization from source to destination.

## Usage
```bash
python3 sync.py -s "Source directory" -d "Destination directory" -l "Logs directory" -i "Synchronization interval in seconds"

python3 sync.py -s C:\source -d D:\destination -l E:\logs -i 60

python3 sync.py -s /home/foo/source -d /home/bar/destination -l /tmp/logs -i 300
```
If destination directory or logs directory doesn't exist it will be created automatically.

## Contributing
Pull requests are welcome :)