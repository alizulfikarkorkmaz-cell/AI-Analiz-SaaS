import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time

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
    st.error("⚠️ API Hatası! Lütfen Secrets ayarlarınızı kontrol edin.")
    st.stop()

# =========================
# TEMİZLEME & GÜVENLİK FONKSİYONU
# =========================
BANNED_WORDS = ["falan", "felan", "şey", "yani", "bi", "herhalde", "tăngellemek", "zkušen"]
BANNED_REGEX = re.compile(r"[šăěščřž]|[\u4e00-\u9fff]|[\u0400-\u04FF]", re.UNICODE)

def sanitize_input(text: str) -> str:
    text = BANNED_REGEX.sub("", text)                  # Bozuk karakterleri temizle
    for w in BANNED_WORDS: text = text.replace(w, "")  # Yasaklı kelimeleri temizle
    text = re.sub(r'\s+', ' ', text).strip()          # Fazla boşluk ve satır başlarını temizle
    return text

# =========================
# PDF OLUŞTUR
# =========================
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io

def create_pdf(report_text, order_no, tarih):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "📄 VIP STRATEJI VE TEKNIK RAPOR")
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

# =========================
# E-POSTA GÖNDER
# =========================
import smtplib
from email.message import EmailMessage

def send_email(pdf_buffer, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"💎 VIP Strateji Raporunuz - No: {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content("Merhaba,\n\nTalep ettiğiniz VIP Strateji ve İş Planı Raporunuz ekte PDF olarak sunulmuştur.")
    pdf_buffer.seek(0)
    msg.add_attachment(pdf_buffer.read(), maintype='application', subtype='pdf', filename=f"VIP_RAPOR_{order_no}.pdf")
    try:
        with smtplib.SMTP_SSL(st.secrets["SMTP_SERVER"], st.secrets["SMTP_PORT"]) as server:
            server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASS"])
            server.send_message(msg)
        return True
    except: 
        return False

# =========================
# YAN MENÜ
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ Yasal Zırh")
    st.error("⚠️ Yapay zeka çıktıları yatırım tavsiyesi değildir.")
    st.info("💎 VIP Rapor Özellikleri:\n* 10.000 Kelimelik Teknik Analiz\n* 12 Aylık ROI Planı\n* Mühendislik & Ar-Ge Desteği")
    st.caption("📩 Destek için Sipariş No ile iletişime geçin.")

# =========================
# ANA EKRAN
# =========================
st.title("📈 Profesyonel AI Strateji Motoru")
st.markdown("##### Müşteri Geri Bildirimlerinden 10.000 Kelimelik Dev İş Planları")

user_input = st.text_area("Analiz edilecek yorum veya verileri girin:", height=200)

col1, col2 = st.columns(2)

# --- ÜCRETSİZ HIZLI ANALİZ ---
with col1:
    if st.button("🔍 Ücretsiz Hızlı Analiz"):
        if user_input:
            temiz_veri = sanitize_input(user_input[:2000])
            with st.spinner('Özetleniyor...'):
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Profesyonelce özetle ve 0-100 arası skor ver: {temiz_veri}"}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.3
                )
                st.success("📊 Hızlı Analiz Sonucu")
                st.write(res.choices[0].message.content)
        else:
            st.warning("Veri girilmedi.")

# --- VIP RAPOR LINKİ ---
with col2:
    st.link_button("💎 VIP: Dev Rapor Satın Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
st.subheader("🔑 VIP Rapor Paneli")
order_no = st.text_input("Shopier Sipariş No:")
email_input = st.text_input("Raporun Gönderileceği E-posta Adresi:")
confirm = st.checkbox("10.000 kelimelik raporun iadesiz olduğunu ve teknik analiz niteliğinde olduğunu onaylıyorum.")

# --- VIP ÜRETİM ---
if st.button("🚀 VIP Raporu Üret ve Mail Gönder"):
    if not user_input or not order_no or not email_input or not confirm:
        st.error("Lütfen tüm alanları doldurun.")
    elif not order_no.isdigit() or len(order_no) < 8:
        st.error("Geçersiz sipariş numarası formatı.")
    else:
        temiz_veri = sanitize_input(user_input[:5000])
        st.warning("⚙️ Dev rapor hazırlanıyor, lütfen bekleyin...")
        tarih = datetime.now().strftime("%d/%m/%Y")
        
        sections = [
            ("1. MÜHENDİSLİK VE TEKNİK ANALİZ", "İşletme kusurları ve teknik çözüm önerileri üzerine 2000 kelime."),
            ("2. STRATEJİK FİYATLANDIRMA VE KONUMLAMA", "Premium algı ve pazar rekabeti üzerine 2000 kelime."),
            ("3. SEKTÖREL GELECEK VE TRENDLER", "Gelecek 5 yılın pazar öngörüleri üzerine 2000 kelime."),
            ("4. AR-GE, İNOVASYON VE AMBALAJ", "Teknik inovasyon ve tasarım önerileri üzerine 2000 kelime."),
            ("5. 12 AYLIK STRATEJİK YOL HARİTASI", "ROI odaklı uygulama ve büyüme planı üzerine 2000 kelime.")
        ]
        
        full_report = ""
        progress = st.progress(0)
        for i, (title, task) in enumerate(sections):
            prompt = f"%100 Türkiye Türkçesi, teknik üslup. {title} için {task} Veriler: {temiz_veri}"
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=3000
            )
            full_report += f"\n\n{res.choices[0].message.content}"
            progress.progress((i+1)/len(sections))
        
        st.success("✅ VIP Rapor Hazır!")
        
        pdf_buf = create_pdf(full_report, order_no, tarih)
        
        if send_email(pdf_buf, email_input, order_no):
            st.success(f"📧 Raporunuz başarıyla {email_input} adresine gönderildi!")
        else:
            st.error("❌ E-posta gönderilemedi. PDF'i aşağıdan manuel indirin.")
        
        st.download_button("📂 PDF Raporu İndir", pdf_buf, file_name=f"VIP_Rapor_{order_no}.pdf")

st.caption("© 2026 AI Analiz SaaS | Professional Edition")
