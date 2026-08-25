import streamlit as st
import base64
from openai import OpenAI
from PIL import Image

# Konfigurasi Tampilan Aplikasi
st.set_page_config(page_title="AI TikTok Affiliate Generator (OpenAI)", layout="centered")

st.title("🚀 TikTok Affiliate Content Generator AI")
st.write("Generate skrip, storytelling, dan panduan visual video TikTok Affiliate dalam hitungan detik menggunakan OpenAI.")

# Form Input Pengguna
with st.form("affiliate_form"):
    nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Solder 80W / Skincare Brightening")
    
    uploaded_image = st.file_uploader(
        "Upload Gambar Referensi Produk (Opsional)", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Unggah foto produk untuk membantu AI memahami bentuk dan detail visualnya."
    )
    
    target_audiens = st.multiselect(
        "Target Audiens",
        ["Ibu Rumah Tangga", "Gen Z", "Pekerja Kantor", "Pelajar/Mahasiswa", "Pria/Wanita Umum"],
        default=["Gen Z"]
    )
    
    keunggulan = st.text_area("Keunggulan Utama Produk", placeholder="Contoh: Cepat panas, hemat listrik, garansi 1 tahun")
    
    gaya_penyampaian = st.selectbox(
        "Gaya Penyampaian / Durasi",
        [
            "Video Pendek Cepat (10-15 Detik)",
            "Review Jujur (30-45 Detik)",
            "Sketsa Drama Pendek (30-45 Detik)",
            "Storytelling Emosional (45-60 Detik)"
        ]
    )
    
    # Ambil default API Key dari secrets jika ada
    default_key = st.secrets.get("OPENAI_API_KEY", "")
    api_key_input = st.text_input("Masukkan OpenAI API Key", value=default_key, type="password", help="Dapatkan API key dari platform OpenAI")
    
    submitted = st.form_submit_button("✨ Generate Konten Sekarang")

# Fungsi pembantu untuk mengonversi gambar ke base64 (Format OpenAI Vision)
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# Proses saat Tombol Diklik
if submitted:
    if not nama_produk:
        st.error("Mohon isi Nama Produk terlebih dahulu!")
    elif not api_key_input:
        st.error("Mohon masukkan OPENAI_API_KEY yang valid!")
    else:
        try:
            # Inisialisasi Klien OpenAI
            client = OpenAI(api_key=api_key_input.strip())
            
            prompt_text = f"""
            Bertindaklah sebagai Senior Content Director dan TikTok Affiliate Expert. 
            Buatkan satu paket lengkap pembuatan konten TikTok siap pakai untuk produk berikut:

            - Nama Produk: {nama_produk}
            - Target Audiens: {', '.join(target_audiens)}
            - Keunggulan Utama: {keunggulan}
            - Gaya Penyampaian: {gaya_penyampaian}

            Catatan: Jika ada gambar terlampir, analisis elemen visual produk tersebut dan masukkan ke dalam panduan adegan visual dan hook.

            Berikan output dengan struktur persis seperti ini:

            1. JUDUL & HOOK (Detik 0-3)
            - Teks di Layar (On-Screen Text): 
            - Kalimat Pembuka (Voiceover): 

            2. NASKAH STORYTELLING & VISUAL
            - Alur Cerita & Dialog: 
            - Panduan Adegan Visual: 

            3. CALL TO ACTION / CTA (Detik Terakhir)
            - Skrip Penutup & Teks Keranjang Kuning: 

            4. TEKNIS PENDUKUNG ALGORITMA
            - Rekomendasi Musik/Sound: 
            - Caption Singkat: 
            - 5 Hashtag FYP: 
            """
            
            # Menyiapkan payload pesan untuk OpenAI API
            user_content = []
            
            if uploaded_image is not None:
                base64_image = encode_image(uploaded_image)
                mime_type = uploaded_image.type
                user_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{base64_image}"
                    }
                })
            
            user_content.append({
                "type": "text",
                "text": prompt_text
            })

            messages = [
                {"role": "system", "content": "Anda adalah pakar pemasaran TikTok Affiliate berpengalaman."},
                {"role": "user", "content": user_content}
            ]
            
            with st.spinner("OpenAI GPT-4o sedang merancang naskah dan konsep visual..."):
                response = client.chat.completions.create(
                    model="gpt-4o",  # Bisa diganti ke "gpt-4o-mini" untuk versi yang lebih hemat biaya
                    messages=messages,
                    max_tokens=1500
                )
                
                output_text = response.choices[0].message.content
                st.success("Berhasil Membuat Konten!")
                st.markdown(output_text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}. Periksa kembali apakah OpenAI API Key Anda valid dan memiliki saldo/kredit aktif.")