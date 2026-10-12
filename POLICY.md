# 收录规则 · Inclusion policy

本目录只是一个索引：不存储、不转码、不转发任何视频，也不提供任何付费频道的访问方式。每条链接在每日构建时都要通过以下全部规则：

This directory is an index only: it stores, transcodes and relays no video and offers no access to paid channels. Every link must pass all of the rules below at each daily build:

1. **频道可识别** · The channel exists in [iptv-org/database](https://github.com/iptv-org/database) with a country and categories.
2. **非成人、未停播** · The channel is not marked NSFW, is not in the `xxx` category and has not closed.
3. **未被投诉** · The channel is not on the iptv-org blocklist (DMCA / NSFW) and is not on our own [takedown list](policy/takedown.csv).
4. **来源可信** · The stream is served either from the channel's own website domain, or from a host in [`policy/allowed-hosts.txt`](policy/allowed-hosts.txt) (broadcast-grade CDNs, official free ad-supported platforms, public access TV). Bare IP addresses, redirectors and unknown relay hosts are always left out.
5. **当前可用** · The stream responds when checked by the build (streams labelled geo-blocked are kept, because a build server cannot reach them).

修改白名单需提交 Pull Request 并说明理由。Changes to the allowlist go through a pull request with a short justification.

## 下架 · Takedown

提交[下架申请](https://github.com/maweis1981/iptv-playlists/issues/new?template=takedown.yml)，或在申请中注明频道 ID / 链接。处理后条目会写入 `policy/takedown.csv`，下一次构建即移除。

File a [takedown request](https://github.com/maweis1981/iptv-playlists/issues/new?template=takedown.yml) naming the channel ID or link. Once handled, the entry is added to `policy/takedown.csv` and disappears from the next build.
