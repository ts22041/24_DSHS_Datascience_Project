import streamlit as st
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt

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