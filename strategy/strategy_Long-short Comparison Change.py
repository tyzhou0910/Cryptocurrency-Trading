import pandas as pd

currency = ['BTC', 'ETH', 'LTC', 'XRP']
bar_length = 30
rolling_window = 30
window1 = 20
window2 = 10

"""
Alpha = EWMA(α, window1) - EWMA(α, window2), window1>window2
α = volume*((close-low)-(high-close))/(high-low)


A larger factor value indicates a weakening of bullish relative to bearish power in the near term, 
while a smaller factor value suggests an increase in the contrast between long and short positions relative to the long-term.
"""

# EWMA calculation
def ema(df, window):
    ema_window = df['factor'].rolling(rolling_window, min_periods=10).apply(lambda x: x.ewm(span=window, adjust=False).mean().to_list()[-1]).iat[-1]
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
            
            ### We found that most of the time, open high low close are equal.
            ### So, we calculate the maximum of high, i.e. maxhigh as the "high" in the equation
            ### Same as low
            ### rolling_window here we choose 30, to ensure they are different
            ### otherwise the denominator will be 0
            
            df['maxhigh'] = df['high'].rolling(window=rolling_window, min_periods=1).max()
            df['minlow'] = df['low'].rolling(window=rolling_window, min_periods=1).min()
            
            ### factor = volume*((close-low)-(high-close))/(high-low)
            
            df['factor'] = df['volume']*(df['close']*2-df['minlow']-df['maxhigh'])/(df['maxhigh']-df['minlow'])
            
            ema_window1 = ema(df, window1)
            ema_window2 = ema(df, window2)
            
            # long
            if ema_window1 >= ema_window2:
                position[currency.index(c)] = cash_balance*0.25/close
            
            # short
            else:
                position[currency.index(c)] = -cash_balance*0.25/close
                    
    else:
        for c in currency:
            memory.data_save[c].loc[(counter + 1) % bar_length - 1] = data[currency.index(c), ]
    
    return position, memory

