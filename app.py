import streamlit as st
from groq import Groq

# Güvenli Anahtar Girişi
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Sistem anahtarı yüklenemedi. Lütfen yönetici ile iletişime geçin.")

st.set_page_config(page_title="AI Pro Strateji", page_icon="📈", layout="centered")

# --- SOL PANEL (PROFESYONEL GÖRÜNÜM) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100) # Temsili Logo
    st.title("Kurumsal Destek")
    st.info("Bu uygulama 256-bit SSL ile korunmaktadır.")
    st.write("---")
    st.error("⚠️ **YASAL SORUMLULUK SINIRI:** Bu raporlar yapay zeka ürünüdür. Yatırım tavsiyesi değildir. Tüm kararlar kullanıcının sorumluluğundadır.")
    st.write("---")
    st.markdown("[Gizlilik Politikası](https://seninsiten.com/gizlilik)") # Örnek link

# --- ANA EKRAN ---
st.title("📈 Profesyonel Ürün Analiz Motoru")
st.subheader("Yorumlardan 5 Sayfalık Büyüme Stratejisi Üretin")

user_input = st.text_area("Yorumları bu alana yapıştırın:", height=200, max_chars=5000, placeholder="Müşterilerinizin geri bildirimlerini buraya ekleyin...")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Ücretsiz Özet Çıkar"):
        if user_input:
            with st.spinner('Yapay Zeka özetliyor...'):
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Aşağıdaki yorumları profesyonel bir dille özetle: {user_input}"}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("Ücretsiz Özet Hazır")
                st.info(res.choices[0].message.content)
        else:
            st.warning("Lütfen veri girişi yapın.")

with col2:
    # VIP Rapor Butonu
    st.link_button("💎 5 Sayfalık VIP Rapor Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")

# VIP RAPOR ÜRETME ALANI (Ödeme sonrası onay ile)
st.subheader("💎 VIP Rapor Paneli")
paid_check = st.checkbox("Ödememi tamamladım, 5 sayfalık raporu oluşturmak istiyorum.")

if paid_check:
    if user_input:
        with st.spinner('🚀 5 Sayfalık Profesyonel Rapor Hazırlanıyor... Bu işlem 40 saniye sürebilir.'):
            try:
                full_report = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Şu yorumlar için 5 sayfalık çok detaylı, bölümlere ayrılmış, profesyonel bir iş stratejisi yaz. En başa yasal uyarıyı koy: {user_input}"}],
                    model="llama-3.3-70b-versatile",
                )
                st.markdown(full_report.choices[0].message.content)
                st.download_button("📂 Raporu İndir (PDF/TXT)", full_report.choices[0].message.content, file_name="VIP_Strateji_Raporu.txt")
            except Exception as e:
                st.error("Sistem yoğunluğu nedeniyle rapor üretilemedi. Lütfen tekrar deneyin.")
    else:
        st.warning("Rapor üretmek için önce yukarıdaki alana yorumları girmelisiniz.")

st.write("---")
st.caption("© 2026 AI Analiz Yazılım A.Ş. | Google Play Store Sürümü v1.0")
