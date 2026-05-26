import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="EduAI Pro", page_icon="🎓")

if 'users' not in st.session_state:
    st.session_state['users'] = {'ayse': {'password': '123'}, 'user': {'password': '123'}}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

def login():
    st.sidebar.title("🔑 Giriş")
    username = st.sidebar.text_input("İstifadəçi adı")
    password = st.sidebar.text_input("Şifrə", type="password")
    if st.sidebar.button("Daxil Ol"):
        if username in st.session_state['users'] and st.session_state['users'][username]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.sidebar.error("Yanlış giriş!")

if not st.session_state['logged_in']:
    st.title("EduAI Pro-ya Xoş Gəlmisiniz!")
    login()
else:
    st.sidebar.write(f"Salam, {st.session_state['username']}!")
    subject = st.selectbox("Sahəni seçin:", ["Riyaziyyat", "Fizika", "Kimya", "Tarix"])
    if st.button("Plan Hazırla 🚀"):
        try:
            with st.spinner("Axtarılır..."):
                results = DDGS().text(f"{subject} üçün tədris planı", max_results=3)
                for r in results:
                    st.write(f"**{r['title']}**")
                    st.write(r['href'])
        except:
            st.error("Bir xəta oldu, yenidən yoxla.")
    if st.sidebar.button("Çıxış"):
        st.session_state['logged_in'] = False
        st.rerun()
