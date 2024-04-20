import numpy as np
import requests
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer


def fetch_rainfall_data(latitude, longitude, api_key='89c929e06a0dd8c891226c5934e3201e'):
    """Fetches rainfall data from OpenWeatherMap API for given coordinates.

    Args:
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
        api_key (str, optional): OpenWeatherMap API key. Defaults to '89c929e06a0dd8c891226c5934e3201e'.

    Returns:
        float: Cumulative rainfall (divided by 2 or set to 5).
               None if error fetching data.
    """

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cumulative_rainfall = 0
        for forecast in data['list']:
            if 'rain' in forecast:
                cumulative_rainfall += forecast['rain'].get('3h', 0)

        return min(cumulative_rainfall / 2, 5)  # Max rainfall of 5
    else:
        print("Error fetching rainfall data from OpenWeatherMap API.")
        return None


def preprocess_landslide_data(data_path):
    """Preprocesses landslide training data (handling missing values, etc.).

    Args:
        data_path (str): Path to the CSV file containing landslide data.

    Returns:
        pandas.DataFrame: Preprocessed landslide data.
    """

    df = pd.read_csv(data_path)
    numerical = df.select_dtypes('number').columns
    categorical = df.select_dtypes('object').columns

    df.replace(-9999, np.nan, inplace=True)
    df.interpolate(method='spline', order=5, inplace=True)

    imputer = SimpleImputer(strategy='mean')
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    X = df.drop("landslide_", axis=1)
    y = df["landslide_"]
    return X, y


def train_random_forest_model(X_train, y_train):
    """Trains a Random Forest classifier for landslide prediction.

    Args:
        X_train (pandas.DataFrame): Training features.
        y_train (pandas.Series): Training labels.

    Returns:
        sklearn.ensemble.RandomForestClassifier: Trained Random Forest model.
    """

    clf_rf = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=350)
    clf_rf.fit(X_train, y_train)
    return clf_rf


def predict_landslides(model, data):
    """Predicts landslide probabilities for new data using the trained model.

    Args:
        model (sklearn.ensemble.RandomForestClassifier): Trained Random Forest model.
        data (pandas.DataFrame): New data to predict landslides for.

    Returns:
        pandas.Series: Predicted landslide probabilities (0 or 1).
    """

    data.replace(-9999, np.nan, inplace=True)
    data.interpolate(method='spline', order=5, inplace=True)

    imputer = SimpleImputer(strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)
    return model.predict(data)


def update_csv_with_predictions(data_path, predictions):
    """Updates a CSV file with predicted landslide probabilities.

    Args:
        data_path (str): Path to the CSV file containing coordinates.
        predictions (pandas.Series): Predicted landslide probabilities.
    """

    existing_df = pd.read_csv(data_path)
    existing_df['results'] = predictions
    existing_df.to_csv(data_path, index=False)
def visualize_predictions(data_path, predictions):
    """Visualizes predicted landslide probabilities on a map using Plotly.

    Args:
        data_path (str): Path to the CSV file containing coordinates.
        predictions (pandas.Series): Predicted landslide probabilities.
    """

    data = pd.read_csv(data_path)
    data['results'] = predictions

    fig = px.scatter_mapbox(data, lat="X", lon="Y", color="results",
                            color_discrete_sequence=["green", "red"], zoom=10)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


if __name__ == "__main__":
    # Example usage (replace paths with your actual file paths)
    data_path = "C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/fyp/2/backend/temprory_backend_data/test.csv"
    landslide_data_path = "C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/fyp/2/backend/temprory_backend_data/landslide_training_table.csv"

    # Fetch rainfall data (assuming coordinates are in the data)
    data = pd.read_csv(data_path)
    data['rainfall_B'] = data.apply(lambda row: fetch_rainfall_data(row['X'], row['Y']), axis=1)

    # Preprocess landslide data
    X, y = preprocess_landslide_data(landslide_data_path)

    # Train the model
    model = train_random_forest_model(X_train, y_train)

    # Predict landslides for the test data
    predictions = predict_landslides(model, data.drop(columns=['X', 'Y', 'results']))

    # Update the CSV file with predictions
    update_csv_with_predictions(data_path, predictions)

    # Visualize the predictions
    visualize_predictions(data_path, predictions)

