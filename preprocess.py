import pandas as pd



def process(df,region):
    
# filtering for summer olympics
    df = df[df['Season'] == 'Summer']
# merging with region
    df = df.merge(region, on = 'NOC', how='left')
# droppping duplicates
    df.drop_duplicates(inplace=True)
# one hot encoding model
    df = pd.concat([df,pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df