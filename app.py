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
# 2. API Anahtarı ve Model
# ==============================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ KRİTİK HATA: 'GEMINI_API_KEY' bulunamadı!")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Mevcut modelleri listele ve sidebar'da göster
    models_response = genai.list_models()
    st.sidebar.subheader("🛰️ Mevcut Gemini Modelleri:")
    for m in models_response.models:  # .models ile listeye erişiyoruz
        st.sidebar.text(f"- {m.name}")  # .name ile model adını alıyoruz

    # Desteklenen model
    model = genai.GenerativeModel(model_name='gemini-2.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası veya Model Bulunamadı: {str(e)}")
    st.stop()

# ==============================
# 3. TDK Temizleyici
# ==============================
class TechnicalEditor:
    @staticmethod
    def fix_all(text):
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı\n\r\t .,;:!?()/%&\-+=*]+', '', text)
        corrections = {
            r"\bmekn\b": "mekan", r"\bkğıt\b": "kağıt", r"\bherşey\b": "her şey",
            r"\bbirşey\b": "bir şey", r"\byada\b": "ya da", r"\bduragı\b": "durağı",
            r"\bfiyatıda\b": "fiyatı da", r"\blezzetide\b": "lezzeti de",
            r"\btşk\b": "teşekkür", r"\bsaglayan\b": "sağlayan"
        }
        for pattern, replacement in corrections.items():
            text = re.compile(pattern, re.IGNORECASE).sub(replacement, text)
        return text.strip()

# ==============================
# 4. Mega Analiz Motoru
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
        status_label.info(f"⏳ {m['title']} örülüyor... Gemini & TDK Editörü Aktif.")
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
                clean_text = TechnicalEditor.fix_all(response.text)
                full_report += f"\n\n{m['title']}\n{'-'*len(m['title'])}\n\n{clean_text}\n"
            else:
                full_report += f"\n\n{m['title']}\nÜretim sırasında teknik bir kesinti yaşandı.\n"
            time.sleep(6)
        except Exception as e:
            st.error(f"{m['title']} hatası: {str(e)}")
            continue

        prog_bar.progress((idx + 1) / len(modules))

    status_label.empty()
    return full_report

# ==============================
# 5. Arayüz
# ==============================
st.title("📈 AI Ultra Analiz & Strateji SaaS")
st.markdown("#### 10.000 Kelimelik Teknik Çözüm ve TDK Onaylı Yazım Motoru")

with st.sidebar:
    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.subheader("VIP Kontrol Merkezi")
    st.error("⚠️ YATIRIM TAVSİYESİ DEĞİLDİR")
    st.success("🛡️ %100 TELAFİ GARANTİSİ")
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    st.caption("v3.0 Master Gold | © 2026")

user_input = st.text_area("Analiz edilecek verileri buraya girin:", height=300, placeholder="Müşteri yorumları, operasyonel veriler...")

if st.button("🔍 Ücretsiz Stratejik Özet"):
    if user_input:
        with st.spinner('Kısa analiz yapılıyor...'):
            try:
                res = model.generate_content(f"Hızlıca özetle ve 3 tavsiye ver: {user_input}")
                st.markdown(f"**Özet:** {TechnicalEditor.fix_all(res.text)}")
            except Exception as e:
                st.error(f"Özet üretim hatası: {str(e)}")

st.divider()
st.subheader("🔑 VIP Rapor Üretim Merkezi")

col1, col2 = st.columns(2)
with col1:
    siparis_no = st.text_input("Shopier Sipariş No:", placeholder="Örn: 1234567")
with col2:
    st.write("##")
    onay = st.checkbox("Sözleşmeyi ve iade olmadığını onaylıyorum.")

st.link_button("💎 VIP Rapor Satın Al (Shopier)", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True)

if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if not user_input or not siparis_no or not onay:
        st.error("❌ Eksik Bilgi: Lütfen Veri, Sipariş No ve Onay kutusunu kontrol edin!")
    else:
        with st.status("🛠️ Raporunuz inşa ediliyor (Tahmini 5-8 dk)...", expanded=True):
            master_doc = run_mega_analysis(user_input, siparis_no)
            if master_doc:
                st.success("✅ 10.000 Kelimelik Rapor Hazır!")
                st.download_button(
                    label="📂 Raporu Bilgisayarına İndir (.txt)",
                    data=master_doc.encode('utf-8-sig'),
                    file_name=f"MASTER_STRATEJI_{siparis_no}.txt",
                    mime="text/plain; charset=utf-8",
                    use_container_width=True
                )
