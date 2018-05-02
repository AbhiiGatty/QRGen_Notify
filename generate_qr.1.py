# Author: AbhiiGatty
# Function: Generates QR code and mails the attendees of an event for easier access and authentication
import pyqrcode, requests, json
import os, time, hashlib 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

Directory = 'QRCodes' 
if not os.path.exists(Directory): # Create a directory to store all QR images if it is not created
    os.makedirs(Directory)

### To make the email work you have to change account access for less secure apps, https://support.google.com/accounts/answer/6010255?hl=en

def sendEmail(toaddr,filename,attendee_name): # Sends Email with attachment
    fromaddr = 'EXAMPLE@EMAIL.COM' 
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'DevHost18: Registration Successful'
    
    body = "Hey! \nWelcome "+name+" to DevHost18! You have successfully completed registration, Here is your QR-Code to access all that DevHost18 has to offer! Have a great day!\n\nRegards,\nSahyadriOpenSourceCommunity\n\nP.S. visit devhost18.in to know more about the events!"
    
    msg.attach(MIMEText(body, 'plain'))
    
    attachment = open(filename, "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= {}".format((filename.split('/'))[1])) # Usually this is kept only to filename but iv'e edited for this special case
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, '')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

attendees_details = json.load(open('test_data.json')) # Loads json data from a file    
# attendees_details =  requests.get(*API ENDPOINT*).json() # Loads json data from an API
# while True: # Enable while loop when using API and want continuous updates and automated mailing list
created_count = 0

for details in attendees_details: 
    code = details['_id']
    name = details['name']
    email = details['email'] 
    image_name = Directory+'/'+name+'.png' 

    if os.path.exists(image_name) == False: # Create only if file does not exist    
        qr = pyqrcode.create(hashlib.md5(code.encode('utf-8')).hexdigest()) # QR object with the code 
        qr.png(image_name, scale=10, module_color='#263238', background = '#22d97c', quiet_zone=3) # Create an image from the object, increase scale to increase size
        sendEmail(toaddr=email, filename=image_name, attendee_name=name)
        created_count+=1
        time.sleep(3) # Time interval so google does not discard the mail sent

if created_count != 0: # Used to see activity on terminal
    print(time.strftime('%a %H:%M:%S'),' Created {} files'.format(created_count))
else:
    print('Nothing to see!')
time.sleep(5) # Time interval before next check of json file updates
