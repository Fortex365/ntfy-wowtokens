### Use Example (LINUX):
mkdir python_scripts/

sudo apt install python3.9-pip (or higher version)

sudo python3 -m pip install requirements.txt

sudo crontab -e

### Put files:
`wowtoken.py` in `~/python_scripts/`

`wowtoken.sh` in `~` (current working directory)

`crontab.txt` in command `sudo crontab -e`


### NTFY Setup:
Create `.env` file in `~/python_scripts/` and put


```
NTFY_SERVER_URL=<your-server-url-endpoint>
TOPIC=<your-topic-to-publish-name>
```