# Bitpy Technical Specification

## Spesifikasi Teknis Detail

### 1. Parameter Jaringan

**Supply & Unit:**
- Total Supply: 1.000.000.000.000.000.000 (1 kuintiliun)
- Unit Terkecil: 0,0001 koin (4 desimal)
- Base Unit: 1 Satoshi = 0,0001 koin

**Block Parameters:**
- Waktu Block Target: 2,5 menit
- Penyesuaian Kesulitan: Setiap 2016 block
- Ukuran Block Maksimum: 4 MB

### 2. Spesifikasi Kriptografi

**Algoritma Hashing:**
- Block Hashing: SHA-256
- Address Generation: SHA-256 + RIPEMD-160
- Digital Signature: ECDSA dengan curve SECP256K1

**Format Address:**
- Base58Check encoding
- Version byte: 0x1C (mainnet)
- Checksum 4 byte

### 3. Struktur Data

**Block Header:**
- Version: 4 byte
- Previous Block Hash: 32 byte
- Merkle Root: 32 byte
- Timestamp: 4 byte
- Difficulty Target: 4 byte
- Nonce: 4 byte

**Transaksi:**
- Version: 4 byte
- Input Count: Variabel
- Inputs: Daftar input transaksi
- Output Count: Variabel
- Outputs: Daftar output transaksi
- Lock Time: 4 byte

### 4. Protokol Jaringan

**Message Types:**
- VERSION: Handshake awal
- VERACK: Konfirmasi handshake
- ADDR: Daftar alamat node
- INV: Inventory (block/transaksi)
- GETDATA: Request data spesifik
- TX: Transaksi
- BLOCK: Block

**Peer Discovery:**
- DNS seeds untuk bootstrap
- Manual peer entry
- Exchange peer lists

### 5. Mekanisme Konsensus

**Proof-of-Work:**
- Target difficulty adjustment
- Valid nonce discovery
- Block validation rules

**Validasi Transaksi:**
- Verifikasi signature
- Check double spend
- Validasi format
- Fee calculation verification

### 6. Economic Parameters

**Fee Structure:**
- Free Quota: 9.999.999 koin per 30 hari
- Tier 1: 0.01% (10-50 juta)
- Tier 2: 0.05% (50-500 juta)
- Tier 3: 0.1% (500 juta-5 miliar)
- Tier 4: 0.2% (>5 miliar)

**Reward Distribution:**
- Miners: 70% dari total fee
- Staking: 20% dari total fee
- Pending Supply: 10% dari total fee

### 7. Keamanan & Privasi

**Model Privasi:**
- Saldo: Private
- Total dikirim: Private
- Pengirim-penerima: Public
- Jumlah transaksi: Public

**Anti-Abuse Measures:**
- Cumulative 30-day tracking
- Transaction rate limiting
- Tiered fee discouragement
