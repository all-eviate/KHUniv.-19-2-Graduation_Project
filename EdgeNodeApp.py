import bluetooth
import time
import requests
import logging
import boto3
from gpiozero import LED
from time import sleep
from botocore.exceptions import ClientError

#gpio setting
r = LED(2)
y = LED(3)
g = LED(4)

#function definition for using AWS S3
def create_presigned_post(bucket_name, object_name, fields=None,
                          conditions=None, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields = fields,
                                                     Conditions = conditions,
                                                     ExpiresIn = expiration)
    
    except ClientError as e:
        logging.error(e)
        return None
    
    return response

On = True
while On:
    #server socket setting
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 3
    server_socket.bind(("", port))
    server_socket.listen(3)

    #client socket setting
    client_socket, address = server_socket.accept()
    print("Accepted connection from ", address)
    while True:
        data = client_socket.recv(1024)
        data = data.decode('utf-8') #decoding 'bytes' into 'string'
        print("Received: %s" % data)
        if data[0] == 'q':
            print("End of connection")
            break
        if data[0:3] == 'off':
            print("Edge node off")
            On = False
            break
        if (len(data) == 16):
            #processing command
            room = data[0]
            onoff = data[1] #(0: off, 1: on)
            year = data[2:6]
            mon = data[6:8]
            date = data[8:10]
            hour = data[10:12]
            min = data[12:14]
            sec = data[14:16]
            if str(room) == '1':
                if onoff == '0':
                    r.off()
                elif str(onoff) == '1':
                    r.on()
            elif room == '2':
                if onoff == '0':
                    y.off()
                elif onoff == '1':
                    y.on()
            elif room == '3':
                if onoff == '0':
                    g.off()
                elif onoff == '1':
                    g.on()
            datestamp = year + '-' + mon + '-' + date
            timestamp = hour + ":" + min + ':' + sec
            print("date: " + datestamp)
            print("time: " + timestamp)
            ctrlog = datestamp + ' ' + timestamp
            
            f = open(ctrlog, 'w')
            f.close()

            #uploading ctrlog to S3
            response = create_presigned_post('cmyoon-capstone2',ctrlog)
            if response is None:
                exit(1)

            with open(ctrlog, 'rb') as f:
                files = {'file':(ctrlog, f)}
                http_response = requests.post(response['url'],
                                               data=response['fields'],
files=files)
        
    client_socket.close()
server_socket.close()