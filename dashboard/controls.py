INSTRUCTION = 'This is a dashboard for assessing the accuracy of the predictions made by different financial institutions on the stock market.\n\n \
               Filter by stock - For selecting the stock you want to look at.\n \
               Filter by issuer - For selecting the issuer(s) you want to look at, multi-selection allowed.\n \
               Overview - Candlestick chart showing the price movements of selected stock and predictions made by the selected issuer(s). Users may also use the range slider at the bottom to filter for a specific timeframe.\n\n \
               To view the details of predictions made by an issuer, hover on any marker in the Candlestick chart.\n\n'

# Controls for webapp
USER = "udgiapuy"
PASSWORD = "HVaHbqd1S07gXIvUJYSJQFw_X0z25WhM"

TABLES = {'stock_predictions': ['id', 'ticker', 'company', 'issuer', 'spot', 'target_price', 'date_posted', 'stock_exist', 'fulfilled_date'], 'stock_history': ['id', 'ticker', 'company', 'dates', 'open', 'high', 'low', 'close', 'adj_close', 'volume']}