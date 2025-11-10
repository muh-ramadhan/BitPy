# Bitpy - Fully Decentralized Cryptocurrency

![Bitpy Banner](https://#)

**Bitpy** adalah cryptocurrency desentralisasi penuh menggunakan Proof-of-Work dengan fokus pada transaksi sehari-hari, UMKM, dan penggunaan internasional. **Dibangun berdasarkan kode Bitcoin versi awal yang diadaptasi ke Python** dan dimodifikasi dengan fitur-fitur inovatif.

**Bitpy** is a fully decentralized cryptocurrency using Proof-of-Work focused on daily transactions, SMEs, and international use. **Built upon early Bitcoin code adapted to Python** and modified with innovative features.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🎯 Origin & Philosophy

**Based on Original Bitcoin Code** - Bitpy dimulai dari kode Bitcoin versi awal yang di-porting ke Python, dengan modifikasi signifikan untuk:
- Transaksi mikro gratis
- Sistem fee bertingkat berdasarkan cumulative 30 hari
- Model privasi hybrid
- Reward block adaptif
- **Auto-recovery wallet tidak aktif 10 tahun**

**Philosophy**: Membuat cryptocurrency yang benar-benar terdesentralisasi dan praktis untuk penggunaan sehari-hari.

## ✨ Fitur Utama / Key Features

- 🔒 **Desentralisasi Penuh** / Fully Decentralized
- 💰 **Transaksi Mikro Gratis** / Free Micro-Transactions (hingga 9.999.999 koin / up to 9,999,999 coins)
- 📊 **Fee Bertingkat** / Tiered Fee System
- 🛡️ **Privasi & Transparansi** / Privacy & Transparency
- 🌍 **Dukungan Internasional** / International Support
- ⛏️ **Proof-of-Work Mining**
- 🔄 **Reward Block Adaptif** / Adaptive Block Reward
- 📱 **CLI-based** - Berjalan di Terminal, Termux, CMD / Runs on Terminal, Termux, CMD
- 💾 **RocksDB Storage** - Database high-performance
- 📧 **QR Code Support** - Untuk alamat penerima / For recipient addresses
- 🔄 **Auto Recovery** - Saldo wallet tidak aktif 10 tahun dikembalikan ke pending supply

## 📚 Dokumentasi / Documentation

### Bahasa Indonesia
- [📖 Whitepaper](docs/id/WHITEPAPER.md) - Konsep dan visi proyek
- [🔧 Blueprint](docs/id/BLUEPRINT.md) - Arsitektur teknis detail
- [⚙️ Spesifikasi Teknis](docs/id/TECHNICAL_SPEC.md) - Spesifikasi teknis lengkap

### English
- [📖 Whitepaper](docs/en/WHITEPAPER.md) - Project concept and vision
- [🔧 Blueprint](docs/en/BLUEPRINT.md) - Detailed technical architecture
- [⚙️ Technical Specification](docs/en/TECHNICAL_SPEC.md) - Complete technical specifications

## 🚀 Quick Start

### Prerequisites

- Python 3.8 atau lebih tinggi / or higher
- pip (Python package manager)

### Installation

1. **Clone repository**
```bash
git clone https://github.com/muh-ramadhan/BitPy.git
cd BitPy
pip install -r requirements.txt
python src/main.py
```
2. **Available Commands:**
```text
  help                      - Show this help
  status                    - Show node status
  createwallet [name]       - Create new wallet
  getbalance [addr]         - Get balance for address
  listaddresses [wallet]    - List addresses in wallet
  send <from> <to> <amount> - Send Bitpy
  mine <address>            - Start mining to address
  stopmining                - Stop mining
  mininginfo                - Show mining information
  getblockcount             - Get current block height
  getblock <hash>           - Get block information
  getbestblockhash          - Get best block hash
  startnode                 - Start P2P network node
  getpeerinfo               - Get peer information
  dumpblockchain            - Dump blockchain info
  quit                      - Exit Bitpy CLI
```

## 📄 License
- Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## 📞 Contact & Support
- GitHub Issues: Laporkan bug atau request fitur
- Discussions: Diskusi komunitas

## 🗺️ Roadmap
- Phase 1: Design & Architecture - Whitepaper completion, technical specifications, system architecture design
- Phase 2: Code Structure Development - Core module development, CLI interface, basic wallet functionality
- Phase 3: Testing & Optimization - Unit testing, security testing, performance optimization
- Phase 4: Official Launch - Mainnet deployment, community mining initiation, documentation completion
- Phase 5: Mobile Adoption - Termux optimization for Android, CLI compatibility across all platforms
- Phase 6: Ecosystem Growth - Merchant tools, payment gateway integration, international expansion

## 🗺️ Peta Jalan
- Fase 1: Perancangan & Arsitektur - Penyelesaian whitepaper, spesifikasi teknis, desain arsitektur sistem
- Fase 2: Pembuatan Struktur Kode - Pengembangan modul inti, antarmuka CLI, fungsionalitas dompet dasar
- Fase 3: Uji Coba & Optimasi - Pengujian unit, pengujian keamanan, optimasi performa
- Fase 4: Peluncuran Resmi - Deployment mainnet, inisiasi penambangan komunitas, penyelesaian dokumentasi
- Fase 5: Adopsi Mobile - Optimasi Termux untuk Android, kompatibilitas CLI di semua platform
- Fase 6: Pertumbuhan Ekosistem - Alat untuk merchant, integrasi gateway pembayaran, ekspansi internasional

