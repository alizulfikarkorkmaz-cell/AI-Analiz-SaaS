import streamlit as st
from groq import Groq

# Kasa anahtarı
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Kasa anahtarı eksik!")

st.set_page_config(page_title="Pro Analiz SaaS", page_icon="💰")

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("Yardım & Destek")
    st.info("Teknik bir sorun yaşarsanız [WhatsApp] üzerinden ulaşabilirsiniz.")
    
    st.write("---")
    st.subheader("💎 VIP Hizmet")
    st.write("Sadece özetle yetinmeyin. Rakip analizi ve 50 sayfalık strateji raporu için:")
    # BURAYA KENDİ SHOPIER LİNKİNİ YAZ
    st.link_button("VIP Rapor Satın Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")
    
    st.write("---")
    st.caption("© 2024 AI Analiz Yazılım")

# --- ANA SAYFA ---
st.title("🚀 Akıllı Ürün Analiz & Strateji Motoru")

user_input = st.text_area("Analiz edilecek yorumları buraya girin:", height=200)

if st.button("Hemen Ücretsiz Analiz Et"):
    if user_input:
        with st.spinner('Yapay Zeka rapor hazırlıyor...'):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Şu yorumları analiz et: {user_input}. Türkçe olarak 1. Memnuniyet, 2. Şikayetler, 3. Tavsiye yaz."}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("Ücretsiz Özet Analiz Tamamlandı!")
                st.markdown(chat_completion.choices[0].message.content)
                
                # Analiz bitince çıkan ekstra teklif
                st.warning("⚠️ Bu sadece bir özetti. Tam kapsamlı profesyonel rapor için yukarıdaki 'VIP Rapor' butonunu kullanabilirsiniz.")
                
            except Exception as e:
                st.error("Bir hata oluştu, lütfen tekrar deneyin.")
    else:
        st.warning("Lütfen önce yorum yapıştırın.")

st.write("---")
st.caption("Uyarı: Yapay zeka hatalı sonuçlar üretebilir.")
