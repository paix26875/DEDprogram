import pandas as pd

if __name__ == '__main__':
    dir_path = "/Users/paix/Desktop/Python_lab/calibration/time_average/"
    df = pd.read_csv(dir_path + 'data/src/sample_pandas_normal.csv', index_col=0)
    print(df)
    print(type(df))
    df.to_csv(dir_path + 'data/dst/to_csv_out.csv')