import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time
import io
import smtplib
import logging
from email.message import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

# =================================================================
# 1. KURUMSAL YAPILANDIRMA VE LOGLAMA
# =================================================================
logging.basicConfig(level=logging.INFO)
st.set_page_config(
    page_title="VIP AI STRATEGY PRO | SUPREME EDITION",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================================================
# 2. KARAKTER KORUMA VE METİN MOTORU
# =================================================================
class TextProcessor:
    @staticmethod
    def fix_turkish_chars(text):
        """PDF'deki kara kutucuk sorununu kökten çözer."""
        mapping = {
            'İ': 'I', 'ı': 'i', 'Ş': 'S', 'ş': 's', 'Ğ': 'G', 'ğ': 'g',
            'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
        }
        for k, v in mapping.items():
            text = text.replace(k, v)
        return text

    @staticmethod
    def sanitize_input(text):
        return re.sub(r"[^a-zA-Z0-9çğıöşüÇĞİÖŞÜ.,;:!?()/%&\-\n ]", "", text).strip()

# =================================================================
# 3. PROFESYONEL PDF MİMARİSİ (ARCHITECT)
# =================================================================
class VIPReportArchitect:
    def __init__(self, order_no):
        self.order_no = order_no
        self.tarih = datetime.now().strftime("%d/%m/%Y")
        self.buffer = io.BytesIO()

    def _header_footer_design(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.dodgerblue)
        canvas.drawString(inch, A4[1] - 0.5 * inch, "VIP AI STRATEGY ENGINE - CONFIDENTIAL")
        canvas.drawRightString(A4[0] - inch, A4[1] - 0.5 * inch, f"Order: {self.order_no} | Page {doc.page}")
        canvas.setStrokeColor(colors.dodgerblue)
        canvas.line(inch, A4[1] - 0.6 * inch, A4[0] - inch, A4[1] - 0.6 * inch)
        canvas.restoreState()

    def create(self, content_map):
        doc = SimpleDocTemplate(self.buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=80, bottomMargin=72)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='VIPTitle', fontSize=22, textColor=colors.dodgerblue, spaceAfter=30, alignment=1))
        styles.add(ParagraphStyle(name='ModuleTitle', fontSize=16, textColor=colors.darkblue, spaceBefore=20, spaceAfter=10))
        
        story = []
        # Kapak
        story.append(Spacer(1, 3 * inch))
        story.append(Paragraph("VIP STRATEJIK ANALIZ RAPORU", styles['VIPTitle']))
        story.append(Paragraph(f"Siparis No: {self.order_no}", styles['Normal']))
        story.append(Paragraph(f"Tarih: {self.tarih}", styles['Normal']))
        story.append(PageBreak())
        
        # İçerik Modülleri
        for title, body in content_map.items():
            story.append(Paragraph(TextProcessor.fix_turkish_chars(title), styles['ModuleTitle']))
            clean_body = TextProcessor.fix_turkish_chars(body)
            for p in clean_body.split('\n'):
                if p.strip():
                    story.append(Paragraph(p, styles['Normal']))
                    story.append(Spacer(1, 0.1 * inch))
            story.append(PageBreak())
        
        doc.build(story, onFirstPage=self._header_footer_design, onLaterPages=self._header_footer_design)
        self.buffer.seek(0)
        return self.buffer

# =================================================================
# 4. HATA TOLERANSLI VIP AI MOTORU (RATE LIMIT FIXER)
# =================================================================
def generate_supreme_content_v2(user_data, order_no):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        st.error("❌ API Anahtarı Bulunamadı!")
        return None

    modules = {
        "1. MAKRO MÜHENDİSLİK ANALİZİ": "Teknik altyapı ve operasyonel verimlilik.",
        "2. PREMİUM PAZAR KONUMLAMA": "Lüks algısı ve stratejik fiyatlandırma.",
        "3. RAKİP ANALİZİ VE DOMİNASYON": "Pazar liderliği için saldırı planı.",
        "4. 12 AYLIK ROI VE BÜYÜME": "Karlılık haritası ve yatırım dönüşü.",
        "5. GELECEK TRENDLERİ VE AR-GE": "5 yıllık inovasyon projeksiyonu."
    }

    final_results = {}
    progress_bar = st.progress(0)
    
    for i, (title, prompt) in enumerate(modules.items()):
        status_msg = st.empty()
        status_msg.info(f"🌀 {title} üretiliyor... (API Limit Kontrolü Aktif)")
        
        success = False
        retry_count = 3
        
        while not success and retry_count > 0:
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Sen dünyanın en iyi strateji danışmanısın. Akademik Türkçe kullan ve her modülü 2000 kelime civarı detaylandır."},
                        {"role": "user", "content": f"Sipariş ID: {order_no}\nKonu: {title}\nDetay: {prompt}\nVeri: {user_data[:3500]}"}
                    ],
                    temperature=0.4
                )
                final_results[title] = response.choices[0].message.content
                success = True
                status_msg.empty()
                time.sleep(12) # Rate limit koruması için zorunlu mola
            except Exception as e:
                if "rate_limit" in str(e).lower():
                    status_msg.warning(f"⚠️ Limit Doldu! 25 saniye bekleniyor... (Kalan Hak: {retry_count})")
                    time.sleep(25)
                    retry_count -= 1
                else:
                    st.error(f"Kritik Hata: {str(e)}")
                    break
        
        if not success:
            final_results[title] = "Bu bölüm API yoğunluğu nedeniyle atlandı."
        
        progress_bar.progress((i + 1) / len(modules))
        
    return final_results

# =================================================================
# 5. SIDEBAR - YASAL ZIRH VE VIP GÖRSELLER
# =================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=150)
    st.title("🛡️ Yasal Zırh & Bilgi")
    st.divider()
    st.error("**⛔ YASAL UYARI:** Bu rapor yapay zeka çıktısıdır, yatırım tavsiyesi değildir.")
    st.info("**💎 VIP ÖZELLİKLERİ:**\n- 10.000+ Kelime Analizi\n- ROI Takvimi\n- Teknik Mühendislik\n- E-Posta Desteği")
    st.divider()
    st.caption("v10.0 Supreme Edition | 2026")

# =================================================================
# 6. ANA KONTROL PANELİ
# =================================================================
st.title("👑 Professional AI Strategy Engine")
st.markdown("#### Müşteri Verilerini 10.000 Kelimelik VIP İş Planlarına Dönüştürün")

user_input = st.text_area("Analiz edilecek ham verileri buraya girin:", height=250)

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Ücretsiz Analiz", use_container_width=True):
        st.info("Hızlı analiz yapılıyor...") # Hızlı özet fonksiyonu buraya gelebilir.

with col2:
    st.link_button("💎 VIP: Dev Rapor Satın Al", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True, type="primary")

st.divider()
st.subheader("🔑 VIP Rapor Talep Paneli")

v1, v2 = st.columns(2)
with v1:
    oid = st.text_input("Sipariş No:", placeholder="Örn: 12345678")
with v2:
    mail = st.text_input("Raporun Gideceği E-Posta:")

accept = st.checkbox("Dijital ürünlerde iade olmadığını ve teknik analizi onaylıyorum.")

if st.button("🚀 VIP STRATEJİK ANALİZİ BAŞLAT", use_container_width=True, type="primary"):
    if not user_input or not oid or not accept:
        st.error("Lütfen tüm alanları ve onay kutusunu doldurun!")
    else:
        with st.status("🚀 VIP İşlem Başlatıldı...", expanded=True) as status:
            # 1. İçerik Üretimi
            report_data = generate_supreme_content_v2(user_input, oid)
            
            if report_data:
                # 2. PDF Mimarisi
                status.update(label="📄 PDF Hazırlanıyor...", state="running")
                arch = VIPReportArchitect(oid)
                pdf_output = arch.create(report_data)
                
                status.update(label="✅ Tamamlandı!", state="complete")
                st.success("Analiz Başarıyla Tamamlandı ve PDF Oluşturuldu!")
                
                st.download_button(
                    label="📂 VIP STRATEJİ RAPORUNU İNDİR",
                    data=pdf_output,
                    file_name=f"VIP_Strategy_{oid}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
