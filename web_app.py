import streamlit as st
from duckduckgo_search import DDGS  # Yenilənmiş kitabxana sinfi

# Səhifə konfiqurasiyası
st.set_page_config(page_title="EduAI Pro", page_icon="🎓", layout="wide")

# Sessiya məlumatlarının yoxlanılması
if 'users' not in st.session_state:
    st.session_state['users'] = {'ayse': {'password': '123'}, 'user': {'password': '123'}}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# Giriş funksiyası
def login_page():
    st.title("🎓 EduAI Pro-ya Xoş Gəlmisiniz!")
    st.subheader("Davam etmək üçün sistemə daxil olun")
    
    # Giriş formunu mərkəzə gətirmək üçün sütunlar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("İstifadəçi adı")
            password = st.text_input("Şifrə", type="password")
            submit = st.form_submit_button("Daxil Ol 🔑")
            
            if submit:
                if username in st.session_state['users'] and st.session_state['users'][username]['password'] == password:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success("Uğurla giriş etdiniz!")
                    st.rerun()
                else:
                    st.error("İstifadəçi adı və ya şifrə yanlışdır!")

# Əsas Panel (Giriş edildikdən sonra)
def main_page():
    # Sol panel (Sidebar) idarəetməsi
    st.sidebar.title(f"👤 Xoş gəldiniz, {st.session_state['username']}!")
    if st.sidebar.button("Çıxış Et 🚪"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.rerun()
        
    # Əsas məzmun
    st.title("EduAI Pro — Öyrənmə Platforması")
    
    subject = st.selectbox("Sahəni seçin:", ["Riyaziyyat", "Fizika", "Kimya", "Tarix"])
    
    if st.button("Plan Hazırla 🚀"):
        st.write(f"### {subject} üçün fərdi tədris planı hazırlanır...")
        
        # DuckDuckGo vasitəsilə axtarış nümunəsi (Gələcəkdə istifadə üçün)
        with st.spinner("Mövzuya uyğun resurslar axtarılır..."):
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(f"{subject} dərsləri və resursları", max_results=3))
                    if results:
                        st.write("📖 **Faydalı xarici resurslar:**")
                        for r in results:
                            st.write(f"- [{r['title']}]({r['href']})")
            except Exception as e:
                st.info("Axtarış sisteminə qoşulmaq mümkün olmadı, lakin planınız tezliklə hazır olacaq!")

# Səhifə axınının idarə edilməsi
if not st.session_state['logged_in']:
    login_page()
else:
    main_page()
