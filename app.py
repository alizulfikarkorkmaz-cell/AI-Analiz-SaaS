import streamlit as st
from groq import Groq

# Kasadaki anahtarı kullanıyoruz
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Lütfen Streamlit Secrets kısmına GROQ_API_KEY ekleyin.")

st.set_page_config(page_title="AI Strateji Merkezi", page_icon="📈")

# --- SOL PANEL (BİLGİ VE YASAL UYARI) ---
with st.sidebar:
    st.title("🛡️ Güvenlik & Yasal")
    st.info("İşlemleriniz SSL şifreleme ile korunmaktadır.")
    st.write("---")
    st.warning("**YASAL UYARI:** Bu platformda sunulan tüm analiz ve raporlar yapay zeka tarafından üretilmiştir. Yatırım tavsiyesi veya kesin ticari garanti içermez. Oluşabilecek ticari risklerden kullanıcı sorumludur.")
    st.write("---")
    st.subheader("İletişim")
    st.write("Destek hattı: [WhatsApp Destek]")

# --- ANA SAYFA ---
st.title("🚀 Profesyonel Ürün Analiz & Strateji Motoru")
st.write("Müşteri yorumlarını girin, yapay zeka saniyeler içinde büyüme planınızı çıkarsın.")

user_input = st.text_area("Yorumları buraya yapıştırın:", height=150, max_chars=5000)

if st.button("Ücretsiz Özet Analiz"):
    if user_input:
        with st.spinner('Yapay zeka verileri okuyor...'):
            try:
                # 1. ADIM: KISA ÖZET
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Şu yorumları kısaca özetle: {user_input}"}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("Özet Analiz Tamamlandı")
                st.write(res.choices[0].message.content)
                
                st.write("---")
                st.subheader("💎 Tam Kapsamlı 5 Sayfalık Strateji Raporu")
                st.write("Derin analiz ve yol haritası için ödemenizi tamamlayıp aşağıdaki onayı veriniz.")
                
                # Shopier Linkin
                st.link_button("💳 Ödemeyi Yap (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")
                
                # Müşteri Onayı ve Yasal Beyan
                if st.checkbox("✅ Ödemeyi tamamladım. Raporun yapay zeka tarafından üretildiğini ve ticari sorumluluğun bana ait olduğunu kabul ediyorum."):
                    with st.spinner('5 Sayfalık Profesyonel Rapor Hazırlanıyor...'):
                        full_report = client.chat.completions.create(
                            messages=[{
                                "role": "user", 
                                "content": f"ÖNEMLİ: Raporun en başına 'BU BİR YAPAY ZEKA ANALİZİDİR, KESİN TAVSİYE İÇERMEZ' notu ekleyerek, şu yorumlara göre 5 sayfalık dev bir strateji raporu yaz: {user_input}"
                            }],
                            model="llama-3.3-70b-versatile",
                        )
                        st.markdown("### 📄 Profesyonel Strateji Raporu")
                        st.markdown(full_report.choices[0].message.content)
                        st.download_button("📂 Raporu İndir", full_report.choices[0].message.content, file_name="strateji_raporu.txt")
            except Exception as e:
                st.error(f"Sistemde geçici bir sorun oluştu. Lütfen tekrar deneyin.")
    else:
        st.warning("Analiz için veri girilmelidir.")

# Sayfa sonu sabit yasal uyarı
st.write("---")
st.caption("© 2026 AI Analiz Yazılım. Tüm hakları saklıdır. Bu uygulama kullanıcıya 'olduğu gibi' sunulur; sunulan içeriklerin doğruluğu veya eksiksizliği konusunda herhangi bir yasal taahhüt verilmez.")
