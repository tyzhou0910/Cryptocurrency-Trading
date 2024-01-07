import pandas as pd
import numpy as np

currency = ['BTC', 'ETH', 'LTC', 'XRP']
bar_length = 32 
factor_length = 22
window1 = 10
window2 = 5


"""
Alpha = Long-term momentum - Short-term momentum
Momentum Term Spread: filter short-term noise
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
            cvec = memory.data_save[c]['close']
            f_list = []
            for i in range(factor_length):
                
                # Long-term momentum - Short-term momentum
                f_list.append((cvec.iat[-i-1] - cvec.iat[-i-window1])/cvec.iat[-i-window1] - 
                              (cvec.iat[-i-1] - cvec.iat[-i-window2])/cvec.iat[-i-window2])
            
            percentile = (np.searchsorted(np.sort(f_list), f_list[0])+1)/len(f_list)
            
            lower, upper = 0.4, 0.6
            
            # short
            ### When Long-term momentum < Short-term momentum
            if percentile <= lower:
                position[currency.index(c)] = -cash_balance*(1-percentile)*0.4/cvec.iat[-1]
                #print('Short ',c,-cash_balance*0.25," dollar")
                #print(percentile)
            
            # long
            ### When Long-term momentum > Short-term momentum
            ### which means, after filtering out some of this short-term volatility,
            ### Still have longer-term trend 
            elif percentile >= upper:
                position[currency.index(c)] = cash_balance*percentile*0.4/cvec.iat[-1]
                #print('Long ',c,min(cash_balance*0.25, 10000)," dollar")
                #print(percentile)
    else:
        for c in currency:
            memory.data_save[c].loc[(counter + 1) % bar_length - 1] = data[currency.index(c), ]
    
    return position, memory
