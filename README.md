# Real estate scraper

## Run Locally

1. Clone the project

```
  git clone <repo>
```

2. Go to the project directory

```
  cd <repo>
```

3. Install dependencies

```
  pip install -r requirements.txt
  
```

4. Edit config file - add URLs with pre-selected categories (simply go to the main page and use filters and then copy URL) + add your email(s)

5. Run the app

```
  python run.py
```

This results in scraping everything once into a .txt file. The file then serves as a "database" so it is updated every time the scraper runs. Proprietary solution.

## Run in the cloud (AWS) every X minutes as a cron job

1. Create free [AWS](https://aws.amazon.com/) account 
2. Create Amazon Linux t2.micro EC2 (free for ~1 year) and create a private key
3. Connect to instance in the browser (using the "connect" option in the instance menu)
4. Download WinSCP and connect to the server via the session (key created in step 2. needed) - see [tutorial](https://winscp.net/eng/docs/guide_amazon_ec2)
5. Copy the folder cloned from git into the server using WinSCP
6. In the server command line, first install chrome

```bash
  sudo curl https://intoli.com/install-google-chrome.sh | bash
  sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
  google-chrome --version && which google-chrome
```

7. then install pip3:

```bash
  sudo curl -O https://bootstrap.pypa.io/get-pip.py
  python3 get-pip.py --user
  pip3 --version
```

8. Install all requirements

```bash
pip install -r requirements.txt
```

9. Edit config file - add URLs with pre-selected categories (simply go to the main page and use filters and then copy URL) + add your email(s)

10. Run cron job (every 15 minutes default, edit the file in notepad for different settings)

```bash
crontab run.cron
```

11. Verify crontab is running - the cronjob should be visible after the following command

```bash
crontab -l
```


