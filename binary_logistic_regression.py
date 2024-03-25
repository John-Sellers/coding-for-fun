{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOjHnT5Yh6esDvm7EXtRglq",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/John-Sellers/coding-for-fun/blob/dev/binary_logistic_regression.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler\n",
        "from sklearn.linear_model import LinearRegression\n",
        "from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report, confusion_matrix\n",
        "from sklearn.linear_model import LogisticRegression\n",
        "\n",
        "# Step 1: Load data\n",
        "df = pd.read_csv('/content/shipping.csv')\n",
        "df\n",
        "# Step 2: Handle missing values (if any)\n",
        "df.info(memory_usage='deep')\n",
        "# Renaming the Reached.on.Time_Y.N to be more readable\n",
        "df.rename(columns={\"Reached.on.Time_Y.N\":\"on_time\"}, inplace=True)\n",
        "\n",
        "# Lowercase all column names\n",
        "df = df.rename(columns={col: col.lower() for col in df.columns})\n",
        "for column in df.columns:\n",
        "    unique_values = df[column].nunique()\n",
        "    print(f\"Unique values in {column}: {unique_values}\")\n",
        "df.describe().T\n",
        "\n",
        "# Step 3: Normalize numerical features\n",
        "scaler = MinMaxScaler()\n",
        "numerical_features = df.select_dtypes(include=np.number).columns\n",
        "df[numerical_features] = scaler.fit_transform(df[numerical_features])\n",
        "\n",
        "# Step 4: Label encode non-numerical features\n",
        "encoder = LabelEncoder()\n",
        "categorical_feature = df.select_dtypes(exclude=np.number).columns\n",
        "\n",
        "for col in categorical_feature:\n",
        "  df[col] = encoder.fit_transform(df[col])\n",
        "\n",
        "# Step 5: Split the data\n",
        "X = df.drop('on_time', axis=1)\n",
        "y = df['on_time']\n",
        "X_train, X_rem, y_train, y_rem = train_test_split(X, y, test_size=0.3, random_state=42)\n",
        "X_val, X_test, y_val, y_test = train_test_split(X_rem, y_rem, test_size=0.5, random_state=42)\n",
        "\n",
        "print(\n",
        "    f'X_train: {X_train.shape = }'\n",
        "    f'\\nX_val: {X_val.shape = }'\n",
        "    f'\\nX_test: {X_test.shape = }'\n",
        "    f'\\ny_train: {y_train.shape = }'\n",
        "    f'\\ny_val: {y_val.shape = }'\n",
        "    f'\\ny_test: {y_test.shape = }'\n",
        ")\n",
        "\n",
        "# Step 6: Build the linear regression model\n",
        "model = LogisticRegression()\n",
        "model.fit(X_train, y_train)\n",
        "\n",
        "# Make predictions\n",
        "y_pred = model.predict(X_test)\n",
        "y_pred\n",
        "\n",
        "# Evaluate accuracy\n",
        "accuracy = accuracy_score(y_test, y_pred)\n",
        "print(f'Accuracy: {accuracy}')\n",
        "\n",
        "# Confusion matrix\n",
        "conf_matrix = confusion_matrix(y_test, y_pred)\n",
        "print('Confusion Matrix:')\n",
        "print(conf_matrix)\n",
        "\n",
        "# Classification report\n",
        "class_report = classification_report(y_test, y_pred)\n",
        "print('Classification Report:')\n",
        "print(class_report)"
      ],
      "metadata": {
        "id": "04qy71C3KMPC"
      },
      "execution_count": 37,
      "outputs": []
    }
  ]
}