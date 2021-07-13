import pandas as pd
import numpy as np

nInst = 100
currentPos = np.zeros(nInst)

def getMyPosition(prcSoFar):
    global currentPos
    (nins,nt) = prcSoFar.shape
    prcSoFar = pd.DataFrame(prcSoFar)
    short_ema = prcSoFar.ewm(span=5, adjust=False, axis=1).mean()
    posSize = 2500
    buy = posSize
    sell = -posSize
    buy_big = posSize*4
    sell_big = -posSize*4
    rpos = np.zeros(nInst)
    trade_count = np.zeros(nInst)
    days = prcSoFar.shape[1]
    curr_pos = np.zeros(nInst)
    r_pos = np.zeros(nInst)
    stock_pnl = np.zeros(nInst)
    ev = np.zeros(nInst)
    
    
    for n in range(days):
        r_pos = np.zeros(nInst)
        for m in range(100):
            if prcSoFar.loc[m, n] < (short_ema.loc[m, n] * 0.991):
                r_pos[m] += round(buy_big/prcSoFar.loc[m, n])
            if prcSoFar.loc[m, n] > (short_ema.loc[m, n] * 1.009):
                r_pos[m] += round(sell_big/prcSoFar.loc[m, n])
            stock_pnl[m] += curr_pos[m] * prcSoFar.loc[m, n] - curr_pos[m] * prcSoFar.iloc[m, n-1]
                
        if n > 1:
            for j in range(0,100):
                if curr_pos[j]*prcSoFar.loc[j,n] != curr_pos[j]*prcSoFar.loc[j, n-1]:
                    trade_count[j] += 1
            
        curr_pos = r_pos

    for i in range(100):
        if trade_count[i] > 0:
            ev[i] = stock_pnl[i] / trade_count[i]
        if prcSoFar.loc[i, nt-1] < (short_ema.loc[i, nt-1] * 0.991):
            if ev[i] == 0:
                rpos[i] += round(buy/prcSoFar.loc[i, nt-1])
            if ev[i] > 0:
                rpos[i] += round(buy_big/prcSoFar.loc[i, nt-1])
        if prcSoFar.loc[i, nt-1] > (short_ema.loc[i, nt-1] * 1.009):
            if ev[i] == 0:
                rpos[i] += round(sell/prcSoFar.loc[i, nt-1])
            if ev[i] > 0:
                rpos[i] += round(sell_big/prcSoFar.loc[i, nt-1])
                
    currentPos = rpos
    return currentPos
