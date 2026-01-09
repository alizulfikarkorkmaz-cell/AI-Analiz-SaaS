import streamlit as st
from groq import Groq
from datetime import datetime
import io
import smtplib
from email.message import EmailMessage

# =========================
# AYARLAR & GÜVENLİK
# =========================
st.set_page_config(page_title="AI Pro Analiz & Strateji", page_icon="📈", layout="centered")

# TEST MODU: Ödeme kontrolünü atlamak için True bırakın. Canlıda False yapın.
TEST_MODE = True 

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ API Hatası! Secrets ayarlarını kontrol edin.")
    st.stop()

# =========================
# PDF & KARAKTER MOTORU (GÜNCELLENDİ)
# =========================
def create_pdf_txt(report_text, order_no, tarih):
    """
    PDF kütüphaneleri Türkçe karakterlerde sorun çıkardığı için 
    en güvenli yol UTF-8 destekli profesyonel bir metin raporu oluşturmaktır.
    """
    header = f"📄 VIP STRATEJI VE TEKNIK ANALIZ RAPORU\n"
    header += f"Siparis No: {order_no} | Tarih: {tarih}\n"
    header += "="*50 + "\n\n"
    full_content = header + report_text
    
    # Karakter hatasını önlemek için UTF-8 encode yapıyoruz
    return full_content.encode('utf-8')

def send_email(report_bytes, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"💎 {'[TEST]' if TEST_MODE else ''} VIP Strateji Raporunuz - No: {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content(f"Merhaba,\n\nTalep ettiğiniz profesyonel VIP Raporunuz ektedir.\n\nSipariş No: {order_no}\n\nİyi çalışmalar dileriz.")
    
    msg.add_attachment(report_bytes, maintype='text', subtype='plain', filename=f"VIP_RAPOR_{order_no}.txt")
    
    try:
        with smtplib.SMTP_SSL(st.secrets["SMTP_SERVER"], st.secrets["SMTP_PORT"]) as server:
            server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASS"])
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"E-posta hatası: {e}")
        return False

# =========================
# YAN MENÜ (SIDEBAR)
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ Yasal Zırh")
    if TEST_MODE:
        st.warning("🛠️ TEST MODU AKTİF\nÖdeme kontrolü bypass edildi.")
    st.error("⚠️ Yapay zeka çıktıları yatırım tavsiyesi değildir. Sorumluluk kullanıcıya aittir.")
    st.write("---")
    st.caption("v1.2.0 - Enterprise Edition")

# =========================
# ANA EKRAN
# =========================
st.title("📈 Profesyonel AI Strateji Motoru")
st.write("Verilerinizi girin ve e-posta adresinize 5 sayfalık dev raporu alın.")

user_input = st.text_area("Analiz edilecek yorumları veya verileri girin:", height=200, placeholder="Verileri buraya yapıştırın...")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Ücretsiz Hızlı Analiz"):
        if user_input:
            with st.spinner('Analiz ediliyor...'):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Aşağıdaki verileri analiz et, memnuniyet skoru ver ve üreticiye 2 tavsiye yaz. Dil tamamen temiz Türkçe olsun: {user_input[:2000]}"}]
                )
                st.success("📊 Hızlı Analiz Sonucu")
                st.write(res.choices[0].message.content)
        else:
            st.warning("Önce veri girmelisiniz.")

with col2:
    # Shopier linkin gelince burayı güncelle
    st.link_button("💎 VIP: Dev Rapor Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
st.subheader("🔑 VIP Rapor Hazırlama & E-Posta Paneli")

order_no = st.text_input("Shopier Sipariş No:", placeholder="Örn: 98765432")
email_input = st.text_input("Raporun Gönderileceği E-posta Adresi:", placeholder="ornek@mail.com")
accept = st.checkbox("Analizin dijital ürün olduğunu, iadesiz olduğunu ve yasal sorumluluğu kabul ediyorum.")

if st.button("🚀 VIP Raporu İnşa Et ve Gönder"):
    if not user_input or not order_no or not accept or not email_input:
        st.error("⚠️ Eksik bilgi! Lütfen Veri, Sipariş No, E-posta ve Onay kutusunu kontrol edin.")
    elif len(order_no) < 8:
        st.error("⚠️ Geçersiz sipariş numarası formatı.")
    else:
        with st.status("🚀 Dev rapor hazırlanıyor...", expanded=True) as status:
            tarih = datetime.now().strftime("%d/%m/%Y")
            
            sections = [
                ("1. TEKNIK ANALIZ", "Üretim ve formülasyon hatalarına yönelik 2000 kelimelik teknik rapor."),
                ("2. STRATEJI", "Fiyatlandırma, pazar konumu ve rakip analizi odaklı 2000 kelime."),
                ("3. GELECEK", "Sektör trendleri ve 12 aylık gelecek tahmini."),
                ("4. AR-GE", "Ürün geliştirme ve inovasyon önerileri."),
                ("5. UYGULAMA PLANI", "Adım adım 1 yıllık büyüme ve aksiyon planı.")
            ]
            
            report_text = ""
            prog = st.progress(0)
            
            for i, (title, task) in enumerate(sections):
                st.write(f"⏳ {title} bölümü yazılıyor...")
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Profesyonel Türkiye Türkçesi ile yaz. {title} başlığı altında {task}. Veriler: {user_input[:4000]}"}],
                    temperature=0.4
                )
                report_text += f"\n\n{'='*20}\n{title}\n{'='*20}\n{res.choices[0].message.content}"
                prog.progress((i + 1) / len(sections))
            
            # Raporu hazırla
            report_bytes = create_pdf_txt(report_text, order_no, tarih)
            
            # E-posta gönder
            st.write("📧 E-posta gönderiliyor...")
            if send_email(report_bytes, email_input, order_no):
                status.update(label="✅ İşlem Başarılı! Rapor gönderildi.", state="complete", expanded=False)
                st.success(f"💎 VIP Raporunuz başarıyla {email_input} adresine gönderildi!")
                st.download_button("📂 Raporu Manuel İndir (.txt)", report_bytes, file_name=f"VIP_Rapor_{order_no}.txt")
            else:
                st.error("❌ Rapor hazırlandı ama e-posta gönderilemedi. Lütfen manuel indirin.")
                st.download_button("📂 Raporu İndir (.txt)", report_bytes, file_name=f"VIP_Rapor_{order_no}.txt")

st.caption("© 2026 AI Analiz Yazılım SaaS | Enterprise Edition")
