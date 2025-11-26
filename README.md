## Tugas 1: Smoothing dan Blurring

## Deskripsi

Program ini menerapkan beberapa teknik smoothing pada video dari webcam. Filter yang digunakan meliputi average blur, Gaussian blur dengan kernel buatan sendiri, dan sharpening.

## Tujuan

* Memahami dasar smoothing pada citra.
* Mengimplementasikan Gaussian kernel manual.
* Melihat perbedaan efek filter secara real-time.

## Fitur

* Normal mode
* Average blur 5x5 dan 9x9
* Gaussian blur custom
* Sharpen filter
* Pergantian mode melalui keyboard

## Cara Menjalankan

   ```bash
   python tugas_1_smoothing_dan_blurring.py
   ```

## Kontrol

* 0: Normal
* 1: Blur 5x5
* 2: Blur 9x9
* 3: Gaussian custom
* 4: Sharpen
* q: Keluar

---

## Tugas 2: Deteksi Warna HSV

## Deskripsi

Program ini mendeteksi objek berwarna merah, hijau, dan biru menggunakan ruang warna HSV. Tersedia dua mode: tracking warna dan tampilan visualisasi HSV.

## Tujuan

* Memahami deteksi warna berbasis HSV.
* Mengoptimalkan segmentasi menggunakan filter Saturation dan Value.
* Menyediakan tampilan HSV untuk mempermudah kalibrasi.

## Fitur

* Deteksi merah, hijau, biru
* Multi-range HSV untuk warna merah
* Filter SV untuk akurasi
* Pengolahan morfologi untuk mengurangi noise
* Mode HSV viewer untuk analisis channel

## Cara Menjalankan

   ```bash
   python tugas_2_deteksi_hsv.py
   ```

## Kontrol

* 1: Mode tracking warna
* 2: Mode HSV viewer
* q: Keluar
