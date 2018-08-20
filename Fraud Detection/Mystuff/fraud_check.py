from Processing.cleaning import clean
from Training.trainer import train
from Testing.tester import tester


class fraud_driver:


    def fraud_check(df):
        df, res = clean.clean_df(df)

        if res > 0:
            raise ValueError("Missing file/data")

        tester.test(df)



    @staticmethod
    def fraud_train(file_path):
        df, res = clean.clean_data(file_path)

        if res > 0:
            raise ValueError("Missing file/data")

        train.trainer(df, replace_model=True)

    def test_cases():

        file_path_temp = "abc.csv"

        print("Test Case1 result: Does file exist")
        df, res = clean.clean_data(file_path_temp)

        if res == 0:
            print("No error!")

        elif res == 1:
            print("File does not exist!")

        elif res == 2:
            print("File is empty!")


fraud_driver.fraud_train("data/data.csv")