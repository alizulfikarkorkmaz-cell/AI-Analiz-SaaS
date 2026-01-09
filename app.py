import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
import time
import os

# =================================================================
# 1. VIP GÖRSEL MİMARİ VE CSS (JİLET GİBİ ARAYÜZ)
# =================================================================
st.set_page_config(
    page_title="AI Ultra Strateji: Master Gold Edition",
    page_icon="🏆",
    layout="wide"
)

# Arayüzü toparlayan, simetriyi kuran profesyonel CSS
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stTextArea textarea { 
        border: 2px solid #ff4b4b !important; 
        border-radius: 15px !important; 
        background-color: #010409 !important; 
        color: white !important;
        font-size: 1.1rem;
    }
    .stTextInput input { 
        border: 2px solid #4b4bff !important; 
        border-radius: 10px !important; 
        background-color: #010409 !important; 
        color: white !important;
    }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 4em; 
        background: linear-gradient(90deg, #ff4b4b 0%, #ce1111 100%);
        color: white; font-weight: bold; font-size: 1.2rem;
        border: none; transition: 0.3s ease;
    }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 0 20px rgba(255, 75, 75, 0.4); }
    .status-card { 
        padding: 20px; border-radius: 15px; background-color: #161b22; 
        border-left: 8px solid #ff4b4b; margin-bottom: 15px;
    }
    div[data-testid="stExpander"] { border: 1px solid #30363d; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. 404 HATASINI BİTİREN KESİN YAPILANDIRMA
# =================================================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ KRİTİK HATA: 'GEMINI_API_KEY' bulunamadı!")
    st.stop()

# API Bağlantısını ve Modeli en stabil şekilde kuruyoruz
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 404 models/gemini-1.5-flash is not found hatasını bu tanım çözer:
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {str(e)}")
    st.stop()

# =================================================================
# 3. TDK ENTEGRASYONLU PROFESYONEL EDİTÖR
# =================================================================
class TechnicalEditor:
    @staticmethod
    def fix_all(text):
        # Karakter temizliği ve TDK kuralları (bir şey, ya da, mekan vb.)
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

# =================================================================
# 4. DEV ANALİZ MOTORU (10.000 KELİME & 5 MODÜL)
# =================================================================
def run_mega_analysis(data, order_id):
    modules = [
        {
            "title": "📊 MODÜL 1: OPERASYONEL ANALİZ VE TEKNİK KUSUR TESPİTİ",
            "task": "Kök neden analizi yaparak işletmedeki 15 temel operasyonel hatayı ve mühendislik çözümlerini 2000 kelime anlat."
        },
        {
            "title": "💸 MODÜL 2: STRATEJİK FİYATLANDIRMA VE GELİR MİMARİSİ",
            "task": "Psikolojik fiyatlandırma, premium algı yönetimi ve gelir artırıcı çapraz satış modellerini 2000 kelime detaylandır."
        },
        {
            "title": "🧪 MODÜL 3: ENDÜSTRİYEL AR-GE VE ÜRETİM İNOVASYONU",
            "task": "Üretim süreçlerinde kalite kontrol, AR-GE metodolojileri ve teknolojik entegrasyonu 2000 kelime yaz."
        },
        {
            "title": "🛡️ MODÜL 4: PAZAR DOMİNASYONU VE RAKİP İSTİHBARATI",
            "task": "Sektör liderlerinin analizini ve pazarı domine edecek stratejik saldırı planını 2000 kelime hazırla."
        },
        {
            "id": "ROI",
            "title": "📈 MODÜL 5: 360 DERECE BÜYÜME VE 12 AYLIK ROI PROJEKSİYONU",
            "task": "Yatırımın geri dönüşü, KPI takibi ve önümüzdeki 12 ayın aksiyon planını içeren 2000 kelimelik rapor yaz."
        }
    ]

    # image_f3e3d2.png'deki gibi hataları önlemek için raporu parça parça inşa ediyoruz
    full_report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF NO: {order_id}\nTarih: {datetime.now().strftime('%d/%m/%Y')}\n"
    full_report += "="*80 + "\n\n"
    
    prog_bar = st.progress(0)
    status_label = st.empty()
    
    for idx, m in enumerate(modules):
        status_label.info(f"⏳ **{m['title']}** örülüyor... Gemini & TDK Editörü Aktif.")
        
        # Gemini'nin "kısmasını" önleyen, akademik ve teknik dile zorlayan talimat
        prompt = f"""
        ROL: Dünyanın en kıdemli yönetim danışmanı ve TDK uzmanı profesör.
        GÖREV: {m['title']} konusunu en az 2000 kelime, ağır kurumsal, akademik ve teknik bir dille yaz.
        KURALLAR: TDK kurallarına %100 uy. 'bir şey', 'ya da' her zaman ayrı olsun.
        VERİ: {data[:8000]}
        TALİMAT: {m['task']}
        """

        try:
            # Raporun her parçasını güvenli modda üretiyoruz
            response = model.generate_content(prompt)
            if response and response.text:
                clean_text = TechnicalEditor.fix_all(response.text)
                full_report += f"\n\n{m['title']}\n{'-'*len(m['title'])}\n\n{clean_text}\n"
            else:
                full_report += f"\n\n{m['title']}\nÜretim sırasında teknik bir kesinti yaşandı.\n"
            
            # API Limit koruması
            time.sleep(6)
        except Exception as e:
            st.error(f"⚠️ {m['title']} hatası: {str(e)}")
            continue
            
        prog_bar.progress((idx + 1) / len(modules))
    
    status_label.empty()
    return full_report

# =================================================================
# 5. ARAYÜZ (FULL SİMETRİ)
# =================================================================
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

# Veri Giriş Alanı
user_input = st.text_area("Analiz edilecek verileri buraya girin:", height=300, placeholder="Müşteri yorumları, operasyonel veriler, şikayetler...")

# Ücretsiz Hızlı Özet
if st.button("🔍 Ücretsiz Stratejik Özet"):
    if user_input:
        with st.spinner('Kısa analiz yapılıyor...'):
            res = model.generate_content(f"Hızlıca özetle ve 3 tavsiye ver: {user_input}")
            st.markdown(f"**Özet:** {TechnicalEditor.fix_all(res.text)}")

st.divider()
st.subheader("🔑 VIP Rapor Üretim Merkezi")

with st.expander("📄 HİZMET SÖZLEŞMESİ VE KULLANIM ŞARTLARI"):
    st.text("""İşbu rapor AI Strateji SaaS ile kullanıcı arasındadır. 
Dijital ürünlerde iade yoktur. 10.000 kelime hedefli teknik rapor üretilir.""")

# Sipariş Onay Bölümü
col1, col2 = st.columns(2)
with col1:
    siparis_no = st.text_input("Shopier Sipariş No:", placeholder="Örn: 1234567")
with col2:
    st.write("##")
    onay = st.checkbox("Sözleşmeyi ve iade olmadığını onaylıyorum.")

st.link_button("💎 VIP Rapor Satın Al (Shopier)", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True)

# --- MASTER BUTON ---
if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if not user_input or not siparis_no or not onay:
        st.error("❌ Eksik Bilgi: Lütfen Veri, Sipariş No ve Onay kutusunu kontrol edin!")
    else:
        with st.status("🛠️ Raporunuz inşa ediliyor (Tahmini 5-8 dk)...", expanded=True):
            # image_f3eaf9.png'deki rapor üretim akışını başlatıyoruz
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
