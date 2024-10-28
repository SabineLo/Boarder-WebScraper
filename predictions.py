import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load and preprocess data
data = pd.read_csv('borderData.csv')

# Rename columns to remove spaces
data.columns = data.columns.str.replace(' ', '_')

# Replace non-standard time representations with standard formats
data['Time'] = data['Time'].replace({
    'Midnight': '12:00 AM',
    'Noon': '12:00 PM'
})

# Convert Date and Time to datetime
data['Date'] = pd.to_datetime(data['Date'])
data['Hour'] = pd.to_datetime(data['Time'], format='%I:%M %p').dt.hour

# Create additional features
data['day_of_week'] = data['Date'].dt.dayofweek  
data['previous_wait_time'] = data['Today_(min)'].shift(1).fillna(0)  

# Example feature selection
features = data[['day_of_week', 'Hour', 'previous_wait_time']]
target = data['Average_(min)']

# Split data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Absolute Error: {mae}')
