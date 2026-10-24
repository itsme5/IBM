import pandas as pd
import joblib

model_young = joblib.load("artifacts\model_young.joblib")
model_rest = joblib.load("artifacts\model_rest.joblib")
scaler_young = joblib.load("artifacts\scaler_young.joblib")
scaler_rest = joblib.load("artifacts\scaler_rest.joblib")


def calculate_normalized_risk(diseases):
    risk_scores = {
        'Diabetes': 6,
        'Heart Disease': 8,
        'High Blood Pressure': 6,
        'Asthma': 5,
        'Cancer': 10,
        'Obesity': 5,
        'Arthritis': 3
    }

    total_risk_score = sum(
        risk_scores.get(disease, 0)
        for disease in diseases
    )

    max_risk_score = len(diseases) * 10

    if max_risk_score == 0:
        return 0

    normalized_risk_score = total_risk_score / max_risk_score

    return normalized_risk_score 
    #split the medical history into potential two parts and convert to lowercase 
    diseases = medical_history.lower().split(" & ")

    #calulate  the total risk score by summing the risk score for each part
    total_risk_score = sum(risk_scores.get(diseases, 0) for disease in diseases) #def

    max_score = 14 #risk score for heart disease (8) + second max risk score (6) for
    min_score = 0 # Since the mimimum score is always 0

    #Normalized the total risk score 
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)

    return normalized_risk_score

def preprocess_input(input_dict):
    #Define the expected columns and initialize the DataFrame with zeros
    expected_columns = [
        'age', 'number of dependants', 'income_lakhs', 'insurance_plan', 'genetical_risk', 'normalized_risk_score',
        'gender_Male', 'region_Northwest', 'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
        'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight', 'smoking_status_Occasional',
        'smoking_status_Regular', 'employment_status_Salaried', 'employment_status_Self-Employed'
    ]
    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}

    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    #df.fillna(0, inplace= True)

    # manually assign value for each categorical input based on input_dict 
    
    for key, value in input_dict.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'BMI Category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking Status':
            if value == 'Occasional':
                df['smoking_status_Occasional']
            elif value =='Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':
            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)
        elif key == 'Age':
            df['age'] = value
        elif key == 'Number of Dependants':
            df['number of dependants'] = value
        elif key == 'Income in Lakhs':
            df['income_lakhs'] = value
        elif key == 'Genetical Risk':
            df['genetical_risk'] = value


    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])
    df = handle_scaling(input_dict['Age'], df)

    return df

def handle_scaling(age, df):

    if age <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df['income_level'] = None
    print("DataFrame columns:", df.columns.tolist())
    print("Columns to scale:", cols_to_scale)
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    df.drop('income_level', axis='columns', inplace=True)

    return df

def predict(input_dict):
    input_df = preprocess_input(input_dict)

    if input_dict['Age'] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction[0])