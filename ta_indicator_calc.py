import numpy as numpy
import talib as ta

def rsi ( quote ):    
    rsi = ta.RSI(numpy.array(quote))
    return rsi[-1];
    
def macd ( quote ):
    macddiv, macdsignal, macdhist = ta.MACD(numpy.array(quote), fastperiod=12, slowperiod=26, signalperiod=9)        
    return macddiv, macdsignal, macdhist;

def macd_dif ( quote ):
    macddiv, macdsignal, macdhist = macd(quote)
    diff = macdsignal - macddiv
    return diff;
    
# TODO: Find how to write the K part. 
def J ( quote ):
    STOCH_K, STOCH_D = ta.STOCH(numpy.array(quote.High), numpy.array(quote.Low), numpy.array(quote.Close),slowk_period=14,slowd_period=3)
    j = 3 * STOCH_K - 2 * STOCH_D
    return j[-1];
       
'''
print(numpy.array(aapl.Close))
#closeprice = ta.SMA(numpy.array(aapl.Close)) # Avoid Argument 'real' has incorrect type (expected numpy.ndarray, got Series) error. 
sma = ta.SMA(numpy.array(aapl.Close))
print(sma)
rsi = ta.RSI(numpy.array(aapl.Close))
print(rsi)

macddiv, macdsignal, macdhist = ta.MACD(numpy.array(aapl.Close), fastperiod=12, slowperiod=26, signalperiod=9)

cross = macdsignal - macddiv

print("MACD cross is ")
print(cross)

 
'''