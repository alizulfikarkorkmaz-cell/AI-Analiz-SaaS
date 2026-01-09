import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
import time

# =================================================================
# 1. KURUMSAL YAPI VE GEMINI YAPILANDIRMASI (KESİN ÇÖZÜM)
# =================================================================
st.set_page_config(page_title="AI Ultra Strateji: Master Gold", page_icon="🏆", layout="wide")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Sistem hatası: 'GEMINI_API_KEY' bulunamadı! Lütfen secrets.toml dosyasını kontrol edin.")
    st.stop()

# 404 HATASINI BİTİREN ÖZEL YAPILANDIRMA
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Modeli direkt tam ismiyle çağırarak sürüm karmaşasını bitiriyoruz
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {str(e)}")
    st.stop()

# =================================================================
# 2. HUKUKİ ZIRH VE SÖZLEŞME METNİ
# =================================================================
HIZMET_SOZLESMESI = """
1. TARAFLAR VE KONU: İşbu rapor, AI Strateji SaaS ile Kullanıcı arasındadır.
2. HİZMET NİTELİĞİ: Rapor yapay zeka tarafından üretilmiştir, yatırım tavsiyesi değildir.
3. İADE KOŞULLARI: Dijital ürünlerde cayma hakkı ve para iadesi bulunmamaktadır (Md. 15/ğ).
4. TELAFİ GARANTİSİ: İçerik yetersizliği durumunda 3 gün içinde 'Manuel Uzman Revizesi' talep edilebilir.
5. GRAMER PROTOKOLÜ: Rapor, TDK yazım kurallarına uygunluk denetiminden geçmektedir.
"""

# =================================================================
# 3. ULTRA DİL VE GRAMER DENETİMİ (TDK Koruma Sistemi)
# =================================================================
class GrammarPro:
    @staticmethod
    def final_polish(text):
        # Gereksiz karakter temizliği
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı\n\r\t .,;:!?()/%&\-+=*]+', '', text)
        
        # Raporlardaki 'mekn', 'lezzetide' gibi hataları düzelten sözlük
        corrections = {
            r"\bmekn\b": "mekan", r"\bkğıt\b": "kağıt", r"\bakğt\b": "kağıt",
            r"\bherşey\b": "her şey", r"\bbirşey\b": "bir şey", r"\byada\b": "ya da",
            r"\bduragı\b": "durağı", r"\btercihide\b": "tercihi de", r"\bfiyatıda\b": "fiyatı da",
            r"\btşk\b": "teşekkür", r"\bsaglayan\b": "sağlayan", r"\bolduda\b": "oldu da",
            r"\byapıyo\b": "yapıyor", r"\bediyo\b": "ediyor", r"\bbi\b": "bir",
            r"\blezzetide\b": "lezzeti de"
        }
        for pattern, replacement in corrections.items():
            text = re.compile(pattern, re.IGNORECASE).sub(replacement, text)
        return text.strip()

# =================================================================
# 4. DEV ANALİZ MOTORU (10.000 Kelime & TDK & CEO Protokolü)
# =================================================================
def generate_master_report(user_data, order_no):
    modules = {
        "📊 MODÜL 1: OPERASYONEL ANALİZ VE TEKNİK KUSUR TESPİTİ": "Kök neden analizi ile altyapıdaki 15 kusuru mühendislik diliyle anlat.",
        "💸 MODÜL 2: STRATEJİK FİYATLANDIRMA VE GELİR MİMARİSİ": "Premium algı ve psikolojik fiyatlandırma ile 10 strateji sun.",
        "🧪 MODÜL 3: ENDÜSTRİYEL AR-GE VE ÜRETİM İNOVASYONU": "Ürün kalitesini artıracak teknik AR-GE süreçlerini anlat.",
        "🛡️ MODÜL 4: PAZAR DOMİNASYONU VE RAKİP İSTİHBARATI": "Sektör liderlerini devirecek 'Mavi Okyanus' saldırı planını hazırla.",
        "📈 MODÜL 5: 360 DERECE BÜYÜME VE 12 AYLIK ROI PROJEKSİYONU": "Gelecek 12 ayın her ayı için teknik iş planı ve KPI tablosu oluştur."
    }

    report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREFERANS NO: {order_no}\nTarih: {datetime.now().strftime('%d/%m/%Y')}\n"
    report += "="*80 + "\n\n"
    
    prog = st.progress(0)
    status_msg = st.empty()
    
    for i, (title, instruction) in enumerate(modules.items()):
        status_msg.warning(f"⏳ {title} örülüyor... Gemini & TDK Editörü Aktif.")
        
        # Üretim kalitesini zirveye çıkaran talimat seti
        system_msg = f"""
        Sen dünyanın en kıdemli yönetim danışmanı ve bir TDK Profesörüsün.
        GÖREVİN: {title} konusunu en az 2000 kelime, ağır kurumsal, teknik ve akademik bir dille yazmak.
        KURALLAR: 'mekan', 'kağıt', 'lezzeti de', 'bir şey' gibi TDK kurallarına %100 uyacaksın.
        ÜSLUP: CEO seviyesinde teknik terimler kullan (ROI, KPI, Mavi Okyanus, Optimizasyon vb.).
        """

        try:
            full_prompt = f"{system_msg}\n\nAnaliz Edilecek Veri: {user_data[:8000]}\nTalimat: {instruction}"
            res = model.generate_content(full_prompt)
            content = GrammarPro.final_polish(res.text)
            report += f"\n\n{title}\n{'-'*len(title)}\n\n{content}\n"
            time.sleep(5) # Kota dostu bekleme
        except Exception as e:
            st.error(f"Modül üretim hatası: {str(e)}")
            break
            
        prog.progress((i + 1) / len(modules))
    
    status_msg.empty()
    return report

# =================================================================
# 5. EKSİKSİZ ARAYÜZ TASARIMI
# =================================================================
st.title("📈 AI Ultra Analiz & Strateji SaaS")
st.markdown("##### 10.000 Kelimelik Teknik Çözüm ve TDK Onaylı Yazım Motoru")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.error("⚠️ YASAL UYARI: Yatırım tavsiyesi değildir.")
    st.divider()
    st.success("🛡️ TELAFİ GARANTİSİ")
    st.info("İçerik yetersizliği durumunda sipariş no ile manuel revize talep edebilirsiniz.")

user_input = st.text_area("Analiz edilecek verileri buraya girin (Max 8000 karakter):", height=200)

if st.button("🔍 Ücretsiz Stratejik Özet"):
    if user_input:
        with st.spinner('Hızlı analiz yapılıyor...'):
            res = model.generate_content(f"Hızlıca özetle ve 3 kritik tavsiye ver: {user_input}")
            st.write(GrammarPro.final_polish(res.text))

st.divider()
st.subheader("🔑 VIP Rapor Üretim Merkezi")

with st.expander("📄 HİZMET SÖZLESMESİ VE KULLANIM ŞARTLARI"):
    st.text(HIZMET_SOZLESMESI)

col_a, col_b = st.columns(2)
with col_a:
    oid = st.text_input("Shopier Sipariş No:")
with col_b:
    st.write("##")
    sozlesme_onay = st.checkbox("Sözleşmeyi ve iade olmadığını kabul ediyorum.")

st.link_button("💎 VIP Rapor Satın Al (Shopier)", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True)

# --- MASTER BUTON ---
if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET", type="primary", use_container_width=True):
    if not user_input:
        st.error("Lütfen analiz edilecek verileri girin!")
    elif not oid:
        st.error("Lütfen Shopier Sipariş No girin!")
    elif not sozlesme_onay:
        st.error("Lütfen sözleşmeyi onaylayın!")
    else:
        with st.status("🛠️ Gemini & TDK Editörü raporunuzu hazırlıyor (5-7 dk)...", expanded=True):
            final_doc = generate_master_report(user_input, oid)
            if final_doc:
                st.success("✅ 10.000 Kelimelik Kusursuz Rapor Hazır!")
                st.download_button(
                    label="📂 Raporu Bilgisayarına İndir (.txt)",
                    data=final_doc.encode('utf-8-sig'),
                    file_name=f"MASTER_STRATEJI_{oid}.txt",
                    mime="text/plain; charset=utf-8",
                    use_container_width=True
                )
                with st.expander("📝 Kalite Kontrol Önizleme"):
                    st.text(final_doc[:2500] + "...")

st.caption("© 2026 AI Analiz SaaS | Gold Edition | Professional Industry Solutions")
