import pandas as pd
import numpy as np

currency = ['BTC', 'ETH', 'LTC', 'XRP']
bar_length = 90

"""
Alpha = -corr(close, volume, window)
&
ALpha = -corr(close, volume, window)*rank(-std(volume))
Actually here rank(-std(volume)) is like weight, ranging from 0 to 1.

The higher the degree of price-volume divergence, 
the greater the probability of increased excess returns.
"""

def handle_bar(counter, time, data, init_cash, transaction, cash_balance, 
               crypto_balance, total_balance, position_current, memory):
    
    position = position_current
    
    # Save data, length of the dataframe = bar_length
    if (counter == 0):
         memory.data_save = {i: pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume']) for i in currency}
    

    # 1 min before the excution, calculate the position
    if ((counter + 1) % bar_length == 0):
        corr = []
        close = []
        std = []
        for c in currency:
            memory.data_save[c].loc[bar_length - 1] = data[currency.index(c), ]
            corr.append(-memory.data_save[c]['close'].corr(memory.data_save[c]['volume']))
            close.append(memory.data_save[c]['close'].iat[-1])
            std.append(-memory.data_save[c]['volume'].std())
        
        # calculate rank(-std(volume)) as weight
        if (max(position) - min(position))==0:
            rank_std = np.repeat(1., 4)
        else:
            rank_std = [(x - min(position)) / (max(position) - min(position)) for x in position]
        
        # control the cash
        # cash of each currency are equal
        position += min([(x / y * z) * cash_balance * 0.25 for x, y, z in zip(corr, close, rank_std)]
                        , [(x / y * z) * 100000 * 0.25 for x, y, z in zip(corr, close, rank_std)])
    
    # save data and do nothing
    else:
        for c in currency:
            memory.data_save[c].loc[(counter + 1) % bar_length - 1] = data[currency.index(c), ]
    
    return position, memory
