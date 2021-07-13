import pandas as pd
import numpy as np

nInst = 100
currentPos = np.zeros(nInst)

def getMyPosition(prcSoFar):
    global currentPos

    (nins,nt) = prcSoFar.shape
    prcSoFar = pd.DataFrame(prcSoFar)

    short_ema = prcSoFar.ewm(span=5, adjust=False, axis=1).mean()
        # 5 day exponential moving average
    posSize = 10000
        #Max allowed size under competition rules
    buy = posSize
    sell = -posSize
    rpos = np.zeros(nInst)

    for i in range(100):
        # opens net long position the instrument if the price is far enough below the 5 day ema to cover commission if the price reverts
        if prcSoFar.iloc[i, -1] < (short_ema.iloc[i, -1] * 0.991):
            rpos[i] += round(buy/prcSoFar.iloc[i, -1])
        # opens net short position the instrument if the price is far enough below the 5 day ema to cover commission if the price reverts
        if prcSoFar.iloc[i, -1] > (short_ema.iloc[i, -1] * 1.009):
            rpos[i] += round(sell/prcSoFar.iloc[i, -1])
    
    currentPos = rpos
    # adapts the currentPos with the new position updates, defaults to no position without a strategy trigger
    return currentPos
