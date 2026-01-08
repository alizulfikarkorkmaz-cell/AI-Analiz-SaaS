import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AI Strateji Merkezi", page_icon="📈")

st.title("🚀 Profesyonel Ürün Analiz & 5 Sayfalık Strateji")

user_input = st.text_area("Yorumları buraya yapıştırın:", height=150, max_chars=5000)

if st.button("Ücretsiz Analiz Et"):
    if user_input:
        with st.spinner('Kısa özet hazırlanıyor...'):
            # 1. ADIM: KISA ÖZET
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": f"Şu yorumları kısaca özetle: {user_input}"}],
                model="llama-3.3-70b-versatile",
            )
            st.success("Özet Analiz Tamam")
            st.write(res.choices[0].message.content)
            
            st.write("---")
            st.subheader("💎 Tam Kapsamlı 5 Sayfalık Strateji Raporu")
            st.write("Bu rapor; rakip analizi, operasyonel iyileştirme ve 12 aylık yol haritası içerir.")
            
            # Ödeme Simülasyonu veya Linki
            st.link_button("Ödemeyi Yap ve Raporu Aç (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")
            
            # TEST İÇİN: Ödeme yapılmış gibi raporu açan bir buton (Geliştirme aşaması)
            if st.checkbox("Ödeme yaptım, raporu hazırla"):
                with st.spinner('5 Sayfalık Dev Rapor Hazırlanıyor... (Bu işlem 30 saniye sürebilir)'):
                    # 2. ADIM: UZUN VE DETAYLI RAPOR
                    full_report = client.chat.completions.create(
                        messages=[{
                            "role": "user", 
                            "content": f"""
                            Aşağıdaki yorumları kullanarak 5 sayfa uzunluğunda profesyonel bir ticari strateji raporu yaz. 
                            Şu bölümler mutlaka olsun ve her bölümü çok detaylandır:
                            1. Müşteri Psikolojisi ve Segmentasyon Analizi (1 Sayfa)
                            2. Ürün Geliştirme ve İade Azaltma Reçetesi (1 Sayfa)
                            3. Rakip Karşısında Konumlandırma Stratejisi (1 Sayfa)
                            4. Pazarlama ve Reklam Metni Önerileri (1 Sayfa)
                            5. 12 Aylık Finansal Büyüme ve Operasyon Planı (1 Sayfa)
                            
                            Yorumlar: {user_input}
                            """
                        }],
                        model="llama-3.3-70b-versatile",
                    )
                    st.markdown(full_report.choices[0].message.content)
                    st.download_button("Raporu PDF/Metin Olarak İndir", full_report.choices[0].message.content)

    else:
        st.warning("Lütfen veri girin.")
