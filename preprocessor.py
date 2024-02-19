import pandas as pd

def preprocessor(df,region):

    # flitering in dataset by summer column
    df=df[df['Season']=='Summer']
    # merging df and region to gether based on "NOC" column
    df=df.merge(region,on="NOC",how="left")
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df

