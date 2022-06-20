import pandas as pd


def main():
    listing_dict = [
        {'bcx':11,'buy_price':5777.0},
        {'bcx':1,'buy_price':540.0},
        {'bcx':2,'buy_price':1100.0},
        {'bcx':1,'buy_price':600.0},
        {'bcx':11,'buy_price':6999.0},
        {'bcx':3,'buy_price':2250.0},
        {'bcx':3,'buy_price':2300.0},
        {'bcx':11,'buy_price':10369.369},
        {'bcx':1,'buy_price':1900.0},
    ]

    df = pd.DataFrame(listing_dict)
    return df.sort_values(by=['bcx'],ascending = False).reset_index()

if __name__=='__main__':
    main()