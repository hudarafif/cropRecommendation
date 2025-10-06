# cropRecommendation

Aplikasi Prediksi Rekomendasi Tanaman berdasarkan Kondisi Tanah dan Lingkungan

## Deskripsi
Aplikasi ini menggunakan model Machine Learning (LightGBM) untuk memprediksi jenis tanaman yang paling sesuai ditanam berdasarkan data kandungan tanah dan lingkungan. Aplikasi ini sangat membantu petani, agronom, atau pihak lain yang ingin melakukan budidaya tanaman secara lebih tepat guna.

Aplikasi ini tersedia secara online:  
[🌱 Demo Streamlit cropRecommendation](https://predcrop-2lgnkfg8t6uwgb6xuxli4v.streamlit.app/)

## Fitur Utama
- Input parameter tanah: Nitrogen (N), Fosfor (P), Kalium (K), Suhu, Kelembapan, pH
- Prediksi tanaman terbaik untuk kondisi yang diinputkan
- Menampilkan 3 rekomendasi tanaman teratas beserta tingkat probabilitasnya
- Model berbasis LightGBM, akurasi tinggi
- Antarmuka sederhana dan mudah digunakan

## Parameter yang Digunakan
1. Nitrogen (N)
2. Fosfor (P)
3. Kalium (K)
4. Suhu Udara (°C)
5. Kelembapan Udara (%)
6. pH Tanah

## Cara Penggunaan Lokal
1. Clone repositori ini
2. Install dependensi:
    ```bash
    pip install -r requirements.txt
    ```
3. Jalankan aplikasi:
    ```bash
    streamlit run app.py
    ```

## Dataset
Dataset yang digunakan berisi informasi kandungan unsur hara tanah dan kondisi lingkungan serta label tanaman yang sesuai.

## Model
Model yang digunakan adalah LightGBM dengan proses training dan evaluasi yang dapat dipelajari di file `croprec.ipynb`.

## Kontributor
- Rafif Huda

## Lisensi
Proyek ini terbuka untuk umum. Silakan gunakan dan kembangkan sesuai kebutuhan, dan wajib cantumkan sumbernya

---
