import pandas as pd

currency = ['BTC', 'ETH', 'LTC', 'XRP']
bar_length = 30
rolling_window = 30
window1 = 20
window2 = 10


"""
Alpha = EWMA(Close, window1)-EWMA(Close, window2)
"""

# EWMA calculation
def ema(df, window):
    ema_window = df['close'].rolling(rolling_window, min_periods=10).apply(lambda x: x.ewm(span=window, adjust=False).mean().to_list()[-1]).iat[-1]
    return ema_window

def handle_bar(counter, time, data, init_cash, transaction, cash_balance, 
               crypto_balance, total_balance, position_current, memory):
    
    position = position_current
    
    # Save data, length of the dataframe = bar_length
    if (counter == 0):
         memory.data_save = {i: pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume']) for i in currency}

    if ((counter + 1) % bar_length == 0):
        for c in currency:
            memory.data_save[c].loc[bar_length - 1] = data[currency.index(c), ]
            close = memory.data_save[c]['close'].iat[-1]
            
            df = memory.data_save[c].copy()
            ema_window1 = ema(df, window1)
            ema_window2 = ema(df, window2)           
            
            ### When the short-term EWMA crosses above the long-term EWMA, forming a Golden Cross, 
            ### it may be considered a buy signal, indicating a potential upward trend.
            if ema_window1 >= ema_window2:
                position[currency.index(c)] = cash_balance*0.25/close
            
            ### When the short-term EWMA crosses below the long-term EWMA, forming a Death Cross, 
            ### it may be considered a sell signal, indicating a potential downward trend.
            else:
                position[currency.index(c)] = -cash_balance*0.25/close
            
    # save data and do nothing       
    else:
        for c in currency:
            memory.data_save[c].loc[(counter + 1) % bar_length - 1] = data[currency.index(c), ]
    
    return position, memory

