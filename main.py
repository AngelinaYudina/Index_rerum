import streamlit as st
import pandas as pd
import numpy as np
from Functions import custom_print

st.set_page_config(
    page_title="Index rerum",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "mailto:avyudina_2@edu.hse.ru",
        "About": """
        Автор: Ангелина Юдина ([GitHub](https://github.com/AngelinaYudina), [cайт](https://www.hse.ru/staff/ayudina))  
        Стажер-исследователь [Международного центра анализа и выбора решений НИУ ВШЭ](https://www.hse.ru/DeCAn/)
        """
    }
)
st.title("Основные понятия философии техники от Э. Каппа до STS. Index rerum")

# global constants
messages = ["Понятие на русском:", "Понятие на английском:", "Понятие на немецком:", "Понятие на французском:",
            "Терминологическое гнездо:", "Определения:", "Цитаты:", "Ключевые авторы:", "Источники:",
            "Институты и исследовательские группы:", "Предметные области:"]
new_row_flags = [False, False, False, False, False, True, True, False, True, True, False]
link_flag = [False, False, False, False, True, False, False, False, False, False, False]

# data preparation
df = pd.read_excel("Demo Data.xlsx")
df.fillna("-", inplace=True)
to_lower_list = ["Понятие_rus", "Понятие_eng", "Понятие_ger", "Понятие_fr", "Терминологическое гнездо"]
for col in to_lower_list:
    df[col] = df[col].str.lower()
rel_terms = dict()
for i in range(len(df.values)):
    df_split = df.values[i][4].split(";\n")
    for el in df_split:
        if el not in rel_terms:
            rel_terms[el] = [df["Понятие_rus"].iloc[i]]
        else:
            rel_terms[el].append(df["Понятие_rus"].iloc[i])

# tabs
tab1_search, tab2_list = st.tabs(["Поиск", "Список понятий"])

# search
with tab1_search:
    user_input = st.text_input("Введите понятие", value="", key="search").lower().strip()
    s1 = df["Понятие_rus"].str.contains(user_input)
    s2 = df["Понятие_eng"].str.contains(user_input)
    s3 = df["Понятие_ger"].str.contains(user_input)
    s4 = df["Понятие_fr"].str.contains(user_input)
    df_search_res = df[s1 | s2 | s3 | s4]
    if user_input:
        if df_search_res.shape[0] == 0 or user_input == "-":
            st.write("Ничего не найдено")
        elif df_search_res.values.shape[0] == 1:
            st.markdown("---")
            data_list = [*df_search_res["Понятие_rus"].values, *df_search_res["Понятие_eng"].values,
                         *df_search_res["Понятие_ger"].values, *df_search_res["Понятие_fr"].values,
                         *df_search_res["Терминологическое гнездо"].values, *df_search_res["Определения"].values,
                         *df_search_res["Цитаты"].values, *df_search_res["Ключевые авторы"].values,
                         *df_search_res["Источники"].values, *df_search_res["Институты и исслед. группы"].values,
                         *df_search_res["Предметные области"].values]
            for i in range(len(data_list)):
                custom_print(*df_search_res["Понятие_rus"].values, messages[i], data_list[i], rel_terms,
                             new_row_flags[i], link_flag[i], data_rel=[messages, df, new_row_flags, link_flag])
            st.markdown("---")
        else:
            if s1.sum():
                words = list(df_search_res["Понятие_rus"])
            else:
                l_name = ["Понятие_eng", "Понятие_ger", "Понятие_fr"][np.array([s2.sum(), s3.sum(), s4.sum()]).argmax()]
                words = list(df_search_res[l_name])
            word_selected = st.selectbox("По вашему запросу найдено несколько понятий", index=None,
                                         placeholder="Выберите подходящее понятие...", options=words)
            st.markdown("---")
            for row in df_search_res.values:
                if word_selected in [row[0], row[1], row[2], row[3]]:
                    data_list = [row[0], row[1], row[2], row[3], row[4], row[9], row[10], row[5], row[6], row[7],
                                 row[8]]
                    for i in range(len(data_list)):
                        custom_print(row[0], messages[i], data_list[i], rel_terms, new_row_flags[i], link_flag[i],
                                     data_rel=[messages, df, new_row_flags, link_flag])
                    st.markdown("---")
                    break

# list
with tab2_list:
    language_selected = st.selectbox("Выберите язык", options=["Rus", "Eng", "Ger", "Fr"])
    index = ["Rus", "Eng", "Ger", "Fr"].index(language_selected)
    for row in df.values:
        with st.expander(f"**{str(row[index]).capitalize()}**"):
            st.markdown("---")
            data_list = [row[0], row[1], row[2], row[3], row[4], row[9], row[10], row[5], row[6], row[7],
                         row[8]]
            for i in range(len(data_list)):
                custom_print(row[0], messages[i], data_list[i], rel_terms, new_row_flags[i], link_flag[i],
                             is_search=False)
