import pandas as pd


def up(kline):
    x = float(kline[4]) - float(kline[1])
    if x > 0:
        return x


def down(kline):
    x = float(kline[4]) - float(kline[1])
    if x < 0:
        return x


def get_RSI(candles, period):
    df = pd.DataFrame({"Close": [float(val[4]) for val in candles]})
    df_diff = df.Close.diff()
    up, down = df_diff.copy(), df_diff.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    rUp = up.ewm(com=period - 1, adjust=False).mean()
    rDown = down.ewm(com=period -1 , adjust=False).mean().abs()

    rsi = 100 - 100 / (1 + rUp / rDown)
    return rsi.values.tolist()[-1]
