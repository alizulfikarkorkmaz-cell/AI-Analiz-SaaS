import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit # Uzun satırları bölmek için
import io
import smtplib
from email.message import EmailMessage

# API BAĞLANTISI
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Hatası! Secrets ayarlarını kontrol edin.")
    st.stop()

# DİL VE GÜVENLİK
BANNED_WORDS = ["falan", "felan", "şey", "yani", "bi", "herhalde", "možnosti", "口碑", "zkušen", "tăngellemek"]
BANNED_REGEX = re.compile(r"[šăěščřž]|[\u4e00-\u9fff]|[\u0400-\u04FF]", re.UNICODE)

def output_is_clean(text: str) -> bool:
    lower = text.lower()
    return not (any(w in lower for w in BANNED_WORDS) or BANNED_REGEX.search(text))

def sanitize_input(text: str) -> str:
    for b in ["system:", "role:", "assistant:", "developer:"]:
        text = text.replace(b, "")
    return text.strip()

# PDF OLUŞTURUCU (Geliştirilmiş - Sayfa Taşmasını Engeller)
def create_pdf(report_text, order_no, tarih):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Başlık
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "VIP STRATEJI VE ANALIZ RAPORU")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height-80, f"Siparis No: {order_no} | Tarih: {tarih}")
    
    # Metin Alanı Ayarları
    y = height - 120
    c.setFont("Helvetica", 10)
    max_width = width - 100 # Sağ ve soldan 50 birim boşluk
    
    for line in report_text.split("\n"):
        # Uzun satırları otomatik böl
        wrapped_lines = simpleSplit(line, "Helvetica", 10, max_width)
        for wrapped_line in wrapped_lines:
            if y < 50: # Sayfa sonu kontrolü
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, wrapped_line)
            y -= 14
            
    c.save()
    buffer.seek(0)
    return buffer

# E-POSTA GÖNDER (Buffer Sıfırlama Eklendi)
def send_email(pdf_buffer, to_email, order_no):
    msg = EmailMessage()
    msg['Subject'] = f"VIP Analiz Raporunuz - Sipariş {order_no}"
    msg['From'] = st.secrets["SMTP_USER"]
    msg['To'] = to_email
    msg.set_content("Değerli İş Ortağımız,\n\nTalep ettiğiniz 10.000 kelimelik VIP strateji raporu ekte sunulmuştur.")

    pdf_buffer.seek(0) # OKUMA ÖNCESİ SIFIRLAMA ŞART
    msg.add_attachment(pdf_buffer.read(), maintype='application', subtype='pdf', filename=f"VIP_Rapor_{order_no}.pdf")
    
    try:
        with smtplib.SMTP_SSL(st.secrets["SMTP_SERVER"], st.secrets["SMTP_PORT"]) as server:
            server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASS"])
            server.send_message(msg)
        return True
    except:
        return False

# BÖLÜM ÜRETİCİ
def generate_section(title, task, data, order_no, tarih):
    prompt = f"Turkiye Turkcesi kullan. Teknik yaz. {title} icin {task}. Veri: {data}"
    for _ in range(2):
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4, max_tokens=3000
            )
            content = res.choices[0].message.content
            if output_is_clean(content): return content
        except: time.sleep(3)
    return f"\n\n--- {title} ---\n[Sistem yoğunluğu nedeniyle özet geçildi.]"

# ARAYÜZ
st.set_page_config(page_title="AI Pro Analiz", layout="centered")
st.title("📈 Profesyonel AI Strateji Motoru")

user_input = st.text_area("Yorumları girin:", height=200)
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Ücretsiz Analiz"):
        if user_input:
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":f"Ozetle: {user_input}"}])
            st.info(res.choices[0].message.content)

with col2:
    st.link_button("💎 VIP Rapor Al", "https://www.shopier.com/SAYFA_LINKIN")

st.write("---")
o_no = st.text_input("Sipariş No:")
e_mail = st.text_input("E-posta:")
accept = st.checkbox("Onaylıyorum")

if st.button("🚀 VIP Raporu İnşa Et"):
    if user_input and o_no and e_mail and accept:
        st.info("Rapor parçalar halinde üretiliyor...")
        tarih = datetime.now().strftime("%d/%m/%Y")
        sections = [
            ("1. MUHENDISLIK", "Teknik hatalar üzerine 2000 kelime."),
            ("2. STRATEJI", "Fiyatlandırma üzerine 2000 kelime."),
            ("3. GELECEK", "Trendler üzerine 2000 kelime."),
            ("4. TASARIM", "Inovasyon üzerine 2000 kelime."),
            ("5. PLAN", "ROI üzerine 2000 kelime.")
        ]
        
        full_report = ""
        prog = st.progress(0)
        for i, (t, task) in enumerate(sections):
            full_report += generate_section(t, task, user_input[:4000], o_no, tarih)
            prog.progress((i+1)/len(sections))
            
        pdf = create_pdf(full_report, o_no, tarih)
        st.success("Rapor Tamamlandı!")
        st.download_button("📂 PDF İndir", pdf, file_name=f"VIP_{o_no}.pdf")
        
        if send_email(pdf, e_mail, o_no):
            st.success("📧 E-posta gönderildi!")
    else:
        st.warning("Eksik alanları doldurun.")


