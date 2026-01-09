import streamlit as st
import requests
import json
from datetime import datetime
import time

# 1. VIP ARAYÜZ TASARIMI
st.set_page_config(page_title="Master Gold Ultra v6.0", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stTextArea textarea { border: 2px solid #ff4b4b !important; border-radius: 10px !important; background: #161b22; color: white; }
    .stButton>button { width: 100%; border-radius: 12px; height: 4em; background: #ff4b4b; color: white; font-weight: bold; font-size: 1.2rem; border: none; }
    .stButton>button:hover { background: #ce1111; box-shadow: 0 0 20px rgba(255, 75, 75, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# 2. REST API BAĞLANTI FONKSİYONU (404 KATİLİ)
def call_gemini_api(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]
    # v1beta HATASINI BİTİREN GÜNCEL ENDPOINT
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 8192, "temperature": 0.7}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        # Yanıtı ayıklıyoruz
        return response_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"KRİTİK BAĞLANTI HATASI: {str(e)}"

# 3. ANALİZ MOTORU
def run_mega_engine(data, oid):
    modules = {
        "📊 OPERASYONEL ANALİZ": "İşletmedeki 15 teknik kusuru ve mühendislik çözümlerini 2000 kelime anlat.",
        "💸 FİYATLANDIRMA": "Premium algı ve gelir mimarisi için 2000 kelimelik strateji yaz.",
        "🧪 ENDÜSTRİYEL AR-GE": "Üretim inovasyonu ve AR-GE süreçlerini 2000 kelime detaylandır.",
        "🛡️ PAZAR DOMİNASYONU": "Rakip analizi ve pazar ele geçirme planını 2000 kelime hazırla.",
        "📈 ROI PROJEKSİYONU": "12 aylık KPI ve büyüme tablosunu 2000 kelime metinle sun."
    }

    report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF: {oid}\n{'-'*60}\n"
    prog = st.progress(0)
    
    for i, (title, task) in enumerate(modules.items()):
        with st.spinner(f"⏳ {title} inşa ediliyor..."):
            prompt = f"GÖREV: {title}\nDETAY: {task}\nVERİ: {data[:5000]}"
            content = call_gemini_api(prompt)
            report += f"\n\n{title}\n{content}\n"
            time.sleep(4) # Kota koruması
        prog.progress((i + 1) / len(modules))
    
    return report

# 4. ARAYÜZ
st.title("📈 AI Ultra Analiz & Strateji SaaS")
input_text = st.text_area("Verileri buraya yapıştırın:", height=250)
siparis_no = st.text_input("Sipariş No:")
onay = st.checkbox("Sözleşmeyi ve iade olmadığını kabul ediyorum.")

if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
    if input_text and siparis_no and onay:
        with st.status("🛠️ Doğrudan Google Sunucularına Bağlanılıyor..."):
            final_report = run_mega_engine(input_text, siparis_no)
            st.success("✅ Rapor Hazır!")
            st.download_button("📂 Raporu İndir (.txt)", final_report.encode('utf-8-sig'), file_name=f"Final_{siparis_no}.txt")
    else:
        st.error("Lütfen tüm alanları doldurun!")

