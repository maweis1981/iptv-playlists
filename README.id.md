[English](README.md) · [简体中文](README.zh-CN.md) · [Bahasa Melayu](README.ms.md) · **Bahasa Indonesia** · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md)

# Direktori Saluran Publik Doubo

Indeks M3U saluran TV yang disiarkan **secara gratis dan terbuka** oleh penyiar di seluruh dunia, diperbarui setiap hari. Jelajahi direktori dalam bahasa Anda di <https://doubo.tv/id/playlists/>

> Repositori ini **tidak menyimpan atau meneruskan video apa pun**. Isinya hanya tautan yang lolos [kebijakan pencantuman](POLICY.md).

## Cara pakai

Tempel salah satu tautan ini ke [Doubo](https://doubo.tv) atau pemutar apa pun yang mendukung playlist M3U:

| Playlist | Tautan |
| --- | --- |
| Semua saluran | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/index.m3u` |
| Berdasarkan negara | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/<code>.m3u` (mis. `my`, `id`, `vn`, `th`) |
| Berdasarkan kategori | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/categories/<id>.m3u` (mis. `news`, `kids`, `sports`) |
| Berdasarkan bahasa | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/languages/<code>.m3u` (kode ISO 639-3, mis. `msa`, `ind`, `vie`) |
| Indeks mesin | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/index.json` |

### Negara populer

- Malaysia: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/my.m3u`
- Indonesia: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/id.m3u`
- Vietnam: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/vn.m3u`
- Thailand: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/th.m3u`
- Filipina: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/ph.m3u`
- Singapura: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/sg.m3u`

Tautan cadangan: jika jsDelivr lambat atau diblokir di jaringan Anda, ganti `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist` dengan `https://raw.githubusercontent.com/maweis1981/iptv-playlists/dist`.

## Apa yang dicantumkan

1. Hanya stream dari domain situs resmi saluran, atau dari CDN penyiaran / platform streaming gratis resmi dalam [daftar izin](policy/allowed-hosts.txt).
2. Tidak ada saluran berbayar, konten dewasa, atau saluran yang sudah tutup.
3. Saluran dalam daftar blokir iptv-org atau [daftar penghapusan](policy/takedown.csv) kami tidak dicantumkan.
4. Setiap build harian memeriksa setiap stream hingga segmen video pertama dan hanya menyimpan yang bisa diputar; stream bertanda pembatasan wilayah tetap dicantumkan karena hanya bisa diperiksa dari negara asalnya.

Detail lengkap: [POLICY.md](POLICY.md).

## Sumber

Data dan tautan saluran berasal dari proyek komunitas [iptv-org/database](https://github.com/iptv-org/database) dan [iptv-org/iptv](https://github.com/iptv-org/iptv), disaring dengan kebijakan yang lebih ketat di atas.

## Permintaan penghapusan

Pemegang hak dapat meminta saluran atau tautan dihapus melalui [permintaan penghapusan](https://github.com/maweis1981/iptv-playlists/issues/new?template=takedown.yml). Permintaan diproses dalam 72 jam dan berlaku pada build harian berikutnya.

## Struktur repositori

- `main`: skrip pembuat (`scripts/build.py`), kebijakan (`policy/`), dan workflow.
- `dist`: playlist yang dibuat setiap hari oleh GitHub Actions. Jangan diedit manual.

## Kontribusi

Usulan untuk daftar izin host diterima melalui pull request; jelaskan mengapa host tersebut sumber resmi. Koreksi data saluran diajukan ke [iptv-org/database](https://github.com/iptv-org/database).

## Lisensi

Kode: [MIT](LICENSE). Playlist dan data indeks: [CC BY 4.0](LICENSE-DATA.md); cantumkan “Doubo Public Channel Directory” saat menerbitkan ulang atau mengembangkan daftar ini. Lisensi ini hanya mencakup pilihan tautan kami; setiap stream milik penyiarnya.
