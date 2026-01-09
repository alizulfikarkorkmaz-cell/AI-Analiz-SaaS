import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io
import smtplib
from email.message import EmailMessage

# =========================
# SAYFA AYARLARI
# =========================
st.set_page_config(
    page_title="AI Pro Analiz & Strateji",
    page_icon="📈",
    layout="centered"
)

# =========================
# API BAĞLANTISI
# =========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Sistem Hatası: API Anahtarı bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
    st.stop()

# =========================
# GÜVENLİK FİLTRELERİ
# =========================
BANNED_WORDS = ["falan", "felan", "şey", "yani", "bi", "herhalde", "možnosti", "口碑", "zkušen", "tăngellemek"]
BANNED_REGEX = re.compile(r"[šăěščřž]|[\u4e00-\u9fff]|[\u0400-\u04FF]", re.UNICODE)

def output_is_clean(text: str) -> bool:
    lower = text.lower()
    return not (any(w in lower for w in BANNED_WORDS) or BANNED_REGEX.search(text))

# =========================
# PDF & E-POSTA MOTORU
# =========================
def create_pdf(report_text, order_no, tarih):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "VIP STRATEJI VE TEKNIK ANALIZ RAPORU")
    c.setFont("Helvetica", 10)
    c.drawString(50, height-80, f"Siparis No: {order_no} | Tarih: {tarih}")
    y = height - 120
    max_width = width - 100
    for line in report_text.split("\n"):
        wrapped_lines = simpleSplit(line, "Helvetica", 10, max_width)
        for wrapped_line in wrapped_lines:
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, wrapped_line.strip())
            y -= 14
    c.save()
    buffer.seek(0)
    return buffer

def send_email(pdf_buffer, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"VIP Analiz Raporunuz - Sipariş No: {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content("Değerli İş Ortağımız,\n\nSatın aldığınız 10.000 kelimelik dev strateji raporu ekte PDF formatında sunulmuştur.\n\nBaşarılar dileriz.")
    pdf_buffer.seek(0)
    msg.add_attachment(pdf_buffer.read(), maintype='application', subtype='pdf', filename=f"VIP_Rapor_{order_no}.pdf")
    try:
        with smtplib.SMTP_SSL(st.secrets["SMTP_SERVER"], st.secrets["SMTP_PORT"]) as server:
            server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASS"])
            server.send_message(msg)
        return True
    except: return False

# =========================
# YAN MENÜ (SIDEBAR) - İŞTE BURASI EKSİKTİ!
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ Kurumsal Panel")
    st.info("📊 **VIP Rapor İçeriği:**\n* Mühendislik Analizi\n* Stratejik Fiyatlandırma\n* 5 Yıllık Gelecek Planı\n* Ar-Ge ve Tasarım\n* 12 Aylık Yol Haritası")
    st.divider()
    st.error("⚠️ **SORUMLULUK REDDİ:**\nÜretilen raporlar yapay zeka çıktısıdır. Kesin yatırım tavsiyesi değildir.")
    st.write("---")
    st.caption("Destek hattı: Sipariş numaranızla mail üzerinden ulaşın.")

# =========================
# ANA EKRAN
# =========================
st.title("📈 Profesyonel AI Strateji Motoru")
st.markdown("##### Müşteri Geri Bildirimlerinden 10.000 Kelimelik Dev İş Planları")

user_input = st.text_area("Analiz edilecek yorumları veya verileri buraya girin:", height=250, placeholder="Verilerinizi buraya yapıştırın...")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Ücretsiz Hızlı Analiz"):
        if user_input:
            with st.spinner('Özetleniyor...'):
                res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": f"Ozetle ve puan ver: {user_input[:2000]}"}])
                st.success("📊 Hızlı Analiz Sonucu")
                st.write(res.choices[0].message.content)
        else: st.warning("Veri girilmedi.")

with col2:
    st.link_button("💎 VIP: 10.000 Kelimelik Rapor Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
st.subheader("🔑 VIP Rapor Üretim ve Teslimat")
st.markdown("> **Not:** VIP rapor 5 parça halinde üretilir ve yaklaşık 2 dakika sürer.")

ord_no = st.text_input("Shopier Sipariş No (8 Haneli):")
e_mail = st.text_input("Raporun Gönderileceği E-posta Adresi:")
confirm = st.checkbox("10.000 kelimelik analiz raporunun iadesiz olduğunu onaylıyorum.")

if st.button("🚀 VIP Raporu İnşa Et ve Mail Gönder"):
    if user_input and ord_no and e_mail and confirm:
        st.warning("⚠️ İşlem başladı. Lütfen tarayıcıyı kapatmayın. Raporunuz hazırlanıyor...")
        tarih = datetime.now().strftime("%d/%m/%Y")
        
        full_report = ""
        sections = [
            ("1. ÜRETİM HATALARI VE MÜHENDİSLİK", "Teknik kusurlar üzerine 2000 kelime akademik analiz."),
            ("2. STRATEJİK FİYATLANDIRMA", "Pazar konumu üzerine 2000 kelime finansal analiz."),
            ("3. SEKTÖREL GELECEK PROJEKSİYONU", "Trendler üzerine 2000 kelime gelecek analizi."),
            ("4. ENDÜSTRİYEL TASARIM VE AR-GE", "İnovasyon üzerine 2000 kelime tasarım analizi."),
            ("5. 12 AYLIK KURUMSAL YOL HARİTASI", "ROI ve KPI odaklı 2000 kelime uygulama planı.")
        ]
        
        bar = st.progress(0)
        for i, (t, task) in enumerate(sections):
            prompt = f"Turkiye Turkcesi kullan. Teknik yaz. {t} icin {task}. Veri: {user_input[:5000]}"
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.4, max_tokens=3000)
            full_report += "\n\n" + res.choices[0].message.content
            bar.progress((i + 1) / len(sections))
            
        pdf_out = create_pdf(full_report, ord_no, tarih)
        st.success("✅ Rapor Hazırlandı!")
        
        if send_email(pdf_out, e_mail, ord_no):
            st.success(f"📧 Raporunuz {e_mail} adresine PDF olarak başarıyla gönderildi!")
        else:
            st.error("❌ Mail gönderiminde hata oluştu. Lütfen PDF'i manuel indirin.")
        
        st.download_button("📂 PDF Olarak İndir", pdf_out, file_name=f"VIP_Rapor_{ord_no}.pdf")
    else:
        st.error("Lütfen tüm alanları (Yorum, Sipariş No, Mail ve Onay) doldurun.")

st.caption("© 2026 AI Analiz SaaS | Global Professional Edition")
