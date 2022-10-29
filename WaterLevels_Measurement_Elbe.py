import requests
import json
import time
import os
import pandas as pd
import smtplib
import threading

# Defintion of global variables

csv_path = 'Desktop/Elbe_Levels' # path of csv file
emailAddress = os.environ.get('my_gmail_address')  # email address is hidden in environment variable
emailPwd = os.environ.get('gmail_password')  # pwd also hidden in environment variable 
waterlevelThreshold = 100    

# The following function writes csv data to file

def write_csv(data):
    # Executed after first write
    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_path+'/measurementData.csv', mode='a', index=False, header=False)
        print("Value successfully written to csv file")

        # Executed for the first write
    except:
        os.mkdir(csv_path)  # creates csv file
        df = pd.DataFrame(data)   # creates dataframe out of data
        df.to_csv(csv_path+'/measurementData.csv', mode='w', index=False, header=True)
        print("First value successfully written to csv file")
    return




# The following function performs read of current waterlevel measurement and pre processing.  
    
def read_waterlevel():
    # A query of all available measuring points of PEGELONLINE is carried out with this URL.
    # The json file is filtered to keep only sections of the river Elbe

    msg1 = "Water level is below threshold, dont panic..."
    msg2 = "Water level is above threshold"
    
    while (True):
        water = {}
        timeseries = {}
        currentMeasurement = {}
        gaugeZero = {}
        query1 = {"waters":"ELBE"}
        response = requests.get("https://pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true", params=query1)
        response_list = response.json()[10:13] # Creates list of 6, 7, 8 dictionary items of the json file

        for dt in response_list:

            # response_list contain sub dictionary water and timeseries
            water = dt['water']  # extracts water subdictionary
            timeseries = dt['timeseries'][0] # extracts timeseries subdictionary

            # timeseries contain two subdictionaries currentMeasurement and gaugeZero
            currentMeasurement = timeseries['currentMeasurement'] # extracts currentMeasurement subdictionary
            gaugeZero = timeseries['gaugeZero'] # extracts currentMeasurement subdictionary

            # delete subdictionaries in dt
            del dt['water']
            del dt['timeseries']

            # Rename duplicate keys
            water['shortname1'] = water.pop('shortname')
            water['longnamename1'] = water.pop('longname') 

            timeseries['shortname2'] = timeseries.pop('shortname')
            timeseries['shortname2'] = timeseries.pop('longname')

            # Appends sub dictionary buffers to original dictionary to produce a single plain dictionary with no subs
            dt.update(water)
            dt.update(timeseries)
            dt.update(currentMeasurement)
            dt.update(gaugeZero)

            # writing dictionary data into csv file
            write_csv(dt)

            # send email
            shortname = dt['shortname1']
            agency = dt['agency']

            if (dt['value'] < 100):
                payloadMsg = f'{shortname}\n\n{agency}\n\n{msg1}'
                sendMail(payloadMsg)
            else:
                payloadMsg = f'{shortname}\n\n{agency}\n\n{msg2}'
                sendMail(payloadMsg)
        time.sleep(5*60)  # produces a delay of 5 mins

    return  # Execution never arrives here. However if it does, the function returns

# The following function sets up a connection to gmail server and sends an email using smtp

def sendMail(msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp: # creates connection to gmail server on port 587
        smtp.ehlo()
        smtp.starttls() # encripts connection
        smtp.ehlo()     # refresh connection

        smtp.login(emailAddress, emailPwd)  # authentification to server 

        subject = "Water level"   # subject of message
        body = msg    # body of the message

        message = f'Subject: {subject} \n\n\n {body}'  # formatting message

        smtp.sendmail(emailAddress, emailAddress, message) # message is sent back to the sender
    return

read_waterlevel()