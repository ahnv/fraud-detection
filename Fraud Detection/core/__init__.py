from core.process.clean import clean
from core.train.train import train
from core.test.test import test


class core:

    def fraud_check(df):
        df = clean.clean_df(df)
        return test.test(df)

    @staticmethod
    def fraud_train(file_path = "models/dataset.csv"):
        df, res = clean.clean_data(file_path)
        
        if res > 0:
            raise ValueError(str(res) + " Missing file/data")
        train.train_models(df, update=True)
