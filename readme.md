> [!NOTE]
Please make sure you have ntfy service or own ntfy server hosted.
See https://github.com/binwiederhier/ntfy

### Example (LINUX):
mkdir python_scripts/ 

sudo apt install python3.9-pip

sudo python3 -m pip install requirements.txt

### Files:
`wowtoken.py` in `~/python_scripts/`

`wowtoken.sh` in `~` (current working directory)

`crontab.txt` in command `sudo crontab -e`


> [!CAUTION]
Create `.env` file in `~/python_scripts/` and put the following:


```
NTFY_SERVER_URL=<your-server-url-endpoint>
NTFY_TOPIC=<your-topic-to-publish-name>
```
