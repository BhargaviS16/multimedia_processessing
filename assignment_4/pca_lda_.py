# -*- coding: utf-8 -*-
"""pca_lda.

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oNM9DG4tmWvV6bWG8ry6yJK2q8GXkDCr
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from matplotlib.colors import ListedColormap

# Load the dataset
dataset_path = "/content/Dry_Bean_Dataset.csv"  # Update path if needed
bean_data = pd.read_csv(dataset_path)

# Encode the target variable (Class)
encoder = LabelEncoder()
bean_data["Class"] = encoder.fit_transform(bean_data["Class"])

# Separate features and target
features = bean_data.drop("Class", axis=1)
target = bean_data["Class"]

# Standardize the features
feature_scaler = StandardScaler()
scaled_features = feature_scaler.fit_transform(features)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, test_size=0.2, random_state=42, stratify=target)

# Apply PCA for dimensionality reduction
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Apply LDA for dimensionality reduction
lda = LDA(n_components=len(np.unique(target)) - 1)
X_train_lda = lda.fit_transform(X_train, y_train)
X_test_lda = lda.transform(X_test)

# Train Logistic Regression on PCA and LDA transformed data
logistic_pca = LogisticRegression(max_iter=1000)
logistic_pca.fit(X_train_pca, y_train)

logistic_lda = LogisticRegression(max_iter=1000)
logistic_lda.fit(X_train_lda, y_train)

# Function to plot decision regions
def plot_decision_boundaries(X, y, model, title, x_label, y_label):
    colors = ('red', 'blue', 'green', 'purple', 'orange', 'pink', 'gray')
    color_map = ListedColormap(colors[:len(np.unique(y))])

    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.02),
                           np.arange(x2_min, x2_max, 0.02))

    grid_data = np.array([xx1.ravel(), xx2.ravel()]).T
    if model.n_features_in_ > 2:
        grid_data = np.c_[grid_data, np.zeros((grid_data.shape[0], model.n_features_in_ - 2))]

    predictions = model.predict(grid_data)
    predictions = predictions.reshape(xx1.shape)

    plt.contourf(xx1, xx2, predictions, alpha=0.3, cmap=color_map)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor='k', cmap=color_map)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

# Plot decision regions for PCA
plot_decision_boundaries(X_train_pca, y_train, logistic_pca,
                         title='PCA - Logistic Regression Decision Boundaries',
                         x_label='Principal Component 1', y_label='Principal Component 2')

# Plot decision regions for LDA
plot_decision_boundaries(X_train_lda, y_train, logistic_lda,
                         title='LDA - Logistic Regression Decision Boundaries',
                         x_label='Linear Discriminant 1', y_label='Linear Discriminant 2')

# Evaluate accuracy vs. number of PCA components
pca_accuracy_scores = []
for n in range(1, features.shape[1] + 1):
    pca = PCA(n_components=n)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    logistic_model = LogisticRegression(max_iter=1000)
    logistic_model.fit(X_train_pca, y_train)
    y_pred = logistic_model.predict(X_test_pca)
    pca_accuracy_scores.append(accuracy_score(y_test, y_pred))

plt.figure(figsize=(8, 5))
plt.plot(range(1, features.shape[1] + 1), pca_accuracy_scores, marker='o', linestyle='-', color='blue')
plt.xlabel("Number of PCA Components")
plt.ylabel("Accuracy")
plt.title("Accuracy vs. Number of PCA Components")
plt.grid()
plt.show()

# Evaluate accuracy vs. number of LDA components
lda_accuracy_scores = []
for n in range(1, len(np.unique(target))):
    lda = LDA(n_components=n)
    X_train_lda = lda.fit_transform(X_train, y_train)
    X_test_lda = lda.transform(X_test)

    logistic_model = LogisticRegression(max_iter=1000)
    logistic_model.fit(X_train_lda, y_train)
    y_pred = logistic_model.predict(X_test_lda)
    lda_accuracy_scores.append(accuracy_score(y_test, y_pred))

plt.figure(figsize=(8, 5))
plt.plot(range(1, len(np.unique(target))), lda_accuracy_scores, marker='s', linestyle='-', color='red')
plt.xlabel("Number of LDA Components")
plt.ylabel("Accuracy")
plt.title("Accuracy vs. Number of LDA Components")
plt.grid()
plt.show()

# Compare accuracy of models on original, PCA, and LDA data
model_results = {}

# Logistic Regression
logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train, y_train)
y_pred = logistic_model.predict(X_test)
model_results["Logistic Regression (Original)"] = accuracy_score(y_test, y_pred)

logistic_model.fit(X_train_pca, y_train)
y_pred = logistic_model.predict(X_test_pca)
model_results["Logistic Regression (PCA)"] = accuracy_score(y_test, y_pred)

logistic_model.fit(X_train_lda, y_train)
y_pred = logistic_model.predict(X_test_lda)
model_results["Logistic Regression (LDA)"] = accuracy_score(y_test, y_pred)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
model_results["Random Forest (Original)"] = accuracy_score(y_test, y_pred)

rf_model.fit(X_train_pca, y_train)
y_pred = rf_model.predict(X_test_pca)
model_results["Random Forest (PCA)"] = accuracy_score(y_test, y_pred)

rf_model.fit(X_train_lda, y_train)
y_pred = rf_model.predict(X_test_lda)
model_results["Random Forest (LDA)"] = accuracy_score(y_test, y_pred)

# Convert results to a DataFrame
results_df = pd.DataFrame(list(model_results.items()), columns=["Model", "Accuracy"])

# Plot accuracy comparison
plt.figure(figsize=(10, 5))
sns.barplot(x="Model", y="Accuracy", data=results_df)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison: Original vs PCA vs LDA")
plt.ylim(0.8, 1.0)
plt.show()

# Display accuracy results
print(results_df)