import matplotlib.pyplot as plt
import platform

# ✅ 운영체제별 폰트 설정 (Streamlit Cloud는 Linux)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Linux (Streamlit Cloud 포함)
    plt.rc('font', family='NanumGothic')  # 나눔고딕으로 설정

# ✅ 마이너스 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="산업재해 분석 대시보드", layout="wide")

st.title("📊 산업별 재해율 및 사망만인율 분석 (2023년 기준)")

# 데이터 불러오기
injury_df = pd.read_csv("data/재해율.csv", encoding='cp949')
death_df = pd.read_csv("data/사망만인율.csv", encoding='cp949')

# 필요한 열 추출 및 이름 변경
injury = injury_df[['대업종', '구분', '2023년 재해율']].rename(columns={'2023년 재해율': '재해율'})
death = death_df[['대업종', '구분', '2023년 사망만인율']].rename(columns={'2023년 사망만인율': '사망만인율'})

# 병합
merged = pd.merge(injury, death, on=['대업종', '구분'])
merged['재해율'] = pd.to_numeric(merged['재해율'], errors='coerce')
merged['사망만인율'] = pd.to_numeric(merged['사망만인율'], errors='coerce')
merged.dropna(inplace=True)

# 상위 10개 추출
top10 = merged.sort_values(by=['재해율', '사망만인율'], ascending=False).head(10)

# 테이블 표시
st.subheader("📌 재해율 및 사망만인율 상위 10개 업종")
st.dataframe(top10)

# 그래프 시각화
st.subheader("📉 업종별 재해율 및 사망만인율 비교")

fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.4
x = range(len(top10))

ax.bar(x, top10['재해율'], width=bar_width, label='재해율', color='skyblue')
ax.bar([i + bar_width for i in x], top10['사망만인율'], width=bar_width, label='사망만인율', color='salmon')
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(top10['구분'], rotation=45, ha='right')
ax.set_ylabel('비율')
ax.set_title('업종별 재해율 및 사망만인율 비교')
ax.legend()

st.pyplot(fig)
