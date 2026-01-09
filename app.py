import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time
import io
import smtplib
import json
import logging
from email.message import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

# =================================================================
# 1. KURUMSAL LOGLAMA VE YAPILANDIRMA
# =================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI STRATEGY PRO | SUPREME",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================================================
# 2. KARAKTER KORUMA VE GÜVENLİK PROTOKOLÜ
# =================================================================
class TextEngine:
    @staticmethod
    def force_tr_compatibility(text):
        """PDF'deki 'kara kutucuk' (glyph) hatasını imha eder."""
        chars = {
            'İ': 'I', 'ı': 'i', 'Ş': 'S', 'ş': 's', 'Ğ': 'G', 'ğ': 'g',
            'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C',
            'â': 'a', 'î': 'i', 'û': 'u'
        }
        for k, v in chars.items():
            text = text.replace(k, v)
        return text

    @staticmethod
    def sanitize(text):
        """Veriyi zararlı karakterlerden arındırır."""
        return re.sub(r"[^a-zA-Z0-9.,;:!?()/%&\-\n ]", "", text)

# =================================================================
# 3. PROFESYONEL PDF GENERATOR (ARCHITECT)
# =================================================================
class ReportArchitect:
    def __init__(self, order_no):
        self.order_no = order_no
        self.tarih = datetime.now().strftime("%d/%m/%Y")
        self.buffer = io.BytesIO()

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(inch, A4[1] - 0.5 * inch, "VIP STRATEJI RAPORU - GIZLIDIR")
        canvas.drawRightString(A4[0] - inch, A4[1] - 0.5 * inch, f"Siparis: {self.order_no} | Sayfa {doc.page}")
        
        canvas.setStrokeColor(colors.dodgerblue)
        canvas.setLineWidth(1)
        canvas.line(inch, A4[1] - 0.6 * inch, A4[0] - inch, A4[1] - 0.6 * inch)
        canvas.restoreState()

    def build(self, content_dict):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=72, leftMargin=72,
            topMargin=72, bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='SubTitle', fontSize=14, textColor=colors.dodgerblue, spaceAfter=12))
        
        story = []
        
        # Kapak Sayfası
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(f"<font size='32' color='dodgerblue'>VIP ANALIZ RAPORU</font>", styles['Title']))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(f"Siparis No: {self.order_no}", styles['Normal']))
        story.append(Paragraph(f"Tarih: {self.tarih}", styles['Normal']))
        story.append(PageBreak())
        
        # İçerik
        for title, body in content_dict.items():
            story.append(Paragraph(TextEngine.force_tr_compatibility(title), styles['SubTitle']))
            story.append(Spacer(1, 0.2 * inch))
            
            clean_body = TextEngine.force_tr_compatibility(body)
            paragraphs = clean_body.split('\n')
            for p in paragraphs:
                if p.strip():
                    story.append(Paragraph(p, styles['Normal']))
                    story.append(Spacer(1, 0.1 * inch))
            story.append(PageBreak())

        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        self.buffer.seek(0)
        return self.buffer

# =================================================================
# 4. VIP AI CORE (LOGIC LAYER)
# =================================================================
def generate_supreme_content(user_data, order_no):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        st.error("API Anahtarı Eksik!")
        return None

    modules = {
        "MODÜL 1: MAKRO TEKNIK ANALIZ": "İşletmenin dijital ve fiziksel altyapısını mühendislik gözüyle analiz et.",
        "MODÜL 2: FIYATLANDIRMA PSIKOLOJISI": "Pazarın %1'ine hitap edecek premium fiyatlandırma stratejisi kur.",
        "MODÜL 3: RAKIP IMHA VE KONUMLAMA": "Rakiplerin zayıf noktalarını bul ve sektörde tekelleşme planı yaz.",
        "MODÜL 4: 12 AYLIK BÜYÜME VE ROI": "Yatırımın geri dönüşünü ay ay hesapla ve aksiyon adımlarını belirle.",
        "MODÜL 5: INOVASYON VE GELECEK": "5 yıl sonraki pazar değişimlerine bugünden hazırlık planı sun."
    }

    final_report = {}
    pb = st.progress(0)
    
    for i, (title, prompt) in enumerate(modules.items()):
        st.write(f"🌀 {title} işleniyor...")
        full_prompt = f"Sen bir CEO danışmanısın. {title} konusunda, şu verilere dayanarak 2000 kelimelik akademik rapor yaz: {user_data[:4000]}"
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Sen dünyanın en pahalı strateji danışmanısın. Sadece profesyonel Türkçe kullan. Detaylarda boğul, asla yüzeysel kalma."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.4
        )
        final_report[title] = response.choices[0].message.content
        pb.progress((i + 1) / len(modules))
        
    return final_report

# =================================================================
# 5. UI - SIDEBAR VE GÖRSEL KATMAN
# =================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=150)
    st.title("🛡️ Yasal Zırh & Protokol")
    st.divider()
    
    st.error("""
    **⛔ YASAL UYARI:**
    Bu raporlar yatırım tavsiyesi değildir. 
    Yalnızca stratejik simülasyon ve analiz amacı taşır.
    """)
    
    st.info("""
    **💎 VIP SUPREME HAKLARI:**
    - 10.000+ Kelime Raporlama
    - Akademik Dil ve Üslup
    - Sektörel ROI Haritası
    - PDF ve Mail Entegrasyonu
    """)
    
    st.markdown("---")
    st.caption("Sürüm: 7.4.2 Supreme Platinum")

# =================================================================
# 6. ANA EKRAN VE AKIŞ
# =================================================================
st.title("👑 Professional AI Strategy Engine")
st.write("SaaS ve İşletme Stratejilerinde Yapay Zeka Devrimi")

raw_input = st.text_area("Analiz Verilerini Girin:", height=300, placeholder="Veri, yorum, pazar bilgisi...")

c1, c2 = st.columns(2)
with c1:
    if st.button("🔍 Ücretsiz Analiz", use_container_width=True):
        st.write("Hızlı analiz hazırlanıyor...") # Buraya kısa bir API çağrısı eklenebilir.

with c2:
    st.link_button("💎 VIP Rapor Satın Al (Shopier)", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True, type="primary")

st.divider()
st.subheader("🔑 VIP Erişim Paneli")

v1, v2 = st.columns(2)
with v1:
    oid = st.text_input("Sipariş Numarası:")
with v2:
    mail = st.text_input("Gönderilecek E-posta:")

confirm = st.checkbox("Raporun dijital nitelikte olduğunu ve iade edilemeyeceğini onaylıyorum.")

if st.button("🚀 VIP STRATEJIYI BASLAT", use_container_width=True, type="primary"):
    if not raw_input or not oid or not confirm:
        st.error("Tüm alanları doldurmanız zorunludur!")
    else:
        with st.status("🚀 Rapor Üretiliyor...", expanded=True) as status:
            content = generate_supreme_content(raw_input, oid)
            if content:
                status.update(label="📄 PDF Mimarisi Oluşturuluyor...", state="running")
                architect = ReportArchitect(oid)
                pdf_buf = architect.build(content)
                status.update(label="✅ Her Şey Hazır!", state="complete")
                
                st.success("Analiz Başarıyla Tamamlandı!")
                st.download_button("📂 VIP PDF RAPORUNU INDIR", pdf_buf, f"VIP_Strategy_{oid}.pdf", "application/pdf")

st.caption("© 2026 High-End AI Corporate Solutions")
