import streamlit as st
from openai import OpenAI
from PIL import Image

# Konfigurasi Tampilan Aplikasi
st.set_page_config(page_title="AI TikTok Affiliate Generator (DeepSeek)", layout="centered", page_icon="🚀")

st.title("🚀 TikTok Affiliate Content Generator AI")
st.write("Generate skrip, storytelling, dan panduan visual video TikTok Affiliate dalam hitungan detik menggunakan DeepSeek.")

# Form Input Pengguna
with st.form("affiliate_form"):
    nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Solder 80W / Skincare Brightening")
    
    uploaded_image = st.file_uploader(
        "Upload Gambar Referensi Produk (Opsional)", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Unggah foto produk untuk referensi Anda."
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
    
    # Ambil default API Key dari Streamlit Secrets jika ada
    default_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    api_key_input = st.text_input(
        "Masukkan DeepSeek API Key", 
        value=default_key, 
        type="password", 
        help="Dapatkan API key dari platform DeepSeek"
    )
    
    submitted = st.form_submit_button("✨ Generate Konten Sekarang")

# Proses saat Tombol Diklik
if submitted:
    if not nama_produk:
        st.error("Mohon isi Nama Produk terlebih dahulu!")
    elif not api_key_input:
        st.error("Mohon masukkan DeepSeek API Key yang valid!")
    else:
        try:
            # Menginisialisasi Client OpenAI yang diarahkan ke Server API DeepSeek
            client = OpenAI(
                api_key=api_key_input.strip(),
                base_url="https://api.deepseek.com"
            )
            
            prompt_text = f"""
            Bertindaklah sebagai Senior Content Director dan TikTok Affiliate Expert. 
            Buatkan satu paket lengkap pembuatan konten TikTok siap pakai untuk produk berikut:

            - Nama Produk: {nama_produk}
            - Target Audiens: {', '.join(target_audiens)}
            - Keunggulan Utama: {keunggulan}
            - Gaya Penyampaian: {gaya_penyampaian}

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

            messages = [
                {"role": "system", "content": "Anda adalah pakar pemasaran TikTok Affiliate berpengalaman."},
                {"role": "user", "content": prompt_text}
            ]
            
            with st.spinner("DeepSeek AI sedang merancang naskah dan konsep visual..."):
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    max_tokens=1500
                )
                
                output_text = response.choices[0].message.content
                st.success("Berhasil Membuat Konten!")
                st.markdown(output_text)
                
                # Fitur Unduh Skrip Langsung
                st.download_button(
                    label="📥 Unduh Skrip (Format TXT)",
                    data=output_text,
                    file_name=f"skrip_tiktok_{nama_produk.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}. Periksa kembali apakah DeepSeek API Key Anda valid dan akun memiliki saldo/kredit aktif.")