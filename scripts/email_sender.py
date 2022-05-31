import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

def send_email(receiver_email = None, links = None):
    '''

    receiver_email = who to send email to (info from tracker)
    links = links to underpriced appartments

    '''

    # establish authentication for email sending
    # TODO: move credentials to airflow storage
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
    for link in links:

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

