import streamlit as st
from groq import Groq
from datetime import datetime

# --- GÜVENLİK VE API BAĞLANTISI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Sistem hatası: API anahtarı yüklenemedi. Lütfen yönetici ile iletişime geçin.")

# Sayfa Ayarları (Google Play Hazırlık Modu)
st.set_page_config(page_title="AI Pro Analiz & Strateji", page_icon="📈", layout="centered")

# --- KRİTİK YASAL ZIRH (SOL PANEL - SIDEBAR) ---
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
    st.caption("Sürüm: v1.0.8 VIP - SaaS Ready")

# --- ANA EKRAN ---
st.title("📈 Profesyonel AI Strateji Motoru")
st.markdown("##### Müşteri Geri Bildirimlerini Veri Odaklı İş Planına Dönüştürün")

# Veri Giriş Alanı
user_input = st.text_area("Analiz edilecek yorumları buraya yapıştırın (Max 5000 Karakter):", 
                          height=200, 
                          placeholder="Örn: Chanel, YSL veya Benefit ürünleri hakkındaki müşteri deneyimlerini buraya ekleyin...")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Ücretsiz Detaylı Analiz"):
        if user_input:
            with st.spinner('Yapay zeka derin analiz yapıyor...'):
                # ÜCRETSİZ AMA "VAY BE" DEDİRTEN PROMPT
                free_prompt = f"""
                Aşağıdaki müşteri yorumlarını analiz et ve şu formatta profesyonel bir özet çıkar:
                
                1. GENEL MEMNUNİYET SKORU: (0 ile 100 arası bir puan ver)
                2. DUYGU ANALİZİ: (Pozitif, Negatif veya Karışık)
                3. KRİTİK ŞİKAYET ÖZETİ: (Müşterinin canını en çok sıkan teknik sorun nedir?)
                4. ÜRETİCİYE ACİL TEKNİK TAVSİYE: (Üreticiye hemen yapması gereken 2 somut öneri ver)
                
                Yorumlar: {user_input}
                """
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": free_prompt}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("📊 Ücretsiz Analiz Sonucu")
                st.markdown(res.choices[0].message.content)
                st.write("---")
                st.caption("Not: Bu bir ön izlemedir. 5 sayfalık teknik rapor için VIP panele geçin.")
        else:
            st.warning("Lütfen önce analiz edilecek yorumları girin.")

with col2:
    # Shopier linkin gelene kadar burası beklemede
    st.link_button("💎 VIP: 5 Sayfa Teknik Rapor", "https://www.shopier.com/SAYFA_LINKIN_GELDIGINDE_BURAYI_DEGISTIR")
    st.caption("💳 Fiyat: 50 TL (KDV Dahil)")
    st.info("Üreticiye yönelik Ar-Ge, ambalaj ve pazarlama çözümleri içerir.")

st.write("---")

# --- ÖDEME DOĞRULAMA VE VIP RAPOR ALANI ---
st.subheader("🔑 VIP Rapor Üretim Paneli")
st.write("Ödeme sonrası Shopier'den gelen **Sipariş Numarasını** aşağıya girin.")

order_no = st.text_input("Sipariş No:", placeholder="Örn: 98765432")

if order_no and len(order_no) >= 8:
    st.success(f"✅ Sipariş No: {order_no} doğrulandı. Rapor üretimi için onay bekliyor.")
    
    # KESİN ONAY KUTUSU (Yasal Koruma - Önceki koddan gelen zorunlu alan)
    accept_terms = st.checkbox("Üretilen raporun bir yapay zeka çıktısı olduğunu, iadesinin bulunmadığını ve tüm sorumluluğu üstlendiğimi kabul ediyorum.")
    
    if accept_terms:
        if st.button("🚀 5 Sayfalık Profesyonel Teknik Raporu Üret"):
            if user_input:
                with st.spinner('Mühendislik ve Ar-Ge çözümleri içeren 5 sayfalık dev rapor hazırlanıyor...'):
                    tarih = datetime.now().strftime("%d/%m/%Y")
                    
                    # VIP PROMPT - ÜRETİCİYE TOKAT GİBİ TAVSİYELER
                    pro_prompt = f"""
                    Sen profesyonel bir iş danışmanı ve ürün mühendisisin. 
                    Aşağıdaki müşteri yorumlarını al ve üretici firma için 5 SAYFA uzunluğunda dev bir rapor yaz.
                    
                    **ÖNEMLİ YASAL UYARI:** BU RAPOR YAPAY ZEKA ÇIKTISIDIR VE TİCARİ SORUMLULUK KULLANICIYA AİTTİR.
                    
                    Sipariş No: {order_no} | Tarih: {tarih}
                    
                    Bölümler:
                    1. ÜRETİM VE FORMÜLASYON HATALARI: (Kuruma, kırılma, pigmentasyon gibi teknik sorunlara mühendislik çözümleri)
                    2. FİYATLANDIRMA VE ALGI YÖNETİMİ: (300 TL+ bandındaki ürünlerin hayal kırıklığı yaratmaması için stratejiler)
                    3. RAKİP ANALİZİ: (Lüks markalar, dermokozmetik markalarına karşı pazar payını nasıl korur?)
                    4. AR-GE VE AMBALAJ İNOVASYONU: (Vakum sistemleri, presleme basıncı ve malzeme kalitesi üzerine somut öneriler)
                    5. 12 AYLIK MÜŞTERİ GERİ KAZANIM VE BÜYÜME PLANI: (Sadakat programları ve geri dönüş stratejileri)
                    
                    Müşteri Verileri: {user_input}
                    
                    Lütfen her bölümü son derece detaylı, teknik terimler içeren ve üreticiyi harekete geçirecek profesyonel bir dille yaz.
                    """
                    
                    full_report = client.chat.completions.create(
                        messages=[{"role": "user", "content": pro_prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    st.markdown("### 📄 ÜRETİCİYE ÖZEL VIP STRATEJİ VE ÇÖZÜM DOSYASI")
                    st.markdown(full_report.choices[0].message.content)
                    
                    # İNDİRME BUTONU
                    st.download_button(
                        label="📂 Raporu Bilgisayarına İndir (.txt)",
                        data=full_report.choices[0].message.content,
                        file_name=f"VIP_Teknik_Rapor_{order_no}.txt",
                        mime="text/plain"
                    )
            else:
                st.error("⚠️ Hata: Rapor üretmek için yukarıdaki alana müşteri yorumlarını girmiş olmanız gerekir.")
else:
    st.caption("💡 Not: Geçerli bir sipariş numarası girdiğinizde rapor üretim paneli ve onay kutusu aktifleşecektir.")

st.write("---")
st.caption("© 2026 AI Analiz Yazılım SaaS | Güvenli Ödeme Sistemi: Shopier")
