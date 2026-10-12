[English](README.md) · [简体中文](README.zh-CN.md) · [Bahasa Melayu](README.ms.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · **ไทย**

# สารบบช่องทีวีสาธารณะ Doubo

ดัชนี M3U ของช่องทีวีที่ผู้แพร่ภาพทั่วโลกเปิดให้รับชม **ฟรีและเป็นสาธารณะ** อัปเดตทุกวัน ดูสารบบในภาษาของคุณได้ที่ <https://doubo.tv/th/playlists/>

> ที่เก็บนี้ **ไม่จัดเก็บและไม่ส่งต่อวิดีโอใด ๆ** มีเพียงลิงก์ที่ผ่าน[นโยบายการคัดเลือก](POLICY.md)เท่านั้น

## วิธีใช้

วางลิงก์ใดก็ได้ด้านล่างใน [Doubo](https://doubo.tv) หรือเครื่องเล่นที่รองรับเพลย์ลิสต์ M3U:

| เพลย์ลิสต์ | ลิงก์ |
| --- | --- |
| ทุกช่อง | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/index.m3u` |
| ตามประเทศ | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/<code>.m3u` (เช่น `my`, `id`, `vn`, `th`) |
| ตามหมวดหมู่ | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/categories/<id>.m3u` (เช่น `news`, `kids`, `sports`) |
| ตามภาษา | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/languages/<code>.m3u` (รหัส ISO 639-3, เช่น `msa`, `ind`, `vie`) |
| ดัชนีสำหรับเครื่อง | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/index.json` |

### ประเทศยอดนิยม

- มาเลเซีย: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/my.m3u`
- อินโดนีเซีย: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/id.m3u`
- เวียดนาม: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/vn.m3u`
- ไทย: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/th.m3u`
- ฟิลิปปินส์: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/ph.m3u`
- สิงคโปร์: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/sg.m3u`

ลิงก์สำรอง: หาก jsDelivr ช้าหรือถูกบล็อกในเครือข่ายของคุณ ให้แทนที่ `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist` ด้วย `https://raw.githubusercontent.com/streamline-iptv/iptv-playlists/dist`.

## หลักการคัดเลือก

1. รวมเฉพาะสตรีมจากโดเมนเว็บไซต์ทางการของช่อง หรือจาก CDN สำหรับการแพร่ภาพ / แพลตฟอร์มดูฟรีอย่างเป็นทางการใน[รายการที่อนุญาต](policy/allowed-hosts.txt)
2. ไม่มีช่องที่ต้องจ่ายเงิน เนื้อหาสำหรับผู้ใหญ่ หรือช่องที่ยุติการออกอากาศแล้ว
3. ไม่รวมช่องในรายการบล็อกของ iptv-org หรือ[รายการนำออก](policy/takedown.csv)ของเรา
4. การสร้างรายวันจะตรวจแต่ละสตรีมจนถึงส่วนวิดีโอแรก และเก็บเฉพาะสตรีมที่เล่นได้ สตรีมที่จำกัดพื้นที่ยังคงอยู่เพราะตรวจได้จากในประเทศนั้นเท่านั้น

รายละเอียดทั้งหมด: [POLICY.md](POLICY.md)

## แหล่งข้อมูล

ข้อมูลและลิงก์ช่องมาจากโครงการชุมชน [iptv-org/database](https://github.com/iptv-org/database) และ [iptv-org/iptv](https://github.com/iptv-org/iptv) คัดกรองตามนโยบายที่เข้มงวดกว่าด้านบน นอกจากนี้ยังรวมรายการสาธารณะอื่นที่มีผู้ดูแล (ดู [sources.yml](sources.yml)) และมีงานรายสัปดาห์ค้นหาเพลย์ลิสต์สาธารณะบน GitHub: สตรีมจากโดเมนเว็บไซต์ทางการของช่องจะถูกเพิ่มอัตโนมัติ ส่วนสตรีมบน CDN ทั่วไปจะถูกบันทึกใน [discovered/REPORT.md](discovered/REPORT.md) เพื่อให้คนตรวจสอบ

## คำขอนำออก

เจ้าของสิทธิ์สามารถขอให้นำช่องหรือลิงก์ออกได้ผ่าน[คำขอนำออก](https://github.com/streamline-iptv/iptv-playlists/issues/new?template=takedown.yml) เราจะดำเนินการภายใน 72 ชั่วโมง และมีผลในการสร้างรายวันครั้งถัดไป

## โครงสร้างที่เก็บ

- `main`: สคริปต์สร้าง (`scripts/build.py`) นโยบาย (`policy/`) และเวิร์กโฟลว์
- `dist`: เพลย์ลิสต์ที่ GitHub Actions สร้างทุกวัน ห้ามแก้ไขด้วยตนเอง

## การมีส่วนร่วม

ยินดีรับข้อเสนอเพิ่มโฮสต์ในรายการที่อนุญาตผ่าน pull request โปรดอธิบายว่าเหตุใดโฮสต์นั้นเป็นแหล่งทางการ การแก้ไขข้อมูลช่องโปรดส่งไปที่ [iptv-org/database](https://github.com/iptv-org/database)

## สัญญาอนุญาต

โค้ด: [MIT](LICENSE) เพลย์ลิสต์และข้อมูลดัชนี: [CC BY 4.0](LICENSE-DATA.md) โปรดระบุ “Doubo Public Channel Directory” เมื่อเผยแพร่ซ้ำหรือนำไปต่อยอด สัญญาอนุญาตนี้ครอบคลุมเฉพาะการคัดเลือกลิงก์ของเรา ทุกสตรีมเป็นของผู้แพร่ภาพนั้น ๆ
