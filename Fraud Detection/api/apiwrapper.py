
import pandas as pd
from pytest import fixture
import json
from pymongo import MongoClient
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import base64
from flask import jsonify
from core import fraud_check
import time


class apiwrapper:
    """description of class"""

    
    cols = [["add_to_cart","int"],["address","str"],["card_no","int"],["card_type","str"],["checkout","int"],["country","str"],["delivery_method","int"],["email","str"],["ip_address","int"],["listed","int"],["no_of_items","int"],["num_order","int"],["product_cost","int"],["product_id","int"],["product_name","str"],["user_created","int"],["user_facebook","int"],["user_name","str"],["user_twitter","int"],["zip","int"]]  
    final_column_names = ["delivery_method", "listed", "num_order", "user_facebook", "user_twitter", "product_cost", "no_of_items","hour_checkout"]

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.data
        self.collection = self.db.fraud_data
        self.testcollection = self.db.test_fraud_data

    def postTransactionDetails(self, jsonData):
        error = ''
        for col in self.cols:
            if (col[0] not in jsonData):
                return 'Json Data Error'
            if (type(jsonData[col[0]]).__name__ != col[1]):
                error += '(' +  col[0] + '. Expected Type: `' + col[1] + '`. Recieved Type:'+ type(jsonData[col[0]]).__name__ +' )'
        
        if error: return error      

        jsonData['diff_order'] = (jsonData['checkout'] - jsonData['add_to_cart']) / float( 60 ** 2)
        print(jsonData['diff_order'])

        data = []
        cols = []
        for col in self.cols:
            data.append(jsonData[col[0]])
            cols.append(col[0])

        df = pd.DataFrame(data=[data], columns=cols)
        df['checkout'] = df['checkout'].apply(lambda x: time.gmtime(x))
        df['hour_checkout'] = df['checkout'].map(lambda x: x.tm_hour)
        print(df)
        is_fraud = fraud_check.fraud_driver.fraud_check(df)
        
        jsonData['fraud'] = is_fraud
        
        self.insertDataToCollection(jsonData, self.collection)

        if (is_fraud): return 'Fraud Transaction Detected'
        return 'No Fraud'+ str(is_fraud)
        
    def insertDataToCollection(self, jsonData, coll):
        id = coll.find_one(jsonData)
        if not id:
            return coll.insert_one(jsonData).inserted_id
        else:
            return id['_id']

    def generateGraph(self):
        lowcounts, midcounts, highcounts = [], [], []
        body = lowcounts, midcounts, highcounts

        highcounts.append(self.collection.find({'fraud' : { "$gt" : 0.7}}).count())
        midcounts.append(self.collection.find({"$and" : [{'fraud' : { "$gt" : 0.5}},{'fraud' : { "$lt" : 0.6}}]}).count())
        lowcounts.append(self.collection.find({'fraud' : { "$lt" : 0.5}}).count())
        
        labels = ['low', 'medium', 'high']
        counts = [lowcounts[0], midcounts[0], highcounts[0]]

        plt.figure()
        plt.bar(np.arange(3), counts, width = 0.5, tick_label=labels, align='center')
        image = BytesIO()
        plt.savefig(image)

        return image.getvalue(), 200, { 'Content-Type' : 'image/png' }
        