import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
import time

# ==============================
# 1. Sayfa ve CSS
# ==============================
st.set_page_config(
    page_title="AI Ultra Strateji: Master Gold Edition",
    page_icon="🏆",
    layout="wide"
)

st.markdown("""
<style>
.main { background-color: #0d1117; }
.stTextArea textarea { border: 2px solid #ff4b4b !important; border-radius: 15px !important; background-color: #010409 !important; color: white !important; font-size: 1.1rem; }
.stTextInput input { border: 2px solid #4b4bff !important; border-radius: 10px !important; background-color: #010409 !important; color: white !important; }
.stButton>button { width: 100%; border-radius: 15px; height: 4em; background: linear-gradient(90deg, #ff4b4b 0%, #ce1111 100%); color: white; font-weight: bold; font-size: 1.2rem; border: none; transition: 0.3s ease; }
.stButton>button:hover { transform: scale(1.01); box-shadow: 0 0 20px rgba(255, 75, 75, 0.4); }
.status-card { padding: 20px; border-radius: 15px; background-color: #161b22; border-left: 8px solid #ff4b4b; margin-bottom: 15px; }
div[data-testid="stExpander"] { border: 1px solid #30363d; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 2. API Anahtarı ve Model Seçimi
# ==============================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY bulunamadı!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Mevcut modelleri al ve generateContent destekleyen modeli seç
try:
    models_resp = genai.list_models()
    model_name = None
    for m in models_resp.models:
        if hasattr(m, "capabilities") and "generateContent" in m.capabilities:
            model_name = m.name
            break
    if not model_name:
        st.error("❌ Hiçbir model generate_content desteklemiyor!")
        st.stop()
    model = genai.GenerativeModel(model_name=model_name)
    st.sidebar.success(f"✅ Kullanılan Model: {model_name}")
except Exception as e:
    st.error(f"Model listesi alınamadı: {e}")
    st.stop()

# ==============================
# 3. Basit TDK Temizleyici
# ==============================
class Editor:
    @staticmethod
    def fix(text):
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı .,;:!?()-]+', '', text)
        return text.strip()

# ==============================
# 4. Arayüz
# ==============================
st.title("📈 AI Ultra Analiz & Strateji SaaS")
user_input = st.text_area("Analiz edilecek veriler:", height=300, placeholder="Müşteri yorumları, operasyonel veriler...")

if st.button("🔍 Ücretsiz Stratejik Özet"):
    if not user_input:
        st.warning("Veri girmediniz!")
    else:
        with st.spinner('Özet üretiliyor...'):
            try:
                res = model.generate_content(f"Hızlıca özetle ve 3 tavsiye ver: {user_input}")
                st.markdown(f"**Özet:** {Editor.fix(res.text)}")
            except Exception as e:
                st.error(f"Özet üretim hatası: {e}")

st.divider()
st.subheader("🔑 VIP Rapor Üretim Merkezi")

col1, col2 = st.columns(2)
with col1:
    siparis_no = st.text_input("Shopier Sipariş No:", placeholder="Örn: 1234567")
with col2:
    st.write("##")
    onay = st.checkbox("Sözleşmeyi ve iade olmadığını onaylıyorum.")

st.link_button("💎 VIP Rapor Satın Al (Shopier)", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True)

# ==============================
# 5. Mega Rapor
# ==============================
def run_mega_analysis(data, order_id):
    modules = [
        {"title": "📊 MODÜL 1: OPERASYONEL ANALİZ", "task": "2000 kelimelik teknik analiz yaz."},
        {"title": "💸 MODÜL 2: STRATEJİK FİYATLANDIRMA", "task": "2000 kelimelik teknik analiz yaz."},
        {"title": "🧪 MODÜL 3: AR-GE VE İNOVASYON", "task": "2000 kelimelik teknik analiz yaz."},
        {"title": "🛡️ MODÜL 4: PAZAR DOMİNASYONU", "task": "2000 kelimelik teknik analiz yaz."},
        {"title": "📈 MODÜL 5: 12 AYLIK ROI PROJEKSİYONU", "task": "2000 kelimelik teknik analiz yaz."}
    ]
    full_report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF NO: {order_id}\nTarih: {datetime.now().strftime('%d/%m/%Y')}\n"
    full_report += "="*80 + "\n\n"

    prog_bar = st.progress(0)
    status_label = st.empty()

    for idx, m in enumerate(modules):
        status_label.info(f"⏳ {m['title']} örülüyor...")
        prompt = f"""
ROL: Dünyanın en kıdemli yönetim danışmanı ve TDK uzmanı profesör.
GÖREV: {m['title']} konusunu en az 2000 kelime, ağır kurumsal, akademik ve teknik bir dille yaz.
KURALLAR: TDK kurallarına %100 uy. 'bir şey', 'ya da' her zaman ayrı olsun.
VERİ: {data[:8000]}
TALİMAT: {m['task']}
"""
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                full_report += f"\n\n{m['title']}\n{'-'*len(m['title'])}\n\n{Editor.fix(response.text)}\n"
            else:
                full_report += f"\n\n{m['title']}\nÜretim sırasında teknik bir kesinti yaşandı.\n"
            time.sleep(6)
        except Exception as e:
            st.error(f"{m['title']} hatası: {e}")
        prog_bar.progress((idx+1)/len(modules))

    status_label.empty()
    return full_report

# MASTER RAPOR BUTONU
if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if not user_input or not siparis_no or not onay:
        st.error("❌ Eksik Bilgi: Veri, Sipariş No veya Onay eksik!")
    else:
        with st.status("🛠️ Raporunuz inşa ediliyor...", expanded=True):
            master_doc = run_mega_analysis(user_input, siparis_no)
            if master_doc:
                st.success("✅ 10.000 Kelimelik Rapor Hazır!")
                st.download_button(
                    label="📂 Raporu İndir (.txt)",
                    data=master_doc.encode('utf-8-sig'),
                    file_name=f"MASTER_STRATEJI_{siparis_no}.txt",
                    mime="text/plain; charset=utf-8",
                    use_container_width=True
                )
