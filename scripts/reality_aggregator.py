from datetime import date
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List
from scripts.config import Config
import json
import requests

class RealityAggregator():

    def __init__(self,
                 config: Config,
                 reality_links: List=[]):

        self.config = config
        self.reality_links = reality_links
        self.filename = self.create_file()
        self.existing_links = self.get_existing_links()

    def create_file(self) -> str:
        '''creates the path to file where links to apts are saved if it doesn't exist, or outputs the path to existing file'''

        filename = os.path.join(os.path.dirname(__file__), '..', 'databases', self.config.database)

        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                pass

        print(filename)

        return filename

    def get_existing_links(self) -> List:

        '''reads the file of existing links with apts and returns a list of existing apts'''


        with open(self.filename, 'r') as f:
            existing_links = [line.rstrip() for line in f.readlines()]

        print(f'Reading existing links from {self.filename}')
        print(f'One of the existing links: {existing_links[1]}')

        return existing_links

    def append_to_txt(self, link: str = None) -> None:

        '''appends the apartment to the file with all apts'''

        print(f'Appending link to {self.filename}')
        with open(self.filename, 'a') as f:
            f.write(link)
            f.write('\n')

    def send_email(self, receiver_email: str = None) -> None:
        '''

        receiver_email = who to send email to

        sends email to the receiver with all new found apts

        '''

        # establish authentication for email sending
        sender_email = "realquik@seznam.cz"
        password = 'R34lquik'

        # set needed variables
        today = date.today().strftime("%d/%m/%Y")

        ### set up message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{today}: NOVÉ BYTY"
        message["From"] = sender_email
        message["To"] = receiver_email

        links_joined = []
        for link in self.reality_links:
            link = '<li>' + f'{link}' + '</li>'
            links_joined.append(link)

        links_joined = ''.join(links_joined)
        # write body
        html = f"""
                <ol>
                {links_joined}
                </ol>
                <p><br></p>
                    """

        # Turn these into plain/html MIMEText objects
        main_text = MIMEText(html, "html")
        message.attach(main_text)
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.seznam.cz", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        print(f'Sending links to {receiver_email} these links: {self.reality_links}')

    # def send_links_to_telegram(self):
    #
    #     # get API parameters for Telegram
    #     token = '5539208971:AAEmkkzGmq0WM0GmTTo8hoWLmgynO5Az2IA'
    #     chat_id = '-750251473'
    #
    #     # instantiate bot
    #     bot = telegram.Bot(token=token)
    #
    #     # send links
    #     for link in self.reality_links:
    #         bot.sendMessage(chat_id=chat_id, text=link)

    def send_telegram_messages(self):

        file = os.path.join(os.path.dirname(__file__), '..', 'authentication', 'telegram.json')

        with open(file) as f:
            auth = json.load(f)

        url = f'https://api.telegram.org/{auth["bot_id"]}/sendMessage'
        chat_id = auth["chat_id"]

        for link in self.reality_links:

            headers = {'Content-Type': 'application/json',
                       'Proxy-Authorization': 'Basic base64'}
            data_dict = {'chat_id': chat_id,
                         'text': link,
                         'parse_mode': 'HTML'}
            data = json.dumps(data_dict)

            requests.post(url,
                        data=data,
                        headers=headers,
                        verify=False)

