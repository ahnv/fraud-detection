from sklearn.externals import joblib
import pandas as pd
import os
from core.Processing.cleaning import clean


class tester:

    def test(df):

        
        model_ada, model_knn, model_svr = None, None, None
        if os.path.isfile("models/model_ada.pkl"):
            model_ada = joblib.load("models/model_ada.pkl")
        else:
            raise ValueError("Adaboost model not available")

        if os.path.isfile("models/model_ada.pkl"):
            model_knn = joblib.load("models/model_knn.pkl")
        else:
            raise ValueError("KNN model not available")

        if os.path.isfile("models/model_ada.pkl"):
            model_svr = joblib.load("models/model_svr.pkl")
        else:
            raise ValueError("SVR model not available")

        model_svr = joblib.load("models/model_svr.pkl")
        model_knn = joblib.load("models/model_knn.pkl")
        model_ada = joblib.load("models/model_ada.pkl")
        df, r = clean.clean_df(df)
        values = df.values
        res = (model_ada.predict(values) + model_knn.predict(values) + model_svr.predict(values)) / 3
        return res


#df = pd.DataFrame()
#tester.test()