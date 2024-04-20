# examples/connection.py

# Let's get this party started!
"""
from wsgiref.simple_server import make_server

import falcon


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class connectionResource:
    def on_get(self, req, resp):
        #Handles GET requests
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')


# falcon.App instances are callable WSGI apps...
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
connections = connectionResource()

# things will handle all requests to the '/things' URL path
app.add_route('/connection', connections)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
        """

# examples/connection.py

# Let's get this party started!
from wsgiref.simple_server import make_server
import falcon
import numpy as np
import requests
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px

# Function to fetch rainfall data for given latitude and longitude
def fetch_rainfall_data(latitude, longitude):
    # Your API key from OpenWeatherMap
    api_key = '89c929e06a0dd8c891226c5934e3201e'

    # Construct the API URL
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Initialize variable to store cumulative rainfall
        cumulative_rainfall = 0

        # Loop through the forecast data
        for forecast in data['list']:
            # Check if there's rainfall data available
            if 'rain' in forecast:
                cumulative_rainfall += forecast['rain'].get('3h', 0)  # Add rainfall if available

        # Divide the cumulative rainfall by 2 unless it exceeds 10, in which case set it to 5
        if cumulative_rainfall > 10:
            return 1
        else:
            return cumulative_rainfall / 10

# Load the trained model
clf_rf = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=350)

# Load CSV file with coordinates
csv_file = "http://localhost:8081/fyp/2/backend/Backend_data/Testing_data.csv"
df = pd.read_csv(csv_file)

# Falcon resource for handling connections
class ConnectionResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        # Iterate over each row
        for index, row in df.iterrows():
            latitude = row['Y']
            longitude = row['X']
            
            # Fetch rainfall data for the coordinates
            rainfall = fetch_rainfall_data(latitude, longitude)
            
            # Update the "Rainfall_B" column with the fetched rainfall value
            df.at[index, 'Rainfall_B'] = rainfall
        
        # Make predictions
        X = df.drop(columns=['X', 'Y', 'results'])  # Assuming you don't need these columns for prediction
        predictions = clf_rf.predict(X)
        
        # Update the 'results' column with predictions
        df['results'] = predictions
        
        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_file, index=False)
        
        # Plot the coordinates using Plotly Express
        fig = px.scatter_mapbox(df, lat="Y", lon="X", color="results",
                                color_discrete_sequence=["green", "red"], zoom=7)
        
        # Customize map layout
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        # Convert Plotly figure to JSON
        plot_json = fig.to_json()
        
        # Set Falcon response
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.body = plot_json

# Falcon App instance
app = falcon.App()

# Connect the resource to the '/connection' endpoint
connection = ConnectionResource()
app.add_route('/connection', connection)

# Start the server
if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
