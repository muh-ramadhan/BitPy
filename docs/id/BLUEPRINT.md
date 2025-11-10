# Bitpy Technical Blueprint

## Arsitektur Sistem

### Komponen Inti

#### 1. Layer Blockchain
- **Struktur Block:** Header + Transactions
- **Konsensus:** Proof-of-Work
- **Penyesuaian Kesulitan:** Dinamis berdasarkan network hash rate

#### 2. Layer Transaksi
- **Model UTXO:** Unspent Transaction Output
- **Perhitungan Fee:** Tiered berdasarkan kumulatif 30 hari
- **Validasi:** Verifikasi signature kriptografi

#### 3. Layer Jaringan
- **Protokol P2P:** Komunikasi node terdesentralisasi
- **Manajemen Mempool:** Pooling dan validasi transaksi
- **Propagasi Block:** Distribusi block yang efisien

#### 4. Layer Wallet
- **Manajemen Kunci:** Kriptografi public/private key
- **Generasi QR:** Encoding permintaan pembayaran
- **Pelacakan Saldo:** Agregasi UTXO

## Detail Implementasi

### Skema Database

**Database Blockchain:**
- Blocks: Menyimpan informasi block (hash, height, timestamp, transactions)
- Chain: Menjaga integritas rantai block

**Database UTXO:**
- Unspent outputs dengan metadata lengkap
- Tracking output yang sudah digunakan

**Pelacakan Kumulatif:**
- Cumulative 30 hari per alamat
- Reset periodik dengan sliding window

### Implementasi Fee Tier

**Struktur Tier:**
- Tier 1: 10-50 juta koin (0.01% fee)
- Tier 2: 50-500 juta koin (0.05% fee) 
- Tier 3: 500 juta-5 miliar koin (0.1% fee)
- Tier 4: >5 miliar koin (0.2% fee)

**Mekanisme Perhitungan:**
- Hanya jumlah yang melebihi kuota gratis yang dikenakan fee
- Perhitungan real-time berdasarkan cumulative 30 hari
- Distribusi otomatis 70/20/10

### Reward Block Adaptif

**Faktor Penentu:**
- Sisa supply terhadap total supply
- Volume transaksi signifikan (non-micro)
- Aktivitas jaringan keseluruhan

**Formula Dasar:**
Reward_Block = Base_Reward × (Remaining_Supply / Total_Supply) × (Total_Significant_Transaction / Max_Transaction)

## Pertimbangan Keamanan

### 1. Perlindungan Double Spend
- Model UTXO dengan pelacakan output terpakai
- Persyaratan konfirmasi transaksi
- Validasi konsensus seluruh jaringan

### 2. Resistensi Serangan Sybil
- Persyaratan Proof-of-Work untuk produksi block
- Penyesuaian kesulitan jaringan
- Skoring reputasi peer

### 3. Perlindungan Privasi
- Tidak ada eksposur saldo langsung
- Obfuskasi grafik transaksi
- Rotasi alamat opsional

## Optimasi Performa

### 1. Indexing Database
- Indexing berbasis hash untuk pencarian cepat
- Pelacakan kumulatif berbasis alamat
- Pemangkasan transaksi berbasis waktu

### 2. Efisiensi Jaringan
- Propagasi block yang kompak
- Bloom filter transaksi
- Optimasi seleksi peer

### 3. Manajemen Memori
- Pemangkasan set UTXO
- Batas ukuran mempool
- Implementasi cache untuk operasi frequent
