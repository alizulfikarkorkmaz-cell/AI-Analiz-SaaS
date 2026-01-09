import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# 1. SAYFA AYARI
st.set_page_config(page_title="Master Gold v5.0", layout="wide")

# 2. API VE MODEL SABİTLEME (404 SAVAR)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API KEY EKSİK!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Hata alınan 'v1beta' sorununu aşmak için modeli en çıplak haliyle tanımlıyoruz
try:
    # 'models/' ön ekini sildik, doğrudan model adını veriyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model yüklenemedi: {e}")

# 3. ANALİZ MOTORU (HATA KONTROLLÜ)
def generate_master_report(user_data, oid):
    modules = {
        "📊 OPERASYONEL ANALİZ": "Teknik kusurlar ve 15 operasyonel hatayı detaylandır.",
        "💸 FİYATLANDIRMA": "Premium strateji ve gelir mimarisi oluştur.",
        "🧪 ENDÜSTRİYEL AR-GE": "Üretim ve inovasyon süreçlerini anlat.",
        "🛡️ PAZAR DOMİNASYONU": "Rakip analizi ve saldırı planı hazırla.",
        "📈 ROI PROJEKSİYONU": "12 aylık büyüme ve KPI tablosu sun."
    }

    report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF: {oid}\n{'-'*60}\n"
    prog = st.progress(0)
    
    for i, (title, task) in enumerate(modules.items()):
        with st.spinner(f"⏳ {title} üretiliyor..."):
            try:
                # 404 hatasını önlemek için en sade prompt yapısı
                prompt = f"{title}\n{task}\nVeri: {user_data[:4000]}"
                response = model.generate_content(prompt)
                
                if response and response.text:
                    report += f"\n\n{title}\n{response.text}\n"
                else:
                    report += f"\n\n{title}\n[Hata: Model boş yanıt döndü.]\n"
                
                time.sleep(4) # Kota koruması
            except Exception as e:
                # Logda gördüğümüz hatayı burada yakalayıp kullanıcıya gösteriyoruz
                st.warning(f"{title} sırasında bir aksama oldu, ama devam ediyorum.")
                report += f"\n\n{title}\nÜretim Hatası: {str(e)}\n"
        
        prog.progress((i + 1) / len(modules))
    
    return report

# 4. ARAYÜZ
st.title("📈 AI Ultra Analiz & Strateji")
input_text = st.text_area("Analiz edilecek veriyi buraya yapıştırın:", height=200)
order_id = st.text_input("Shopier Sipariş No:")
confirm = st.checkbox("Sözleşmeyi onaylıyorum.")

if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if input_text and order_id and confirm:
        with st.status("🛠️ Rapor inşa ediliyor (Bu sefer 404'süz)..."):
            final_report = generate_master_report(input_text, order_id)
            st.success("Analiz Tamamlandı!")
            st.download_button("📂 Raporu İndir (.txt)", final_report, file_name=f"Master_{order_id}.txt")
    else:
        st.error("Lütfen tüm alanları doldurun!")
