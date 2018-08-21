"""
This script runs the Fraud_Detection application using a development server.
"""

from os import environ
from api import app
from api.apiwrapper import apiwrapper
import sys
from core import core
import numpy as np

if len(sys.argv) > 1:
    if (sys.argv[1] == 'train'):
        core.fraud_train()
        print("Training Complete")
        sys.exit(0)
    if (sys.argv[1] == 'train' and sys.argv[2]):
        core.fraud_train(sys.argv[2])
        print("Training Complete")
        sys.exit(0)

    if (sys.argv[1] == 'updateDB'):
        aw = apiwrapper()
        data = aw.getFromDB(aw.collection)
        for i in data:
            if 'fraud' in i:
                del i['fraud']
            if 'diff_order' in i:
                del i['diff_order']
            i['card_no'] = int(i['card_no'])
            i['ip_address'] = int(i['ip_address'])            
            aw.updateDB(i['_id'],aw.postTransactionDetails(i,insert=False), aw.collection)
            
        sys.exit(0)

elif __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
