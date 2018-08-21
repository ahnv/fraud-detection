
import pandas as pd
import os.path
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib 
import time

class clean:

    @staticmethod
    def preprocess(df):
        if not type(df) == pd.DataFrame: 
            raise ValueError("Invalid input type")

        temp = None

        for val in df.columns:
            df[val] = df[val].astype("float64")
        if os.path.isfile("models/scaler_model.pkl"):
            scaler = joblib.load("models/scaler_model.pkl")
        else:
            scaler = StandardScaler(copy=False, with_mean=True,with_std=True)
        
        if "fraud" in df:
            temp = pd.DataFrame()
            temp["fraud"] = df["fraud"]
            df.drop("fraud", axis=1, inplace=True)
            scaler.fit(df)
            df["fraud"] = temp["fraud"]
        else:
            scaler.fit(df)
        
        joblib.dump(scaler, 'scaler_model.pkl') 

        return df



    @staticmethod
    def clean_df(df):

        if not type(df) == pd.DataFrame:
            raise ValueError("Invalid input type")

        arr = ["delivery_method","hour_checkout","listed","no_of_items","num_order","product_cost","user_facebook","user_twitter"]

        for col in df.columns:
            if col not in arr:
                df.drop(col, axis =1, inplace = True)

        df_clean = df[arr]
        df_clean = clean.preprocess(df_clean)
        return df_clean


    # Return dataframe
    @staticmethod
    def clean_data(file_path):
        
        arr = ["delivery_method","hour_checkout","listed","no_of_items","num_order","product_cost","user_facebook","user_twitter", "fraud"]

        if not os.path.isfile(file_path):
            # TO-DO raise exception instead of returning string
            print("FILE DOES NOT EXIST")
            return None, 1

        statinfo = os.stat(file_path)
        if statinfo.st_size == 0:
            print("File empty")
            return None, 2


        df = pd.read_csv(file_path)

        # print(df.head(10))

        df.replace('', np.nan, inplace=True)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # print(df.head(10))

        df.sort_index(inplace=True, axis=1)
        df['checkout'] = df['checkout'].apply(lambda x: time.gmtime(x))
        df['hour_checkout'] = df['checkout'].map(lambda x: x.tm_hour)
        df = df[arr]
        df = clean.preprocess(df)

        # print(df.head(10))
        return df, 0
