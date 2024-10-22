import streamlit as st
import time
import random

# 단어 저장 및 연습 상태 관리 함수
def load_word_file(file):
    word_dict = {}
    lines = file.read().decode("utf-8").splitlines()
    for line in lines:
        parts = line.split(",")
        word = parts[0].strip()
        meaning = parts[1].strip() if len(parts) > 1 else ""
        word_dict[word] = meaning
    return word_dict

# Streamlit 앱 설정
st.set_page_config(page_title="타자 연습 프로그램", page_icon="🎓", layout="wide")

# 앱 제목 및 설명
st.title("타자 연습 프로그램")
st.markdown("<h3 style='text-align: center; color: #4CAF50;'>단어 연습을 통해 타자 속도를 높이세요!</h3>", unsafe_allow_html=True)

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
stage = st.radio("연습 단계 선택", stage_options, index=0, horizontal=True)

order_options = ["순차적으로", "랜덤하게"]
order = st.radio("단어 순서 선택", order_options, index=0, horizontal=True)

practice_time = st.number_input("연습 시간 (초)", min_value=10, max_value=300, value=60)
mute = st.checkbox("음소거", value=False)

# 연습 시작 버튼
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

        # 첫 단어 설정
        current_word = word_list.pop(0)

        while time.time() - start_time < practice_time:
            if not word_list:
                word_list = words[:]
                if is_random:
                    random.shuffle(word_list)

            meaning = word_dict[current_word]

            # 현재 단어와 해석 표시
            if stage == "단어+해석":
                st.markdown(f"<h4 style='color: #333;'>단어: <span style='color: #4CAF50;'>{current_word}</span>, 해석: <span style='color: #ff6347;'>{meaning}</span></h4>", unsafe_allow_html=True)
            elif stage == "단어만 보기":
                st.markdown(f"<h4 style='color: #333;'>단어: <span style='color: #4CAF50;'>{current_word}</span></h4>", unsafe_allow_html=True)
            elif stage == "해석만 보기":
                st.markdown(f"<h4 style='color: #333;'>해석: <span style='color: #ff6347;'>{meaning}</span></h4>", unsafe_allow_html=True)

            # 사용자 입력 받기
            user_input = st.text_input("단어를 입력하세요 (엔터를 누르세요):", "", key=f"input_{total_words}")

            if user_input.strip() == current_word:
                correct_words += 1
                if not mute:
                    st.success("정답입니다! 🎉")
                total_words += 1
                if word_list:
                    current_word = word_list.pop(0)
                else:
                    break
                st.experimental_rerun()

        # 연습 종료 후 결과 표시
        elapsed_time = time.time() - start_time
        speed = (correct_words / elapsed_time) * 60
        accuracy = (correct_words / total_words) * 100 if total_words else 0

        st.info(f"✅ 연습 종료! 총 연습 시간: {elapsed_time:.2f}초")
        st.markdown(f"**속도**: {speed:.2f} WPM (단어 분당)\n**정확도**: {accuracy:.2f}%")

# 푸터 추가
st.markdown("""
    <hr style='border: 1px solid #ddd;'>
    <footer style='text-align: center; color: #888;'>
        © 2024 타자 연습 프로그램 - 개발자와 함께하는 즐거운 학습
    </footer>
""", unsafe_allow_html=True)


