import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import smtplib
from email.message import EmailMessage

# =========================
# FONT AYARI (UNICODE) - PDF için
# =========================
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))  # Font dosyasını projeye koy

# =========================
# SAYFA AYARLARI
# =========================
st.set_page_config(page_title="AI Pro Analiz & Strateji", page_icon="📈", layout="centered")

# =========================
# API BAĞLANTISI
# =========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ API Hatası! Lütfen Secrets ayarlarınızı kontrol edin.")
    st.stop()

# =========================
# TEMİZLEME FONKSİYONLARI
# =========================
BANNED_WORDS = ["falan","felan","şey","yani","bi","herhalde","možnosti","口碑","zkušen","tăngellemek"]
BANNED_REGEX = re.compile(r"[šăěščřž]|[\u4e00-\u9fff]|[\u0400-\u04FF]", re.UNICODE)

def output_is_clean(text: str) -> bool:
    lower = text.lower()
    return not (any(w in lower for w in BANNED_WORDS) or BANNED_REGEX.search(text))

def sanitize_for_pdf(text: str) -> str:
    text = text.replace("\u200b","")  # zero-width space
    text = re.sub(r"[^\x00-\x7FğüşöçıİĞÜŞÖÇ\n]", "", text)  # Türkçe + Latin karakter
    text = re.sub(r"\s+", " ", text)  # Fazla boşluk
    return text.strip()

# =========================
# PDF OLUŞTURMA
# =========================
def create_pdf(report_text, order_no, tarih):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("DejaVu", 18)
    c.drawCentredString(width/2, height-50, "📄 VIP STRATEJI & TEKNIK RAPOR")
    c.setFont("DejaVu", 10)
    c.drawString(50, height-80, f"Sipariş No: {order_no} | Tarih: {tarih}")
    y = height - 120
    max_width = width - 100
    for line in report_text.split("\n"):
        wrapped = simpleSplit(line, "DejaVu", 10, max_width)
        for wline in wrapped:
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("DejaVu", 10)
            c.drawString(50, y, wline.strip())
            y -= 14
    c.save()
    buffer.seek(0)
    return buffer

# =========================
# E-POSTA GÖNDERME
# =========================
def send_email(pdf_buffer, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"💎 VIP Raporunuz - Sipariş No: {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content("Merhaba,\n\nTalep ettiğiniz 10.000 kelimelik VIP raporunuz ekte PDF olarak sunulmuştur.\n\nBaşarılar dileriz.")
    pdf_buffer.seek(0)
    msg.add_attachment(pdf_buffer.read(), maintype='application', subtype='pdf', filename=f"VIP_Rapor_{order_no}.pdf")
    try:
        with smtplib.SMTP_SSL(st.secrets["SMTP_SERVER"], st.secrets["SMTP_PORT"]) as server:
            server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASS"])
            server.send_message(msg)
        return True
    except:
        return False

# =========================
# BÖLÜM ÜRETİCİ (VIP / ÜCRETSİZ)
# =========================
def generate_section(title, task, data, order_no, tarih):
    prompt = f"%100 Saf Türkiye Türkçesi. Teknik üslup. {title} için {task}. Veriler: {data}"
    for _ in range(2):
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"user","content":prompt}],
                temperature=0.4,
                max_tokens=3000
            )
            content = sanitize_for_pdf(res.choices[0].message.content)
            if output_is_clean(content):
                return content
        except:
            time.sleep(2)
    return f"--- {title} ---\n[Sistem yoğunluğu nedeniyle özet geçildi.]"

# =========================
# YAN MENÜ
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ Yasal Zırh & Bilgi")
    st.error("⚠️ Yapay zeka çıktıları yatırım tavsiyesi değildir.")
    st.info("💎 VIP Rapor: 10.000 Kelimelik Teknik Analiz, 12 Aylık Yol Haritası, Mühendislik & Ar-Ge")

# =========================
# ANA EKRAN
# =========================
st.title("📈 Profesyonel AI Strateji Motoru")
st.markdown("#### Müşteri Verilerinden 10.000 Kelimelik VIP Rapor Oluşturun")

user_input = st.text_area("Verileri buraya girin:", height=200, placeholder="Yorum veya iş verilerini ekleyin...")

col1, col2 = st.columns(2)

# --- ÜCRETSİZ ANALİZ ---
with col1:
    if st.button("🔍 Ücretsiz Hızlı Analiz"):
        if user_input:
            with st.spinner("Analiz ediliyor..."):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":f"Verileri özetle ve 0-100 arası skorla: {user_input[:2000]}"}],
                    temperature=0.3
                )
                st.success("📊 Ücretsiz Analiz")
                st.code(sanitize_for_pdf(res.choices[0].message.content))
        else:
            st.warning("Analiz için veri girin.")

# --- VIP SATIN AL LINK ---
with col2:
    st.link_button("💎 VIP: 10.000 Kelimelik Rapor Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
st.subheader("🔑 VIP Rapor Üretim Paneli")

order_no = st.text_input("Shopier Sipariş No:")
email_input = st.text_input("Raporun Gönderileceği E-posta:")
confirm = st.checkbox("10.000 kelimelik raporun iadesiz olduğunu ve teknik analiz niteliğinde olduğunu onaylıyorum.")

# --- VIP RAPOR BUTONU ---
if st.button("🚀 VIP Raporu Üret & PDF Gönder"):
    if not user_input or not order_no or not confirm or not email_input:
        st.error("Tüm alanları doldurun.")
    elif not order_no.isdigit() or len(order_no) < 8:
        st.error("Geçersiz sipariş numarası formatı.")
    else:
        st.warning("⚙️ Rapor hazırlanıyor. Lütfen bekleyin...")
        tarih = datetime.now().strftime("%d/%m/%Y")
        report = ""
        sections = [
            ("1. ÜRETİM & MÜHENDİSLİK", "Kusurlar ve çözüm önerileri üzerine 2000 kelime."),
            ("2. STRATEJİK FİYATLANDIRMA", "Pazar ve değer analizi üzerine 2000 kelime."),
            ("3. SEKTÖREL GELECEK", "Gelecek trendleri üzerine 2000 kelime."),
            ("4. AR-GE & TASARIM", "İnovasyon ve ambalaj önerileri üzerine 2000 kelime."),
            ("5. 12 AYLIK YOL HARİTASI", "ROI ve KPI odaklı 2000 kelime uygulama planı.")
        ]

        progress = st.progress(0)
        for i, (t, task) in enumerate(sections):
            report += "\n\n" + generate_section(t, task, user_input[:5000], order_no, tarih)
            progress.progress((i+1)/len(sections))

        st.success("✅ VIP Rapor Hazır!")

        pdf_buf = create_pdf(report, order_no, tarih)

        # Mail Gönder
        if send_email(pdf_buf, email_input, order_no):
            st.success(f"📧 Rapor {email_input} adresine gönderildi!")
        else:
            st.error("❌ Mail gönderilemedi. PDF'i aşağıdan indir.")

        st.download_button("📂 PDF İndir", pdf_buf, file_name=f"VIP_Rapor_{order_no}.pdf")

st.caption("© 2026 AI Analiz SaaS | Professional Edition")
