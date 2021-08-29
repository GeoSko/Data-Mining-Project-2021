# -*- coding: utf-8 -*-
"""DM_1_B_missing_value_handling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16FFUeDwq3-bFSXG2zgs0wWNvsnAAJRyG
"""

#Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, metrics
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

# Versions of libraries
import sklearn
print(f'Numpy:{np.__version__}\nSklearn:{sklearn.__version__}')

#Load the dataset
df = pd.read_csv('drive/MyDrive/DataMining/healthcare-dataset-stroke-data/healthcare-dataset-stroke-data.csv')
df.head()

#Replace 'Unknown' values from feature smoking status as NaN value
df['smoking_status'].replace('Unknown', np.NaN, inplace=True)
# df.head()

df.shape

#Remove Columns with missing values (bmi and smoking_status)
df1 = df.dropna(axis=1)
df1.head()

#We droped 2 columns
df1.shape

# Calculata bmi mean
bmi_mean = df['bmi'].mean()
bmi_mean

# Replace bmi missing values with column mean
df2 = df.copy()
df2.bmi = df2['bmi'].fillna(value= bmi_mean)
df2.head()

#Create dataframe withnout smoking status, stroke columns
df3_training = df.drop(columns=['smoking_status','stroke']).dropna(axis=0)
df3_training.head()

df3_training.shape

#Get Dummy variables. Drop first column to avoid multicollinearity
df3_training_dummies = pd.get_dummies(df3_training,drop_first=True).drop(['id'], axis=1)
df3_training_dummies.head()

# Calculate correlation matrix
df3_dummies_corr = pd.get_dummies(data=df3_training_dummies).corr()
# df3_dummies_corr.head()

# Absolute value sort of bmi correlation values
bmi_corr_sorted = df3_dummies_corr[['bmi']].sort_values(by='bmi', key=abs,ascending=False)
bmi_corr_sorted

# Plot bmi correlation values
bmi_corr = df3_dummies_corr[['bmi']].sort_values(by=['bmi'], ascending= False)
sns.heatmap(bmi_corr, annot=True)

# List of the values that have the most correlation with bmi
bmi_correlated_features = ['bmi','ever_married_Yes','age','work_type_Private','avg_glucose_level','hypertension','work_type_children']

# Create numeric representation of the categorical data
df3_training_dummies = df3_training_dummies[bmi_correlated_features]
df3_training_dummies.head()

X = df3_training_dummies.drop(columns=['bmi']).values
X.shape

X

y = df3_training_dummies['bmi'].values
y

y.size

# Train test split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.25, random_state=42)

#Fitting the test Linear Regression model based on 75% of the bmi data
test_model = LinearRegression().fit(X_train, y_train)

# Calculate predictions
y_pred = test_model.predict (X_test)

#Evaluating the test model
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print(f"Bmi range: {df.bmi.min()} - {df.bmi.max()}")

sns.displot(df['bmi'], kde=True)

#Fitting the Linear Regression model basen on all the data
model = LinearRegression().fit(X, y)

#Keeping the indeces of the records with bmi missing values
bmi_missing_df = df[df['bmi'].isnull()]
bmi_missing_indeces = df[df['bmi'].isnull()].index
bmi_missing_indeces

bmi_missing_indeces.shape

# df3_application_dummies = pd.get_dummies(bmi_missing_df,drop_first=True).drop(['id','bmi'], axis=1)
# df3_application_dummies.head()

# Create the prediction dataset
df3_application_dummies = df.iloc[bmi_missing_indeces]
df3_application_dummies = pd.get_dummies(df3_application_dummies,drop_first=True).drop(['id'], axis=1)
df3_application_dummies = df3_application_dummies[bmi_correlated_features]
df3_application_dummies

df3_application_dummies.shape

X_apply = df3_application_dummies.drop(columns='bmi').values
# X_apply

X_apply.shape

predicted_bmi = model.predict (X_apply)
# predicted_bmi

predicted_bmi.shape

# Start making final df3
df3 = df.drop(columns='smoking_status')
df3

#Fill the missing values if bmi with the predicted ones
df3['bmi'].iloc[bmi_missing_indeces] = predicted_bmi

df3.head()

#Ensure there are no null values in bmi column
print(f"Number of null values in bmi column:{df3['bmi'].isnull().sum(axis = 0)}")

df4_training = df.drop(labels=['id','stroke','bmi'], axis=1)
df4_training.head()

#Keep the indeces of records with NaN on smoking_status
smoking_status_missing_df = df[df['smoking_status'].isnull()]
smoking_status_missing_indeces = df[df['smoking_status'].isnull()].index
smoking_status_missing_indeces

#Drop the rows with NaN values on the smoking_status feature
df4_training.dropna(subset=['smoking_status'], axis=0, inplace=True)
# df4_training

# Label encode smoking status
smoking_encoded = df4_training['smoking_status'].str.replace('never smoked','0')
smoking_encoded = smoking_encoded.str.replace('formerly smoked',' 1')
smoking_encoded = smoking_encoded.str.replace('smokes',' 2')
df4_training['smoking_status'] = smoking_encoded
df4_training['smoking_status'] = df4_training['smoking_status'].astype(int)

#Get the one hot encoded dataset
df4_training_dummies = pd.get_dummies(df4_training.drop(labels=['smoking_status'], axis=1), drop_first=True)
df4_training_dummies['smoking_status'] = df4_training['smoking_status']
df4_training_dummies.head()

#Calculate correlation of smoking_status to other features
df4_dummies_corr = pd.get_dummies(data=df4_training_dummies).corr()
smoking_status_corr_sorted = df4_dummies_corr[['smoking_status']].sort_values(by='smoking_status', key=abs,ascending=False)
# smoking_status_corr_sorted

#Plotting smoking_status correlation
smoking_status_corr = df4_dummies_corr[['smoking_status']].sort_values(by=['smoking_status'], ascending= False)
sns.heatmap(smoking_status_corr, annot=True)

#Training array
X = df4_training_dummies.drop(columns=['smoking_status']).values
X.shape

#Prediction vector
y = df4_training_dummies['smoking_status'].values
y.shape

#Train test split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.25, random_state=42)

#Find the best value of K
accuracy = []
for i in range(1,100):
 knn = KNeighborsClassifier(n_neighbors=i)
 knn.fit(X_train,y_train)
 pred_i = knn.predict(X_test)
 accuracy.append(np.mean(pred_i == y_test))

plt.figure(figsize=(10,6))
plt.plot(range(1,100),accuracy,color='blue', linestyle='dashed', 
         marker='o',markerfacecolor='red', markersize=10)
plt.title('Accuracy based on the value of K')
plt.xlabel('K')
plt.ylabel('Accuracy')
print("Maximum:-",max(accuracy),"at K =",accuracy.index(max(accuracy)))

knn_test = KNeighborsClassifier(n_neighbors=86,
                                # p=7,
                                # algorithm='kd_tree',
                                metric='minkowski' 
                                )
knn_test.fit(X_train, y_train)

y_pred = knn_test.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

#Fitting the final smoking_status filling model
knn_apply = KNeighborsClassifier(n_neighbors=86, p=7,weights='uniform',algorithm='kd_tree', metric='minkowski' )
knn_apply.fit(X, y)

#Creating the final smoking_status training dataframe
df4_application_dummies = df.drop(labels=['id','stroke','bmi'], axis=1)
df4_application_dummies = pd.get_dummies(df4_application_dummies.drop(labels=['smoking_status'], axis=1), drop_first=True)
df4_application_dummies = df4_application_dummies.iloc[smoking_status_missing_indeces,:]
df4_application_dummies.head()

X = df4_application_dummies.values
X.shape

# Predict smoking status
smoking_status_prediction = knn_apply.predict(X)
smoking_status_prediction.shape

# Cast integer values to str
smoking_status_prediction = pd.Series(smoking_status_prediction).astype(str)
smoking_status_prediction.values

df4 = df.drop(labels='bmi', axis=1)

#FIll the missing values if smoking_status with the predicted ones
df4['smoking_status'].iloc[smoking_status_missing_indeces] = smoking_status_prediction.values
df4

# Decode encoded smoking status labels
smoking_decoded = df4['smoking_status'].str.replace('never smoked','0')
smoking_decoded = smoking_decoded.str.replace('formerly smoked', '1')
smoking_decoded = smoking_decoded.str.replace('smokes', '2')
df4['smoking_status'] = smoking_decoded.astype(int)
df4.head()

#Ensure there are no null values in bmi column
print(f"Number of null values in bmi column: {df4['smoking_status'].isnull().sum(axis = 0)}")

df5 = df.copy()
df5['bmi'] = df3['bmi']
df5['smoking_status'] = df4['smoking_status']
df5.head()

df5['bmi'].isnull().sum(axis = 0)

#Save the datasets
df1.to_csv("drive/MyDrive/DataMining/healthcare_processed_datasets/df1.csv")
df2.to_csv("drive/MyDrive/DataMining/healthcare_processed_datasets/df2.csv")
df3.to_csv("drive/MyDrive/DataMining/healthcare_processed_datasets/df3.csv")
df4.to_csv("drive/MyDrive/DataMining/healthcare_processed_datasets/df4.csv")
df5.to_csv("drive/MyDrive/DataMining/healthcare_processed_datasets/df5.csv")

