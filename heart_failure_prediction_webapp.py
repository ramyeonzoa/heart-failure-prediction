import streamlit as st
import pandas as pd

def main():
    st.title("Heart Disease Prediction")
    placeholder = st.empty()

    # 초기 내용 설정
    placeholder.text("This is the initial content")

    # 버튼 클릭 시 내용 변경
    if st.button("Change content"):
        placeholder.text("This is the updated content")

    # 복잡한 내용 변경 예제
    if st.button("Show chart"):
        with placeholder.container():
            st.write("Here is a chart:")
            st.line_chart({"data": [1, 2, 3, 4]})
    # 입력 폼 생성
with st.form(key='prediction_form'):
    st.title("Heart Disease Prediction")
    st.write("by using Machine Learning Algorithm")

    age = st.number_input('Age', min_value=1, max_value=120, value=25)
    sex = st.selectbox('Sex', ['Male', 'Female'])
    chest_pain_type = st.selectbox('Chest Pain Type', ['ATA', 'NAP', 'ASY', 'TA'])
    resting_bp = st.number_input('Resting Blood Pressure', min_value=50, max_value=200, value=120)
    cholesterol = st.number_input('Cholesterol', min_value=100, max_value=600, value=200)
    fasting_bs = st.checkbox('Fasting Blood Sugar > 120 mg/dl')
    resting_ecg = st.selectbox('Resting ECG', ['Normal', 'ST', 'LVH'])
    max_hr = st.number_input('Maximum Heart Rate', min_value=60, max_value=220, value=185)
    exercise_angina = st.radio('Exercise Induced Angina', ['Yes', 'No'])
    oldpeak = st.number_input('Oldpeak', min_value=-5.0, max_value=10.0, value=0.0)
    st_slope = st.selectbox('ST Slope', ['Up', 'Flat', 'Down'])

    submit_button = st.form_submit_button(label='Predict')

# 폼 제출 시 처리
if submit_button:
    # 예측을 위한 입력 데이터 수집
    input_data = [[age,
                   sex,
                   chest_pain_type,
                   resting_bp,
                   cholesterol,
                   1 if fasting_bs else 0,
                   resting_ecg, max_hr,
                   1 if exercise_angina == 'Yes' else 0,
                    oldpeak,
                    st_slope ]]

    # 입력 데이터 출력 (여기서 예측 모델을 호출할 수 있음)
    st.write("Input Data:", input_data)
    st.info("hi")

    # 예측 결과 (예시)
    # 예측 모델을 사용하여 결과를 얻어야 합니다.
    prediction = "Heart Disease Likely"  # 예시 결과
    st.write("Prediction Result:", prediction)

if __name__ == "__main__":
    main()