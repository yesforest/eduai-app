import streamlit as st
import random

st.set_page_config(page_title="EduAI Ultra Global Scheduler", page_icon="🌍", layout="wide")

# 🌐 SÜNİ İNTELLEKTÜAL QLOVAL TƏRCÜMƏ SİSTEMİ
st.markdown(
    """
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
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
    """,
    unsafe_allow_html=True
)

st.title("🤖 EduAI Ağıllı Tədris Asistanı / Smart Study Assistant")
st.write("Dinamik planlaşdırma, mövzu tövsiyələri və motivasiya bir arada! / Dynamic scheduling and motivation!")

# Motivasiya sözləri
motivations = [
    "Uğur, hər gün təkrarlanan kiçik səylərin cəmidir! ✨",
    "Kompüter yavaş ola bilər, amma sənin hədəflərin sürətlidir! 💻🚀",
    "Bu gün qoyduğun hər kərpic, sabah quracağın gələcəyin təməlidir. 💪",
    "Böyük hədəflər, böyük səbirlər tələb edir. Sən bunu bacaracaqsan! 🎯"
]

# 💰 SOL PANEL: BİZNES VƏ AYARLAR HİSSƏSİ
st.sidebar.header("⚙️ Tənzimləmələr / Settings")
total_days = st.sidebar.slider("İmtahana neçə gün qalıb? / Days left?", 1, 60, 15)
daily_hours = st.sidebar.slider("Günlük dərs saatın? / Daily hours?", 1, 12, 4)

if st.sidebar.button("✨ Motivasiya Sözü Al / Get Motivation"):
    st.sidebar.info(random.choice(motivations))

st.sidebar.markdown("---")
st.sidebar.subheader("☕ Layihəyə Dəstək Ol / Support Us")
st.sidebar.write("Bu tətbiq tələbələr üçün hazırlanıb. Müəllifə kiçik bir dəstək olmaq istərdiniz?")
st.sidebar.markdown("[📊 Buy Me a Coffee (Mənə Qəhvə Ismarla)](https://www.buymeacoffee.com)") 

# Sessiya yaddaşı
if "my_subjects" not in st.session_state:
    st.session_state.my_subjects = {
        "Riyaziyyat (Mathematics)": {"difficulty": 5, "tips": "Törəmə, İnteqral və Funksiyaları təkrarla! 📐 / Review Derivatives!"},
        "İngilis dili (English)": {"difficulty": 4, "tips": "Advanced Vocabulary və Oxu strategiyaları! 📚 / Focus on Vocabulary!"},
        "Rus dili (Russian)": {"difficulty": 4, "tips": "Qrammatika qaydalarına və cümlə strukturuna diqqət et! ✍️"}
    }

# Fənn əlavə etmə
st.subheader("➕ Yeni Fənn Əlavə Et / Add New Subject")
new_sub = st.text_input("Fənnin adı (Subject Name):")
new_diff = st.slider("Bu fənnin çətinliyi? (Difficulty):", 1, 5, 3)

if st.button("➕ Siyahıya Əlavə Et / Add to List"):
    if new_sub and new_sub not in st.session_state.my_subjects:
        # Çətinlik dərəcəsinə görə dinamik məsləhət generatoru
        if new_diff >= 4:
            tip_text = "Bu çətin fəndir! Mövzuları xırda hissələrə böl və bol test işlə. 🧠"
        else:
            tip_text = "Nisbətən rahat fəndir, sürətli təkrar və qeydlər kifayət edər. 📑"
            
        st.session_state.my_subjects[new_sub] = {"difficulty": new_diff, "tips": tip_text}
        st.rerun()  # Səhifəni yeniləyir ki, dərhal siyahıda görünsün
    elif new_sub in st.session_state.my_subjects:
        st.warning("Bu fənn artıq siyahıda var!")

st.markdown("---")

# Fənləri göstərmək və Silmək
st.subheader("📚 Mövcud Fənləriniz və Kritik Tövsiyələr / Current Subjects")

# Silinəcək fənni izləmək üçün siyahı yaradırıq
to_delete = None

for sub, info in st.session_state.my_subjects.items():
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        st.warning(f"📘 **{sub}** (Çətinlik: {info['difficulty']}/5)")
    with col2:
        st.caption(f"💡 *Tövsiyə:* {info['tips']}")
    with col3:
        # Hər fənn üçün unikal düymə açarı (key) yaradırıq
        if st.button("🗑️ Sil", key=f"del_{sub}"):
            to_delete = sub

# Əgər silmə düyməsi basılıbsa, elementi silib səhifəni yeniləyirik
if to_delete:
    del st.session_state.my_subjects[to_delete]
    st.rerun()

st.markdown("---")

# Hesablama hissəsi
if st.button("🚀 Yeni Proqramı Hesabla / Calculate Schedule"):
    if not st.session_state.my_subjects:
        st.error("⚠️ Siyahıda heç bir fənn yoxdur! Zəhmət olmasa əvvəlcə fənn əlavə edin.")
    else:
        st.subheader("📊 Sizin Üçün Detallı Günlük Plan / Your Plan:")
        total_difficulty = sum(info["difficulty"] for info in st.session_state.my_subjects.values())
        
        for sub, info in st.session_state.my_subjects.items():
            sub_hours = (info["difficulty"] / total_difficulty) * daily_hours
            st.write(f"**{sub}** üçün ayrılan vaxt: **{sub_hours:.1f} saat/hours**")
            st.progress(min(sub_hours / daily_hours, 1.0))
            
        st.success(f"🎯 Mükəmməl! {total_days} gün ərzində bu templə hər şeyi tam çatdıracaqsınız!")