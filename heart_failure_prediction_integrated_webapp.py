import streamlit as st
import pandas as pd
import pickle
from streamlit_option_menu import option_menu

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# 모델 불러오기
model_path = 'C:/PythonWorkspace/heart_failure_prediction_model.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# 스타일 적용
st.markdown(
    """
    <style>
    .stTextInput, .stSelectbox, .stRadio, .stNumberInput {
        margin-top: -35px;
        margin-bottom: 20px;
    }
    .stFormSubmitButton {
        margin-top: 20px;
    }
    .title {
        font-variant: small-caps;
        text-align: center;
    }
    .eng_title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def single_prediction():
    st.markdown("<h1 class='title'>Heart Failure Prediction</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color:grey; text-align:center; margin-bottom:30px'>머신러닝 분류 알고리즘을 활용한 심장병 여부 예측</div>", unsafe_allow_html=True)

    with st.form(key='prediction_form'):
        st.markdown("<p><strong>나이</strong> <span style='color:grey;'>/ Age</span></p>", unsafe_allow_html=True)
        age = st.number_input('', min_value=0, max_value=120, value=60)
        
        st.markdown("<p><strong>성별</strong> <span style='color:grey;'>/ Sex</span></p>", unsafe_allow_html=True)
        sex = st.radio('', ['남자', '여자'], captions=['Male', 'Female'], horizontal=True, index=0)
        
        st.markdown("<p><strong>안정시 혈압</strong>(mmHg) <span style='color:grey;'>/ Resting Blood Pressure</span></p>", unsafe_allow_html=True)
        resting_bp = st.number_input('', min_value=1, max_value=200, value=120)
        
        st.markdown("<p><strong>최대 심박수</strong>(BPM) <span style='color:grey;'>/ Maximum Heart Rate</span></p>", unsafe_allow_html=True)
        max_hr = st.number_input('', min_value=60, max_value=220, value=185)
        
        st.markdown("<p><strong>당뇨병 유무</strong> (공복 혈당 > 120 mg/dL) <span style='color:grey;'>/ Diabetes Status (Fasting Blood Sugar > 120 mg/dL)</span></p>", unsafe_allow_html=True)
        fasting_bs = st.radio('', ['예', '아니오'], index=1, horizontal=True, captions=['Yes', 'No'])
        
        st.markdown("<p><strong>가슴 통증 유형</strong> <span style='color:grey;'>/ Chest Pain Type</span></p>", unsafe_allow_html=True)
        chest_pain_type = st.selectbox('', [
            '무증상 (ASY)',
            '전형적 협심증 (TA)', 
            '비전형적 협심증 (ATA)', 
            '비협심증성 통증 (NAP)'
            ], index=0)

        st.markdown("<p><strong>운동 유발성 협심증</strong> <span style='color:grey;'>/ Exercise Induced Angina</span></p>", unsafe_allow_html=True)
        exercise_angina = st.radio('', ['예 ', '아니오 '], index=1, horizontal=True, captions=['Yes', 'No'])
        
        st.markdown("<p><strong>안정시 심전도</strong> <span style='color:grey;'>/ Resting ECG</span></p>", unsafe_allow_html=True)
        resting_ecg = st.selectbox('', ['정상 (Normal)', 'ST-T파 이상 (ST)', '좌심실 비대 (LVH)'])
        
        st.markdown("<p><strong>ST 분절 저하 정도</strong> (mm) <span style='color:grey;'>/ Oldpeak</span></p>", unsafe_allow_html=True)
        oldpeak = st.number_input('', min_value=-5.0, max_value=10.0, value=0.0)
       
        st.markdown("<p><strong>ST 분절 기울기</strong> <span style='color:grey;'>/ ST Slope</span></p>", unsafe_allow_html=True)
        st_slope = st.selectbox('', ['상향 기울기 (Up)', '평탄 (Flat)', '하향 기울기 (Down)'])

        submit_button = st.form_submit_button(label='Predict :stethoscope:', type='secondary')

    if submit_button:
        # 입력 데이터를 모델이 훈련된 형식으로 변환
        input_data = {
            'Age': age,
            'RestingBP': resting_bp,
            'FastingBS': 1 if fasting_bs == '예' else 0,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Sex_M': 1 if sex == '남자' else 0,
            'ChestPainType_ATA': 1 if chest_pain_type == '비전형적 협심증 (ATA)' else 0,
            'ChestPainType_NAP': 1 if chest_pain_type == '비협심증성 통증 (NAP)' else 0,
            'ChestPainType_TA': 1 if chest_pain_type == '전형적 협심증 (TA)' else 0,
            'RestingECG_Normal': 1 if resting_ecg == '정상 (Normal)' else 0,
            'RestingECG_ST': 1 if resting_ecg == 'ST-T파 이상 (ST)' else 0,
            'ExerciseAngina_Y': 1 if exercise_angina == '예 ' else 0,
            'ST_Slope_Flat': 1 if st_slope == '평탄 (Flat)' else 0,
            'ST_Slope_Up': 1 if st_slope == '상향 기울기 (Up)' else 0
        }

        # 필요한 데이터 컬럼의 순서에 맞게 정렬
        input_df = pd.DataFrame([input_data])

        # 예측 수행
        model.predict(input_df)
        prediction_proba = model.predict_proba(input_df)

        # 예측 결과 출력 부분 변경
        prob = prediction_proba[0][1] * 100

        if prob < 25:
            result = '심장병 가능성 낮음'
            color = 'green'
        elif prob < 50:
            result = '심장병 가능성 낮으나 주의 필요'
            color = 'yellow'
        elif prob < 90:
            result = '심장병 가능성 높음'
            color = 'red'
        else:
            result = '심장병 가능성 매우 높음'
            color = '#800000'

        st.markdown(
            f"""
            <div style="border: 2px solid #D3D3D3; border-radius: 10px; padding: 20px; text-align:center; margin-top:20px;">
                <h2 style="color:{color};"><strong>{result}</strong></h2>
                <p>예측 위험도: <strong>{prob:.2f}%</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

def batch_prediction():
    st.markdown("<h1 class='title'>Heart Failure Prediction (<span style='color: limegreen;'>CSV</span>)</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color:grey; text-align:center; margin-bottom:30px'>머신러닝 분류 알고리즘을 활용한 심장병 여부 예측</div>", unsafe_allow_html=True)

    st.markdown("---")

    uploaded_file = st.file_uploader("", type=["csv"], help='원-핫 인코딩 이전의 원본 데이터를 업로드해 주세요!')
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file, header=0)
        st.write("**업로드된 데이터**", df.head())
        
        if st.button("예측 수행 :stethoscope:"):
            df['Sex_M'] = df['Sex'].apply(lambda x: 1 if x == 'M' else 0)
            df['ChestPainType_ATA'] = df['ChestPainType'].apply(lambda x: 1 if x == 'ATA' else 0)
            df['ChestPainType_NAP'] = df['ChestPainType'].apply(lambda x: 1 if x == 'NAP' else 0)
            df['ChestPainType_TA'] = df['ChestPainType'].apply(lambda x: 1 if x == 'TA' else 0)
            df['RestingECG_Normal'] = df['RestingECG'].apply(lambda x: 1 if x == 'Normal' else 0)
            df['RestingECG_ST'] = df['RestingECG'].apply(lambda x: 1 if x == 'ST' else 0)
            df['ExerciseAngina_Y'] = df['ExerciseAngina'].apply(lambda x: 1 if x == 'Y' else 0)
            df['ST_Slope_Flat'] = df['ST_Slope'].apply(lambda x: 1 if x == 'Flat' else 0)
            df['ST_Slope_Up'] = df['ST_Slope'].apply(lambda x: 1 if x == 'Up' else 0)

            input_data = df[['Age', 'RestingBP', 'FastingBS', 'MaxHR', 'Oldpeak', 'Sex_M', 'ChestPainType_ATA',
                             'ChestPainType_NAP', 'ChestPainType_TA', 'RestingECG_Normal', 'RestingECG_ST',
                             'ExerciseAngina_Y', 'ST_Slope_Flat', 'ST_Slope_Up']]

            predictions = model.predict(input_data)
            probs = model.predict_proba(input_data)[:, 1]

            df.insert(0, 'Prediction', predictions)
            df.insert(1, 'Probability', probs)

            st.write("**예측 결과**", df)

            csv = df.to_csv(index=False)
            st.download_button(label=":arrow_down: 예측 결과 다운로드", data=csv, file_name=uploaded_file.name[:-4]+'_predictions.csv', mime='text/csv')

with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Single Prediction", "Batch Prediction"],
        icons=["hand-point-right", "cloud-upload-alt"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Single Prediction":
    single_prediction()
elif selected == "Batch Prediction":
    batch_prediction()

st.markdown("---")
st.markdown(
"""
<div style="text-align:center; margin-top:20px; color: grey;">
    © 2024 최민혁.
</div>
""", unsafe_allow_html=True
)
st.markdown(
"""
<style>
.icon {
    margin: 0 5px;
    color: grey;
    transition: color 0.3s;
}
.icon:hover {
    color: lightblue;
}
</style>
<div style="text-align:center;">
    <a href="mailto:m120971209@gmail.com" class="icon"><i class="fas fa-envelope"></i></a>
    <a href="https://mhc-cv.streamlit.app" target="_blank" class="icon"><i class="fas fa-home"></i></a>
</div>
""", unsafe_allow_html=True
)