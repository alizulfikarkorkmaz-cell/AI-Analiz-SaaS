import streamlit as st
from groq import Groq
from datetime import datetime

# --- GÜVENLİK ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Anahtarı bulunamadı!")

st.set_page_config(page_title="AI İş Stratejisti", page_icon="📈")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Yasal Uyarı")
    st.error("Bu raporlar yapay zeka çıktısıdır. Kesinlikle yatırım tavsiyesi değildir.")
    st.write("---")
    st.info("Shopier Sipariş No ile destek alabilirsiniz.")

st.title("🚀 Üretici İçin AI Strateji Motoru")
st.subheader("Veri Odaklı Müşteri ve Üretim Analizi")

user_input = st.text_area("Yorumları buraya yapıştırın:", height=150, placeholder="Müşteri deneyimlerini buraya ekleyin...")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Ücretsiz Detaylı Analiz"):
        if user_input:
            with st.spinner('Veriler işleniyor...'):
                # ÜCRETSİZ AMA DETAYLI ANALİZ PROMPT'U
                free_prompt = f"""
                Aşağıdaki yorumları analiz et ve şu formatta bir özet çıkar:
                1. GENEL MEMNUNİYET SKORU: (0-100 arası bir puan ver)
                2. DUYGU ANALİZİ: (Pozitif, Negatif veya Karışık olarak belirt)
                3. ÖZET: (Müşterinin ana şikayeti nedir?)
                4. ÜRETİCİYE KRİTİK NOT: (Üreticiye hemen yapması gereken 2 tavsiye ver)
                
                Yorumlar: {user_input}
                """
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": free_prompt}],
                    model="llama-3.3-70b-versatile",
                )
                st.success("📊 Ücretsiz Analiz Sonucu")
                st.markdown(res.choices[0].message.content)
                st.write("---")
                st.caption("Daha derin teknik analiz ve 5 sayfalık çözüm planı için VIP raporu tercih edin.")
        else:
            st.warning("Lütfen veri girin.")

with col2:
    st.link_button("💎 5 Sayfa VIP Teknik Rapor", "https://www.shopier.com/SAYFA_LINKIN")
    st.caption("Mühendislik ve Ar-Ge çözümleri içeren tam rapor.")

st.write("---")

# --- VIP PANEL ---
st.subheader("🔑 VIP Rapor Kilidini Aç")
order_no = st.text_input("Shopier Sipariş No:")

if order_no and len(order_no) >= 8:
    st.success(f"Sipariş No: {order_no} onaylandı.")
    if st.checkbox("İadesiz dijital içeriği ve yasal şartları kabul ediyorum."):
        if st.button("🚀 5 Sayfalık Teknik Raporu Üret"):
            with st.spinner('Üreticiye özel strateji dosyası hazırlanıyor...'):
                tarih = datetime.now().strftime("%d/%m/%Y")
                pro_prompt = f"""
                Müşteri yorumlarını analiz et ve üretici için 5 SAYFALIK detaylı bir strateji yaz.
                Sipariş No: {order_no} | Tarih: {tarih}
                
                İçerik Şunları Kapsasın:
                1. Üretim ve Formülasyon Hataları: (Kuruma, kırılma vb. teknik çözümler)
                2. Fiyat/Performans Mühendisliği: (Pazar konumlandırma stratejisi)
                3. Rakip Analizi: (Lüks vs. Dermokozmetik savaşı)
                4. Ar-Ge ve Ambalaj İnovasyonu: (Vakum, presleme, materyal kalitesi)
                5. 12 Aylık Finansal ve Operasyonel Yol Haritası.
                
                Yorumlar: {user_input}
                """
                full_report = client.chat.completions.create(
                    messages=[{"role": "user", "content": pro_prompt}],
                    model="llama-3.3-70b-versatile",
                )
                st.markdown("### 📄 ÜRETİCİYE ÖZEL VIP STRATEJİ RAPORU")
                st.markdown(full_report.choices[0].message.content)
                st.download_button("📂 Raporu İndir (.txt)", full_report.choices[0].message.content, file_name=f"Vip_Strateji_{order_no}.txt")

st.write("---")
st.caption("© 2026 AI Analiz SaaS | Güvenli Ödeme Altyapısı: Shopier")
