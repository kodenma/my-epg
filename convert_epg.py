import urllib.request

# EPG(guides.xml)の channel id -> プレイリスト(m3u8)の tvg-id への置換マップ
ID_MAP = {
    "NHK東京・総合_jp": "JOAKDTV.jp",
    "NHK東京・教育_jp": "JOABDTV.jp",
    "日本テレビ_jp": "JOAXDTV.jp",
    "テレビ朝日_jp": "JOEXDTV.jp",
    "TBS_jp": "JORXDTV.jp",
    "テレ東_jp": "JOTXDTV.jp",
    "フジテレビ_jp": "JOCXDTV.jp",
    "NHK・BS_jp": "NHKBS.jp",
    "BS日テレ_jp": "BSNipponTV.jp",
    "BS朝日_jp": "BSAsahi.jp",
    "BS-TBS_jp": "BSTBS.jp",
    "BSテレ東_jp": "BSTVTokyo.jp",
    "BSフジ_jp": "BSFuji.jp",
    "WOWOWプライム_jp": "WOWOWPrime.jp",
    "BS10_jp": "jcom_120_110_4",
    "ショップチャンネル_jp": "ShopChannel.jp",
    "QVC_jp": "QVC.jp",
    "ジュエリー☆GSTV_jp": "GSTV.jp",
}

SOURCE_URL = "https://raw.githubusercontent.com/karenda-jp/etc/refs/heads/main/guides.xml"

def main():
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    content = urllib.request.urlopen(req).read().decode('utf-8')

    for old_id, new_id in ID_MAP.items():
        content = content.replace(f'channel="{old_id}"', f'channel="{new_id}"')
        content = content.replace(f'id="{old_id}"', f'id="{new_id}"')

    with open("converted_guides.xml", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
