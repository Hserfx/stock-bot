import pandas as pd

df = pd.DataFrame({"a": [2, 4, 1, 5, 1]})

print(df.a.diff())
