import pandas as pd


# Import csv
def display_data(csv_path):
    csv_path = csv_path.replace('"', "").replace("\\", "/")
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)
    print(df)


def main():

    csv_path = input("Give path to csv file: ")
    display_data(csv_path)
