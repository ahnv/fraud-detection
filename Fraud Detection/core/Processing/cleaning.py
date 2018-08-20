
import pandas as pd
import os.path
import numpy as np
from sklearn.preprocessing import StandardScaler


class clean:

    @staticmethod
    def preprocess(df):
        # scaling done
        if not type(df) == pd.DataFrame:
            raise ValueError("Invalid input type")

        temp = None

        for val in df.columns:
            df[val] = df[val].astype("float64")

        scaler = StandardScaler(copy=False, with_mean=True,with_std=True)
        if "fraud" in df:
            temp = pd.DataFrame()
            temp["fraud"] = df["fraud"]
            df.drop("fraud", axis=1, inplace=True)
            scaler.fit(df)
            df["fraud"] = temp["fraud"]
        else:

            scaler.fit(df)

        return df



    @staticmethod
    def clean_df(df):

        if not type(df) == pd.DataFrame:
            raise ValueError("Invalid input type")

        arr = ["delivery_method", "listed", "num_order", "user_facebook", "user_twitter", "product_cost", "no_of_items",
               "hour_checkout"]

        for col in df.columns:
            if col not in arr:
                df.drop(col, axis =1, inplace = True)

        df2 = pd.DataFrame()

        for val in arr:
            if val in df:
                df2[val] = df[val]
            else:
                raise ValueError("Missing feature", val)

        df2 = clean.preprocess(df2)

        return df2, 0


    # Return dataframe
    @staticmethod
    def clean_data(file_path):
        arr = ["delivery_method", "listed", "num_order", "user_facebook", "user_twitter", "product_cost", "no_of_items",
               "hour_checkout", "fraud"]

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
        for val in df.columns:
            if not (val in arr):
                df.drop(val, axis=1, inplace=True)

        temp = pd.DataFrame()
        temp["fraud"] = df["fraud"]
        df.drop("fraud", inplace=True, axis=1)
        df = clean.preprocess(df)
        df["fraud"] = temp["fraud"]

        # print(df.head(10))
        return df, 0
