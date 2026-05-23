import streamlit as st
from duckduckgo_search import DDGS

# 1. Səhifə Ayarları
st.set_page_config(page_title="EduAI Pro", page_icon="🎓", layout="wide")

# 2. İstifadəçi Bazası (Sessiyada saxlanılır ki, VIP statusu dinamik dəyişə bilsin)
if 'users' not in st.session_state:
    st.session_state['users'] = {
        'ayse': {'name': 'Aysel', 'password': '123', 'is_vip': True},
        'user': {'name': 'Tələbə', 'password': '123', 'is_vip': False}
    }

# Login funksiyası
def login():
    st.sidebar.title("🔑 Giriş Paneli")
    username = st.sidebar.text_input("İstifadəçi adı")
    password = st.sidebar.text_input("Şifrə", type="password")
    if st.sidebar.button("Daxil Ol", use_container_width=True):
        if username in st.session_state['users'] and st.session_state['users'][username]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.sidebar.error("Yanlış istifadəçi adı və ya şifrə!")

# 3. Əsas Proqram Məntiqi
if 'logged_in' not in st.session_state:
    login()
    st.title("🎓 EduAI Pro-ya Xoş Gəlmisiniz!")
    st.info("💡 Davam etmək üçün sol paneldən daxil olun.")
    st.write("Sınaq üçün VIP: `ayse` (şifrə: 123) və ya Standart: `user` (şifrə: 123) istifadə edə bilərsiniz.")
else:
    # Cari istifadəçinin məlumatları
    username = st.session_state['username']
    current_user = st.session_state['users'][username]
    is_vip = current_user.get('is_vip', False)
    
    # Sol Panel (Sidebar) İdarəetməsi
    st.sidebar.title(f"👤 {current_user['name']}")
    
    # --- VIP Paneli və Aktivləşdirmə Sistemi ---
    if is_vip:
        st.sidebar.success("⭐ VIP Üzv statusu aktivdir")
    else:
        st.sidebar.info("📉 Standart Hesab")
        st.sidebar.subheader("VIP Olmaq")
        st.sidebar.write("Ödəniş etmək üçün bura klikləyin: [Ödəniş Linki](https://example.com)")
        
        vip_kod_input = st.sidebar.text_input("VIP Kodunuzu daxil edin:", type="password")
        if st.sidebar.button("Aktivləşdir", use_container_width=True):
            # Kod təhlükəsizliyi üçün real layihədə st.secrets daxilində saxlanılması məsləhətdir
            if vip_kod_input == "GIZLIN_VIP_KOD":
                st.session_state['users'][username]['is_vip'] = True
                st.sidebar.success("Təbriklər! VIP statusunuz aktivləşdirildi.")
                st.rerun()
            else:
                st.sidebar.error("Yanlış kod daxil edilib!")
                
    st.sidebar.divider()
    lang = st.sidebar.selectbox("Dil / Language", ["Azərbaycan", "English"])
    
    if st.sidebar.button("🚪 Çıxış", use_container_width=True):
        del st.session_state['logged_in']
        del st.session_state['username']
        st.rerun()
        
    # --- Əsas Səhifə Kontenti ---
    st.title(f"🎓 EduAI Pro — Öyrənmə Platforması")
    
    options = [
        "Riyaziyyat", "Azərbaycan dili", "Ədəbiyyat", "Fizika", "Kimya", 
        "Biologiya", "Tarix", "Coğrafiya", "İngilis dili", "İnformatika",
        "Proqramlaşdırma (Python/Java/C++)", "Data Elmi", "Fəlsəfə", "Astronomiya"
    ]
    subject = st.selectbox("Öyrənmək istədiyiniz sahəni seçin:", options)

    # Çoxdilli Mətn Lüğəti
    texts = {
        "Azərbaycan": {
            "button": "Plan Hazırla 🚀", 
            "loading": "Dərin məlumatlar toplanır və analiz edilir...", 
            "header": "Haqqında Ətraflı Tədris Materialı",
            "vip_text": "💎 VIP Eksklüziv: Sizin üçün internetdən çoxşaxəli və dərin metodoloji təhlil toplandı."
        },
        "English": {
            "button": "Generate Plan 🚀", 
            "loading": "Fetching and analyzing deep insights...", 
            "header": "Detailed Educational Material",
            "vip_text": "💎 VIP Exclusive: Deep methodological analysis and multiple sources gathered for you."
        }
    }

    # "Plan Hazırla" düyməsi basıldıqda
    if st.button(texts[lang]["button"], type="primary"):
        with st.spinner(texts[lang]["loading"]):
            try:
                with DDGS() as ddgs:
                    # VIP statusuna görə axtarış həcmi dəyişir
                    max_res = 3 if is_vip else 1
                    sorgu = f"{subject} fənni üzrə geniş akademik dərslər" if is_vip else f"{subject} haqqında qısa məlumat"
                    
                    results = list(ddgs.text(sorgu, max_results=max_res))
                    
                    if results:
                        st.subheader(f"📖 {subject} - {texts[lang]['header']}")
                        st.divider()
                        
                        # Nəticələrin ekrana çıxarılması
                        for idx, res in enumerate(results):
                            if is_vip:
                                with st.expander(f"📚 Mənbə {idx+1}: {res.get('title', 'Tədris Materialı')}", expanded=(idx==0)):
                                    st.write(res.get('body', ''))
                                    st.caption(f"🔗 [Mənbəyə keçid]({res.get('href', '#')})")
                            else:
                                st.write(res.get('body', ''))
                                st.caption(f"🔗 [Mənbəyə keçid]({res.get('href', '#')})")
                        
                        if is_vip:
                            st.info(texts[lang]["vip_text"])
                    else:
                        st.warning("Təəssüf ki, resurs tapılmadı. Yenidən yoxlayın.")
            except Exception:
                st.error("Axtarış zamanı bir xəta baş verdi.")

    # Tədris Metodları Bölməsi
    st.divider()
    st.subheader("🎯 Effektiv Tədris Metodları")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 💡 Feynman Texnikası
        Bir mövunu öyrənməyin ən yaxşı yolu onu **sadə dillə başqasına izah etməkdir**. 
        Anlamadığınız hissələri qeyd edin və yenidən mənbəyə qayıdın.
        """)
    with col2:
        st.markdown("""
        ### ⏳ Aralıqlı Təkrar (Spaced Repetition)
        Məlumatı uzunmüddətli yaddaşda saxlamaq üçün onu müəyyən fasilələrlə (1 gün, 3 gün, 7 gün sonra) yenidən təkrar edin.
        """)

import streamlit as st
from duckduckgo_search import DDGS

# 1. Səhifə Ayarları
st.set_page_config(page_title="EduAI Pro", page_icon="🎓", layout="centered")

# 2. İstifadəçi Bazası (Session-da saxlanılır)
if 'users' not in st.session_state:
    st.session_state['users'] = {'ayse': {'password': '123'}, 'user': {'password': '123'}}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. Funksiyalar
def login():
    st.sidebar.title("🔑 Giriş Paneli")
    username = st.sidebar.text_input("İstifadəçi adı", key="login_user")
    password = st.sidebar.text_input("Şifrə", type="password", key="login_pass")
    
    if st.sidebar.button("Daxil Ol"):
        if username in st.session_state['users'] and st.session_state['users'][username]['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.sidebar.error("Yanlış ad və ya şifrə!")

def signup():
    st.sidebar.title("📝 Qeydiyyat")
    new_user = st.sidebar.text_input("Yeni istifadəçi adı", key="signup_user")
    new_pass = st.sidebar.text_input("Yeni şifrə", type="password", key="signup_pass")
    
    if st.sidebar.button("Qeydiyyatdan keç"):
        if not new_user or not new_pass:
            st.sidebar.warning("Zəhmət olmasa bütün xanaları doldurun.")
        elif new_user not in st.session_state['users']:
            st.session_state['users'][new_user] = {'password': new_pass}
            st.sidebar.success("Hesab yaradıldı! İndi daxil ola bilərsiniz.")
        else:
            st.sidebar.warning("Bu istifadəçi artıq mövcuddur.")

# 4. Əsas Proqram
if not st.session_state['logged_in']:
    menu = st.sidebar.radio("Menyu", ["Daxil ol", "Qeydiyyatdan keç"])
    if menu == "Daxil ol": 
        login()
    else: 
        signup()
    
    # Giriş etməyən istifadəçilər üçün qarşılama ekranı
    st.title("EduAI Pro-ya Xoş Gəlmisiniz! 👋")
    st.info("Platformanın imkanlarından yararlanmaq üçün soldakı paneldən daxil olun və ya qeydiyyatdan keçin.")
else:
    # Giriş etmiş istifadəçinin interfeysi
    st.title(f"EduAI Pro — Öyrənmə Platforması 🚀")
    st.subheader(f"Xoş gördük, {st.session_state['username']}!")
    
    subject = st.selectbox("Öyrənmək istədiyiniz sahəni seçin:", ["Riyaziyyat", "Fizika", "Kimya", "Tarix"])
    
    if st.button("Plan Hazırla ✨"):
        try:
            with st.spinner("Sizin üçün ən yaxşı resurslar araşdırılır..."):
                # DuckDuckGo axtarışı
                with DDGS() as ddgs:
                    results = list(ddgs.text(f"{subject} dərsləri üçün tədris planı və resurslar", max_results=3))
                
                if results:
                    st.success(f"**{subject}** sahəsi üzrə tapılan resurslar:")
                    st.write("---")
                    for i, r in enumerate(results, 1):
                        st.markdown(f"### {i}. {r['title']}")
                        st.markdown(f"[Resursa keçid edin]({r['href']})")
                        if 'body' in r:
                            st.caption(r['body'])
                        st.write("---")
                else:
                    st.warning("Təəssüf ki, uyğun resurs tapılmadı.")
                    
        except Exception as e:
            st.error("Hazırda internet axtarışı zamanı xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin.")

    # Çıxış düyməsi
    if st.sidebar.button("Çıxış Paneli 🚪"):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        st.rerun()
