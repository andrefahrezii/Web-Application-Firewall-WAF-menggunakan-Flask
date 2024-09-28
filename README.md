# Web Application Firewall (WAF) Project

## Deskripsi

Proyek ini berfokus pada pengembangan Web Application Firewall (WAF) menggunakan Flask, Python, dan Docker. Proyek ini mengintegrasikan beberapa fitur keamanan seperti deteksi SQL Injection, deteksi Cross-Site Scripting (XSS), dan penyaringan User-Agent untuk meningkatkan keamanan aplikasi web.

## Prerequisites

Sebelum memulai, pastikan Anda telah menginstal perangkat lunak berikut:

- **Python 3.6 atau yang lebih baru**
- **Docker** (untuk menjalankan Elasticsearch dan Logstash)
- **Pip** (untuk menginstal dependensi Python)

## Langkah-langkah Menjalankan Proyek

### 1. Clone Repository

Jika Anda belum melakukannya, klon repositori ke mesin lokal Anda:

```bash
docker compose up -d
```

### 5. Jalankan Aplikasi Flask

Jalankan kontainer aplikasi Flask:

```bash
docker run -p 5001:5000 flask-waf
```

## Dokumentasi Payload untuk Pengujian

### Uji Coba Dengan curl

# Uji Deteksi User-Agent Berbahaya

Coba kirim request dengan User-Agent yang berbahaya:

```bash
curl -v -H "User-Agent: sqlmap" http://localhost:5001
```

# Uji Deteksi SQL Injection

Kirimkan payload SQL Injection:

```bash
curl -v "http://localhost:5001?input=%27%20OR%20%271%27=%271"
```

# Uji Deteksi XSS

Kirimkan payload XSS:

```bash
curl -v "http://localhost:5001?input=<script>alert('XSS')</script>"

```

## Jika terdeteksi sebagai serangan SQL Injection, Anda harus mendapatkan respons 403 Forbidden.
