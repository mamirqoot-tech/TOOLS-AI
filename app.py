import streamlit as st
import requests
from PIL import Image

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Generator Skrip TikTok SANGAT PADAT", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop SANGAT PADAT")
st.write("Buat naskah video 20 detik ringkas secara gratis (Target < 200 Kata Total).")

# Form Input
with st.form("tiktok_form"):
    nama_produk = st.text_input("Nama Produk TikTok Shop", placeholder="Contoh: Solder 80W / Lampu Akrilik")
    keunggulan = st.text_area("Keunggulan / Promo Produk", placeholder="Contoh: Gratis ongkir, diskon 50%, cepat panas")
    
    # Menu Upload Referensi Gambar Produk
    uploaded_image = st.file_uploader(
        "Upload Referensi Gambar Produk (Opsional)", 
        type=["jpg", "jpeg", "png", "webp"]
    )
    
    gaya = st.selectbox("Gaya Video", ["Review Jujur", "Hard Sell", "Soft Sell", "Spill Harga Murah"])
    
    submitted = st.form_submit_button("🚀 Buat Skrip Sekarang")

def get_recommended_hashtags(style, produk):
    tag_produk = f"#{produk.lower().replace(' ', '')}"
    if style == "Spill Harga Murah":
        hashtags = f"{tag_produk} #fypindonesia #viral2026 #trendingindonesia #tiktoktrend #harianviral"
    elif style == "Soft Sell":
        hashtags = f"{tag_produk} #inspirasi2026 #kontenpositif #idekreatif #kreatorindo #edukatif"
    elif style == "Review Jujur":
        hashtags = f"{tag_produk} #trendingnow #tiktokindo #videoviral #kreatifbanget #foryoupage"
    else:  # Hard Sell
        hashtags = f"{tag_produk} #fypindonesia #foryou #viralindonesia #explorepage #supportlokal"
    return hashtags

def count_words(text):
    if not text:
        return 0
    return len(text.split())

def generate_script_free(produk, promo, style):
    # Header Perintah SANGAT MINIMALIS (Tidak dihitung dalam 100 kata target AI)
    header_perintah = f"""[PANDUAN VIDEO 20 DETIK: {produk}]
Gaya: Realistis/Elektronik. VO: Natural, jelas. Musik: Tidak Ada.\n\n"""

    # Footer ATURAN PENTING SANGAT MINIMALIS
    footer_aturan = """\n\nATURAN: Gunakan hanya yang ada di gambar. Bentuk/warna akurat. No klaim berlebihan/api/asap. VO natural, durasi pas 20s."""

    hashtags = get_recommended_hashtags(style, produk)
    
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    # Prompt sangat ketat: Minta format tunggal, sangat ringkas, satu paragraf tunggal.
    prompt = f"<s>[INST] Buatkan skrip TikTok Shop SATU PARAGRAF SAJA, SANGAT SINGKAT (Tepat 20 detik VO) untuk produk {produk} ({promo}). Gaya {style}. Format: Hook, Isi, CTA. Maksimal 150 kata TOTAL. Jangan bertele-tele. Gunakan bahasa Indonesia. Tag: {hashtags} [/INST]"
    
    try:
        # max_new_tokens diset SANGAT KECIL (misalnya 150) untuk memaksa AI berhenti membuat teks panjang.
        response = requests.post(API_URL, json={"inputs": prompt, "parameters": {"max_new_tokens": 150}}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            generated = result[0]["generated_text"].replace(prompt, "").strip()
            
            # Gabungkan skrip lengkap
            skrip_padat = header_perintah + generated + footer_aturan
            
            return skrip_padat
                
    except Exception:
        pass
    
    # Fallback Template SANGAT SINGKAT (Jika AI Error atau Padat)
    template_singkat = f"""📌 Hook: {produk} viral, promo {promo}!
🎬 Isi: Kualitas mantap, cepat panas, hemat listrik. Stok terbatas.
🛒 CTA: Checkout sekarang di keranjang kuning!
Tag: {hashtags}"""
    
    return header_perintah + template_singkat + footer_aturan

# Proses Saat Tombol Diklik
if submitted:
    if not nama_produk:
        st.error("Isi nama produk terlebih dahulu!")
    else:
        # Menampilkan Gambar Referensi jika diunggah
        if uploaded_image is not None:
            st.image(uploaded_image, caption=f"Referensi: {nama_produk}", use_container_width=True)
            
        with st.spinner("Sedang memproses skrip sangat padat..."):
            skrip = generate_script_free(nama_produk, keunggulan, gaya)
            jumlah_kata = count_words(skrip)
            
            st.success(f"✨ Skrip Sangat Padat Berhasil Dibuat! (Total: {jumlah_kata} Kata)")
            st.write("### 📋 Naskah (Klik Icon Copy di Pojok Kanan Atas):")
            
            st.code(skrip, language="markdown")
            st.download_button(
                label="📥 Download Skrip (TXT)",
                data=skrip,
                file_name=f"skrip_padat_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )