import pandas as pd
import numpy as np

currency = ['BTC', 'ETH', 'LTC', 'XRP']
bar_length = 30
window = 20
std_length = 10

"""
Alpha = -std(volume)
Lower volatility represents an industry with stable bullish market sentiment
"""

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
            std_list = []
            for i in range(window):
                std_list.append(memory.data_save[c]['volume'][bar_length-i-std_length: bar_length-i].std())
            
            lower, upper = np.quantile(std_list, 0.5), np.quantile(std_list, 0.5)
            
            # We opt to long with lower volatility and short with higher volatility.
            if std_list[0] <= lower:
                position[currency.index(c)] = cash_balance*0.25/close
            
            elif std_list[0] >= upper:
                position[currency.index(c)] = -cash_balance*0.25/close
                    
    else:
        for c in currency:
            memory.data_save[c].loc[(counter + 1) % bar_length - 1] = data[currency.index(c), ]
    
    return position, memory

