import streamlit

from page import *

if 'username' not in st.session_state:
    st.session_state.username = 'DSHS'
if 'dailyamount' not in st.session_state:
    st.session_state.dailyamount = 40
if 'userprogress' not in st.session_state:
    st.session_state.userprogress = 1
if 'sessionnumber' not in st.session_state:
    st.session_state.sessionnumber = 40
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = set()
if 'learnPageRequest' not in st.session_state:
    st.session_state.learnPageRequest = 0
if 'dayPageRequest' not in st.session_state:
    st.session_state.dayPageRequest = 0
if 'testPageRequest' not in st.session_state:
    st.session_state.testPageRequest = 50
if 'questionPageRequest' not in st.session_state:
    st.session_state.questionPageRequest = 0
if 'testPageResponses' not in st.session_state:
    st.session_state.testPageResponses = 0
if 'testQuestions' not in st.session_state:
    st.session_state.testQuestions = []
if 'resultPageRequest' not in st.session_state:
    st.session_state.resultPageRequest = []



if 'page' not in st.session_state:
    st.session_state.page = 'Home'


if st.session_state.page == 'Home':
    page_home()
elif st.session_state.page == 'SelectLevel':
    page_selectLevel()
elif st.session_state.page == 'SelectDailyAmount':
    page_selectDailyAmount()
elif st.session_state.page == 'Home2':
    page_home2()
elif st.session_state.page == 'Learn':
    page_learn()
elif st.session_state.page == 'Day':
    page_day()
elif st.session_state.page == 'Test':
    page_test()
elif st.session_state.page == 'Question':
    page_question()
elif st.session_state.page == 'Bookmark':
    page_bookmark()
elif st.session_state.page == 'Result':
    page_result()
elif st.session_state.page == 'Analysis':
    page_analysis()
elif st.session_state.page == 'TextAnalysis':
    page_textAnalysis()
elif st.session_state.page == 'Info':
    page_info()