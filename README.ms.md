[English](README.md) · [简体中文](README.zh-CN.md) · **Bahasa Melayu** · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md)

# Direktori Saluran Awam Doubo

Indeks M3U saluran TV yang disiarkan **secara percuma dan terbuka** oleh penyiar di seluruh dunia, dikemas kini setiap hari. Layari direktori dalam bahasa anda di <https://doubo.tv/ms/playlists/>

> Repositori ini **tidak menyimpan atau menyalurkan semula sebarang video**. Ia hanya menyenaraikan pautan yang lulus [dasar penyenaraian](POLICY.md).

## Cara guna

Tampal mana-mana pautan ini dalam [Doubo](https://doubo.tv) atau mana-mana pemain yang menyokong senarai main M3U:

| Senarai main | Pautan |
| --- | --- |
| Semua saluran | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/index.m3u` |
| Mengikut negara | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/<code>.m3u` (cth. `my`, `id`, `vn`, `th`) |
| Mengikut kategori | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/categories/<id>.m3u` (cth. `news`, `kids`, `sports`) |
| Mengikut bahasa | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/languages/<code>.m3u` (kod ISO 639-3, cth. `msa`, `ind`, `vie`) |
| Indeks mesin | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/index.json` |

### Negara popular

- Malaysia: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/my.m3u`
- Indonesia: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/id.m3u`
- Vietnam: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/vn.m3u`
- Thailand: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/th.m3u`
- Filipina: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/ph.m3u`
- Singapura: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/sg.m3u`

Pautan alternatif: jika jsDelivr perlahan atau disekat di rangkaian anda, gantikan `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist` dengan `https://raw.githubusercontent.com/streamline-iptv/iptv-playlists/dist`.

## Apa yang disenaraikan

1. Hanya strim daripada domain laman web rasmi saluran, atau daripada CDN penyiaran / platform penstriman percuma rasmi dalam [senarai dibenarkan](policy/allowed-hosts.txt).
2. Tiada saluran berbayar, kandungan dewasa atau saluran yang telah ditutup.
3. Saluran dalam senarai sekatan iptv-org atau [senarai pengeluaran](policy/takedown.csv) kami tidak disenaraikan.
4. Setiap binaan harian menyemak setiap strim sehingga segmen video pertama dan hanya menyimpan yang boleh dimainkan; strim bertanda sekatan geografi dikekalkan kerana hanya boleh disemak dari negara asalnya.

Butiran penuh: [POLICY.md](POLICY.md).

## Sumber

Data dan pautan saluran daripada projek komuniti [iptv-org/database](https://github.com/iptv-org/database) dan [iptv-org/iptv](https://github.com/iptv-org/iptv), ditapis dengan dasar yang lebih ketat di atas. Senarai awam lain yang diselenggara turut digabungkan (lihat [sources.yml](sources.yml)), dan tugas mingguan mencari senarai main awam di GitHub: strim daripada domain laman web rasmi saluran ditambah secara automatik, manakala strim pada CDN awam hanya disenaraikan dalam [discovered/REPORT.md](discovered/REPORT.md) untuk semakan.

## Permintaan pengeluaran

Pemegang hak boleh meminta saluran atau pautan dikeluarkan melalui [permintaan pengeluaran](https://github.com/streamline-iptv/iptv-playlists/issues/new?template=takedown.yml). Permintaan diproses dalam 72 jam dan berkuat kuasa dalam binaan harian seterusnya.

## Struktur repositori

- `main`: skrip penjana (`scripts/build.py`), dasar (`policy/`) dan aliran kerja.
- `dist`: senarai main yang dijana setiap hari oleh GitHub Actions. Jangan sunting secara manual.

## Sumbangan

Cadangan untuk senarai hos dibenarkan dialu-alukan sebagai pull request; sila terangkan mengapa hos itu sumber rasmi. Pembetulan data saluran dihantar ke [iptv-org/database](https://github.com/iptv-org/database).

## Lesen

Kod: [MIT](LICENSE). Senarai main dan data indeks: [CC BY 4.0](LICENSE-DATA.md); sila nyatakan “Doubo Public Channel Directory” apabila menerbitkan semula atau membina di atas senarai ini. Lesen ini hanya meliputi pemilihan pautan kami; setiap strim milik penyiarnya.
