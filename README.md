# Cryptocurrency-Trading

Artificial Intelligence in Fintech Course Project

This study proposes several innovative trading strategies for cryptocurrency markets. Each strategy is designed to exploit specific market conditions and maximize profit
potential. Extensive backtesting and performance analysis are conducted to evaluate the effectiveness of each strategy.

## Overview of Data Structure
![price volume](https://github.com/tyzhou0910/Cryptocurrency-Trading/assets/147459488/1c1b1c57-2c87-4c25-b7ba-d706e79460bc)


## Price-Volume Factors
<table>
    <tr>
        <th>Category</th><th>Strategy</th><th>Formula</th>
    </tr>
    <tr>
        <td rowspan="2">Momentum</td><td>Golden Cross</td><td>$EWMA(Close, window_1)−EWMA(Close, window_2)$</td>
    </tr>
    <tr>
        <td> Momentum Term Spread </td><td> $\frac{Close_t-Close_{t-window_1}}{Close_{t-window_1}} - \frac{Close_t-Close_{t-window_2}}{Close_{t-window_2}}$ </td>
    </tr>
    <tr>
        <td rowspan="3">Volatility</td><td>Volume Volatility</td><td>$−std(Volume)$</td>
    </tr>
    <tr>
        <td>Price Change Volatility </td><td> $abs(Open − Close) ∗ std(Close)$ </td>
    </tr>
    <tr>
        <td> Return Volatility </td><td> $\log{\frac{Open-Close}{Open}} / std(Close)$ </td>
    </tr>
    <tr>
        <td> Price-Volume Divergence </td><td> Price-Volume Correlation </td><td> $−corr(Close, Volume, window)$ </td>
    </tr>
    <tr>
        <td> Long-Short Comparison </td><td> LS Comparison Change </td><td> $EWMA(\alpha, window_1)-EWMA(\alpha, window_2),$ <br> $\alpha=Volume×\frac{(Close-Low)-(High-close)}{High-Low}$ </td>
    </tr>
    
</table>
