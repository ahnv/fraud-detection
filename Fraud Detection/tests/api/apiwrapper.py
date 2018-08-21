from api.apiwrapper import apiwrapper

def test_post_request_with_accurate_data():
    jsonData = {"delivery_method" : 0,"add_to_cart" : 1259613954,"checkout" : 1259622673,"listed" : 1,"num_order" : 0,"user_name" : "Modestine Puckinghorne","user_created" : 1259613950,"user_facebook" : 0,"user_twitter" : 0,"address" : "16666 Fieldstone Point","country" : "United States","card_no" : 3530006808859550,"card_type" : "jcb","ip_address" : 2771431369,"email" : "mpuckinghorne8o@icio.us","zip" : 62705,"product_name" : "tempora maxime a","product_cost" : 359,"product_id" : 326192,"no_of_items" : 561}
    aw = apiwrapper()
    res = aw.postTransactionDetails(jsonData)
    assert res == 'Fraud Transaction Detected' or res == 'No Fraud'

def test_post_request_with_incomplete_data():
    jsonData = {"delivery_method" : 0,"add_to_cart" : 1259613954,"checkout" : 1259622673,"listed" : 1,"num_order" : 0,"user_name" : "Modestine Puckinghorne","user_created" : 1259613950,"user_facebook" : 0,"user_twitter" : 0,"address" : "16666 Fieldstone Point","country" : "United States","card_no" : 3530006808859550,"card_type" : "jcb","ip_address" : 2771431369,"email" : "mpuckinghorne8o@icio.us","zip" : 62705,"product_name" : "tempora maxime a","product_cost" : 359,"product_id" : 326192}
    aw = apiwrapper()
    res = aw.postTransactionDetails(jsonData)
    assert res == 'Json Data Error'

def test_post_request_with_incorrect_data():
    jsonData = {"delivery_method" : 0,"add_to_cart" : 1259613954,"checkout" : "1259622673","listed" : 1,"num_order" : 0,"user_name" : "Modestine Puckinghorne","user_created" : 1259613950,"user_facebook" : 0,"user_twitter" : 0,"address" : "16666 Fieldstone Point","country" : "United States","card_no" : 3530006808859550,"card_type" : "jcb","ip_address" : 2771431369,"email" : "mpuckinghorne8o@icio.us","zip" : 62705,"product_name" : "tempora maxime a","product_cost" : 359,"product_id" : 326192,"no_of_items" : 561}
    aw = apiwrapper()
    res = aw.postTransactionDetails(jsonData)
    assert res == '(checkout. Expected Type: `int`. Recieved Type:str )'

def test_db_connect():
    aw = apiwrapper()
    assert type(aw.client).__name__ == 'MongoClient'

def test_db_input():
    jsonData = {"data" : {"array": [1,2,3],"boolean": True,"number": 123,"string": "Hello World"}}
    cols = ["array", "boolean", "number", "string"]
    aw = apiwrapper()
    aw.testcollection.drop()
    id = aw.insertDataToCollection(jsonData, aw.testcollection)
    res = aw.testcollection.find_one({"_id" : id})
    for col in cols:
        assert res['data'][col] == jsonData['data'][col]
    