import base64
from io import BytesIO
import xlsxwriter
import streamlit as st
import insta_analysis as ia
import pandas as pd
import urllib.request as req


# 엑셀 다운로드 기능
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df, name):
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<div align="left"><font size="2"><a href="data:application/octet-stream;base64,{b64.decode()}" download="{name}.xlsx">Download Excel File</a></font></div>'


# * 용어 정리------------------------------
# KS : Keyword Search
# AC : Account Check
# MAC : Multiple Account Check
# LMAC : Light ver. Multiple Account Check
# PC : Posts Check
# -----------------------------------------

# 레이아웃 설정
st.set_page_config(page_title="59_Insight", page_icon=":cat:", layout="wide", initial_sidebar_state="expanded")
menu_box = ['선택', '1. 키워드가 존재하는 게시글 찾기', '2. 계정 분석하기', '3. 계정 여러개 분석하기(CSV)', '4. 라이트 - 계정 여러개 분석(CSV)', '5. 게시글 여러개 분석하기']
st.sidebar.title("Menu")
Anal_menu = st.sidebar.selectbox('원하시는 기능을 선택해주세요.', menu_box, index=0)

# 기본 화면
if Anal_menu == menu_box[0]:
    # 메인 타이틀과 메시지
    st.title("59_Insight" + "\n" + "#### 인스타그램 계정과 게시글을 분석해보세요.")
    st.code('''
😺 원하는 인스타그램 계정을 분석해보세요.
😸 인스타그램 계정에서, 특정 키워드가 포함된 게시글을 찾아보세요
😿 인스타그램은 시간당 조회 제한이 있어요. 
  (오류가 뜨거나 검색이 되지 않는다면 조회 허용 범위가 초과된 것이니, 잠시 후 다시 시도해주세요.)
    ''')

# 1. 키워드 분석 화면
if Anal_menu == menu_box[1]:
    img_list = []
    st.title("59_Insight" + "\n" + "#### 💡 인스타그램 계정에서, 특정 키워드가 포함된 게시글을 분석합니다.")
    st.code('''
😿 인스타그램은 시간당 조회 제한이 있어요. 
  (오류가 뜨거나 검색이 되지 않는다면 조회 허용 범위가 초과된 것이니, 잠시 후 다시 시도해주세요.)
    ''')
    with st.sidebar:
        with st.form(key="Keyword_form"):
            st.write("분석 정보 입력")
            KS_account = st.text_input("계정명", help="인스타그램 주소를 제외한 계정명만 입력하세요.")
            KS_key = st.text_input("검색할 키워드", help="여러개의 키워드를 입력할 경우, 쉼표로 구분해주세요.", args=True)
            KS_posts_num = st.slider("분석할 게시글 수를 선택하세요.", min_value=10, max_value=100, value=10)
            KS_button = st.form_submit_button(label="분석시작")

    if KS_button:
        result = ia.keyword_check(KS_account, KS_posts_num, KS_key)
        st.write(
            f'<br><br><font color="blue" font size="5">💡\"{KS_key}\" </font>키워드 분석 결과 {len(result)}개의 게시글이 검색되었습니다.',
            unsafe_allow_html=True)
        if len(result) > 0:
            idx = 1
            for i in result:
                url = i["thumbnail"]
                req.urlretrieve(url, "./test.png")
                if idx % 3 == 1:
                    col1, col2, col3 = st.beta_columns(3)
                with col1:
                    if idx % 3 == 1:
                        st.write('▼   ' + f'https://instagram.com/p/{i["url"]}')
                        st.image("./test.png")
                        st.markdown("")
                with col2:
                    if idx % 3 == 2:
                        st.write('▼   ' + f'https://instagram.com/p/{i["url"]}')
                        st.image("./test.png")
                        st.markdown("")
                with col3:
                    if idx % 3 == 0:
                        st.markdown('▼   ' + f'https://instagram.com/p/{i["url"]}')
                        st.image("./test.png")
                        st.markdown("")
                idx += 1


# 2. 단일 계정 분석 화면
if Anal_menu == menu_box[2]:
    st.title("59_Insight" + "\n" + "#### 인스타그램 계정의 간략한 정보를 분석합니다.")
    st.code('''
❗️ 평균 좋아요 / 평균 댓글은 최근 15개 게시글의 평균입니다. 
😿 인스타그램은 시간당 조회 제한이 있어요. 
  (오류가 뜨거나 검색이 되지 않는다면 조회 허용 범위가 초과된 것이니, 잠시 후 다시 시도해주세요.)
    ''')
    with st.sidebar:
        upload = False
        with st.form(key="account_form"):
            st.write("분석 정보 입력")
            AC_account = st.text_input("계정명", help="인스타그램 주소를 제외한 계정명만 입력하세요.")
            AC_button = st.form_submit_button(label="계정 분석 시작")

    if AC_button:
        result = ia.test_single_account_check(AC_account)
        st.write(
            f'<br><br><font color="blue" font size="5">💡<a href={result["account"]}>\"{AC_account}\"</a></font> 계정 분석이 완료되었습니다.',
            unsafe_allow_html=True)
        st.code(
            f'''
⭐️ 팔로워 : {result["followers"]} 명
❤️ 평균 좋아요 : {result["avg_likes"]}
💌 평균 댓글 : {result["avg_comments"]}
            ''')
        st.write(
            f'<br><br><font color="blue" font size="6">🌃 최근 15개 게시글',
            unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.beta_columns(5)
        idx = 1
        for i in result["photos"]:
            url = result["photos"][idx - 1][0]
            req.urlretrieve(url, "./test.png")
            with col1:
                if idx % 5 == 1:
                    st.image("./test.png", width=250)
            with col2:
                if idx % 5 == 2:
                    st.image("./test.png", width=250)
            with col3:
                if idx % 5 == 3:
                    st.image("./test.png", width=250)
            with col4:
                if idx % 5 == 4:
                    st.image("./test.png", width=250)
            with col5:
                if idx % 5 == 0:
                    st.image("./test.png", width=250)
            idx += 1


# 3. 여러 계정 분석 (CSV 업로드)
if Anal_menu == menu_box[3]:
    st.title("59_Insight" + "\n" + "#### 💡 여러개의 인스타그램 계정 정보를 분석합니다.")
    st.code('''
❗️ CSV 파일의 A열에 인스타그램 계정명을 입력 후, 업로드 해주세요. (https://instagram.com/ <-- 을 제외한 계정명만 입력) 
❗️ 평균 좋아요 / 평균 댓글은 최근 15개 게시글의 평균입니다. 
❗️ 많은 계정을 분석하시면 시간이 오래 걸릴 수 있으니, 인내심을 가져주세요!
😿 인스타그램은 시간당 조회 제한이 있어요. 
  (오류가 뜨거나 검색이 되지 않는다면 조회 허용 범위가 초과된 것이니, 잠시 후 다시 시도해주세요.)
    ''')
    with st.sidebar:
        upload = False
        with st.form(key="multi_account_form"):
            st.write("파일 업로드")
            MAC_file = st.file_uploader("❗️ CSV 파일을 업로드해주세요.", help="A열에 분석하고자 하는 계정명을 나열한 후, 'csv' 파일로 저장해주세요.")
            MAC_button = st.form_submit_button(label="계정 분석 시작")

    if MAC_button:
        data = MAC_file.getvalue()
        data_pd = pd.read_csv(MAC_file, names=['ID'], encoding='cp949')
        value = data_pd['ID'].values.tolist()
        pd.set_option('display.float_format', '{:,.2f}'.format)
        result = ia.multi_account_check(value)

        col1, col2 = st.beta_columns(2)
        with col1:
            st.write(
                f'<br><br><font color="blue" font size="5">💡\"{len(result[0])}\"</font> 개의 계정 분석이 완료되었습니다.',
                unsafe_allow_html=True)

            data_list = ([i["username"], i["followers"], i["avg_likes"], i["avg_comments"]] for i in result[0])
            df = pd.DataFrame(
                data=data_list, index=range(1, len(result[0]) + 1), columns=["계정명", "팔로워", "평균 좋아요", "평균 댓글"]
            )
            st.dataframe(df)

            # 엑셀 다운로드 기능
            st.markdown(get_table_download_link(df, "result"), unsafe_allow_html=True)

        with col2:
            if result[1]["account"] > 0:
                st.write(
                    f'<br><br><font color="blue" font size="5">❗\"{result[1]["account"]}\"</font> 개의 계정은 계정명 확인이 필요해요.',
                    unsafe_allow_html=True)
                for i in result[1]["list"]:
                    st.code(i)


# 4. 라이트 - 여러 계정 분석 (CSV 업로드)
if Anal_menu == menu_box[4]:
    st.title("59_Insight" + "\n" + "#### 💡 여러개의 인스타그램 계정 정보를 분석합니다.")
    st.code('''
❗️ CSV 파일의 A열에 인스타그램 계정명을 입력 후, 업로드 해주세요. (https://instagram.com/ <-- 을 제외한 계정명만 입력) 
❗️ 평균 좋아요 / 평균 댓글을 제외한 팔로워 수만 분석합니다.
😿 인스타그램은 시간당 조회 제한이 있어요. 
  (오류가 뜨거나 검색이 되지 않는다면 조회 허용 범위가 초과된 것이니, 잠시 후 다시 시도해주세요.)
    ''')
    with st.sidebar:
        upload = False
        with st.form(key="light_multi_account_form"):
            st.write("파일 업로드")
            LMAC_file = st.file_uploader("❗️ CSV 파일을 업로드해주세요.", help="A열에 분석하고자 하는 계정명을 나열한 후, 'csv' 파일로 저장해주세요.")
            LMAC_button = st.form_submit_button(label="계정 분석 시작")

    if LMAC_button:
        data = LMAC_file.getvalue()
        data_pd = pd.read_csv(LMAC_file, names=['ID'], encoding='cp949')
        value = data_pd['ID'].values.tolist()
        pd.set_option('display.float_format', '{:,.2f}'.format)
        result = ia.multi_account_check_light(value)

        col1, col2 = st.beta_columns(2)
        with col1:
            st.write(
                f'<br><br><font color="blue" font size="5">💡\"{len(result[0])}\"</font> 개의 계정 분석이 완료되었습니다.',
                unsafe_allow_html=True)

            data_list = ([i["username"], i["followers"]] for i in result[0])
            df = pd.DataFrame(
                data=data_list, index=range(1, len(result[0]) + 1), columns=["계정명", "팔로워"]
            )
            st.dataframe(df)

            # 엑셀 다운로드 기능
            st.markdown(get_table_download_link(df, "result"), unsafe_allow_html=True)

        with col2:
            if result[1]["account"] > 0:
                st.write(
                    f'<br><br><font color="blue" font size="5">❗\"{result[1]["account"]}\"</font> 개의 계정은 계정명 확인이 필요해요.',
                    unsafe_allow_html=True)
                for i in result[1]["list"]:
                    st.code(i)


# 5. 포스팅 여러개 분석하기
if Anal_menu == menu_box[5]:
    st.title("59_Insight" + "\n" + "#### 💡 여러개의 인스타그램 게시글 정보를 분석합니다.")
    st.code('''
❗️ CSV 파일의 A열에 게시글 주소를 입력 후, 업로드 해주세요. 
❗️ https://www.instagram.com/p/ <-- 으로 시작하는 주소 전체를 정확하게 입력하셔야 분석이 가능합니다.
❗️ 많은 게시글을 분석하시면 시간이 오래 걸릴 수 있으니, 인내심을 가져주세요!
😿 인스타그램은 시간당 조회 제한이 있어요. 
  (오류가 뜨거나 검색이 되지 않는다면 조회 허용 범위가 초과된 것이니, 잠시 후 다시 시도해주세요.)
    ''')
    with st.sidebar:
        upload = False
        with st.form(key="posts_check_form"):
            st.write("파일 업로드")
            PC_file = st.file_uploader("❗️ CSV 파일을 업로드해주세요.", help="A열에 분석하고자 하는 게시글 주소를 나열한 후, 'csv' 파일로 저장해주세요.")
            PC_button = st.form_submit_button(label="게시글 분석 시작")

    if PC_button:
        data = PC_file.getvalue()
        data_pd = pd.read_csv(PC_file, names=['PC_ID'], encoding='cp949')
        value = data_pd['PC_ID'].values.tolist()
        result = ia.posts_check(value)

        col1, col2 = st.beta_columns([3, 1])
        with col1:
            st.write(
                f'<br><br><font color="blue" font size="5">💡\"{len(result[0])}\"</font> 개의 게시글 분석이 완료되었습니다.',
                unsafe_allow_html=True)

            data_list = ([i["username"], i["followers"], i["likes"], i["comments"], i["tagged"], i["upload_date"]] for i in result[0])
            df = pd.DataFrame(
                data=data_list, index=range(1, len(result[0]) + 1), columns=["계정명", "팔로워", "좋아요", "댓글", "태그된 계정", "업로드 시간"]
            )
            st.dataframe(df)

            # 엑셀 다운로드 기능
            st.markdown(get_table_download_link(df, "result_post"), unsafe_allow_html=True)

        with col2:
            if result[1]["count"] > 0:
                st.write(
                    f'<br><br><font color="blue" font size="5">❗\"{result[1]["count"]}\"</font> 개의 게시글은 주소 확인이 필요해요.',
                    unsafe_allow_html=True)
                for i in result[1]["list"]:
                    st.code(i)


st.sidebar.markdown("<div align='right'><font color='gray' font size = '2'>made by 59</font></div>",
                    unsafe_allow_html=True)
