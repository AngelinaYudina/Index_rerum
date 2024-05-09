import streamlit as st


def custom_print(current_word, message, data, rel_terms, new_row, link_flag=False, is_search=True, data_rel=None):
    data_spl = data.split(";\n")
    if link_flag:
        st.write(f"**{message}** {data}")
        words = set()
        for el in data_spl:
            if el == "-":
                return
            for word in rel_terms[el.lower()]:
                if word != current_word:
                    words.add(word)
        if not words:
            return
        if is_search:
            st.write("Смежные понятия:")
            messages, df, new_row_flags, link_flag = data_rel
            for word in words:
                with st.expander(f"**{word}**"):
                    st.markdown("---")
                    s1 = df["Понятие_rus"] == word
                    s2 = df["Понятие_eng"] == word
                    s3 = df["Понятие_ger"] == word
                    s4 = df["Понятие_fr"] == word
                    df_search_res = df[s1 | s2 | s3 | s4]
                    data_list = [*df_search_res["Понятие_rus"].values, *df_search_res["Понятие_eng"].values,
                                 *df_search_res["Понятие_ger"].values, *df_search_res["Понятие_fr"].values,
                                 *df_search_res["Понятие_иное"].values,
                                 *df_search_res["Терминологическое гнездо"].values,
                                 *df_search_res["Определения"].values, *df_search_res["Цитаты"].values,
                                 *df_search_res["Ключевые авторы"].values, *df_search_res["Источники"].values,
                                 *df_search_res["Институты и исслед. группы"].values,
                                 *df_search_res["Предметные области"].values]
                    for i in range(len(data_list)):
                        custom_print(word, messages[i], data_list[i], rel_terms, new_row_flags[i], link_flag[i],
                                     is_search=False)
        else:
            st.write(f"**Смежные понятия:** {'; '.join(list(words))}")
    elif message == "Переводы на другие языки:" and data == "-":
        return
    elif data_spl[0] == "-" or not new_row:
        st.write(f"**{message}** {data}")
    elif len(data_spl) == 1:
        st.write(f"**{message}**")
        st.write(data)
    else:
        st.write(f"**{message}**")
        for i in range(len(data_spl)):
            text_res = str(i+1) + "\) " + data_spl[i]
            st.markdown(text_res, unsafe_allow_html=True)
