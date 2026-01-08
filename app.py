import streamlit as st
from groq import Groq

# Kasa anahtarı
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Pro Analiz SaaS", page_icon="💰")

# Sol tarafa bir bilgi paneli (Güven için)
with st.sidebar:
    st.title("Yardım & Destek")
    st.info("Teknik bir sorun yaşarsanız veya raporunuz ulaşmazsa [WhatsApp Hattımızdan] ulaşabilirsiniz.")
    st.write("---")
    st.write("© 2024 AI Analiz Yazılım")

st.title("🚀 Akıllı Ürün Analiz & Strateji Motoru")

user_input = st.text_area("Analiz edilecek yorumları buraya girin:", height=200)

if st.button("Hemen Ücretsiz Analiz Et"):
    if user_input:
        with st.spinner('Yapay Zeka rapor hazırlıyor...'):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Şu yorumları analiz et: {user_input}. Türkçe kısa özet ver."}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("Özet Analiz Hazır!")
                st.write(chat_completion.choices[0].message.content)
                
                st.write("---")
                # İŞTE SATIŞ BÖLÜMÜ
                st.subheader("🎯 Daha Fazlasını İster Misiniz?")
                st.write("Bu yorumlara özel 50 sayfalık 'İade Düşürme ve Satış Artırma' strateji dosyasını hemen alın.")
                
                # Buraya kendi Shopier linkini koyacaksın usta
                st.link_button("💎 Full Strateji Raporunu Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")
                st.caption("Ödeme sonrası raporunuz 1 saat içinde mail adresinize gönderilir.")
                
            except Exception as e:
                st.error("Sistemde yoğunluk var, lütfen az sonra tekrar deneyin.")
    else:
        st.warning("Lütfen yorum girin.")

st.write("---")
st.caption("Uyarı: Yapay zeka hatalı sonuçlar üretebilir. Ticari kararlar almadan önce verileri doğrulamanız önerilir.")
