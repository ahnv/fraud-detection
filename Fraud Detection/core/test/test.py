from sklearn.externals import joblib
import pandas as pd
import os
from core.process.clean import clean
import numpy as np

class test:

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
        
        df = clean.clean_df(df)
        values = df.values
        ada = model_ada.predict(values)
        knn = model_knn.predict(values)
        svr = model_svr.predict(values)

        res = np.mean([ada,knn,svr])

        return res