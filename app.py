import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time
import json

# --- KURUMSAL YAPILANDIRMA ---
st.set_page_config(page_title="AI Ultra Strateji Pro", page_icon="📈", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Sistem hatası: API anahtarı yüklenemedi!")

# =================================================================
# 1. ÖZEL DATA & DİL KORUMA SÖZLÜĞÜ (Kritik Bölüm)
# =================================================================
# Bu sözlük, AI'nın "anlamsız" kelimeler yerine profesyonel terimler kullanmasını zorunlu kılar.
DIL_KORUMA_DATASI = {
    "yasakli_karakterler": r'[^\x00-\x7FçğıöşüÇĞİÖŞÜ\n\r\t .,;:!?()/%&\-+=*]+',
    "terim_sozlugu": {
        "zkušenilerini": "deneyimlerini",
        "tăngellemek": "engellemek",
        "felan": "ve benzeri",
        "şeyler": "stratejik unsurlar",
        "kötü": "operasyonel yetersizlik",
        "pahalı": "yüksek fiyatlandırma segmenti"
    }
}

class TextProcessor:
    @staticmethod
    def clean_text(text):
        # 1. Adım: Çince ve bozuk karakterleri temizle
        text = re.sub(DIL_KORUMA_DATASI["yasakli_karakterler"], '', text)
        # 2. Adım: Sözlükteki hatalı kelimeleri profesyonelleriyle değiştir
        for hatali, dogru in DIL_KORUMA_DATASI["terim_sozlugu"].items():
            text = text.replace(hatali, dogru)
        return text.strip()

# =================================================================
# 2. KATMANLI DEV RAPOR MOTORU (MODÜL MİMARİSİ)
# =================================================================
def generate_vip_content(user_data, order_no):
    # Raporun iskeleti - Her modül 2000 kelime hedefli
    modules = {
        "📊 MODÜL 1: OPERASYONEL ANALİZ VE SİSTEMATİK KUSUR TESPİTİ": (
            "Verilen ham verileri 'Kök Neden Analizi' (Root Cause Analysis) yöntemiyle incele. "
            "Personel davranışları, hizmet hızı ve teknik altyapıdaki 15 ana kusuru detaylandır."
        ),
        "💸 MODÜL 2: STRATEJİK FİYATLANDIRMA VE GELİR OPTİMİZASYONU": (
            "Fiyat-değer dengesini analiz et. 'Premium' algısı yaratmak için 10 farklı psikolojik "
            "fiyatlandırma ve maliyet düşürme stratejisi sun."
        ),
        "🧪 MODÜL 3: TEKNİK AR-GE VE ÜRETİM İNOVASYONU": (
            "Ürünün fiziksel ömrünü ve kalitesini artıracak kimyasal, mekanik veya dijital "
            "çözümleri mühendislik perspektifiyle anlat."
        ),
        "🛡️ MODÜL 4: PAZAR KONUMLANDIRMA VE RAKİP İSTİHBARATI": (
            "Sektör liderlerinin zayıf noktalarını tespit et. 'Mavi Okyanus' stratejisiyle "
            "nasıl tekel olunacağını akademik bir dille açıkla."
        ),
        "📈 MODÜL 5: 360 DERECE BÜYÜME VE 12 AYLIK ROI PLANI": (
            "Gelecek 12 ayın her ayı için yatırım getirisi odaklı somut iş planı oluştur. "
            "KPI ve performans ölçütlerini içeren dev bir kapanış yap."
        )
    }

    full_report = f"💎 VIP STRATEJİK ÇÖZÜM RAPORU\nNo: {order_no}\n"
    full_report += "="*70 + "\n\n"
    
    progress_bar = st.progress(0)
    
    for i, (title, instruction) in enumerate(modules.items()):
        status_msg = st.empty()
        status_msg.warning(f"⚙️ {title} örülüyor...")
        
        system_msg = f"""
        Sen dünyanın en kıdemli iş stratejisti ve endüstri mühendisisin. 
        Görevin: Aşağıdaki verilerden yola çıkarak {title} bölümünü en az 2000 kelime olacak şekilde yazmak.
        DİL KURALLARI: Sadece Türkiye Türkçesi. 'zkušenilerini' veya 'tăngellemek' gibi saçma kelimeler kullanma. 
        Yerine profesyonel karşılıklarını (deneyim, engellemek) kullan.
        ÜSLUP: Teknik, ağırbaşlı ve kurumsal.
        """

        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": f"Sipariş: {order_no}\nTalimat: {instruction}\nVeri: {user_input[:4500]}"}
                ],
                temperature=0.3
            )
            content = TextProcessor.clean_text(res.choices[0].message.content)
            full_report += f"\n\n{title}\n{'-'*len(title)}\n\n{content}\n"
            time.sleep(10) # API Limit koruması
        except Exception as e:
            st.error(f"Hata: {str(e)}")
            break
            
        progress_bar.progress((i + 1) / len(modules))
        status_msg.empty()

    return full_report

# =================================================================
# 3. ARAYÜZ TASARIMI
# =================================================================
st.title("📈 AI Ultra Analiz & Strateji SaaS")
st.markdown("##### 10.000 Kelimelik Teknik Çözüm ve İş Geliştirme Motoru")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("🛡️ Güvenlik & Veri Koruma")
    st.info("Sistemimiz UTF-8-SIG karakter koruma altyapısıyla çalışmaktadır.")
    st.caption("Özel Dil Datası v1.2 Aktif")

user_input = st.text_area("Analiz edilecek verileri buraya girin (Max 5000 karakter):", height=200)

c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 Ücretsiz Stratejik Analiz", use_container_width=True):
        if user_input:
            with st.spinner('Hızlı analiz yapılıyor...'):
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Aşağıdaki verileri profesyonelce özetle ve 3 stratejik tavsiye ver: {user_input}"}],
                    model="llama-3.3-70b-versatile"
                )
                st.success("📊 Hızlı Analiz Sonucu")
                st.write(TextProcessor.clean_text(res.choices[0].message.content))

with c2:
    st.link_button("💎 VIP: 10.000 Kelimelik Dev Rapor", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True)

st.write("---")
st.subheader("🔑 VIP Rapor Üretim Merkezi")

col_a, col_b = st.columns(2)
with col_a:
    oid = st.text_input("Sipariş No:")
with col_b:
    confirm = st.checkbox("Dijital rapor şartlarını ve teknik analiz modelini onaylıyorum.")

if st.button("🚀 VIP Raporu Şimdi İnşa Et", type="primary", use_container_width=True):
    if not user_input or not oid or not confirm:
        st.error("Giriş bilgileri eksik!")
    else:
        with st.status("🛠️ Raporunuz katman katman örülüyor. Bu işlem ~3-4 dakika sürebilir.", expanded=True):
            final_doc = generate_vip_content(user_input, oid)
            if final_doc:
                st.success("✅ 10.000 Kelimelik Rapor Hazır!")
                st.download_button(
                    label="📂 Raporu Bilgisayarına İndir (.txt)",
                    data=final_doc.encode('utf-8-sig'),
                    file_name=f"ULTRA_STRATEJI_{oid}.txt",
                    mime="text/plain; charset=utf-8",
                    use_container_width=True
                )
                with st.expander("📝 Rapor Önizleme"):
                    st.text(final_doc[:3000] + "...")

st.caption("© 2026 AI Analiz SaaS | Professional Industry Solutions")
