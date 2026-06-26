"""
MakeMeAHanzi Data Importer

Reads the raw MakeMeAHanzi dataset (jsonl) and converts it into
Chinese Chars' internal storage format. This script runs ONLY once (or when data is updated).
It is NOT used by the main workbook generator.
"""

import json
import sys
from pathlib import Path

# ── Constants ────────────────────────────────────────────────

RAW_DATA_PATH = Path("/home/yli/Dropbox/github/makemeahanzi/graphics.txt")
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "generated" / "characters"


def parse_svg_path(path_str: str) -> list[float]:
    """
    Extract coordinates from MakeMeAHanzi SVG path data (e.g. 'M 10 20 L 15 ... Z').
    Converts it to a flat list of float coordinates [x1, y1, x2, y2, ...].
    """
    clean_path = path_str.replace("Z", "").replace("L", " ").replace("M", " ").replace("Q", " ")
    return [float(c) for c in clean_path.split() if c.strip().lstrip('-').isdigit() or (c.startswith('-') and c[1:].lstrip('.').isdigit())]


def import_data() -> None:
    print(f"📥 正在读取原始数据：{RAW_DATA_PATH}")
    
    if not RAW_DATA_PATH.exists():
        print(f"❌ 错误：找不到文件 {RAW_DATA_PATH}。请先下载 MakeMeAHanzi 并更新路径。")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_imported = 0
    error_count = 0
    
    with open(RAW_DATA_PATH, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                obj = json.loads(line) # MakeMeAHanzi is JSON-Lines
                
                char = obj.get("character")
                strokes_data = obj.get("strokes", [])
                
                if not char or not strokes_data:
                    sys.stderr.write(f"⚠️ 跳过第 {line_num} 行：缺失字符或笔画数据\n")
                    error_count += 1
                    continue
                
                # Internal Format Conversion
                internal_strokes = []
                for order_idx, svg_path in enumerate(strokes_data):
                    flat_points = parse_svg_path(svg_path)
                    if len(flat_points) >= 4: # Must have at least one segment (2 points)
                        internal_strokes.append({
                            "order": order_idx + 1,
                            "path": [round(p, 2) for p in flat_points]
                        })
                
                # Save to the target folder using the internal JSON schema
                output_file = OUTPUT_DIR / f"{char}.json"
                with open(output_file, 'w', encoding='utf-8') as out:
                    json.dump({
                        "character": char,
                        "stroke_count": len(internal_strokes),
                        "strokes": internal_strokes
                    }, out, ensure_ascii=False, indent=2)
                
                total_imported += 1
                
            except (json.JSONDecodeError, ValueError) as e:
                sys.stderr.write(f"⚠️ 解析第 {line_num} 行失败：{e}\n")
                error_count += 1

    print(f"✅ 导入完成：成功 {total_imported} | 跳过/错误 {error_count}")


if __name__ == "__main__":
    import_data()
