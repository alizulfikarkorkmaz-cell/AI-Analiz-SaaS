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
    st.caption("Sürüm: v1.1.0 VIP - Professional Turkish Edition")

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
                # ÜCRETSİZ ANALİZ: UZMAN DİLİ VE YAZIM KONTROLÜ EKLENDİ
                free_prompt = f"""
                Sen kıdemli bir İş Analistisin. Aşağıdaki müşteri yorumlarını analiz et.
                DİL KURALLARI: Sadece kusursuz Türkiye Türkçesi kullan. Yabancı karakter (š, ă vb.) kullanma. 
                Yazım hatası yapma. Profesyonel ve akademik bir üslup benimse.
                
                Format:
                1. GENEL MEMNUNİYET SKORU: (0-100 arası sayısal veri)
                2. DUYGU ANALİZİ: (Pozitif, Negatif veya Karışık)
                3. STRATEJİK ÖZET: (Müşterinin temel teknik şikayeti)
                4. ÜRETİCİYE KRİTİK TAVSİYE: (Hemen uygulanabilir 2 profesyonel öneri)
                
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
    
    accept_terms = st.checkbox("Üretilen raporun bir yapay zeka çıktısı olduğunu, iadesinin bulunmadığını ve tüm sorumluluğu üstlendiğimi kabul ediyorum.")
    
    if accept_terms:
        if st.button("🚀 5 Sayfalık Profesyonel Teknik Raporu Üret"):
            if user_input:
                with st.spinner('Uzman heyeti raporu hazırlıyor...'):
                    tarih = datetime.now().strftime("%d/%m/%Y")
                    
                    # VIP PROMPT: MÜHENDİS, CEO VE DANIŞMAN KİMLİĞİ EKLENDİ
                    pro_prompt = f"""
                    Sen; bir Ürün Mühendisi, bir CEO ve bir Strateji Danışmanından oluşan bir heyetsin.
                    ÖNEMLİ: Raporu kusursuz bir Türkiye Türkçesi ile, hiçbir yazım hatası ve yabancı karakter (zkušen, tăngellemek gibi hatalar ASLA olmayacak) olmadan yaz. 
                    Daima profesyonel, ciddi ve teknik bir terminoloji kullan.
                    
                    Sipariş No: {order_no} | Tarih: {tarih}
                    
                    Bölümler:
                    1. ÜRETİM VE FORMÜLASYON ANALİZİ: (Mühendis gözüyle teknik kusurlar ve kimyasal/yapısal iyileştirme formülleri)
                    2. STRATEJİK FİYATLANDIRMA VE MARKA KONUMLANDIRMA: (CEO perspektifiyle lüks segment tutundurma stratejileri)
                    3. SEKTÖREL REKABET VE PAZAR ANALİZİ: (Dermokozmetik vs Lüks makyaj savaşı yönetimi)
                    4. ENDÜSTRİYEL TASARIM VE AMBALAJ İNOVASYONU: (Vakum, basınç ve malzeme mukavemeti önerileri)
                    5. 12 AYLIK KURUMSAL BÜYÜME VE SADAKAT PROJEKSİYONU: (Pazarlama Danışmanı gözüyle yol haritası)
                    
                    Müşteri Verileri: {user_input}
                    
                    Raporu en az 2000 kelimeye eşdeğer derinlikte, her bölümü teknik alt başlıklarla detaylandırarak yaz.
                    """
                    
                    full_report = client.chat.completions.create(
                        messages=[{"role": "user", "content": pro_prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    st.markdown("### 📄 ÜRETİCİYE ÖZEL VIP STRATEJİ VE ÇÖZÜM DOSYASI")
                    st.markdown(full_report.choices[0].message.content)
                    
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


