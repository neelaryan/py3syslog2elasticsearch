import socketserver
from datetime import datetime
import time, re

#https://docs.python.org/3/library/socketserver.html
class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """
    Decodes syslog data and add timestamp.
    This class takes the recieved syslog entries and writes them to the database.
    """

    def handle(self):

        # open elasticsearch connection for creating index and document

        data = bytes.decode(self.request[0].strip(), encoding="utf-8")

        # add data as document into index

        if data.startswith('<14>'):
            alert_id = re.findall(r'(?<=externalId=)([0-9a-zA-Z\-]+)(?=\smsg)', data)
        print('At {} recieved following message:\n{}\nALERT ID == {}'.format(time.time(), data, alert_id))

if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 514

    # define constants and connect to elasticsearch
    # make sure index exists of current datet
    # if not make one

    server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
    
    #self defined variables which are needed in handle()
    #https://stackoverflow.com/questions/6875599/with-python-socketserver-how-can-i-pass-a-variable-to-the-constructor-of-the-han
    
    # pass necessary values to as self defined variables for SyslogUDPHandler to work

    #handle requests until explicit shutdown(), see python docs
    server.serve_forever()
