import streamlit as st
from prediction_helper import predict

st.set_page_config(
    page_title="Health Insurance Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f7ff 0%, #f8fbff 100%);
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #075985, #0284c7);
        padding: 32px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.18);
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e0f2fe;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 21px;
        font-weight: 700;
        color: #075985;
        margin: 22px 0 15px 0;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border: 1px solid #dbeafe;
        border-radius: 18px;
        padding: 18px;
    }

    .stNumberInput label,
    .stSelectbox label {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stNumberInput"] input {
        border-radius: 10px;
    }

    div[data-testid="stSelectbox"] > div > div {
        border-radius: 10px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #0284c7, #0369a1);
        color: white;
        font-size: 17px;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 13px 20px;
        width: 100%;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #075985;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(2, 132, 199, 0.2);
    }

    .result-card {
        background: white;
        border: 2px solid #bae6fd;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        margin-top: 25px;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.10);
    }

    .result-label {
        color: #475569;
        font-size: 17px;
        font-weight: 600;
    }

    .result-value {
        color: #0369a1;
        font-size: 34px;
        font-weight: 800;
        margin-top: 8px;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 35px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🏥 Health Insurance Cost Predictor</h1>
    <p>
        Estimate health insurance costs using personal,
        lifestyle and medical information.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- OPTIONS ----------
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': [
        'Salaried', 'Self-Employed', 'Freelancer', ''
    ],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease',
        'Diabetes',
        'High blood pressure',
        'Diabetes & High blood pressure',
        'Thyroid',
        'Heart disease',
        'High blood pressure & Heart disease',
        'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}


# ---------- PERSONAL DETAILS ----------
st.markdown(
    '<div class="section-title">👤 Personal Information</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    row1 = st.columns(3)

    with row1[0]:
        age = st.number_input(
            'Age (years)',
            min_value=18, max_value=100, value=25, step=1
        )

    with row1[1]:
        gender = st.selectbox(
            'Gender', categorical_options['Gender']
        )

    with row1[2]:
        marital_status = st.selectbox(
            'Marital Status', categorical_options['Marital Status']
        )

    row2 = st.columns(3)

    with row2[0]:
        number_of_dependants = st.number_input(
            'Number of Dependants',
            min_value=0, max_value=20, value=0, step=1
        )

    with row2[1]:
        income_lakhs = st.number_input(
            'Annual Income (Lakhs)',
            min_value=0.0, max_value=200.0,
            value=5.0, step=1.0
        )

    with row2[2]:
        employment_status = st.selectbox(
            'Employment Status',
            categorical_options['Employment Status']
        )


# ---------- HEALTH DETAILS ----------
st.markdown(
    '<div class="section-title">🩺 Health & Lifestyle</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    row3 = st.columns(3)

    with row3[0]:
        bmi_category = st.selectbox(
            'BMI Category', categorical_options['BMI Category']
        )

    with row3[1]:
        smoking_status = st.selectbox(
            'Smoking Status', categorical_options['Smoking Status']
        )

    with row3[2]:
        genetical_risk = st.number_input(
            'Genetical Risk',
            min_value=0, max_value=5, value=0, step=1
        )

    row4 = st.columns(2)

    with row4[0]:
        medical_history = st.selectbox(
            'Medical History', categorical_options['Medical History']
        )

    with row4[1]:
        region = st.selectbox(
            'Region', categorical_options['Region']
        )


# ---------- INSURANCE PLAN ----------
st.markdown(
    '<div class="section-title">🛡️ Insurance Plan</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    insurance_plan = st.select_slider(
        'Choose your insurance plan',
        options=categorical_options['Insurance Plan'],
        value='Silver',
        help='Select Bronze, Silver or Gold.'
    )

    plan_col1, plan_col2, plan_col3 = st.columns(3)

    with plan_col1:
        st.markdown("🥉 **Bronze**")
        st.caption("Basic coverage tier")

    with plan_col2:
        st.markdown("🥈 **Silver**")
        st.caption("Mid-level coverage tier")

    with plan_col3:
        st.markdown("🥇 **Gold**")
        st.caption("Higher coverage tier")


# ---------- PREDICTION INPUT ----------
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}


# ---------- PREDICT BUTTON ----------
st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with center:
    predict_button = st.button(
        '✨ Predict Insurance Cost',
        use_container_width=True
    )

if predict_button:
    try:
        with st.spinner('Calculating your estimated insurance cost...'):
            prediction = predict(input_dict)

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">
                💰 Estimated Health Insurance Cost
            </div>
            <div class="result-value">
                {prediction}
            </div>
            <p style="color:#64748b; margin-top:12px;">
                This is a model-based estimate, not a confirmed insurance quote.
            </p>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Unable to calculate prediction: {e}")


# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    🏥 Health Insurance Cost Predictor | Powered by Machine Learning
</div>
""", unsafe_allow_html=True)