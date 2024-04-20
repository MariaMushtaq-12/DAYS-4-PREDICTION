import numpy as np
import requests
import pandas as pd
import pandas as pd
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
            return 5
        else:
            return cumulative_rainfall / 2

    else:
        print("Error fetching data from the API.")
        return None

# Function to update rainfall data in a CSV file
def update_rainfall_data_in_csv(csv_file):
    df = pd.read_csv(csv_file)

    # Iterate over each row
    for index, row in df.iterrows():
        latitude = row['X']
        longitude = row['Y']

        # Fetch rainfall data for the coordinates
        rainfall = fetch_rainfall_data(latitude, longitude)

        # Update the "rainfall_B" column with the fetched rainfall value
        df.at[index, 'rainfall_B'] = rainfall

    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

# Function to preprocess the landslide training data
def preprocess_landslide_data(csv_file):
    LS_df = pd.read_csv(csv_file)

    numerical=LS_df.select_dtypes('number').columns
    categorical = LS_df.select_dtypes('object').columns

    # Count occurrences of -9999 in each column
    missing_values_count = (LS_df == -9999).sum()
    LS_df.replace(-9999, np.nan, inplace=True)

    # Interpolate NaN values using spline interpolation
    LS_df.interpolate(method='spline', order=5, inplace=True)

    from sklearn.impute import SimpleImputer
    # Replace -9999.0 with NaN
    LS_df.replace(-9999.0, np.nan, inplace=True)

    # Handle missing values
    imputer = SimpleImputer(strategy='mean')  # You can use other strategies like median or most_frequent
    LS_df = pd.DataFrame(imputer.fit_transform(LS_df), columns=LS_df.columns)

    return LS_df

# Function to train the Random Forest model
def train_random_forest_model(X, y):
    from sklearn.ensemble import RandomForestClassifier
    clf_rf = RandomForestClassifier(n_estimators=5, max_depth=3,random_state=350)
    clf_rf.fit(X, y)
    return clf_rf

# Function to predict landslide results using the trained model
def predict_landslide_results(model, X):
    return model.predict(X)

# Function to update the results in the CSV file
def update_results_in_csv(existing_df, rf_pred):
    # Assuming rf_pred is your DataFrame containing the results
    # You may need to adjust the column names if they are different
    rf_pred = pd.DataFrame(rf_pred, columns=['results'])

    # Replace the existing 'results' column with the new values
    existing_df['results'] = rf_pred['results']

    # Save the modified DataFrame back to the CSV file
    existing_df.to_csv("C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/fyp/2/backend/temprory_backend_data/test.csv", index=False)

# Function to plot the results on a map
def plot_results_on_map(data):
    # Plot the coordinates using Plotly Express
    fig = px.scatter_mapbox(data, lat="X", lon="Y", color="results",
                            color_discrete_sequence=["green", "red"], zoom=10)

    # Customize map layout
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Show the plot
    fig.show()

# Example usage of the functions
csv_file = r"C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/fyp/2/backend/temprory_backend_data/test.csv"
update_rainfall_data_in_csv(csv_file)
