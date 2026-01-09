import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
import time

# =================================================================
# 1. YAPI VE GEMINI SABİTLEME (KESİN ÇÖZÜM)
# =================================================================
st.set_page_config(page_title="AI Ultra Strateji: Master Gold", page_icon="🏆", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets.toml içinde 'GEMINI_API_KEY' bulunamadı!")
    st.stop()

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 404 hatasını ve sürüm karmaşasını bitirmek için tam path kullanıyoruz
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {str(e)}")
    st.stop()

# =================================================================
# 2. GRAMER VE TDK ZIRHI
# =================================================================
class GrammarPro:
    @staticmethod
    def final_polish(text):
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı\n\r\t .,;:!?()/%&\-+=*]+', '', text)
        corrections = {
            r"\bmekn\b": "mekan", r"\bkğıt\b": "kağıt", r"\bherşey\b": "her şey",
            r"\bbirşey\b": "bir şey", r"\byada\b": "ya da", r"\bduragı\b": "durağı",
            r"\bfiyatıda\b": "fiyatı da", r"\blezzetide\b": "lezzeti de"
        }
        for pattern, replacement in corrections.items():
            text = re.compile(pattern, re.IGNORECASE).sub(replacement, text)
        return text.strip()

# =================================================================
# 3. MASTER ANALİZ MOTORU (10.000 KELİME HEDEFİ)
# =================================================================
def generate_master_report(user_data, order_no):
    # Senin o meşhur 5 modülün
    modules = {
        "📊 MODÜL 1: OPERASYONEL ANALİZ VE TEKNİK KUSUR TESPİTİ": "Kök neden analizi ile altyapıdaki 15 kusuru teknik dille anlat.",
        "💸 MODÜL 2: STRATEJİK FİYATLANDIRMA VE GELİR MİMARİSİ": "Premium algı ve psikolojik fiyatlandırma stratejileri sun.",
        "🧪 MODÜL 3: ENDÜSTRİYEL AR-GE VE ÜRETİM İNOVASYONU": "Kaliteyi artıracak AR-GE süreçlerini detaylandır.",
        "🛡️ MODÜL 4: PAZAR DOMİNASYONU VE RAKİP İSTİHBARATI": "Sektör liderlerini devirecek saldırı planını hazırla.",
        "📈 MODÜL 5: 360 DERECE BÜYÜME VE 12 AYLIK ROI PROJEKSİYONU": "Gelecek 12 ayın KPI ve iş planı tablosunu oluştur."
    }

    report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF NO: {order_no}\nTarih: {datetime.now().strftime('%d/%m/%Y')}\n"
    report += "="*60 + "\n\n"
    
    prog = st.progress(0)
    status_msg = st.empty()
    
    for i, (title, instruction) in enumerate(modules.items()):
        status_msg.warning(f"⏳ {title} örülüyor...")
        
        # Gemini'nin "kısmasını" önlemek için promptu çok net veriyoruz
        full_prompt = f"""
        ROL: Dünyanın en kıdemli yönetim danışmanı ve TDK uzmanısın.
        GÖREV: {title} konusunu en az 1500-2000 kelime uzunluğunda, çok detaylı yaz.
        KURALLAR: TDK yazım kurallarına uy (bir şey, ya da, mekan, kağıt). Ağır kurumsal dil kullan.
        VERİ: {user_data[:8000]}
        TALİMAT: {instruction}
        """

        try:
            res = model.generate_content(full_prompt)
            if res and res.text:
                content = GrammarPro.final_polish(res.text)
                report += f"\n\n{title}\n{'-'*len(title)}\n\n{content}\n"
                time.sleep(4) # Kota koruması
            else:
                st.error(f"{title} için boş yanıt döndü!")
        except Exception as e:
            st.error(f"Modül Hatası: {str(e)}")
            break
            
        prog.progress((i + 1) / len(modules))
    
    status_msg.empty()
    return report

# =================================================================
# 4. ARAYÜZ TASARIMI
# =================================================================
st.title("📈 AI Ultra Analiz & Strateji SaaS")

user_input = st.text_area("Analiz edilecek verileri girin:", height=150)
oid = st.text_input("Shopier Sipariş No:")
sozlesme_onay = st.checkbox("Sözleşmeyi ve iade olmadığını kabul ediyorum.")

if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET", type="primary", use_container_width=True):
    if not user_input or not oid or not sozlesme_onay:
        st.error("Eksik bilgi var! Veri, Sipariş No ve Onay zorunludur.")
    else:
        with st.status("🛠️ Rapor hazırlanıyor (5-7 dk)...", expanded=True):
            final_doc = generate_master_report(user_input, oid)
            if final_doc:
                st.success("✅ Rapor Hazır!")
                st.download_button(
                    label="📂 Raporu İndir (.txt)",
                    data=final_doc.encode('utf-8-sig'),
                    file_name=f"MASTER_{oid}.txt",
                    mime="text/plain; charset=utf-8",
                    use_container_width=True
                )
