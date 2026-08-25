import streamlit as st
import requests
from PIL import Image

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Generator Skrip TikTok Shop", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop")
st.write("Buat naskah video jualan TikTok Shop secara gratis tanpa API Key.")

# Form Input
with st.form("tiktok_form"):
    nama_produk = st.text_input("Nama Produk TikTok Shop", placeholder="Contoh: Lampu Tidur Akrilik")
    keunggulan = st.text_area("Keunggulan / Promo Produk", placeholder="Contoh: Gratis ongkir, diskon 50%")
    
    # Menu Upload Referensi Gambar Produk
    uploaded_image = st.file_uploader(
        "Upload Referensi Gambar Produk (Opsional)", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Unggah foto produk untuk pratinjau referensi visual."
    )
    
    gaya = st.selectbox("Gaya Video", ["Hard Sell", "Soft Sell / Storytelling", "Review Jujur", "Spill Harga Murah"])
    
    submitted = st.form_submit_button("🚀 Buat Skrip Sekarang")

def get_recommended_hashtags(style, produk):
    tag_produk = f"#{produk.lower().replace(' ', '')}"
    
    if style == "Spill Harga Murah":
        hashtags = f"{tag_produk} #fypindonesia #viral2026 #trendingindonesia #kontenkekinian #tiktoktrend #harianviral"
    elif style == "Soft Sell / Storytelling":
        hashtags = f"{tag_produk} #inspirasi2026 #kontenpositif #idekreatif #kreatorindo #vibespositif #edukatif"
    elif style == "Review Jujur":
        hashtags = f"{tag_produk} #trendingnow #tiktokindo #videoviral #kreatifbanget #foryoupage #contentcreator"
    else:  # Hard Sell
        hashtags = f"{tag_produk} #fypindonesia #foryou #viralindonesia #explorepage #supportlokal #tiktokcommunity"
        
    return hashtags

def generate_script_free(produk, promo, style):
    # 1. Header Perintah Kustom di Bagian Paling Atas
    header_perintah = f"""Gunakan gambar produk yang diberikan sebagai referensi utama dan pertahankan bentuk produk secara akurat. Buat video promosi realistis untuk: {produk}.
Format: Vertikal 9:16
Durasi: tepat 20 detik
Gaya: realistis, profesional, clean, modern, seperti video review produk elektronik
Voice-over: Bahasa Indonesia, suara natural, jelas, energik
Musik: tidak ada\n\n"""

    # 2. Catatan Aturan Penting di Bagian Paling Akhir
    footer_aturan = """\n\nATURAN PENTING
Gunakan hanya produk dan perlengkapan yang terlihat pada gambar referensi. Jangan mengubah warna, bentuk, jumlah, atau desain produk. Jangan menambahkan produk atau fitur yang tidak terlihat. Jangan membuat klaim berlebihan. Jangan menampilkan api, percikan listrik, atau asap berlebihan. Jangan menggunakan musik. Pastikan voice-over terdengar natural dan seluruh video tepat 20 detik."""

    hashtags = get_recommended_hashtags(style, produk)
    
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    prompt = f"<s>[INST] Buatkan skrip TikTok Shop singkat untuk produk {produk} dengan keunggulan {promo} dan gaya {style}. Berikan HOOK, ISI, dan CALL TO ACTION dalam bahasa Indonesia. Gunakan hashtag: {hashtags} [/INST]"
    
    try:
        response = requests.post(API_URL, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}}, timeout=10)
        if response.status_code == 200:
            result = response.json()
            generated = result[0]["generated_text"].replace(prompt, "").strip()
            return header_perintah + generated + footer_aturan
    except Exception:
        pass
    
    # Template Otomatis Instan jika Server API Sedang Padat
    if style == "Spill Harga Murah":
        body = f"""📌 HOOK (Detik 0-3)
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
    else:
        body = f"""📌 HOOK (Detik 0-3)
Teks Layar: SOLUSI BUAT KAMU! ✨
Voiceover: "Sering bingung cari {produk} yang bagus? Kamu wajib lihat yang satu ini."

🎬 ISI KONTEN (Detik 3-15)
Visual: Perlihatkan keunggulan produk {produk} saat digunakan.
Voiceover: "Produk ini punya keunggulan {promo}. Dijamin worth it banget buat dimiliki!"

🛒 CALL TO ACTION (Detik 15-20)
Visual: Tunjukkan jari mengarah ke keranjang kuning.
Voiceover: "Mumpung lagi ready stock, langsung klik keranjang kuning di kiri bawah ya!"

📝 CAPTION & HASHTAG
Caption: Rekomendasi {produk} terbaik! {promo}.
Hashtag: {hashtags}"""

    return header_perintah + body + footer_aturan

# Proses Saat Tombol Diklik
if submitted:
    if not nama_produk:
        st.error("Isi nama produk terlebih dahulu!")
    else:
        # Menampilkan Gambar Referensi jika diunggah
        if uploaded_image is not None:
            st.image(uploaded_image, caption=f"Gambar Referensi Produk: {nama_produk}", use_container_width=True)
            
        with st.spinner("Sedang memproses skrip..."):
            skrip = generate_script_free(nama_produk, keunggulan, gaya)
            
            st.success("✨ Skrip Berhasil Dibuat!")
            st.write("### 📋 Hasil Naskah Skrip (Klik Icon Copy di Pojok Kanan Atas Teks):")
            
            # Menampilkan skrip dalam bentuk blok kode dengan tombol copy bawaan Streamlit
            st.code(skrip, language="markdown")
            
            # Tombol Download Skrip TXT
            st.download_button(
                label="📥 Download Skrip (TXT)",
                data=skrip,
                file_name=f"skrip_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )