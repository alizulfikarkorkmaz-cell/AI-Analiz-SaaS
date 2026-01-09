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
    st.error("⚠️ API Hatası! Secrets ayarlarınızı kontrol edin.")
    st.stop()

# =========================
# GÜVENLİK VE KARAKTER FİLTRESİ
# =========================
BANNED_WORDS = ["falan", "felan", "şey", "yani", "bi", "herhalde",
                "možnosti", "口碑", "zkušen", "tăngellemek"]
BANNED_REGEX = re.compile(r"[šăěščřž]|[\u4e00-\u9fff]|[\u0400-\u04FF]", re.UNICODE)

def output_is_clean(text: str) -> bool:
    lower = text.lower()
    return not (any(w in lower for w in BANNED_WORDS) or BANNED_REGEX.search(text))

def sanitize_input(text: str) -> str:
    for b in ["system:", "role:", "assistant:", "developer:"]:
        text = text.replace(b, "")
    return text.strip()

# =========================
# PDF OLUŞTURMA MOTORU
# =========================
def create_pdf(report_text, order_no, tarih):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Başlık
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "📄 VIP STRATEJI VE TEKNIK RAPORU")
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
# E-POSTA GÖNDERİM MOTORU
# =========================
def send_email(pdf_buffer, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"💎 VIP Strateji Raporunuz - No: {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content("Merhaba,\n\nTalep ettiğiniz 10.000 kelimelik VIP Strateji ve İş Planı Raporunuz ekte PDF olarak sunulmuştur.\n\nBol kazançlar dileriz.")
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
# BÖLÜM ÜRETİCİ
# =========================
def generate_section(title, task, data, order_no, tarih):
    prompt = f"%100 Türkiye Türkçesi. Akademik ve teknik üslup zorunludur.\nBölüm: {title}\nGörev: {task}\nVeri: {data[:4000]}\nSipariş No: {order_no} | Tarih: {tarih}"
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
    return f"\n\n--- {title} ---\n[Sistem yoğunluğu nedeniyle bu bölüm özet geçildi.]"

# =========================
# YAN MENÜ
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ Yasal Zırh & Bilgi")
    st.error("⚠️ **SORUMLULUK REDDİ:** Yapay zeka çıktıları yatırım tavsiyesi değildir.")
    st.info("💎 VIP Rapor Özellikleri:\n* 10.000 Kelimelik Teknik Analiz\n* 12 Aylık ROI Planı\n* Mühendislik & Ar-Ge Desteği")
    st.caption("📩 Destek için Sipariş No ile iletişime geçin.")

# =========================
# ANA EKRAN
# =========================
st.title("📈 Profesyonel AI Strateji Motoru")
st.markdown("#### Müşteri Geri Bildirimlerinden 10.000 Kelimelik Dev İş Planları")

user_input = st.text_area("Analiz edilecek yorum veya verileri girin:", height=200)

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Ücretsiz Hızlı Analiz"):
        if user_input:
            with st.spinner("Özetleniyor..."):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Şu veriyi profesyonelce özetle ve 0-100 arası skor ver: {user_input[:2000]}"}],
                    temperature=0.3
                )
                st.success("📊 Hızlı Analiz Sonucu")
                st.write(res.choices[0].message.content)
        else:
            st.warning("Lütfen veri girin.")

with col2:
    st.link_button("💎 VIP: 10.000 Kelimelik Rapor Al (50 TL)", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
st.subheader("🔑 VIP Rapor Paneli")
st.markdown("> VIP rapor 5 bölümden oluşur ve yaklaşık 1-2 dakika sürer.")

order_no = st.text_input("Shopier Sipariş No:")
email_input = st.text_input("Raporun gönderileceği E-posta:")
accept = st.checkbox("10.000 kelimelik raporun iadesiz olduğunu ve teknik analiz niteliğinde olduğunu onaylıyorum.")

if st.button("🚀 VIP Raporu İnşa Et ve Gönder"):
    if not user_input or not order_no or not email_input or not accept:
        st.error("Lütfen tüm alanları doldurun.")
    elif not order_no.isdigit() or len(order_no) < 8:
        st.error("Geçersiz sipariş numarası formatı.")
    else:
        st.warning("⚙️ Dev rapor hazırlanıyor. Tarayıcıyı kapatmayın...")
        tarih = datetime.now().strftime("%d/%m/%Y")

        report = ""
        sections = [
            ("1. MÜHENDİSLİK VE TEKNİK ANALİZ", "İşletme kusurları ve teknik çözüm önerileri üzerine 2000 kelime."),
            ("2. STRATEJİK FİYATLANDIRMA VE KONUMLAMA", "Premium algı ve pazar rekabeti üzerine 2000 kelime."),
            ("3. SEKTÖREL GELECEK VE TRENDLER", "Gelecek 5 yılın pazar öngörüleri üzerine 2000 kelime."),
            ("4. AR-GE, İNOVASYON VE AMBALAJ", "Teknik inovasyon ve tasarım önerileri üzerine 2000 kelime."),
            ("5. 12 AYLIK STRATEJİK YOL HARİTASI", "ROI odaklı uygulama ve büyüme planı üzerine 2000 kelime.")
        ]

        progress = st.progress(0)
        for i, (sec_title, sec_task) in enumerate(sections):
            section_text = generate_section(sec_title, sec_task, user_input, order_no, tarih)
            report += f"\n\n{section_text}"
            progress.progress((i + 1) / len(sections))

        st.success("✅ 10.000 Kelimelik VIP Rapor Hazır!")
        pdf_buf = create_pdf(report, order_no, tarih)

        # Mail Gönder
        if send_email(pdf_buf, email_input, order_no):
            st.success(f"📧 Raporunuz başarıyla {email_input} adresine gönderildi!")
        else:
            st.error("❌ Mail gönderilemedi. PDF'i aşağıdan indirebilirsiniz.")

        st.download_button("📂 PDF Raporu İndir", pdf_buf, file_name=f"VIP_Rapor_{order_no}.pdf")

st.caption("© 2026 AI Analiz SaaS | Professional Edition")
