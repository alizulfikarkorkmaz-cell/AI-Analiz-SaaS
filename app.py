import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
import time

# =================================================================
# 1. KESİN ÇÖZÜM: MODELİ 'STABLE' SÜRÜME ZORLAMA
# =================================================================
st.set_page_config(page_title="AI Ultra Strateji: Master Gold", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("API Anahtarı eksik!")
    st.stop()

# ÖNEMLİ: v1beta hatalarını aşmak için konfigürasyonu en sade haliyle yapıyoruz
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 'models/gemini-1.5-flash' ismi Google'ın şu anki en stabil yoludur.
# Eğer bu da hata verirse sadece 'gemini-1.5-flash' dene.
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model Bağlantı Hatası: {e}")
    st.stop()

# =================================================================
# 2. ARAYÜZ VE VIP TASARIM (HİÇBİR ŞEYİ KISMADAN)
# =================================================================
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextArea textarea { border: 2px solid #ff4b4b !important; border-radius: 12px !important; }
    .stButton>button { width: 100%; border-radius: 15px; height: 4em; background: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

class TechnicalEditor:
    @staticmethod
    def fix(text):
        # TDK ve harf hatalarını temizleyen motor
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı\n\r\t .,;:!?()/%&\-+=*]+', '', text)
        return text.strip()

# =================================================================
# 3. DEV ANALİZ MOTORU (10.000 KELİME PROTOKOLÜ)
# =================================================================
def build_mega_report(data, oid):
    # Senin o meşhur 5 dev modülün
    modules = {
        "📊 OPERASYONEL ANALİZ": "Teknik kusurları ve 15 operasyonel hatayı detaylandır.",
        "💸 FİYATLANDIRMA": "Premium strateji ve gelir mimarisi oluştur.",
        "🧪 ENDÜSTRİYEL AR-GE": "Üretim ve inovasyon süreçlerini anlat.",
        "🛡️ PAZAR DOMİNASYONU": "Rakip analizi ve saldırı planı hazırla.",
        "📈 ROI PROJEKSİYONU": "12 aylık büyüme ve KPI tablosu sun."
    }

    final_report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF: {oid}\n"
    final_report += "="*60 + "\n\n"
    
    prog = st.progress(0)
    for i, (title, task) in enumerate(modules.items()):
        with st.spinner(f"⏳ {title} hazırlanıyor..."):
            try:
                # Modeller kullanılmıyor olsa burada hata alırdık. 
                # Ama biz en güncel yolu kullanıyoruz.
                prompt = f"GÖREV: {title} konusunu 2000 kelime yaz. TDK kurallarına uy. Veri: {data[:5000]}\nTalimat: {task}"
                res = model.generate_content(prompt)
                final_report += f"\n\n{title}\n{'-'*len(title)}\n\n{TechnicalEditor.fix(res.text)}\n"
                time.sleep(5) # Rate limit koruması
            except Exception as e:
                final_report += f"\n\n{title} HATASI: {str(e)}\n"
        prog.progress((i + 1) / len(modules))
    
    return final_report

# =================================================================
# 4. ANA EKRAN
# =================================================================
st.title("📈 AI Ultra Analiz & Strateji SaaS")
user_input = st.text_area("Verileri girin:", height=250)

col1, col2 = st.columns(2)
with col1:
    oid = st.text_input("Sipariş No:")
with col2:
    st.write("##")
    onay = st.checkbox("Sözleşmeyi onaylıyorum.")

if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if not user_input or not oid or not onay:
        st.error("Eksik bilgi girdiniz!")
    else:
        with st.status("🛠️ Rapor inşa ediliyor...", expanded=True):
            report_content = build_mega_report(user_input, oid)
            st.success("Rapor Tamamlandı!")
            st.download_button("📂 Dosyayı İndir (.txt)", report_content.encode('utf-8-sig'), file_name=f"{oid}.txt")

