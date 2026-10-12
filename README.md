# Doubo 公共频道目录 · Doubo Public Channel Directory

全球**公开、免费播出**的电视频道 M3U 索引，每日自动更新。网页版目录：<https://doubo.tv/playlists/>

A daily-updated M3U index of TV channels that broadcasters make **freely and publicly available**. Browse it at <https://doubo.tv/playlists/>.

> 本仓库**不存储、不转发任何视频**，只收录链接，并按[收录规则](POLICY.md)筛选。
> This repository stores and relays **no video**. It only lists links that pass the [inclusion policy](POLICY.md).

## 使用 · Usage

把下面任一地址粘贴到 Doubo（或任何支持 M3U 的播放器）即可：

| 内容 Playlist | 地址 URL |
| --- | --- |
| 全部频道 All channels | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/index.m3u` |
| 按国家 By country | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/<code>.m3u` （例 e.g. `my`、`id`、`vn`、`th`） |
| 按分类 By category | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/categories/<id>.m3u` （例 e.g. `news`、`kids`、`sports`） |
| 按语言 By language | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/languages/<code>.m3u` （ISO 639-3，例 e.g. `msa`、`ind`、`vie`） |
| 机器可读索引 Index | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/index.json` |

备用镜像 Mirror：把 `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist` 换成 `https://raw.githubusercontent.com/maweis1981/iptv-playlists/dist`。

## 数据来源 · Sources

频道资料与链接来自社区项目 [iptv-org/database](https://github.com/iptv-org/database) 和 [iptv-org/iptv](https://github.com/iptv-org/iptv)（公有领域）。在此基础上，本目录采用[更严格的收录规则](POLICY.md)：只保留由频道官方网站域名或正规广播 CDN / 官方免费频道平台提供的直播流。

Channel data and links come from [iptv-org/database](https://github.com/iptv-org/database) and [iptv-org/iptv](https://github.com/iptv-org/iptv) (public domain), filtered by a [stricter policy](POLICY.md): only streams served from the channel's own domain or from an allowlisted broadcast CDN / official FAST platform are listed.

## 版权投诉与下架 · Takedown

权利人可通过[下架申请](../../issues/new?template=takedown.yml)要求移除链接，我们会在 72 小时内处理，下一次每日构建即生效。

Rights holders can request removal through a [takedown request](../../issues/new?template=takedown.yml). Requests are handled within 72 hours and take effect in the next daily build.

## 目录结构 · Layout

- `main` 分支：生成脚本 `scripts/build.py`、收录规则 `policy/`、工作流
- `dist` 分支：每日生成的播放列表（由 GitHub Actions 自动发布，请勿手动修改）

## 许可 · License

[The Unlicense](LICENSE)（公有领域 · public domain）
