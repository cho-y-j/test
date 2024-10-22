import streamlit as st
import time
import random

# 단어 저장 및 연습 상태 관리 클래스
def load_word_file(file):
    word_dict = {}
    lines = file.read().decode("utf-8").splitlines()
    for line in lines:
        parts = line.split(",")
        word = parts[0].strip()
        meaning = parts[1].strip() if len(parts) > 1 else ""
        word_dict[word] = meaning
    return word_dict

# Streamlit 앱 UI 생성 및 로직 구현
st.title("타자 연습 프로그램")

# 파일 업로드
uploaded_file = st.file_uploader("단어 파일 업로드 (텍스트 형식)", type="txt")

if uploaded_file is not None:
    word_dict = load_word_file(uploaded_file)
    words = list(word_dict.keys())
    st.success("단어 파일이 성공적으로 불러와졌습니다.")
else:
    st.warning("단어 파일을 업로드해주세요.")
    words = []

# 연습 단계 및 설정 선택
stage_options = ["단어+해석", "단어만 보기", "해석만 보기"]
stage = st.radio("연습 단계 선택", stage_options)

order_options = ["순차적으로", "랜덤하게"]
order = st.radio("단어 순서 선택", order_options)

practice_time = st.number_input("연습 시간 (초)", min_value=10, max_value=300, value=60)
mute = st.checkbox("음소거")

# 연습 시작
if st.button('연습 시작'):
    if not words:
        st.error("단어 파일이 없습니다. 단어 파일을 업로드해주세요.")
    else:
        is_random = order == "랜덤하게"
        word_list = words[:]
        if is_random:
            random.shuffle(word_list)

        correct_words = 0
        total_words = 0
        start_time = time.time()

        # 연습 시간 카운트 시작
        while time.time() - start_time < practice_time:
            if not word_list:
                word_list = words[:]
                if is_random:
                    random.shuffle(word_list)

            current_word = word_list.pop(0)
            meaning = word_dict[current_word]

            # 현재 단어와 해석 표시
            if stage == "단어+해석":
                st.write(f"단어: {current_word}, 해석: {meaning}")
            elif stage == "단어만 보기":
                st.write(f"단어: {current_word}")
            elif stage == "해석만 보기":
                st.write(f"해석: {meaning}")

            # 사용자 입력 받기
            user_input = st.text_input("단어를 입력하세요:", "", key=f"input_{total_words}")

            if user_input:
                if user_input.strip() == current_word:
                    correct_words += 1
                    if not mute:
                        st.balloons()  # 성공 시 시각적 피드백
                total_words += 1

        # 연습 종료 후 결과 표시
        elapsed_time = time.time() - start_time
        speed = (correct_words / elapsed_time) * 60
        accuracy = (correct_words / total_words) * 100 if total_words else 0

        st.info(f"연습 종료! 총 연습 시간: {elapsed_time:.2f}초")
        st.write(f"속도: {speed:.2f} WPM")
        st.write(f"정확도: {accuracy:.2f}%")
