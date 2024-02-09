import pymongo
import pandas as pd
import plotly.express as px

# Connect to MongoDB 
client = pymongo.MongoClient('MongoDB_URL')  
db = client['database_name']  
collection = db['collection_name']  

# Query data for a single track run 
track_run_id = 'track_run_id'
query = {'track_run_id': track_run_id}
cursor = collection.find(query)

# Convert MongoDB cursor to DataFrame
df = pd.DataFrame(list(cursor))

# Define the analog variables (hover data)
analog_variables = ['Analog #1 (volts)', 'Analog #2 (volts)', 'Analog #3 (volts)',
                    'Analog #4 (volts)', 'Analog #5 (volts)', 'Analog #6 (volts)',
                    'Analog #7 (volts)', 'Analog #8 (volts)']

# Create scatter plot with multiple variables, including analogs in hover_data
fig = px.scatter(df, x='Time (sec)', y='RPM', color='MAP (psi)',
                 size='TPS (%)', hover_data=['Air Temp (F)', 'Coolant Temp (F)', 'Battery Volt (V)', 'Fuel Open Time (ms)'] + analog_variables)

# Customize the plot layout
fig.update_layout(title='Multiple Variables vs. Time for Track Run',
                  xaxis_title='Time (sec)',
                  yaxis_title='RPM')

# Show the plot
fig.show()