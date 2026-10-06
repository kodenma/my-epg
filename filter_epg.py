import gzip
import re
import xml.etree.ElementTree as ET

# ==============================================================
# Custom_JP1.xml に完全準拠したチャンネル定義マッピング
# ==============================================================
TARGET_CHANNELS = [
    # 地上波キー局
    {"match": r"NHK.*総合", "id": "JOAKDTV.jp", "name": "NHK総合 (東京)"},
    {"match": r"NHK.*(Eテレ|教育)", "id": "JOABDTV.jp", "name": "NHK Eテレ（東京）"},
    {"match": r"日本テレビ|日テレ", "id": "JOAXDTV.jp", "name": "日本テレビ"},
    {"match": r"テレビ朝日|テレ朝", "id": "JOEXDTV.jp", "name": "テレビ朝日"},
    {"match": r"TBS", "id": "JORXDTV.jp", "name": "TBSテレビ"},
    {"match": r"テレビ東京|テレ東", "id": "JOTXDTV.jp", "name": "テレビ東京"},
    {"match": r"フジテレビ", "id": "JOCXDTV.jp", "name": "フジテレビ"},
    {"match": r"TOKYO\s*MX|東京MX", "id": "TOKYOMX.jp", "name": "TOKYO MX チャンネル"},

    # BSデジタル
    {"match": r"NHK\s*BS(?!P|4K)", "id": "NHKBS.jp", "name": "NHK BS"},
    {"match": r"NHK\s*(BSP4K|BS4K)", "id": "NHKBSP4K.jp", "name": "NHK BSP4K"},
    {"match": r"BS日テレ", "id": "BSNipponTV.jp", "name": "BS日テレ"},
    {"match": r"BS朝日", "id": "BSAsahi.jp", "name": "BS朝日"},
    {"match": r"BS-TBS", "id": "BSTBS.jp", "name": "BS-TBS"},
    {"match": r"BSテレ東", "id": "BSTVTokyo.jp", "name": "BSテレ東"},
    {"match": r"BSフジ", "id": "BSFuji.jp", "name": "BSフジ"},
    {"match": r"WOWOW\s*プライム", "id": "WOWOWPrime.jp", "name": "WOWOWプライム"},
    {"match": r"WOWOW\s*ライブ", "id": "WOWOWLive.jp", "name": "WOWOWライブ"},
    {"match": r"WOWOW\s*シネマ", "id": "WOWOWCinema.jp", "name": "WOWOWシネマ"},
    {"match": r"BS10(?!スター)", "id": "jcom_120_110_4", "name": "BS10"},
    {"match": r"スター\s*チャンネル|BS10スター", "id": "jcom_120_200_4", "name": "BS10スターチャンネル"},

    # CS・専門・スポーツ
    {"match": r"アニマックス|Animax", "id": "AnimaxAsia.sg@Japan", "name": "アニマックス"},
    {"match": r"J\s*SPORTS\s*1", "id": "JSPORTS1.jp", "name": "J SPORTS 1"},
    {"match": r"J\s*SPORTS\s*2", "id": "JSPORTS2.jp", "name": "J SPORTS 2"},
    {"match": r"J\s*SPORTS\s*3", "id": "JSPORTS3.jp", "name": "J SPORTS 3"},
    {"match": r"J\s*SPORTS\s*4", "id": "JSPORTS4.jp", "name": "J SPORTS 4"},
    {"match": r"ショップチャンネル", "id": "ShopChannel.jp", "name": "ショップチャンネル"},
    {"match": r"QVC", "id": "QVC.jp", "name": "QVC"},
    {"match": r"GSTV", "id": "GSTV.jp", "name": "GSTV"},
    {"match": r"NHK\s*WORLD", "id": "NHKWorldJapan.jp", "name": "NHK WORLD JAPAN"},

    # ニュース・配信チャンネル
    {"match": r"ウェザーニュース", "id": "rch_45", "name": "ウェザーニュースLiVE"},
    {"match": r"日テレNEWS|日テレニュース", "id": "rch_47", "name": "日テレNEWS"},
    {"match": r"FNNプライム", "id": "rch_108", "name": "FNNプライムオンライン"},
    {"match": r"MBSニュース", "id": "rch_115", "name": "MBSニュース"},
]

RAW_XML = "public/raw_epg.xml"
OUTPUT_XML = "public/epg.xml"


def process():
    print(f"Reading {RAW_XML}...")
    tree = ET.parse(RAW_XML)
    root = tree.getroot()

    old_id_to_target = {}
    matched_target_ids = set()

    # 新しいルート要素の準備
    new_root = ET.Element("tv", root.attrib)

    # 1. チャンネルのマッチングと定義作成
    for channel in root.findall("channel"):
        old_id = channel.get("id")
        disp_names = [dn.text for dn in channel.findall("display-name") if dn.text]

        for target in TARGET_CHANNELS:
            target_id = target["id"]
            if target_id in matched_target_ids:
                continue

            matched = False
            for dn in disp_names:
                if re.search(target["match"], dn, re.IGNORECASE):
                    matched = True
                    break

            if matched:
                old_id_to_target[old_id] = target
                matched_target_ids.add(target_id)

                # Custom_JP1.xml と完全同一のタグ構造を作成
                new_ch = ET.SubElement(new_root, "channel", id=target["id"])
                dn_elem = ET.SubElement(new_ch, "display-name", lang="ja")
                dn_elem.text = target["name"]
                url_elem = ET.SubElement(new_ch, "url")
                url_elem.text = "http://www.tvkingdom.jp"

                print(f"[Match] '{disp_names[0]}' -> id='{target['id']}' name='{target['name']}'")
                break

    # 2. 番組データ (<programme>) の抽出と channel 属性の書換え
    prog_count = 0
    for prog in root.findall("programme"):
        ch_id = prog.get("channel")
        if ch_id in old_id_to_target:
            target = old_id_to_target[ch_id]
            prog.set("channel", target["id"])
            new_root.append(prog)
            prog_count += 1

    print("--------------------------------------------------")
    print(f"Matched channels: {len(matched_target_ids)} / {len(TARGET_CHANNELS)}")
    print(f"Total programmes extracted: {prog_count}")

    # 3. XML保存
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space="  ", level=0)
    new_tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
    print(f"Saved custom EPG to {OUTPUT_XML}")


if __name__ == "__main__":
    process()
