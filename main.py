#Get the main flow. 
'''
https://cryptotrader.org/talib

Latest Status:
Implement ADXR and applied into confidence.
Implement ADX and its trend check to recommendation, but not applied
bull power and bear power is implemented, but not applied. 
Implement the volumn detect

e.g. RSI Do not calculation multiple time, Calculate once just use the last five element in the array?
Check all the [-1] is correctly return the value. 
Need condiser the back testing. 
When to buy a stock. 
When to sell a stock.

Profit / Loss if followe the strategy. 

e.g. When recommendation > 1.5 buy stock at the high of next day. 
     Watch and when recommendation < -0.5 sell that stock at the low of next day. 
     transaction is fixed at 30.  
'''

import ta_indicator_calc as ind_calc
import recommendation as rec_calc
from recommendation import GetRecommendation
import parameters as param
import time

def CalculateRecommendation(*args):
    '''
        Calculation the recommendation based on the quote input
        input:  1. quote of symbol
                2. option: data shift from today, to calculate recommendation of previous days. default 1
        output:  macd, macd_pos, rsi, j, adxr,recommendation        
    '''
    
    quote = args[0]
    if (len(args) == 2):
        data_shift = args[1]
    else:
        data_shift = 0
    rec = 0 
    macd_r = 0
    macd_pos = 0
    rsi_today = 0
    j = 0    
    adx = 0
    adx_trend = 0
    adx_r = 0
    adxr = 0
    
    if not(isinstance(quote, str)):         
        rsi_today = ind_calc.rsi(quote.Close)
        macd_diff, macd_pos = ind_calc.macd_dif(quote.Close)   
        j = ind_calc.J(quote)
        #adx, adx_trend = ind_calc.ADX(quote)
        if len(ind_calc.ADXR(quote)) > 1:
            adxr = ind_calc.ADXR(quote)[-1]
        quote_lastday = quote.iloc[-1]        
        if not(isinstance(quote_lastday, str)):
            rec, macd_r, macd_pos = GetRecommendation(rsi_today,macd_diff,macd_pos, j, adxr,quote_lastday)  
            print("Final recommendation of ", symbol , " is ", rec)             
        else:
            print("No last day quote, no recommendation.") 
                                                     
    else:
        print("No Quote for ", symbol)
    
    return macd_r, macd_pos, rsi_today, j, adxr, rec    


def CalculateTrend(*args):
    '''
    Calculate the trend following the K.Lien instruction.
    '''
    quote = args[0]

    if (len(args) == 2):
        data_shift = args[1]
    else:
        data_shift = 0

    issma20 = False
    issma50 = False
    issma100 = False
    isbollinger = False
    isadx = False

    if not(isinstance(quote, str)):      
        sma20 = ind_calc.SMA(quote, 20)   
        sma50 = ind_calc.SMA(quote, 50)
        sma100 = ind_calc.SMA(quote, 100)
        bollinger = ind_calc.Bollinger(quote,1)[0]
        bollinger2 = ind_calc.Bollinger(quote,2)[0]
        if len(ind_calc.ADXR(quote)) > 1:
            adxr = ind_calc.ADXR(quote)[-1]
        if len(ind_calc.ADX(quote)) > 1:
            adx = ind_calc.ADXR(quote)[-1]
        quote_lastday = quote.iloc[-1]        
        if not(isinstance(quote_lastday, str)):
            if (adx > 25):
                isadx = True
            print("Last close are " , quote.Close[-1] , " & " , quote.Close[-2])
            issma20 = rec_calc.isCross(quote.Close, sma20)
            print("Last sma20 are " , sma20[-1] , " & " , sma20[-2])
            issma50 = rec_calc.isCross(quote.Close, sma50)
            print("Last sma50 are " , sma50[-1] , " & " , sma50[-2])
            issma100 = rec_calc.isCross(quote.Close, sma100)
            print("Last sma100 are " , sma100[-1] , " & " , sma100[-2])
            isbollinger = rec_calc.isCrossBollinger(quote.Close, bollinger)
            print("Last Bollinger are " , bollinger[-1] , " & " , bollinger[-2])

            isAboveSMA20 = quote.Close[-1] > sma20[-1]
            isAboveSMA50 = quote.Close[-1] > sma50[-1]
            isAboveSMA100 = quote.Close[-1] > sma100[-1]
            isAboveBollinger1 = quote.Close[-1] > bollinger[-1]
            isBelowBollinger2 = quote.Close[-1] <= bollinger2[-1] and quote.Close[-1] >= bollinger[-1]
        else:
            print("No last day quote, no recommendation.")                                                      
    else:
        print("No Quote for ", symbol)
    
    return isadx,issma20, issma50, issma100, isbollinger, isAboveSMA20, isAboveSMA50, isAboveSMA100, isAboveBollinger1, isBelowBollinger2    

#Create a blank file
from recommendation import CleanRecommendation
CleanRecommendation(param.BUYLIST)
CleanRecommendation(param.SELLLIST)


# Get the symbols from the text files.
from stock import GetStockSymbol
symbols = GetStockSymbol(param.STOCKLIST_CPH, param.CPHEXCHANGE) +  GetStockSymbol(param.STOCKLIST_AMS) + GetStockSymbol(param.STOCKLIST_FX, param.FXEXCHANGE)
porto_symbols = GetStockSymbol(param.MYPF)
#symbols = ['SALB.CO', 'GEN.CO', 'SIM.CO', 'NOVO-B.CO','PAAL-B'] 
#symbols = ['NOVO-B.CO']
#symbols = ['EUR=X', 'JPY=X']
from stock import GetStockQuote
from recommendation import WriteRecommendation
import ReportManager as rm

## dd/mm/yyyy format
today = time.strftime("%d/%m/%Y")

rm.CreateHTMLFile(param.HTML_REPORT_FILENAME)   #Create the header part of HTML report
rm.CreateHTMLFile(param.HTML_PORTOFOLIO_REPORT_FULLNAME)
rm.CreateHTMLFile(param.HTML_TREND_REPORT_FILENAME, "Trend Report")
line = ["Symbol ",  today +" Close", today + " High", today + "Low", "10-Day High", "10-Day Low", " Recommendation", "ADX > 25", "Cross SMA20", "Cross SMA50", "Cross SMA100", "Cross Bollinger", "Abover SMA20", "Above SMA50", "Above SMA100", "Above Bollinger 1", "Between Bollinger 1 & 2", "MACD Diff" ,"ADXR", "RSI", "J"]
rm.AddLineToHTMLTable(param.HTML_TREND_REPORT_FILENAME, line)

for symbol in symbols:    
    print(symbol)            
    quote = GetStockQuote(symbol, param.QUOTE_LENGTH, 0)
    if (len(quote) > param.QUOTE_LENGTH * 0.5):  #if not enough valid quote, do not calculate.
        quote.index =quote.index.map(lambda t: t.strftime('%Y-%m-%d'))
        line = ['', '', quote.index[len(quote)-1], quote.index[len(quote)-2],quote.index[len(quote)-3], quote.index[len(quote)-4], quote.index[len(quote)-5]]         
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)
        quote_shift = quote[4:len(quote)]
        macd_r, macd_pos, rsi, j, adxr, rec = CalculateRecommendation(quote_shift,0)  # Today's recommendation
        
        if (rec > 1):
            WriteRecommendation(symbol, rec, param.BUYLIST)   # Only write those may buy
        elif (rec<=-1):
            WriteRecommendation(symbol, rec, param.SELLLIST)  # only write those need sell.         

        quote_shift = quote[3:len(quote)-1]
        macd_r_1, macd_pos_1, rsi_1, j_1, adxr_1, rec_1 = CalculateRecommendation(quote_shift, 0)
        quote_shift = quote[2:len(quote)-2]
        macd_r_2, macd_pos_2, rsi_2, j_2, adxr_2, rec_2 = CalculateRecommendation(quote_shift, 0)
        quote_shift = quote[1:len(quote)-3]    
        macd_r_3, macd_pos_3, rsi_3, j_3, adxr_3, rec_3 = CalculateRecommendation(quote_shift, 0)
        quote_shift = quote[0:len(quote)-4]    
        macd_r_4, macd_pos_4, rsi_4, j_4, adxr_4, rec_4 = CalculateRecommendation(quote_shift, 0)
        
        
        line = [symbol, param.MACD_TYPE, macd_r , macd_r_1, macd_r_2 , macd_r_3 , macd_r_4]
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)
        if symbol in porto_symbols:
            rm.AddLineToHTMLTable(param.HTML_PORTOFOLIO_REPORT_FULLNAME, line)
        line = [symbol, param.MACD_POS_TYPE, macd_pos , macd_pos_1 , macd_pos_2 , macd_pos_3,macd_pos_4]
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)    
        if symbol in porto_symbols:
            rm.AddLineToHTMLTable(param.HTML_PORTOFOLIO_REPORT_FULLNAME, line)
        line = [symbol, param.ADXR_TYPE, adxr , adxr_1 , adxr_2 , adxr_3,adxr_4]
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)    
        if symbol in porto_symbols:
            rm.AddLineToHTMLTable(param.HTML_PORTOFOLIO_REPORT_FULLNAME, line)
        line = [symbol, param.RSI_TYPE, rsi , rsi_1 , rsi_2 , rsi_3 , rsi_4]          
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)    
        if symbol in porto_symbols:
            rm.AddLineToHTMLTable(param.HTML_PORTOFOLIO_REPORT_FULLNAME, line)
        line = [symbol, param.J_TYPE, j , j_1 , j_2 , j_3 , j_4]
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)
        if symbol in porto_symbols:
            rm.AddLineToHTMLTable(param.HTML_PORTOFOLIO_REPORT_FULLNAME, line)
        line = [symbol, param.RECOMMENDATION_TYPE, rec , rec_1 , rec_2 , rec_3 , rec_4]
        rm.AddLineToHTMLTable(param.HTML_REPORT_FILENAME, line)    
        if symbol in porto_symbols:
            rm.AddLineToHTMLTable(param.HTML_PORTOFOLIO_REPORT_FULLNAME, line)        
        
        
        counter = 0
        isadx,issma20, issma50, issma100, isbollinger,isAboveSMA20, isAboveSMA50, isAboveSMA100, isAboveBollinger1, isBelowBollinger2 = CalculateTrend(quote)
        for _ in [isadx,issma20, issma50, issma100, isbollinger]:
            if(_):
                counter = counter + 1
        line = [symbol, quote.Close[-1], quote.High[-1], quote.Low[-1], max(quote.High[len(quote.High)-10:len(quote.High)]), min(quote.Low[len(quote.Low)-10:len(quote.High)]),counter, isadx, issma20, issma50, issma100, isbollinger, isAboveSMA20, isAboveSMA50, isAboveSMA100, isAboveBollinger1, isBelowBollinger2, macd_r, adxr,rsi,j]
        rm.AddLineToHTMLTable2(param.HTML_TREND_REPORT_FILENAME, line)        

    else:
        print(symbol, " does not have enough valid quotes to calculation the recommendation")
        
rm.CloseHTMLFile(param.HTML_REPORT_FILENAME)  # write the rest of HTML.  
rm.CloseHTMLFile(param.HTML_PORTOFOLIO_REPORT_FULLNAME)

from ftpupload import UploadFileToFTP
UploadFileToFTP() 

