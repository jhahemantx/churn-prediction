# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import tensorflow as tf
import streamlit as st
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

model = tf.keras.models.load_model('model.h5')

with open('gender_encoding.pkl', 'rb') as file:
  label_encoder = pickle.load(file)

with open('geography_encoder.pkl', 'rb') as file:
  ohe = pickle.load(file)

with open('standard_scaler.pkl', 'rb') as file:
  scaler = pickle.load(file)

"""## App"""

st.title('Customer Churn Prediction')

# takeing input
geography = st.selectbox('Geography', ohe.categories_[0])
gender = st.selectbox('Gender', label_encoder.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# adding geography
geo_encoded = ohe.transform([[geography]])
geo_encoded_df = pd.DataFrame(geo_encoded, columns=ohe.get_feature_names_out(['Geography']))

# concat
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)
input_data

input_data_scaled = scaler.transform(input_data)

prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]
prediction_proba

st.write(f'Curn probability: {prediction_proba:2f}')

if prediction_proba > 0.5:
  st.write('The customer is likely to churn.')
else:
  st.write('The customer is not likely t churn.')
