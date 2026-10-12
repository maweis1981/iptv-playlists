[English](README.md) · **简体中文** · [Bahasa Melayu](README.ms.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md)

# Doubo 公共频道目录

全球电视台**官方公开、免费播出**的电视频道 M3U 索引，每日自动更新。网页版目录： <https://doubo.tv/playlists/>

> 本仓库**不存储、不转发任何视频**，只收录通过[收录规则](POLICY.md)的链接。

## 使用方法

把下面任一链接粘贴到[都播](https://doubo.tv)或任何支持 M3U 的播放器即可：

| 播放列表 | 链接 |
| --- | --- |
| 全部频道 | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/index.m3u` |
| 按国家和地区 | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/<code>.m3u` (例如 `my`, `id`, `vn`, `th`) |
| 按分类 | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/categories/<id>.m3u` (例如 `news`, `kids`, `sports`) |
| 按语言 | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/languages/<code>.m3u` (ISO 639-3 代码, 例如 `msa`, `ind`, `vie`) |
| 机器可读索引 | `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/index.json` |

### 热门国家和地区

- 马来西亚: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/my.m3u`
- 印度尼西亚: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/id.m3u`
- 越南: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/vn.m3u`
- 泰国: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/th.m3u`
- 菲律宾: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/ph.m3u`
- 新加坡: `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist/countries/sg.m3u`

备用镜像：如果 jsDelivr 在你的网络下访问慢或无法访问，把 `https://cdn.jsdelivr.net/gh/maweis1981/iptv-playlists@dist` 替换为 `https://raw.githubusercontent.com/maweis1981/iptv-playlists/dist`.

## 收录规则

1. 只收录由频道官方网站域名，或[白名单](policy/allowed-hosts.txt)中的正规广播 CDN、官方免费频道平台提供的直播流。
2. 不收录付费频道、成人内容和已停播频道。
3. 排除 iptv-org 屏蔽名单及我们[下架名单](policy/takedown.csv)中的频道。
4. 每日构建时无响应的直播流不会出现在列表中。

完整说明见 [POLICY.md](POLICY.md)。

## 数据来源

频道资料与链接来自社区项目 [iptv-org/database](https://github.com/iptv-org/database) 和 [iptv-org/iptv](https://github.com/iptv-org/iptv)，并按上述更严格的规则筛选。

## 版权投诉与下架

权利人可以通过[下架申请](https://github.com/maweis1981/iptv-playlists/issues/new?template=takedown.yml)要求移除某个频道或链接。我们会在 72 小时内处理，下一次每日构建即生效。

## 仓库结构

- `main` 分支：生成脚本 `scripts/build.py`、收录规则 `policy/` 和工作流。
- `dist` 分支：GitHub Actions 每日生成的播放列表，请勿手动修改。

## 参与贡献

欢迎通过 Pull Request 建议白名单域名，请说明它为何属于官方来源。频道资料的更正请提交到上游 [iptv-org/database](https://github.com/iptv-org/database)。

## 许可

[The Unlicense](LICENSE)（公有领域）。
