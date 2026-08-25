import streamlit as st
import requests
from PIL import Image

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Generator Skrip TikTok Shop", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop")
st.write("Buat naskah video jualan TikTok Shop (Maksimal 900 kata).")

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

def enforce_max_words(text, limit=900):
    """Memotong teks secara ketat jika melebihi batas kata."""
    words = text.split()
    if len(words) > limit:
        return " ".join(words[:limit])
    return text

def generate_script_free(produk, promo, style):
    # Header Perintah Kustom
    header_perintah = f"""[PANDUAN VIDEO 20 DETIK: {produk}]
Gaya: Realistis/Elektronik. VO: Natural, jelas. Musik: Tidak Ada.\n\n"""

    # Footer ATURAN PENTING Kustom
    footer_aturan = """\n\nATURAN PENTING
Gunakan hanya produk dan perlengkapan yang terlihat pada gambar referensi. Jangan mengubah warna, bentuk, jumlah, atau desain produk. Jangan menambahkan produk atau fitur yang tidak terlihat. Jangan membuat klaim berlebihan. Jangan menampilkan api, percikan listrik, atau asap berlebihan. Jangan menggunakan musik. Pastikan voice-over terdengar natural dan seluruh video tepat 20 detik."""

    hashtags = get_recommended_hashtags(style, produk)
    
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    prompt = f"<s>[INST] Buatkan skrip TikTok Shop rinci untuk produk {produk} ({promo}) dengan gaya {style}. Berikan HOOK, ISI, dan CALL TO ACTION serta visual deskriptif. Gunakan bahasa Indonesia. Tag: {hashtags} [/INST]"
    
    try:
        response = requests.post(API_URL, json={"inputs": prompt, "parameters": {"max_new_tokens": 800}}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            generated = result[0]["generated_text"].replace(prompt, "").strip()
            
            # Gabungkan skrip lengkap
            skrip_lengkap = header_perintah + generated + footer_aturan
            
            # Pastikan TIDAK LEBIH dari 900 kata
            return enforce_max_words(skrip_lengkap, limit=900)
                
    except Exception:
        pass
    
    # Fallback Template jika API error
    template_singkat = f"""📌 HOOK (Detik 0-3)
Teks Layar: JANGAN BELI {produk.upper()} SEBELUM LIHAT INI! 😱
Voiceover: "Jangan beli {produk} sebelum kamu lihat promo hari ini!"

🎬 ISI KONTEN (Detik 3-15)
Visual: Tunjukkan detail produk {produk} secara dekat di depan kamera.
Voiceover: "Biasanya harganya mahal, tapi khusus hari ini lagi ada promo {promo}. Kualitasnya mantap banget!"

🛒 CALL TO ACTION (Detik 15-20)
Visual: Tunjuk panah ke arah keranjang kuning.
Voiceover: "Langsung klik keranjang kuning di kiri bawah sebelum stok promonya habis!"

📝 CAPTION & HASHTAG
Caption: Promo {produk} hari ini! {promo}. Yuk checkout sekarang!
Hashtag: {hashtags}"""
    
    skrip_fallback = header_perintah + template_singkat + footer_aturan
    return enforce_max_words(skrip_fallback, limit=900)

# Proses Saat Tombol Diklik
if submitted:
    if not nama_produk:
        st.error("Isi nama produk terlebih dahulu!")
    else:
        if uploaded_image is not None:
            st.image(uploaded_image, caption=f"Referensi: {nama_produk}", use_container_width=True)
            
        with st.spinner("Sedang memproses skrip..."):
            skrip = generate_script_free(nama_produk, keunggulan, gaya)
            jumlah_kata = count_words(skrip)
            
            st.success(f"✨ Skrip Berhasil Dibuat! (Total: {jumlah_kata} Kata - Maks 900 Kata)")
            st.write("### 📋 Naskah (Klik Icon Copy di Pojok Kanan Atas):")
            
            st.code(skrip, language="markdown")
            st.download_button(
                label="📥 Download Skrip (TXT)",
                data=skrip,
                file_name=f"skrip_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )