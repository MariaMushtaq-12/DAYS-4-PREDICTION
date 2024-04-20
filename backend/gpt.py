import numpy as np
import requests
import pandas as pd
import plotly.express as px
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def fetch_rainfall_data(latitude, longitude):
    api_key = '89c929e06a0dd8c891226c5934e3201e'
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cumulative_rainfall = 0
        for forecast in data['list']:
            if 'rain' in forecast:
                cumulative_rainfall += forecast['rain'].get('3h', 0)
        if cumulative_rainfall > 10:
            return 5
        else:
            return cumulative_rainfall / 2
    else:
        print("Error fetching data from the API.")
        return None

def preprocess_data(df):
    missing_values_count = (df == -9999).sum()
    df.replace(-9999, np.nan, inplace=True)
    df.interpolate(method='spline', order=5, inplace=True)
    df.replace(-9999.0, np.nan, inplace=True)
    imputer = SimpleImputer(strategy='mean')
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    return df

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=True)
    clf_rf = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=350)
    clf_rf.fit(X_train, y_train)
    return clf_rf

def predict_landslide(df, model):
    X = df.drop(columns=['X', 'Y', 'results'])
    return model.predict(X)

def update_results_in_csv(predictions, csv_file):
    existing_df = pd.read_csv(csv_file)
    existing_df['results'] = predictions
    existing_df.to_csv(csv_file, index=False)

def plot_results_on_map(csv_file):
    data = pd.read_csv(csv_file)
    fig = px.scatter_mapbox(data, lat="X", lon="Y", color="results",
                            color_discrete_sequence=["green", "red"], zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

def main():
    # Read CSV file with coordinates
    csv_file = r"C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/fyp/2/backend/temprory_backend_data/test.csv"
    df = pd.read_csv(csv_file)
    
    # Fetch rainfall data for each coordinate
    df['rainfall_B'] = df.apply(lambda row: fetch_rainfall_data(row['X'], row['Y']), axis=1)
    
    # Preprocess landslide data
    LS_df = pd.read_csv("C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/fyp/2/backend/temprory_backend_data/landslide_training_table.csv")
    LS_df = preprocess_data(LS_df)
    
    # Train Random Forest model
    X = LS_df.drop("landslide_", axis=1)
    y = LS_df['landslide_']
    model = train_model(X, y)
    
    # Predict landslide using trained model
    predictions = predict_landslide(df, model)
    
    # Update results in CSV file
    update_results_in_csv(predictions, csv_file)
    
    # Plot results on map
    plot_results_on_map(csv_file)

if __name__ == "__main__":
    main()
