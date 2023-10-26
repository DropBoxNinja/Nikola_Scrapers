import requests
from bs4 import BeautifulSoup
import time
import smtplib, ssl
from email.mime.text import MIMEText
import pandas as pd

def send_email(message, user):
    port = 465  # For SSL
    password = "hkybgbihegzamqpl"
    sender_email = "spilxperten3@gmail.com"
    receiver_email = "nikolab96@yahoo.com"
    message = MIMEText(message, 'html') # set the content type to "text/html"
    message['Subject'] = "user {} has posted in spilxperten".format(user)
    message['From'] = sender_email
    message['To'] = receiver_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", port)
    server.login(sender_email, password)

    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)


url="https://www.spilxperten.com/ekspert/bettingguru/"
user=url.split("/")[-2]

# initial request
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
div_element = soup.find('div', {'class': 'bc-tips-block bc-tips-tips-list-1'})
#het text where div class is bc-tips-list__event-title text-dark-1 w-3/5
matches=div_element.find_all("div",{"class":"bc-tips-list__event-title text-dark-1 w-3/5"})
tippet=div_element.find_all("span",{"class":"bc-tips-list__bet__odds ms-auto ms-md-0 text-dark"})
timeseries=div_element.find_all("span",{"class":"bc-tips-list__event-time text-dark"})
times=[]

#time is like [<span class="bc-tips-list__event-time text-dark">20:45</span>,

for t in timeseries:
    times.append(t.text)
times

# initialize the data dataframe
data = pd.DataFrame(columns=["match","time", "link", "user", "tip"])

for match in matches:
    #send to data df
    text=match.text
    text=text.replace("\n","")
    text=text.rstrip()
    text=text.lstrip()
    link=match.find("a")["href"]
    tip=tippet[matches.index(match)].text
    tip=tip.replace("\n","")
    tip=tip.rstrip()
    tip=tip.lstrip()
    timedata=times[matches.index(match)]
    data=pd.concat([data,pd.DataFrame({"match":[text],"link":[link], "tip":[tip], "time":[timedata], "user":[user]})])

old_div_element = div_element

while True:
    # wait for 1 second
    time.sleep(1)

    # make a new request
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    new_div_element = soup.find('div', {'class': 'bc-tips-block bc-tips-tips-list-1'})
    #het text where div class is bc-tips-list__event-title text-dark-1 w-3/5
    matches=new_div_element.find_all("div",{"class":"bc-tips-list__event-title text-dark-1 w-3/5"})
    tippet=new_div_element.find_all("span",{"class":"bc-tips-list__bet__odds ms-auto ms-md-0 text-dark"})
    timeseries=new_div_element.find_all("span",{"class":"bc-tips-list__event-time text-dark"})
    times=[]
    newdata=pd.DataFrame(columns=["match","time", "link", "user", "tip"])

    for t in timeseries:
        times.append(t.text)
    for match in matches:
        #send to data df
        text=match.text
        text=text.replace("\n","")
        text=text.rstrip()
        text=text.lstrip()
        link=match.find("a")["href"]
        tip=tippet[matches.index(match)].text
        tip=tip.replace("\n","")
        tip=tip.rstrip()
        tip=tip.lstrip()
        timedata=times[matches.index(match)]
        newdata=pd.concat([newdata,pd.DataFrame({"match":[text],"link":[link], "tip":[tip], "time":[timedata], "user":[user]})])

    # check if the new div element is different from the old one
    if new_div_element != old_div_element:

        print("user {} has posted new data".format(user))
        # if it is, then send an email
        #print(data)
        #print(newdata)

        print("sending email")
        #what is new
        changelog=newdata[~newdata["link"].isin(data["link"])]
        # the info about the post in the body, so send the actual table and the new post
        body="""
        <html>
        <head>
        <style>
        table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
        }}
        </style>
        </head>
        <body>
        <h2>user {} has posted in spilxperten!!!</h2>
        <h3>the new post is:</h3>
        {}
        <h3>the table with all the posts is:</h3>
        {}
        </body>
        </html>

        """.format(user, changelog.to_html(escape=False), newdata.to_html(escape=False))
        #send the email
        send_email(body, user)
        print("email sent")
        #update the data
        data=newdata


    else:
        print("user {} has not posted new tips".format(user))

    # update the old div element with the new one
    old_div_element = new_div_element
