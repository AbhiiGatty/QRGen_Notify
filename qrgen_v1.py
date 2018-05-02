# Author: AbhiiGatty
# Function: Generates QR code for the attendees of an event for easier access and authentication
import pyqrcode, requests
import json
import os, time 
attendees = json.load(open('test_data.json')) # Loads json data into dict from a file
# while True:    
# attendees =  requests.get('*APIENDPOINT*').json()
created_count = 0
for details in attendees: 
    code = details['_id']
    if os.path.exists('/hello/'+code+'.png') == True: # Create only if file does not exist    
        qr = pyqrcode.create(code) # QR object with the code 
        qr.png(code+'.png', scale=10, module_color="263238", background = "#22d97c",quiet_zone=3)# Create an image from the object, increase scale to increase size
        created_count+=1
if created_count != 0:
    print(time.strftime('%a %H:%M:%S'),' Created {} files'.format(created_count))
else:
    print('Nothing to see!')
#time.sleep(5) # Time interval before next check to see if new attendee is added
