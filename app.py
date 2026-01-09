import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# 1. VIP ARAYÜZ (GÖRÜNTÜYÜ JİLET GİBİ YAPAR)
st.set_page_config(page_title="AI Ultra Strateji: Master Gold", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stTextArea textarea { border: 2px solid #ff4b4b !important; border-radius: 12px !important; background-color: #161b22 !important; color: white !important; }
    .stButton>button { width: 100%; border-radius: 12px; height: 4em; background: linear-gradient(90deg, #ff4b4b 0%, #ce1111 100%); color: white; font-weight: bold; font-size: 1.2rem; }
    .status-card { padding: 20px; border-radius: 15px; background-color: #161b22; border-left: 10px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# 2. API VE MODEL SABİTLEME (404 HATASINI BİTİREN REÇETE)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ API KEY BULUNAMADI!")
    st.stop()

# v1beta saçmalığını aşmak için konfigürasyonu en sade hale getiriyoruz
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

try:
    # 'models/' ön ekini sildik, en stabil model ismini verdik.
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Model bağlantı hatası: {e}")

# 3. ANALİZ MOTORU (10.000 KELİME PROTOKOLÜ)
def generate_master_report(data, oid):
    modules = {
        "📊 OPERASYONEL ANALİZ": "İşletmedeki 15 teknik kusuru bul ve mühendislik çözümleriyle 2000 kelime anlat.",
        "💸 FİYATLANDIRMA": "Premium algı ve gelir artırıcı psikolojik fiyatlandırma stratejilerini 2000 kelime detaylandır.",
        "🧪 ENDÜSTRİYEL AR-GE": "Üretim inovasyonu ve teknik AR-GE süreçlerini 2000 kelime yaz.",
        "🛡️ PAZAR DOMİNASYONU": "Rakip analizi ve pazarı ele geçirme planını 2000 kelime hazırla.",
        "📈 ROI PROJEKSİYONU": "12 aylık KPI ve büyüme tablosunu 2000 kelime metinle sun."
    }

    report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF NO: {oid}\nTarih: {datetime.now().strftime('%d/%m/%Y')}\n"
    report += "="*80 + "\n\n"
    
    prog = st.progress(0)
    for i, (title, task) in enumerate(modules.items()):
        with st.status(f"⏳ {title} inşa ediliyor...", expanded=False):
            try:
                # Modeli uzun yazmaya zorlayan 'CEO Prompt'u
                full_prompt = f"GÖREV: {title}\nDETAY: {task}\nKURALLAR: ASLA KISALTMA YAPMA, TDK KURALLARINA UY.\nVERİ: {data[:6000]}"
                response = model.generate_content(full_prompt)
                
                if response and response.text:
                    report += f"\n\n{title}\n{'-'*len(title)}\n\n{response.text}\n"
                else:
                    report += f"\n\n{title}\n[HATA: Gemini yanıt veremedi.]\n"
                
                time.sleep(5) # Rate limit (429) koruması
            except Exception as e:
                report += f"\n\n{title}\nÜretim Hatası: {str(e)}\n"
        
        prog.progress((i + 1) / len(modules))
    
    return report

# 4. ARAYÜZ KATMANI
st.title("📈 AI Ultra Analiz & Strateji SaaS")
input_data = st.text_area("Analiz edilecek verileri buraya girin:", height=250)

# LOGDA PATLAYAN ÖZET KISMI İÇİN GÜVENLİ BUTON
if st.button("🔍 Ücretsiz Stratejik Özet"):
    if input_data:
        with st.spinner("Özetleniyor..."):
            try:
                res = model.generate_content(f"Hızlıca özetle ve 3 kritik tavsiye ver: {input_data}")
                st.info(res.text)
            except Exception as e:
                st.error(f"Özet hatası: {e}")

st.divider()
c1, c2 = st.columns(2)
with c1:
    siparis_no = st.text_input("Shopier Sipariş No:", placeholder="12365478")
with c2:
    st.write("##")
    onay = st.checkbox("Sözleşmeyi ve iade olmadığını kabul ediyorum.")

if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if input_data and siparis_no and onay:
        final_doc = generate_master_report(input_data, siparis_no)
        st.success("✅ Rapor Hazır!")
        st.download_button("📂 Raporu İndir (.txt)", final_doc.encode('utf-8-sig'), file_name=f"Master_{siparis_no}.txt")
    else:
        st.error("❌ Eksik bilgi: Veri, Sipariş No ve Onay gereklidir!")
