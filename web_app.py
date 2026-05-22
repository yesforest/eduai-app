import random
import streamlit as st
import streamlit.components.v1 as components

# 1. SƏHİFƏ KONFİQURASİYASI (Mütləq ən birinci gəlməlidir)
st.set_page_config(page_title="EduAI Ultra Global Scheduler", page_icon="🤖", layout="wide")

# 2. SÜNİ İNTELLEKT QLOVAL TƏRCÜMƏ SİSTEMİ (Google Translate)
html_kodu = """
<div style="text-align: right; padding: 10px;">
    <div id="google_translate_element"></div>
</div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'az', 
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element');
}
</script>
<script type="text/javascript" src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""

# Tərcümə düyməsini ekrana buraxırıq
components.html(html_kodu, height=60, scrolling=False)


# 3. SƏHİFƏNİN ƏSAS BAŞLIQLARI
st.title("🤖 EduAI Ağıllı Tədris Asistanı / Smart Study Assistant")
st.subheader("Dinamik planlaşdırma, mövzu tövsiyələri və motivasiya bir arada! 🚀")

st.write("---")

# 4. DATA VƏ MƏNTİQ SİSTEMİ (Sənin kodunun ardı)

# Motivasiya sözləri bazası
motivasiya_sozleri = [
    "Uğur, hər gün təkrarlanan kiçik səylərin cəmidir! 💪",
    "Başlamaq üçün mükəmməl olmaq məcburiyyətində deyilsən, amma mükəmməl olmaq üçün başlamalısan! ✨",
    "Dahilik 1% istedad, 99% tərləməkdir. – Tomas Edison 💡",
    "Bu gün atdığın kiçik bir addım, sabahkı böyük uğurunun təməlidir! 🔥",
    "Çətinliklər səni qorxutmasın, onlar səni daha da gücləndirir! 🌟"
]

# Mövzular üzrə tövsiyə lüğəti
movzu_hovuzu = {
    "Riyaziyyat": ["Törəmə və İnteqral tətbiqləri", "Ehtimal nəzəriyyəsi", "Xətti tənliklər sistemi", "Triqonometriya"],
    "Proqramlaşdırma (Python)": ["List Comprehensions və Lamda", "OOP (Obyektyönümlü proqramlaşdırma)", "Streamlit ilə Web API", "Pandas ilə Data Analizi"],
    "Xarici Dil (İngilis dili)": ["Phrasal Verbs (Frazeoloji fellər)", "Advanced Speaking Practice", "Writing (Essay strukturu)", "Listening - TED Talks"],
    "Data Elmi": ["Xətti Reqressiya modeli", "Data Təmizləmə (Data Cleaning)", "Matplotlib ilə vizuallaşdırma", "SQL sorğuları"]
}

# Sol menyu (Sidebar) - İstifadəçi məlumatları daxil edir
st.sidebar.header("🎯 Planlaşdırma Ayarları")
ad = st.sidebar.text_input("Adınızı daxil edin:", placeholder="Məsələn: Əli")
sahə = st.sidebar.selectbox("Öyrənmək istədiyiniz sahə:", list(movzu_hovuzu.keys()))
gunler = st.sidebar.slider("Həftədə neçə gün oxuya bilərsiniz?", 1, 7, 3)
saat = st.sidebar.number_input("Günlük neçə saat ayıra bilərsiniz?", min_value=1, max_value=12, value=2)

# Əsas interfeys elementləri
col1, col2 = st.columns([2, 1])

with col1:
    st.write(f"### 👋 Xoş gəldin, **{ad if ad else 'Tələbə'}**!")
    st.info("Aşağıdakı düyməyə klikləyərək AI tərəfindən optimallaşdırılmış fərdi dərs planını əldə edə bilərsən.")
    
    # Plan yaratma düyməsi
    if st.button("📅 Dinamik Plan Yarat"):
        st.success(f"🎉 **{sahə}** sahəsi üçün fərdi tədris planınız hazırdır!")
        
        # Seçilmiş sahəyə uyğun mövzuları qarışdırıb təqdim edirik
        secilmis_movzular = movzu_hovuzu[sahə]
        
        # Günlük cədvəl cədvəli yaradılır
        st.write("#### 🗓️ Həftəlik Təqvim:")
        for i in range(1, gunler + 1):
            # Əgər mövzu sayı gün sayından azdırsa, dövrü təkrarlayırıq
            movzu = secilmis_movzular[(i - 1) % len(secilmis_movzular)]
            
            with st.expander(f"🟢 {i}-ci Gün Planı"):
                st.write(f"**Öyrəniləcək Mövzu:** {movzu}")
                st.write(f"**Ayrılan Zaman:** {saat} saat")
                st.write(f"**Tövsiyə olunan metod:** Pomodoro texnikası ilə {saat * 2} seans ({saat * 2} x 25 dəq).")
                st.checkbox("Tamamlandı kimi qeyd et", key=f"check_{i}")

with col2:
    st.write("### ⚡ Günün Motivasiyası")
    # Təsadüfi motivasiya sözü seçən mexanizm
    if st.button("🎲 Yeni Motivasiya Sözü"):
        st.session_state['motivasiya'] = random.choice(motivasiya_sozleri)
    
    # İlkin dəyər təyin edilir
    if 'motivasiya' not in st.session_state:
        st.session_state['motivasiya'] = motivasiya_sozleri[0]
        
    st.warning(st.session_state['motivasiya'])
    
    # Faydalı qeydlər bölməsi
    st.write("---")
    st.write("### 📝 Qeyd Dəftəri")
    qeyd = st.text_area("Öyrənərkən vacib qeydlərini bura yaz:", placeholder="Məsələn: Sabah mütləq OOP mövzusunu təkrar etməliyəm...")
    if qeyd:
        st.toast("Qeydiniz yadda saxlanıldı (Səhifə yenilənənə qədər)!", icon="💾")