import streamlit as st
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('word_list_with_examples.csv',  delimiter=';', encoding='utf-8')
word_data = pd.DataFrame(data)

data = pd.read_csv('2023_kice_eng_text_sample.csv')
kice_data = pd.DataFrame(data)


plt.rc("font", family = "Malgun Gothic")
sns.set(font="Malgun Gothic", rc={"axes.unicode_minus":False}, style='white')

def draw_figure1():
    pos_map = {
        '명': '명사',
        '동': '동사',
        '형': '형용사',
        '부': '부사',
        '전': '전치사',
        '접': '접사'
    }
    pos_counts = word_data['품사1'].map(pos_map).value_counts()
    plt.figure(figsize=(4, 4))
    st.write('**품사별 단어 수**')
    sns.barplot(x=pos_counts.index, y=pos_counts.values, palette=sns.color_palette("plasma")[::-1])
    plt.xlabel('품사')
    plt.ylabel('단어 수')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def draw_figure2():
    theme_counts = word_data['테마'].value_counts()
    plt.figure(figsize=(4, 4))
    st.write('**테마별 단어 분포**')
    sns.barplot(x=theme_counts.index, y=theme_counts.values/16, palette=sns.color_palette("plasma")[::-1])
    plt.xlabel('테마 종류')
    plt.ylabel('단어 분포[%]')
    plt.xticks([], [])
    st.pyplot(plt)

def draw_figure3():
    theme_counts2 = word_data['테마'].value_counts()
    most_frequent_theme = theme_counts2.idxmax()
    theme_counts = theme_counts2.drop(most_frequent_theme)
    plt.figure(figsize=(4, 4))
    st.write('**기타 테마별 단어 수**')
    sns.barplot(x=theme_counts.index, y=theme_counts.values, palette=sns.color_palette("plasma")[::-1][1:])
    plt.xlabel('테마 종류(기타)')
    plt.ylabel('단어 수')
    plt.xticks(rotation=90)
    st.pyplot(plt)

def draw_figure4():
    pass

def func_textAnalysis():
    text = st.text_input("아래 내용을 삭제하고 입력하세요", 'There is something deeply paradoxical about the professional status of sports journalism, especially in the medium of print.  In discharging their usual responsibilities of description and commentary, reporters’ accounts of sports events are eagerly consulted by sports fans, while in their broader journalistic role of covering sport in its many forms, sports journalists are among the most visible of all contemporary writers.  The ruminations of the elite class of ‘celebrity’ sports journalists are much sought after by the major newspapers, their lucrative contracts being the envy of colleagues in other ‘disciplines’ of journalism.  Yet sports journalists do not have a standing in their profession that corresponds to the size of their readerships or of their pay packets, with the old saying (now reaching the status of cliché) that sport is the ‘toy department of the news media’ still readily to hand as a dismissal of the worth of what sports journalists do.  This reluctance to take sports journalism seriously produces the paradoxical outcome that sports newspaper writers are much read but little admired.', placeholder='분석할 텍스트를 입력하세요.')
    with st.container():
        st.write('-'*70)
        st.write('**지문**')
        st.write(text)
        st.write('-'*70)

    words = text.lower().split()
    word_themes = word_data[word_data['영어단어'].isin(words)]['테마'].value_counts()
    dominant_theme = word_themes.idxmax() if not word_themes.empty else "No dominant theme"
    st.write(f'Dominant theme in the text:{dominant_theme}')

    col1, col2, col3 = st.columns([2,6,2])
    with col2:
        plt.figure(figsize=(4,4))
        plt.pie(word_themes, labels=word_themes.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
        plt.axis('equal')
        st.pyplot(plt)

    for theme in word_themes.index:
        theme_words = word_data[word_data['테마'] == theme]
        theme_words = theme_words[theme_words['영어단어'].isin(words)]
        st.write("-" * 30)
        st.write(f"**Theme: {theme}**")
        for _, row in theme_words.iterrows():
            meanings = ', '.join(
                [str(meaning) for meaning in [row['의미1'], row.get('의미2'), row.get('의미3')] if pd.notna(meaning)])
            st.write(f"**{row['영어단어']}**: {meanings}")

def func_showWords(wordId):
    if wordId in word_data['번호'].values:
        word_row = word_data.loc[word_data['번호'] == wordId].iloc[0]
        word = word_row['영어단어']
        theme = word_row['테마']
        pos1 = word_row['품사1']
        pos2 = word_row['품사2']
        pos3 = word_row['품사3']
        meaning1 = word_row['의미1']
        meaning2 = word_row['의미2']
        meaning3 = word_row['의미3']
        example1 = word_row['예시문1']
        example2 = word_row['예시문2']
        example3 = word_row['예시문3']

        st.title(word)
        st.write(f'**테마: {theme}**')
        st.write('_' * 50)
        col1, col2, col3 = st.columns([2, 1, 7])
        with col1:
            st.write(f'**{meaning1}**')
        with col2:
            st.write(f'{pos1}')
        with col3:
            st.write(example1)
        st.write('_' * 50)

        if not pd.isna(pos2):
            col1, col2, col3 = st.columns([2, 1, 7])
            with col1:
                st.write(f'**{meaning2}**')
            with col2:
                st.write(f'{pos2}')
            with col3:
                st.write(example2)
            st.write('_' * 50)

        if not pd.isna(pos3):
            col1, col2, col3 = st.columns([2, 1, 7])
            with col1:
                st.write(f'**{meaning3}**')
            with col2:
                st.write(f'{pos3}')
            with col3:
                st.write(example3)
            st.write('_' * 50)

        st.write('_'*50)
        st.write(f'**평가원 예시문**')
        for i in range(395):
            sen = kice_data.loc[kice_data['key'] == i + 1].iloc[0]['문장']
            sen = sen.lower().replace(',', '').split()
            if word in sen:
                year = int(kice_data.loc[kice_data['key'] == i + 1].iloc[0]['응시년도'])
                month = int(kice_data.loc[kice_data['key'] == i + 1].iloc[0]['모의고사'])
                num = kice_data.loc[kice_data['key'] == i + 1].iloc[0]['문항번호']
                sen = kice_data.loc[kice_data['key'] == i + 1].iloc[0]['문장']
                st.write(f'**{year}.{month}.{num}번 문항** {sen}')
        st.write('_'*50)

    else:
        st.write("ID not found.")

def func_createQuestions(num_questions):
    questions = []
    data = word_data
    data = data.dropna(subset=['의미1'])
    meanings = list(data['의미1'])

    for _ in range(num_questions):
        correct_row = data.sample(1)
        correct_word = correct_row['영어단어'].values[0]
        correct_meaning = correct_row['의미1'].values[0].split(",")[0].strip()

        wrong_meanings = random.sample([m for m in meanings if m != correct_meaning], 3)
        choices = random.sample([correct_meaning] + wrong_meanings, k=4)

        questions.append({'word': correct_word, 'choices': choices, 'correct_answer': correct_meaning})

    return questions

def page_home():
    st.title("영어 학습 플랫폼")
    name = st.text_input("Enter your name (10자 이내):", max_chars=10, placeholder="user name")
    if st.button("Submit"):
        st.session_state.username = name
        st.session_state.page = 'SelectLevel'
        st.experimental_rerun()

def page_selectLevel():
    st.title("영어 학습 플랫폼")
    st.write("Choose your level:")
    level_options = ["Beginner", "Intermediate", "Advanced"]
    level = st.radio("", level_options)
    st.write('고3 영어 기준, 1등급 (Advanced), 1~2등급 (Intermediate), 3등급 이하 (Beginner)이 적정합니다')
    if st.button("Submit"):
        st.session_state.level = level
        st.session_state.page = 'SelectDailyAmount'
        st.experimental_rerun()

def page_selectDailyAmount():
    st.title("영어 학습 플랫폼")
    st.write("Choose your daily amount:")
    amount_options = ["25개 (64일 완성)", "40개 (40일 완성)", "50개 (32일 완성)"]
    option = st.radio("", amount_options, key="daily_words")
    if st.button("Submit"):
        if option == "25개 (64일 완성)":
            st.session_state.dailyamount = 25
            st.session_state.sessionnumber = 64
        elif option == "40개 (40일 완성)":
            st.session_state.dailyamount = 40
            st.session_state.sessionnumber = 40
        else:
            st.session_state.dailyamount = 50
            st.session_state.sessionnumber = 32
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_home2():
    today = datetime.datetime.now().strftime('%Y-%m-%d (%A)')
    st.write(f"Today: {today}")
    st.subheader(f"Hi, {st.session_state.username}!")
    st.header('단어 학습 시작하기')
    st.markdown(f"""
        <div style="color: gray; font-weight: bold; font-size: 25px;">
            최근 학습 진도
        </div>
        """, unsafe_allow_html=True)
    if st.button(f"Day {st.session_state.userprogress}"):
        st.session_state.learnPageRequest = st.session_state.userprogress
        st.session_state.dayPageRequest = (st.session_state.learnPageRequest - 1) * st.session_state.dailyamount + 1
        st.session_state.page = 'Day'
        st.experimental_rerun()
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            text = f'{st.session_state.userprogress * st.session_state.dailyamount} / 1600 단어'
            st.markdown(f"""
                <div style="color: gray; font-weight: bold; font-size: 25px; line-height: 0.7;">
                    학습 진행도
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="color: gray; font-size: 18px;">
                    ({text})
                </div>
                """, unsafe_allow_html=True)

            progress = st.session_state.userprogress / st.session_state.sessionnumber * 100
            sizes = [progress, 100 - progress]
            colors = ['orange', 'gray']
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, colors=colors, startangle=90, counterclock=False)
            centre_circle = plt.Circle((0, 0), 0.80, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            ax1.text(0, 0, f'{progress:.1f}%', ha='center', va='center', fontsize=20, color='black')
            ax1.axis('equal')

            st.pyplot(fig1)

    with col2:
        with st.container():
            st.markdown(f"""
                <div style="color: gray; font-weight: bold; font-size: 25px; line-height: 1.2;">
                    나만의 북마크
                </div>
                """, unsafe_allow_html=True)
            st.image('bookmark_icon.png', width=200)
            col1, col2 = st.columns([6, 4])
            with col1:
                with st.container():
                    st.markdown(f"""
                            <div style="color: gray; font-weight: bold; font-size: 22px; line-height: 0.7;">
                                추가된 단어
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown(f"""
                            <div style="font-weight: bold; font-size: 20px;">
                                {len(st.session_state.bookmarks)}단어
                            </div>
                            """, unsafe_allow_html=True)
            with col2:
                if st.button('→'):
                    st.session_state.page = 'Bookmark'
                    st.experimental_rerun()

    st.write('')
    st.container()

    if st.button("Logout"):
        st.session_state.username = 'DSHS'
        st.session_state.dailyamount = 40
        st.session_state.userprogress = 1
        st.session_state.sessionnumber = 40
        st.session_state.bookmarks = set()
        st.session_state.learnPageRequest = 0
        st.session_state.dayPageRequest = 0
        st.session_state.testPageRequest = 50
        st.session_state.questionPageRequest = 0
        st.session_state.testPageResponses = 0
        st.session_state.testQuestions = []
        st.session_state.resultPageRequest = []
        st.session_state.page = 'Home'
        st.experimental_rerun()

    with st.sidebar:
        st.title("영어 단어장")
        if st.button("단어 학습"):
            st.session_state.page = 'Learn'
            st.experimental_rerun()
        if st.button("테스트 응시"):
            st.session_state.page = 'Test'
            st.experimental_rerun()
        if st.button("성적 분석"):
            st.session_state.page = 'Result'
            st.experimental_rerun()
        if st.button("지문 분석(beta)"):
            st.session_state.page = 'TextAnalysis'
            st.experimental_rerun()
        if st.button("단어장 설명"):
            st.session_state.page = 'Info'
            st.experimental_rerun()

def page_bookmark():
    st.title("북마크")
    st.write("**북마크한 단어를 확인해 보세요.**")
    for wordId in st.session_state.bookmarks:
        word_row = word_data.loc[word_data['번호'] == wordId].iloc[0]
        word = word_row['영어단어']
        theme = word_row['테마']
        pos1 = word_row['품사1']
        pos2 = word_row['품사2']
        pos3 = word_row['품사3']
        meaning1 = word_row['의미1']
        meaning2 = word_row['의미2']
        meaning3 = word_row['의미3']
        example1 = word_row['예시문1']
        example2 = word_row['예시문2']
        example3 = word_row['예시문3']

        st.title(word)
        st.write(f'**테마: {theme}**')
        st.write('_' * 50)
        col1, col2, col3 = st.columns([2, 1, 7])
        with col1:
            st.write(f'**{meaning1}**')
        with col2:
            st.write(f'{pos1}')
        with col3:
            st.write(example1)
        st.write('_' * 50)

        if not pd.isna(pos2):
            col1, col2, col3 = st.columns([2, 1, 7])
            with col1:
                st.write(f'**{meaning2}**')
            with col2:
                st.write(f'{pos2}')
            with col3:
                st.write(example2)
            st.write('_' * 50)

        if not pd.isna(pos3):
            col1, col2, col3 = st.columns([2, 1, 7])
            with col1:
                st.write(f'**{meaning3}**')
            with col2:
                st.write(f'{pos3}')
            with col3:
                st.write(example3)
            st.write('_' * 50)

        if st.button('북마크 제거', key=f'choice{word}'):
            st.session_state.bookmarks.remove(wordId)
            st.experimental_rerun()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_learn():
    st.title("단어 학습")
    st.write(f"**하루에 {st.session_state.dailyamount}단어씩 학습합니다.**")
    col1, col2, col3 = st.columns([1, 7, 2])
    with col1:
        st.write('Day')
    with col2:
        st.write('Theme')
    with col3:
        st.write('완료')
    for i in range(int(st.session_state.sessionnumber)):
        with st.container():
            col1, col2, col3 = st.columns([1,7,2])
            with col1:
                if st.button(f'**Day {i+1}**'):
                    st.session_state.learnPageRequest = i+1
                    st.session_state.dayPageRequest = (st.session_state.learnPageRequest - 1) * st.session_state.dailyamount + 1
                    st.session_state.page = 'Day'
                    st.experimental_rerun()
            with col2:
                st.write('1324')
            with col3:
                st.write('1')
    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_day():
    st.title(f'**단어 학습 Day {st.session_state.learnPageRequest}**')
    func_showWords(st.session_state.dayPageRequest)
    col1, col2, col3 = st.columns([3.75, 5.25, 2])
    with col1:
        if st.button('이전'):
            st.session_state.dayPageRequest -= 1
            st.session_state.page = 'Day'
            st.experimental_rerun()
    with col2:
        if st.button('북마크 추가'):
            st.session_state.bookmarks.add(st.session_state.dayPageRequest)
            st.experimental_rerun()
    with col3:
        if st.button('다음'):
            st.session_state.dayPageRequest += 1
            st.session_state.page = 'Day'
            st.experimental_rerun()

    if st.sidebar.button("학습 리스트"):
        st.session_state.page = 'Learn'
        st.experimental_rerun()

def page_test():
    st.title("테스트 응시")
    st.write("**테스트를 통해 모르는 단어를 점검해 보세요**")
    if st.button('20단어 테스트'):
        st.session_state.testPageRequest = 20
        st.session_state.questionPageRequest = 0
        st.session_state.testQuestions = func_createQuestions(st.session_state.testPageRequest)
        st.session_state.testPageResponses = []
        st.session_state.page = 'Question'
        st.experimental_rerun()
    if st.button('30단어 테스트'):
        st.session_state.testPageRequest = 30
        st.session_state.questionPageRequest = 0
        st.session_state.testQuestions = func_createQuestions(st.session_state.testPageRequest)
        st.session_state.testPageResponses = []
        st.session_state.page = 'Question'
        st.experimental_rerun()
    if st.button('50단어 테스트'):
        st.session_state.testPageRequest = 50
        st.session_state.questionPageRequest = 0
        st.session_state.testQuestions = func_createQuestions(st.session_state.testPageRequest)
        st.session_state.testPageResponses = []
        st.session_state.page = 'Question'
        st.experimental_rerun()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_question():
    if st.session_state.questionPageRequest == st.session_state.testPageRequest:
        st.title('테스트 결과')
        results_df = pd.DataFrame(st.session_state.testPageResponses)
        st.write(results_df)
    else:
        st.write(f'**{st.session_state.questionPageRequest + 1}/{st.session_state.testPageRequest}**')
        question = st.session_state.testQuestions[st.session_state.questionPageRequest]
        st.title(f'**{question["word"]}**')

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f'1. {question["choices"][0]}', key='choice1'):
                user_answer = question["choices"][0]
                is_correct = user_answer == question['correct_answer']
                st.session_state.testPageResponses.append(
                    {'question': question['word'], 'user_answer': user_answer, 'correct': is_correct})
                st.session_state.questionPageRequest += 1
                st.experimental_rerun()
            if st.button(f'3. {question["choices"][2]}', key='choice3'):
                user_answer = question["choices"][2]
                is_correct = user_answer == question['correct_answer']
                st.session_state.testPageResponses.append(
                    {'question': question['word'], 'user_answer': user_answer, 'correct': is_correct})
                st.session_state.questionPageRequest += 1
                st.experimental_rerun()

        with col2:
            if st.button(f'2. {question["choices"][1]}', key='choice2'):
                user_answer = question["choices"][1]
                is_correct = user_answer == question['correct_answer']
                st.session_state.testPageResponses.append(
                    {'question': question['word'], 'user_answer': user_answer, 'correct': is_correct})
                st.session_state.questionPageRequest += 1
                st.experimental_rerun()
            if st.button(f'4. {question["choices"][3]}', key='choice4'):
                user_answer = question["choices"][3]
                is_correct = user_answer == question['correct_answer']
                st.session_state.testPageResponses.append(
                    {'question': question['word'], 'user_answer': user_answer, 'correct': is_correct})
                st.session_state.questionPageRequest += 1
                st.experimental_rerun()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_result():
    st.title("테스트 응시 결과 분석")
    st.write("**분석할 테스트 결과 파일을 업로드해주세요.**")
    uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
    incorrect_words = []

    for file in uploaded_files:
        name = file.name
        st.write(name)
        file = pd.read_csv(file)
        file = pd.DataFrame(file)
        file.index = file.index+1
        col1, col2 = st.columns(2)
        with col1:
            result = file.drop(columns=['Unnamed: 0'])
            st.write(result)
        with col2:
            st.write(f'{name.split('-')[0]}년 {name.split('-')[1]}월 {name.split('-')[2][:2]}일 응시')
            st.write(f'**{len(file)}문항 테스트 응시 결과**')
            col1, col2, col3 = st.columns([1.5,7,1.5])
            with col2:
                result = result['correct'].value_counts()
                colors = ['navy', 'gray']
                fig1, ax1 = plt.subplots()
                ax1.pie(result, colors=colors, startangle=90)
                centre_circle = plt.Circle((0, 0), 0.75, fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(centre_circle)
                ax1.text(0, 0, f'{result[0]}/{len(file)}', ha='center', va='center', fontsize=25, color='black')
                st.pyplot(fig1)

            st.write('_'*20)

            st.write('**틀린 문항 확인**')
            incorrect = file.loc[file['correct'] == False]
            incorrect_words.extend(incorrect['question'].tolist())
            incorrect = incorrect.drop(columns=['Unnamed: 0', 'correct'])
            st.write(incorrect)
        st.write('_'*50)

    if st.button("Submit"):
        st.session_state.resultPageRequest = incorrect_words
        st.session_state.page = 'Analysis'
        st.experimental_rerun()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_analysis():
    st.title("틀린 단어 학습")
    incorrect_words = st.session_state.resultPageRequest
    for word in incorrect_words:
        word_row = word_data.loc[word_data['영어단어'] == word].iloc[0]
        wordId = word_row['번호']
        word = word_row['영어단어']
        theme = word_row['테마']
        pos1 = word_row['품사1']
        pos2 = word_row['품사2']
        pos3 = word_row['품사3']
        meaning1 = word_row['의미1']
        meaning2 = word_row['의미2']
        meaning3 = word_row['의미3']
        example1 = word_row['예시문1']
        example2 = word_row['예시문2']
        example3 = word_row['예시문3']

        st.title(word)
        st.write(f'**테마: {theme}**')
        st.write('_' * 50)
        col1, col2, col3 = st.columns([2, 1, 7])
        with col1:
            st.write(f'**{meaning1}**')
        with col2:
            st.write(f'{pos1}')
        with col3:
            st.write(example1)
        st.write('_' * 50)

        if not pd.isna(pos2):
            col1, col2, col3 = st.columns([2, 1, 7])
            with col1:
                st.write(f'**{meaning2}**')
            with col2:
                st.write(f'{pos2}')
            with col3:
                st.write(example2)
            st.write('_' * 50)

        if not pd.isna(pos3):
            col1, col2, col3 = st.columns([2, 1, 7])
            with col1:
                st.write(f'**{meaning3}**')
            with col2:
                st.write(f'{pos3}')
            with col3:
                st.write(example3)
            st.write('_' * 50)
        #st.write(f'**{st.session_state.username}이 혼동하는 의미: {word[1]}**')

        if st.button('북마크 추가', key=f'choice{word}'):
            st.session_state.bookmarks.add(wordId)
            st.experimental_rerun()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_textAnalysis():
    st.title("지문 분석(beta)")
    st.write("**지문 분석 기능은 구현했으나, minor한 기능이라 beta로 구분했습니다.**")
    func_textAnalysis()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

def page_info():
    st.title("단어장 정보")
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            draw_figure1()
    with col2:
        with st.container():
            obtion = st.selectbox('**품사별 단어 학습 전략**',('명사', '동사'))
            if obtion == '명사':
                st.write('**명사 학습 전략**')
                st.write('1. **분류별 학습**: 명사를 그룹화하여 학습하는 것이 좋습니다. 예를 들어, 생활용품, 식료품, 직업, 장소 등으로 분류하여 각 카테고리에 속한 명사를 함께 배울 수 있습니다. 이 방법은 관련 단어들 사이의 연관성을 이해하는 데 도움이 됩니다.')
                st.write('2. **시각 자료 활용**: 명사는 구체적인 사물이나 개념을 나타내므로 이미지, 사진 또는 실제 물건을 사용하여 학습하는 것이 효과적입니다. 이를 통해 단어와 그 대상의 시각적 연관성을 강화할 수 있습니다.')
                st.write("3. **맥락 연결**: 명사를 배울 때 그 명사가 사용되는 일반적인 상황이나 문맥을 함께 고려하면 좋습니다. 예를 들어 '커피'(명사)는 '마시다', '주문하다' 등의 동사와 자주 쓰이므로 이런 연결을 이해하는 것이 중요합니다.")
            if obtion == '동사':
                st.write('**동사 학습 전략**')
                st.write('1. **동사의 변형 연습**: 동사는 시제, 인칭, 수에 따라 형태가 변하는 경우가 많으므로, 다양한 변형을 연습하는 것이 중요합니다. 이를 위해 간단한 변형 표를 만들어 연습하거나, 해당 동사를 사용한 문장을 만들어보는 것이 도움이 됩니다.')
                st.write('2. **동사의 기능 이해**: 동사는 동작, 상태, 발생을 나타내므로, 각 동사가 어떤 동작이나 상태를 의미하는지, 어떤 상황에서 사용되는지를 명확히 이해하는 것이 중요합니다. 이를 위해 동사를 문장 안에서 사용해 보고, 해당 동작을 직접 수행해 보거나 시각화해 보는 것도 좋습니다.')
                st.write("3. **동사와 명사의 조합 연습**: 동사는 특정 명사와 자주 쓰이는 경향이 있습니다. 예를 들어 '쓰다'는 '편지', '노트', '리포트' 등과 같이 사용됩니다. 이러한 조합을 함께 연습함으로써 보다 자연스럽게 언어를 사용할 수 있습니다.")

    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.write('**단어 테마 분석**')
    with col2:
        with st.container():
            draw_figure2()
            draw_figure3()

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home2'
        st.experimental_rerun()

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