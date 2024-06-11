import streamlit as st
import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt
from data import *


data = pd.read_csv('2023_kice_eng_text_sample.csv')
kice_data = pd.DataFrame(data)

print(kice_data.head())

senIds = []
word = word_data.loc[word_data['번호']==6].iloc[0]['영어단어']

print(word)

for i in range(395):
    sen = kice_data.loc[kice_data['key'] == i+1].iloc[0]['문장']
    sen = sen.lower().replace(',', '').split()
    if word in sen:
        senIds.append(i+1)
        print(int(kice_data.loc[kice_data['key'] == i+1].iloc[0]['응시년도']), end='.')
        print(int(kice_data.loc[kice_data['key'] == i+1].iloc[0]['모의고사']), end='.')
        print(kice_data.loc[kice_data['key'] == i+1].iloc[0]['문항번호'], end='번 문항 ')
        print(kice_data.loc[kice_data['key'] == i+1].iloc[0]['문장'])