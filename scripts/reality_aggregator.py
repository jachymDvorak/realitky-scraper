from datetime import date
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class RealityAggregator():

    def __init__(self, config = None, reality_links = []):

        self.config = config
        self.reality_links = reality_links
        self.filename = self.create_file()
        self.existing_links = self.get_existing_links()

    def create_file(self):

        filename = os.path.join(os.path.dirname(__file__), 'links.txt')

        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                pass

        return filename

    def get_existing_links(self):

        with open(self.filename, 'r') as f:
            existing_links = [line.rstrip() for line in f.readlines()]

        return existing_links

    def append_to_txt(self, link):

        print(f'Appending link to {self.filename}')
        with open(self.filename, 'a') as f:
            f.write(link)
            f.write('\n')

    def send_email(self, receiver_email=None):
        '''

        receiver_email = who to send email to
        links = links to found apartments

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
