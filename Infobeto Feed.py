import asyncio
import requests
import time
import smtplib, ssl
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET


# Load variables from .env into the environment
load_dotenv()
isStart = 0

history = []


port = 465
smtp_server = "smtp.gmail.com"
server_email = "jaircarlos3302@gmail.com"
password = "sjhjckcqzovqriss"

sender_email = "jaircarlos3302@gmail.com"
receiver_email = "coldgoldbet@gmail.com"

def send_mail(subject, content):
    
    message = f"""\
Subject: {subject}

{content}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(server_email, password)
        server.sendmail(sender_email, receiver_email, message)
user1 = 0
user2 = 0

status = False

def scraper():
    global user1, user2, status
    try:
        feed = 'https://www.infobeto.com/tipsters-prognostika/feed'

        # browser = launch(ignoreHTTPSErrors=True)
        # page = browser.newPage()
        # page.setDefaultNavigationTimeout(60000); # Increases the timeout limit to 60 seconds


        # page.goto('https://betdiary.io/tipster/bets/4915/hamexrodregan/')
        # page.waitForSelector('div[id^="kupong"]', timeout=5000)
        # html = page.content()
        response = requests.get(feed)
        time.sleep(1)
        tree = ET.fromstring(response.content)
        print(tree, "finding...")
        demo0 = 0
        demo1 = 0
        for author in tree.iter('author'):
            if (author.text.__contains__('noreply@gmail.com (ΗΛΙΑΚΗΣ)')):
                demo0 = demo0 + 1
                print(author.tag, author.text)
                if(demo0 > user1):
                    if(status):
                        send_mail('a new pick was published by Illiakis from infobeto https://www.infobeto.com/author/iliakis', '')
                    user1 = user1 + 1
            if (author.text.__contains__('noreply@gmail.com (FOUNDOULAKIS)')and demo0 >= user1):
                print(author.tag, author.text)
                if(demo1 > user2):
                    if(status):
                        send_mail('a new pick was published by Illiakis from infobeto https://www.infobeto.com/author/iliakis', '')
                    user2 = user2 + 1
        status = True
    except Exception as err:
        print(err)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while not loop.is_closed():
        scraper()
        time.sleep(1)

    