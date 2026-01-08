import streamlit as st
from groq import Groq
from datetime import datetime

# --- GÜVENLİK VE API BAĞLANTISI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Sistem hatası: API anahtarı yüklenemedi. Lütfen yönetici ile iletişime geçin.")

# Sayfa Ayarları
st.set_page_config(page_title="AI Pro Strateji", page_icon="📈", layout="centered")

# --- KRİTİK YASAL UYARI VE DESTEK (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("🛡️ Yasal Bilgilendirme")
    st.error("⚠️ **SORUMLULUK REDDİ:**")
    st.write("""
    Bu platform tarafından üretilen tüm analiz ve raporlar **yapay zeka ürünüdür**. 
    Kesinlikle yatırım tavsiyesi niteliği taşımaz. Verilen stratejilerin uygulanması sonucu 
    oluşabilecek maddi veya manevi zararlardan yazılım sahibi sorumlu tutulamaz. 
    Ticari kararların sorumluluğu tamamen kullanıcıya aittir.
    """)
    st.write("---")
    st.info("📩 **Destek:** Sorularınız veya ödeme hataları için lütfen sipariş numaranızla birlikte bize ulaşın.")
    st.caption("Sürüm: v1.0.5 Pro")

# --- ANA EKRAN ---
st.title("📈 Profesyonel AI Strateji Motoru")
st.subheader("Veri Girişi")

# Veri Giriş Alanı
user_input = st.text_area("Yorumları buraya yapıştırın (Max 5000 Karakter):", height=150, placeholder="Analiz edilecek müşteri yorumlarını buraya ekleyin...")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Ücretsiz Özet Analiz"):
        if user_input:
            with st.spinner('Özetleniyor...'):
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Aşağıdaki yorumları profesyonel bir dille özetle: {user_input}"}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("✅ Ücretsiz Özet Hazır")
                st.info(res.choices[0].message.content)
        else:
            st.warning("Lütfen önce yorumları girin.")

with col2:
    # Shopier linkin gelene kadar bu buton yönlendirme yapar
    st.link_button("💎 VIP Rapor Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN_GELDIGINDE_BURAYI_DEGISTIR")
    st.caption("ℹ️ 5 Sayfalık detaylı strateji raporu.")

st.write("---")

# --- ÖDEME DOĞRULAMA VE VIP RAPOR ALANI ---
st.subheader("🔑 VIP Rapor Kilidini Aç")
st.write("Ödeme yaptıktan sonra Shopier'den gelen **Sipariş Numarasını** girin.")

order_no = st.text_input("Sipariş No:", placeholder="Örn: 12345678")

if order_no and len(order_no) >= 8:
    st.success(f"Sipariş No: {order_no} tanımlandı.")
    
    # KESİN ONAY KUTUSU (Yasal Koruma)
    accept_terms = st.checkbox("Üretilen raporun bir yapay zeka çıktısı olduğunu, iadesinin bulunmadığını ve tüm sorumluluğu üstlendiğimi kabul ediyorum.")
    
    if accept_terms:
        if st.button("🚀 5 Sayfalık VIP Raporu Şimdi Üret"):
            if user_input:
                with st.spinner('Derin analiz yapılıyor... Bu işlem 40-50 saniye sürebilir.'):
                    tarih = datetime.now().strftime("%d/%m/%Y")
                    
                    # Raporun içine de yasal uyarıyı gömüyoruz ki çıktı alınca da orada dursun
                    prompt = f"""
                    Aşağıdaki verilere dayanarak 5 sayfalık derinlemesine bir iş stratejisi yaz.
                    
                    **ÖNEMLİ YASAL UYARI:** BU RAPOR YAPAY ZEKA TARAFINDAN ÜRETİLMİŞTİR. TİCARİ KARARLARDA TEK DAYANAK OLARAK KULLANILMAMALIDIR.
                    
                    Sipariş No: {order_no}
                    Tarih: {tarih}
                    
                    Bölümler:
                    1. Stratejik Yönetici Özeti
                    2. Müşteri Davranış ve Beklenti Analizi
                    3. Ürün/Hizmet Optimizasyon Planı
                    4. Dijital Pazarlama ve Rekabet Yol Haritası
                    5. 12 Aylık Büyüme ve Ölçeklenme Stratejisi
                    
                    Veriler: {user_input}
                    """
                    
                    full_report = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    st.markdown("### 📄 ÖZEL STRATEJİ RAPORUNUZ")
                    st.markdown(full_report.choices[0].message.content)
                    
                    st.download_button(
                        label="📂 Raporu Bilgisayarına İndir",
                        data=full_report.choices[0].message.content,
                        file_name=f"Strateji_Raporu_{order_no}.txt",
                        mime="text/plain"
                    )
            else:
                st.error("Hata: Rapor üretmek için yukarıdaki alana verileri girmiş olmanız gerekir.")
else:
    st.caption("Not: Geçerli bir sipariş numarası girdiğinizde rapor üretim paneli aktifleşecektir.")

st.write("---")
st.caption("© 2026 AI Analiz Yazılım | Tüm Hakları Saklıdır.")
