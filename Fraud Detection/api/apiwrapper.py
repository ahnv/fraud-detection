
import pandas as pd
from pytest import fixture
import json
from pymongo import MongoClient
#from core import fraud_check

class apiwrapper:
    """description of class"""

    
    cols = [["add_to_cart","int"],["address","str"],["card_no","int"],["card_type","str"],["checkout","int"],["country","str"],["delivery_method","int"],["email","str"],["ip_address","int"],["listed","str"],["no_of_items","int"],["num_order","int"],["product_cost","int"],["product_id","int"],["product_name","str"],["user_created","int"],["user_facebook","int"],["user_name","str"],["user_twitter","int"],["zip","int"]]  
    final_column_names = ["delivery_ind", "listed", "num_order", "fb_ind", "twitter_ind", "product_cost", "no_of_items", "diff_orders","hour_checkout"]

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

        data = []
        cols = []
        for col in self.cols:
            data.append(jsonData[col[0]])
            cols.append(col[0])

        df = pd.DataFrame(data=[data], columns=cols)
         
        is_fraud = 1 # Call Function core.fraud_check(df)
        
        jsonData['fraud'] = is_fraud
        
        self.insertDataToCollection(jsonData, self.collection)

        if (is_fraud): return 'Fraud Transaction Detected'
        return 'No Fraud'
        
    def insertDataToCollection(self, jsonData, coll):
        id = coll.find_one(jsonData)
        if not id:
            return coll.insert_one(jsonData).inserted_id
        else:
            return id['_id']


