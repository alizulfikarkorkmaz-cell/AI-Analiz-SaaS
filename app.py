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
st.set_page_config(page_title="AI Pro Analiz & Strateji", page_icon="📈", layout="centered")

# =========================
# API BAĞLANTISI
# =========================
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ API Hatası! Secrets ayarlarınızı kontrol edin.")
    st.stop()

# =========================
# FİLTRELER VE TEMİZLEME
# =========================
BANNED_WORDS = ["falan", "felan", "şey", "yani", "bi", "herhalde",
                "možnosti", "口碑", "zkušen", "tăngellemek"]
BANNED_REGEX = re.compile(r"[šăěščřž]|[\u4e00-\u9fff]|[\u0400-\u04FF]", re.UNICODE)

def sanitize_input(text: str) -> str:
    for b in ["system:", "role:", "assistant:", "developer:"]:
        text = text.replace(b, "")
    return text.strip()

def output_is_clean(text: str) -> bool:
    text = text.lower()
    if any(w in text for w in BANNED_WORDS):
        return False
    if BANNED_REGEX.search(text):
        return False
    return True

# =========================
# PDF OLUŞTURMA
# =========================
def create_pdf(report_text, order_no, tarih):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "📄 VIP STRATEJI VE TEKNIK RAPOR")
    c.setFont("Helvetica", 10)
    c.drawString(50, height-80, f"Sipariş No: {order_no} | Tarih: {tarih}")
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
# MAIL GÖNDERME
# =========================
def send_email(pdf_buffer, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"💎 VIP Raporunuz - Sipariş No: {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content(f"Merhaba,\n\nTalep ettiğiniz VIP rapor ekte PDF olarak sunulmuştur.\n\nBaşarılar dileriz.")
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
# BÖLÜM ÜRETİCİ
# =========================
def generate_section(title, task, data, order_no, tarih):
    prompt = f"""
    %100 Saf Türkiye Türkçesi. Akademik ve teknik üslup zorunludur.
    Asla kısa kesme ve yasaklı kelime kullanma.
    BÖLÜM: {title}
    GÖREV: {task}
    VERİLER: {data}
    """
    for _ in range(3):
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=3000
            )
            content = res.choices[0].message.content
            if output_is_clean(content):
                return content
        except:
            time.sleep(2)
    return f"{title}\n\n[Sistem yoğunluğu nedeniyle özet geçildi.]"

# =========================
# YAN MENÜ
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ Yasal Zırh & Bilgi")
    st.error("⚠️ Yapay zeka çıktıları yatırım tavsiyesi değildir.")
    st.write("---")
    st.info("💎 VIP Rapor Özellikleri:\n* 10.000 Kelime\n* 12 Aylık Yol Haritası\n* Mühendislik & Ar-Ge")
    st.caption("📩 Destek için sipariş numaranız ile mail atın.")

# =========================
# ANA EKRAN
# =========================
st.title("📈 Profesyonel AI Strateji Motoru")
st.markdown("#### Müşteri Geri Bildirimlerinden Dev İş Planları")

user_input = st.text_area("Analiz edilecek yorum/veri:", height=200)

col1, col2 = st.columns(2)

# --- Ücretsiz Hızlı Analiz ---
with col1:
    if st.button("🔍 Ücretsiz Hızlı Analiz"):
        if user_input:
            with st.spinner('Analiz ediliyor...'):
                free_prompt = f"""
                Lütfen 0-100 arası puan ver ve özetle, duygu analizi yap:
                Veri: {user_input[:2000]}
                """
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":free_prompt}],
                    temperature=0.3,
                    max_tokens=1500
                )
                output_text = res.choices[0].message.content
                if not output_is_clean(output_text):
                    st.error("⚠️ Çıktı karakter standardına uymuyor, tekrar deneyin.")
                else:
                    st.success("📊 Ücretsiz Analiz")
                    st.write(output_text)
        else:
            st.warning("Lütfen veri girin.")

# --- VIP Satın Alma Linki ---
with col2:
    st.link_button("💎 VIP Rapor Satın Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
st.subheader("🔑 VIP Rapor Paneli")
order_no = st.text_input("Shopier Sipariş No:")
email_input = st.text_input("Raporun Gönderileceği E-posta:")
accept = st.checkbox("10.000 kelimelik VIP raporun iadesiz olduğunu ve teknik analiz niteliğinde olduğunu onaylıyorum.")

if st.button("🚀 VIP Raporu İnşa Et ve Mail Gönder"):
    if not user_input or not order_no or not email_input or not accept:
        st.error("Eksik alanlar!")
    elif not order_no.isdigit() or len(order_no) < 8:
        st.error("Geçersiz sipariş numarası.")
    else:
        st.warning("⚙️ Rapor hazırlanıyor. Tarayıcıyı kapatmayın, işlem 2-3 dakika sürebilir...")
        tarih = datetime.now().strftime("%d/%m/%Y")
        report = ""
        sections = [
            ("1. Üretim ve Mühendislik Analizi", "Teknik kusurlar ve çözüm önerileri üzerine 2000 kelime"),
            ("2. Stratejik Fiyatlandırma", "Pazar konumu ve premium algı üzerine 2000 kelime"),
            ("3. Sektörel Gelecek ve Trendler", "Gelecek 5 yıl pazar projeksiyonu üzerine 2000 kelime"),
            ("4. Ar-Ge ve Tasarım İnovasyonu", "İnovasyon ve ambalaj çözümleri üzerine 2000 kelime"),
            ("5. 12 Aylık Stratejik Yol Haritası", "ROI ve KPI odaklı 2000 kelime")
        ]
        prog = st.progress(0)
        for i, (t, task) in enumerate(sections):
            sec_text = generate_section(t, task, user_input[:5000], order_no, tarih)
            report += f"\n\n{sec_text}"
            prog.progress((i+1)/len(sections))
        st.success("✅ VIP Rapor Hazır!")
        
        # PDF oluştur
        pdf_buf = create_pdf(report, order_no, tarih)
        
        # Mail gönder
        if send_email(pdf_buf, email_input, order_no):
            st.success(f"📧 Rapor {email_input} adresine gönderildi!")
        else:
            st.error("❌ Mail gönderilemedi, lütfen PDF'i indiriniz.")
        
        st.download_button("📂 PDF Olarak İndir", pdf_buf, file_name=f"VIP_Rapor_{order_no}.pdf")
