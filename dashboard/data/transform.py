import pandas as pd

df_history = pd.read_csv('stock_history.csv').drop(['id'], axis=1)
df_predictions = pd.read_csv('stock_predictions.csv').drop(['id'], axis=1)

print(df_history.head())
print(df_predictions[df_predictions.ticker == 700])

for ticker in df_predictions.ticker.unique():
     try:
          company_name = df_history[df_history.ticker == ticker]['company'].values[0]
     except:
          continue
     df_predictions.loc[df_predictions.ticker == ticker, 'company'] = company_name

print(df_predictions[df_predictions.ticker == 700])

df_predictions.to_csv('stock_predictions.csv')