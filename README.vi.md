[English](README.md) · [简体中文](README.zh-CN.md) · [Bahasa Melayu](README.ms.md) · [Bahasa Indonesia](README.id.md) · **Tiếng Việt** · [ไทย](README.th.md)

# Danh bạ kênh công khai Doubo

Chỉ mục M3U các kênh truyền hình được đài phát sóng **công khai, miễn phí** trên toàn thế giới, cập nhật hằng ngày. Xem danh bạ bằng ngôn ngữ của bạn tại <https://doubo.tv/vi/playlists/>

> Kho mã này **không lưu trữ hay chuyển tiếp bất kỳ video nào**. Nó chỉ liệt kê các liên kết đạt [chính sách chọn kênh](POLICY.md).

## Cách dùng

Dán bất kỳ liên kết nào dưới đây vào [Doubo](https://doubo.tv) hoặc trình phát bất kỳ hỗ trợ danh sách phát M3U:

| Danh sách phát | Liên kết |
| --- | --- |
| Tất cả kênh | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/index.m3u` |
| Theo quốc gia | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/<code>.m3u` (vd. `my`, `id`, `vn`, `th`) |
| Theo thể loại | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/categories/<id>.m3u` (vd. `news`, `kids`, `sports`) |
| Theo ngôn ngữ | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/languages/<code>.m3u` (mã ISO 639-3, vd. `msa`, `ind`, `vie`) |
| Chỉ mục cho máy đọc | `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/index.json` |

### Quốc gia phổ biến

- Malaysia: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/my.m3u`
- Indonesia: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/id.m3u`
- Việt Nam: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/vn.m3u`
- Thái Lan: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/th.m3u`
- Philippines: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/ph.m3u`
- Singapore: `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist/countries/sg.m3u`

Liên kết dự phòng: nếu jsDelivr chậm hoặc bị chặn trên mạng của bạn, thay `https://cdn.jsdelivr.net/gh/streamline-iptv/iptv-playlists@dist` bằng `https://raw.githubusercontent.com/streamline-iptv/iptv-playlists/dist`.

## Nguyên tắc chọn kênh

1. Chỉ đưa vào luồng phát từ tên miền trang web chính thức của kênh, hoặc từ CDN phát sóng / nền tảng xem miễn phí chính thức trong [danh sách cho phép](policy/allowed-hosts.txt).
2. Không có kênh trả phí, nội dung người lớn hay kênh đã ngừng phát sóng.
3. Loại bỏ các kênh trong danh sách chặn của iptv-org hoặc [danh sách gỡ bỏ](policy/takedown.csv) của chúng tôi.
4. Mỗi bản dựng hằng ngày kiểm tra từng luồng đến phân đoạn video đầu tiên và chỉ giữ lại luồng phát được; các luồng bị giới hạn khu vực vẫn được giữ vì chỉ có thể kiểm tra từ trong nước sở tại.

Chi tiết đầy đủ: [POLICY.md](POLICY.md).

## Nguồn dữ liệu

Dữ liệu và liên kết kênh lấy từ các dự án cộng đồng [iptv-org/database](https://github.com/iptv-org/database) và [iptv-org/iptv](https://github.com/iptv-org/iptv), được lọc theo chính sách chặt chẽ hơn ở trên.

## Yêu cầu gỡ bỏ

Chủ sở hữu bản quyền có thể yêu cầu gỡ kênh hoặc liên kết qua [yêu cầu gỡ bỏ](https://github.com/streamline-iptv/iptv-playlists/issues/new?template=takedown.yml). Yêu cầu được xử lý trong vòng 72 giờ và có hiệu lực ở bản dựng hằng ngày tiếp theo.

## Cấu trúc kho mã

- `main`: mã tạo danh sách (`scripts/build.py`), chính sách (`policy/`) và workflow.
- `dist`: danh sách phát do GitHub Actions tạo hằng ngày. Không chỉnh sửa thủ công.

## Đóng góp

Hoan nghênh đề xuất bổ sung danh sách cho phép qua pull request; vui lòng giải thích vì sao máy chủ đó là nguồn chính thức. Sửa dữ liệu kênh xin gửi lên [iptv-org/database](https://github.com/iptv-org/database).

## Giấy phép

Mã nguồn: [MIT](LICENSE). Danh sách phát và dữ liệu chỉ mục: [CC BY 4.0](LICENSE-DATA.md); vui lòng ghi nguồn “Doubo Public Channel Directory” khi đăng lại hoặc phát triển từ danh sách này. Giấy phép chỉ áp dụng cho việc chọn lọc liên kết của chúng tôi; mỗi luồng phát thuộc về đài phát sóng của nó.
