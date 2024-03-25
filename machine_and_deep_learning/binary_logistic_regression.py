import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression

# Step 1: Load data
df = pd.read_csv('/content/shipping.csv')

# Step 2: Handle missing values (if any)
df.info(memory_usage='deep')

# Renaming the Reached.on.Time_Y.N to be more readable
df.rename(columns={"Reached.on.Time_Y.N":"on_time"}, inplace=True)

# Lowercase all column names
df = df.rename(columns={col: col.lower() for col in df.columns})
for column in df.columns:
    unique_values = df[column].nunique()
    print(f"Unique values in {column}: {unique_values}")

# Viewing statistics of all numerical features
df.describe().T

# Step 3: Normalize numerical features
scaler = MinMaxScaler()

numerical_features = df.select_dtypes(include=np.number).columns

df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Step 4: Label encode non-numerical features
encoder = LabelEncoder()

categorical_feature = df.select_dtypes(exclude=np.number).columns

for col in categorical_feature:
  df[col] = encoder.fit_transform(df[col])

# Step 5: Split the data
X = df.drop('on_time', axis=1)

y = df['on_time']

X_train, X_rem, y_train, y_rem = train_test_split(X, y, test_size=0.3, random_state=42)

X_val, X_test, y_val, y_test = train_test_split(X_rem, y_rem, test_size=0.5, random_state=42)

print(
    f'X_train: {X_train.shape = }'
    f'\nX_val: {X_val.shape = }'
    f'\nX_test: {X_test.shape = }'
    f'\ny_train: {y_train.shape = }'
    f'\ny_val: {y_val.shape = }'
    f'\ny_test: {y_test.shape = }'
)

# Step 6: Build the linear regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f'Accuracy: {accuracy}')

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)

print('Confusion Matrix:')

print(conf_matrix)

# Classification report
class_report = classification_report(y_test, y_pred)

print('Classification Report:')

print(class_report)