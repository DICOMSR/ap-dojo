"""
既存のJSONファイルに解答データを追加
"""

import json
import re
from pathlib import Path

# R07秋期の解答データ（debug_matching.pyで取得済み）
ANSWERS_TEXT = """
問 1      エ     T       問 21     ア     T       問 41     ア     T       問 61     ア     S
問 2      イ     T       問 22     ウ     T       問 42     ア     T       問 62     エ     S
問 3      イ     T       問 23     エ     T       問 43     ウ     T       問 63     イ      S
問 4      ウ     T        問 24     ウ     T        問 44     イ      T        問 64     ウ     S
間 5      イ     T       問 25     ウ     T       問45 | ア     T       間65 | イ      S
問 6      イ     T       問 26     イ     T       問 46     エ     T       間 66     ウ     S
問 7      ア     T       問 27     エ     T       問 47     イ     T       問 67     ウ     S
問8      エ     T        問 28     ア     T        問 48     イ      T        問 68     イ      S
問 9      イ     T       問 29     イ     T       問 49     エ     T       間 69     ア     S
問 10     ア     T       問 30     ウ     T       問 50     エ     T       問 70     イ     S
"""

def parse_answers_from_text(text):
    """テキストから解答を抽出"""
    # 前処理
    text = text.replace('間', '問')
    
    answers = {}
    pattern = r'問\s*(\d+)\s+([アイウエ])'
    matches = re.findall(pattern, text)
    
    answer_map = {"ア": "a", "イ": "b", "ウ": "c", "エ": "d"}
    
    for q_num, ans in matches:
        answers[int(q_num)] = answer_map[ans]
    
    return answers

def update_json_with_answers(json_file, answers):
    """JSONファイルに解答を追加"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updated = 0
    for question in data:
        q_num = question['questionNumber']
        if q_num in answers:
            question['correctAnswer'] = answers[q_num]
            updated += 1
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ {updated}問の正解を更新しました")

def main():
    # 解答を抽出
    answers = parse_answers_from_text(ANSWERS_TEXT)
    print(f"抽出した解答数: {len(answers)}")
    
    # JSONファイルを更新
    json_file = Path("parsed_questions/R07_秋期.json")
    if json_file.exists():
        update_json_with_answers(json_file, answers)
        
        # Firestoreに再アップロード
        print("\nFirestoreに再アップロードしますか？ (y/n)")
        # ここでは手動で upload_to_firebase.py を実行
    else:
        print(f"✗ {json_file} が見つかりません")

if __name__ == "__main__":
    main()