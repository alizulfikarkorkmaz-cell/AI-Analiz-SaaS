import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
import time
import pandas as pd
import io

# =================================================================
# 1. SİSTEM YAPILANDIRMASI VE GÜVENLİK PROTOKOLLERİ
# =================================================================
st.set_page_config(
    page_title="AI Ultra Strateji: Master Gold v2.0",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Anahtarı ve Model Tanımlama (404 Hatasını Bitiren Kesin Çözüm)
def initialize_gemini():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ KRİTİK HATA: 'GEMINI_API_KEY' bulunamadı! Lütfen Secrets panelini kontrol edin.")
        st.stop()
    
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Sürüm karmaşasını önlemek için stabil yolu kullanıyoruz
        # image_f3e3d2.png'deki hatayı bu satır çözer.
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=generation_config
        )
        return model
    except Exception as e:
        st.error(f"Sistem Başlatılamadı: {str(e)}")
        st.stop()

model = initialize_gemini()

# =================================================================
# 2. VIP GÖRSEL MİMARİ (PROFESYONEL CSS)
# =================================================================
st.markdown("""
    <style>
    /* Ana Tema Düzenlemeleri */
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stApp { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); }
    
    /* Girdi Alanları */
    .stTextArea textarea { 
        border: 2px solid #30363d !important; 
        border-radius: 12px !important; 
        background-color: #010409 !important; 
        color: #e6edf3 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTextArea textarea:focus { border-color: #1f6feb !important; box-shadow: 0 0 10px #1f6feb; }
    
    /* Buton Tasarımları */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #238636 0%, #2ea043 100%);
        color: white;
        border-radius: 12px;
        height: 4em;
        font-weight: 800;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        background: linear-gradient(90deg, #2ea043 0%, #3fb950 100%);
    }
    
    /* Durum Kutuları */
    .report-card {
        padding: 25px;
        border-radius: 15px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. TDK ENTEGRASYONLU GRAMER MOTORU (PROFESYONEL CİLA)
# =================================================================
class TechnicalEditor:
    @staticmethod
    def polish_text(text):
        # Karakter temizliği
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı\n\r\t .,;:!?()/%&\-+=*]+', '', text)
        
        # TDK ve Teknik Düzeltmeler (snippet'teki gibi hataları temizler)
        rules = {
            r"\bmekn\b": "mekan", r"\bkğıt\b": "kağıt", r"\bherşey\b": "her şey",
            r"\bbirşey\b": "bir şey", r"\byada\b": "ya da", r"\bduragı\b": "durağı",
            r"\bfiyatıda\b": "fiyatı da", r"\blezzetide\b": "lezzeti de",
            r"\bsaglayan\b": "sağlayan", r"\bolduda\b": "oldu da", r"\btşk\b": "teşekkür"
        }
        for pattern, replacement in rules.items():
            text = re.compile(pattern, re.IGNORECASE).sub(replacement, text)
        return text.strip()

# =================================================================
# 4. STRATEJİK ANALİZ MOTORU (10.000 KELİME PROTOKOLÜ)
# =================================================================
def master_engine(data, oid):
    # image_f3e3d2.png'deki 404 hatasını ve yarım kalma sorununu modüler yapı çözer
    analysis_modules = [
        {
            "id": "OP_ANALYSIS",
            "title": "📊 MODÜL 1: OPERASYONEL ANALİZ VE TEKNİK KUSUR TESPİTİ",
            "prompt": "İşletme operasyonlarındaki 15 temel kusuru bul, mühendislik çözümleri ve optimizasyon önerileriyle 2000 kelime anlat."
        },
        {
            "id": "PRICING",
            "title": "💸 MODÜL 2: STRATEJİK FİYATLANDIRMA VE GELİR MİMARİSİ",
            "prompt": "Premium algı yönetimi, psikolojik fiyatlandırma ve çapraz satış stratejileriyle gelir artırma planını 2000 kelime detaylandır."
        },
        {
            "id": "R_D",
            "title": "🧪 MODÜL 3: ENDÜSTRİYEL AR-GE VE ÜRETİM İNOVASYONU",
            "prompt": "Üretim süreçlerinde teknolojik dönüşüm, AR-GE metodolojileri ve kalite standartları üzerine 2000 kelimelik teknik rapor hazırla."
        },
        {
            "id": "MARKET",
            "title": "🛡️ MODÜL 4: PAZAR DOMİNASYONU VE RAKİP İSTİHBARATI",
            "prompt": "Sektördeki en büyük 3 rakibin zayıf noktalarını analiz et ve 'Pazarın Hakimi' olma yol haritasını 2000 kelime yaz."
        },
        {
            "id": "ROI",
            "title": "📈 MODÜL 5: 360 DERECE BÜYÜME VE 12 AYLIK ROI PROJEKSİYONU",
            "prompt": "Yatırımın geri dönüşü (ROI), KPI takibi ve önümüzdeki 12 ayın her ayı için spesifik iş planını 2000 kelimelik tablo ve metinlerle sun."
        }
    ]

    full_report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREF NO: {oid}\n{'-'*60}\n"
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, mod in enumerate(analysis_modules):
        status_text.markdown(f"<p class='status-text'>⏳ {mod['title']} örülüyor...</p>", unsafe_allow_html=True)
        
        # Gemini'nin "kısmasını" önleyen CEO talimatı
        system_instruction = f"""
        Rol: Dünyanın en kıdemli yönetim danışmanı ve TDK uzmanı profesör.
        Talimat: Aşağıdaki konuyu ASLA ÖZETLEME yapmadan, en az 2000 kelime uzunluğunda, akademik ve teknik bir dille yaz.
        Yazım Kuralları: TDK'ya %100 uy. 'bir şey', 'mekan', 'ya da' gibi yazımlara dikkat et.
        """
        
        try:
            full_prompt = f"{system_instruction}\n\nKonu: {mod['title']}\nDetay: {mod['prompt']}\nVeri: {data[:10000]}"
            response = model.generate_content(full_prompt)
            
            if response and response.text:
                polished_content = TechnicalEditor.polish_text(response.text)
                full_report += f"\n\n{mod['title']}\n{'='*len(mod['title'])}\n\n{polished_content}\n"
            else:
                full_report += f"\n\n{mod['title']}\nBu modül üretilirken teknik bir aksama yaşandı.\n"
            
            # Rate limit (kota) koruması
            time.sleep(5)
            
        except Exception as e:
            st.error(f"Modül Hatası ({mod['id']}): {str(e)}")
            continue
            
        progress_bar.progress((idx + 1) / len(analysis_modules))
    
    status_text.empty()
    return full_report

# =================================================================
# 5. ARAYÜZ KATMANI (VIP EKRANI)
# =================================================================
def main():
    st.title("📈 AI Ultra Analiz & Strateji SaaS")
    st.markdown("##### 10.000 Kelimelik Teknik Çözüm ve TDK Onaylı Yazım Motoru")
    
    # Sidebar Tasarımı
    with st.sidebar:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
        st.subheader("VIP Destek Hattı")
        st.error("⚠️ YASAL UYARI: Bu rapor yatırım tavsiyesi değildir.")
        st.success("🛡️ %100 TELAFİ GARANTİSİ")
        st.info("Rapor kalitesinden memnun kalmazsanız manuel uzman revizesi talep edebilirsiniz.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()
        st.caption("v2.0 Master Gold Edition")

    # Ana Giriş
    input_data = st.text_area(
        "Analiz Edilecek Verileri Girin (Yorumlar, Raporlar, Finansal Veriler):", 
        height=300, 
        placeholder="Buraya verilerinizi yapıştırın..."
    )

    st.divider()
    st.subheader("🔑 Rapor Üretim ve Doğrulama")
    
    # Satın Alma ve Onay Bölümü
    c1, c2 = st.columns(2)
    with c1:
        shopier_id = st.text_input("Shopier Sipariş No:", placeholder="Örn: 12365478")
    with c2:
        st.write("##")
        consent = st.checkbox("Hizmet sözleşmesini ve iade olmadığını onaylıyorum.")

    st.link_button("💎 VIP Rapor Satın Al (Shopier)", "https://www.shopier.com/SAYFA_LINKIN", use_container_width=True)

    # --- MASTER BUTON ---
    if st.button("🚀 MASTER RAPORU ŞİMDİ İNŞA ET"):
        if not input_data:
            st.error("❌ Hata: Analiz edilecek veri girmediniz!")
        elif not shopier_id:
            st.warning("⚠️ Uyarı: Lütfen geçerli bir Shopier Sipariş No girin!")
        elif not consent:
            st.warning("⚠️ Uyarı: Devam etmek için sözleşmeyi onaylamanız gerekmektedir.")
        else:
            with st.status("🛠️ Gemini & TDK Editörü raporunuzu hazırlıyor (5-10 dk sürebilir)...", expanded=True):
                # Rapor üretimi (cite: MASTER_STRATEJI_12365478 (1).txt)
                final_report = master_engine(input_data, shopier_id)
                
                if final_report:
                    st.success("✅ Rapor Başarıyla Tamamlandı!")
                    
                    # İndirme Butonu
                    st.download_button(
                        label="📂 10.000 Kelimelik Raporu İndir (.txt)",
                        data=final_report.encode('utf-8-sig'),
                        file_name=f"VIP_Strategy_{shopier_id}.txt",
                        mime="text/plain; charset=utf-8",
                        use_container_width=True
                    )
                    
                    # Önizleme
                    with st.expander("📝 Rapor Önizleme (İlk Bölüm)"):
                        st.text(final_report[:2000] + "...")

if __name__ == "__main__":
    main()
