# from can import CSVReader
# from data_deserializer import MessageData
# import pandas as pd
# from tqdm import tqdm
import plotly.express as px
# file = 'can-_ecu_25.csv'

# df = pd.DataFrame()

# for msg in tqdm(CSVReader(file)):    
#     data = MessageData(msg)
    
#     new_df = pd.DataFrame({"timestamp": msg.timestamp, **data.to_dict()}, index=[0])
#     df = pd.concat([df, new_df])
    
    
# df.ffill(inplace=True)
# df.to_csv(f'ecu_data.csv', index=False)
import pandas as pd
df = pd.read_csv("ecu_data.csv")

df["Driven Avg Wheel Speed"] /= 1.467
df["Non-Driven Avg Wheel Speed"] /= 1.467

fig = px.line(df, x="timestamp", y=["Driven Avg Wheel Speed","Non-Driven Avg Wheel Speed"])

fig.show()