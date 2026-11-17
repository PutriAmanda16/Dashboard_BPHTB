# Laporan Audit Awal BPHTB Kota Surabaya

## 1. Ruang Lingkup
Audit menggunakan tiga workbook BPHTB.
Hasil belum divalidasi ke sistem keuangan primer.

## 2. Struktur Dataset
- Master bulanan: 72 observasi
- Rincian kategori: 24 observasi
- Historis lengkap: 2021–2025
- Realisasi 2026: Januari–Agustus
- Proyeksi 2026: September–Desember

## 3. Hasil Pemeriksaan
- Duplikasi master: 0
- Duplikasi kategori: 0
- Missing kritis: 0
- Rekonsiliasi tidak cocok: 0
- SSPD rekap AF18: 6,695
- SSPD Januari–Agustus: 12,376
- Formula rekap AF18: =SUM(AF6:AF11)

## 4. Tindak Lanjut
- Konfirmasi cakupan rekap SSPD 2026.
- Konfirmasi perbedaan target kedua kategori.
- Pisahkan realisasi dan proyeksi dalam analisis.
- Jangan menghitung ganda master dan kategori.

## 5. Catatan
Audit membaca nilai yang tersimpan di Excel.
Formula Excel tidak dihitung ulang oleh Python.