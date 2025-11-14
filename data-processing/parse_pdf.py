"""
IPA応用情報技術者試験の過去問PDFから問題・選択肢・正解を抽出するスクリプト

使い方:
1. download_ipa_exams.pyでPDFをダウンロード済みであること
2. python parse_pdf.py を実行
3. parsed_questions/ フォルダにJSONファイルが出力される
"""

import re
import json
from pathlib import Path
from PyPDF2 import PdfReader
import sys

# 入力・出力フォルダ
INPUT_DIR = Path("downloaded_pdfs")
OUTPUT_DIR = Path("parsed_questions")
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """PDFからテキストを抽出"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"  ✗ PDFの読み込みエラー: {e}")
        return None

def parse_am_questions(text, year, season):
    """
    午前問題のテキストから問題データを抽出
    
    フォーマット:
    問1 問題文...
    
    ア 選択肢A
    イ 選択肢B
    ウ 選択肢C
    エ 選択肢D
    """
    questions = []
    
    # 「問」で分割
    # 問1、問2...問80 のパターンを探す
    pattern = r'問\s*(\d+)\s+'
    splits = re.split(pattern, text)
    
    # splits[0]は前置き、その後は [問番号, 問題本文, 問番号, 問題本文, ...]
    for i in range(1, len(splits), 2):
        if i + 1 >= len(splits):
            break
        
        question_num = splits[i].strip()
        question_content = splits[i + 1]
        
        # 選択肢を抽出
        choices = extract_choices(question_content)
        
        if choices and len(choices) == 4:
            # 選択肢を除いた問題文を取得
            question_text = clean_question_text(question_content, choices)
            
            question_data = {
                "questionId": f"{year}_{season}_Q{question_num.zfill(2)}",
                "examYear": year,
                "examSeason": season,
                "questionNumber": int(question_num),
                "questionText": question_text,
                "choices": {
                    "a": choices[0],
                    "b": choices[1],
                    "c": choices[2],
                    "d": choices[3]
                },
                "correctAnswer": None,  # 後で解答PDFから追加
                "category": None,
                "subcategory": None,
                "difficulty": None,
                "explanation": None,
            }
            questions.append(question_data)
        else:
            # 選択肢が4つでない場合はスキップ（デバッグ用に出力）
            if len(question_num) <= 2:  # 問番号が妥当な場合のみ警告
                print(f"    ⚠ 問{question_num}: 選択肢が{len(choices)}個（スキップ）")
    
    return questions

def extract_choices(text):
    """問題文から選択肢（ア、イ、ウ、エ）を抽出"""
    choices = []
    
    # 選択肢を示すカタカナ
    markers = ['ア', 'イ', 'ウ', 'エ']
    
    for i, marker in enumerate(markers):
        # 次のマーカーまでを抽出
        if i < len(markers) - 1:
            next_marker = markers[i + 1]
            pattern = f'{marker}[\\s　]+(.+?)(?={next_marker}|\\Z)'
        else:
            # 最後の選択肢
            pattern = f'{marker}[\\s　]+(.+?)(?=\\n\\n|\\Z)'
        
        match = re.search(pattern, text, re.DOTALL)
        if match:
            choice_text = match.group(1).strip()
            # 改行や余分な空白を整理
            choice_text = re.sub(r'\s+', ' ', choice_text)
            choices.append(choice_text)
    
    return choices

def clean_question_text(full_text, choices):
    """選択肢部分を除いた問題文を抽出"""
    # 最初の選択肢（ア）の前までを問題文とする
    idx = full_text.find('ア')
    if idx != -1:
        question_text = full_text[:idx].strip()
        # 余分な空白や改行を整理
        question_text = re.sub(r'\s+', ' ', question_text)
        return question_text
    
    return full_text.strip()

def parse_am_answers(text, year, season):
    """
    午前解答PDFから正解を抽出
    
    フォーマット:
    問1 イ
    問2 ウ
    ...
    """
    answers = {}
    
    # 「問[数字] [ア-エ]」のパターンを抽出
    # 複数の形式に対応
    patterns = [
        r'問\s*(\d+)\s+([アイウエ])',
        r'(\d+)\s+([アイウエ])',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            for question_num, answer in matches:
                question_id = f"{year}_{season}_Q{question_num.zfill(2)}"
                # カタカナをアルファベットに変換
                answer_map = {"ア": "a", "イ": "b", "ウ": "c", "エ": "d"}
                answers[question_id] = answer_map.get(answer)
            break  # 最初にマッチしたパターンを使用
    
    return answers

def merge_questions_and_answers(questions, answers):
    """問題データに正解を追加"""
    for question in questions:
        question_id = question["questionId"]
        if question_id in answers:
            question["correctAnswer"] = answers[question_id]
    
    return questions

def process_exam_pair(year, season):
    """1回分の試験（問題+解答）を処理"""
    print(f"\n【{year} {season}】")
    
    # ファイルパス
    question_pdf = INPUT_DIR / f"{year}_{season}_午前問題.pdf"
    answer_pdf = INPUT_DIR / f"{year}_{season}_午前解答.pdf"
    
    if not question_pdf.exists():
        print(f"  ✗ 問題PDFが見つかりません: {question_pdf}")
        return None
    
    if not answer_pdf.exists():
        print(f"  ✗ 解答PDFが見つかりません: {answer_pdf}")
        return None
    
    # PDFからテキスト抽出
    print(f"  問題PDFを読み込み中...")
    question_text = extract_text_from_pdf(question_pdf)
    
    print(f"  解答PDFを読み込み中...")
    answer_text = extract_text_from_pdf(answer_pdf)
    
    if not question_text or not answer_text:
        return None
    
    # 問題をパース
    print(f"  問題をパース中...")
    questions = parse_am_questions(question_text, year, season)
    print(f"    ✓ {len(questions)}問を抽出")
    
    # 解答をパース
    print(f"  解答をパース中...")
    answers = parse_am_answers(answer_text, year, season)
    print(f"    ✓ {len(answers)}問の正解を抽出")
    
    # マージ
    questions = merge_questions_and_answers(questions, answers)
    
    # 正解が設定された問題数を確認
    with_answer = sum(1 for q in questions if q['correctAnswer'])
    print(f"    ✓ {with_answer}/{len(questions)}問に正解を設定")
    
    # JSON出力
    output_file = OUTPUT_DIR / f"{year}_{season}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ 保存完了: {output_file.name}")
    
    return questions

def main():
    """メイン処理"""
    print("=" * 80)
    print("IPA過去問 PDFパース処理")
    print("=" * 80)
    
    # ダウンロード済みのPDFファイルを確認
    pdf_files = list(INPUT_DIR.glob("*_午前問題.pdf"))
    
    if not pdf_files:
        print("\n✗ PDFファイルが見つかりません")
        print(f"  {INPUT_DIR.absolute()} にPDFをダウンロードしてください")
        return
    
    print(f"\n{len(pdf_files)}回分の試験を発見しました")
    
    # 年度と期を抽出
    exam_pairs = []
    for pdf_file in pdf_files:
        filename = pdf_file.stem
        parts = filename.split('_')
        if len(parts) >= 2:
            year = parts[0]
            season = parts[1]
            exam_pairs.append((year, season))
    
    # 重複を除去してソート
    exam_pairs = list(set(exam_pairs))
    exam_pairs.sort(reverse=True)  # 新しい順
    
    print(f"処理対象: {len(exam_pairs)}回分")
    print()
    
    # 各試験を処理
    all_questions = []
    success_count = 0
    
    for year, season in exam_pairs:
        questions = process_exam_pair(year, season)
        if questions:
            all_questions.extend(questions)
            success_count += 1
    
    # 全問題を1つのファイルにまとめる
    if all_questions:
        all_file = OUTPUT_DIR / "all_questions.json"
        with open(all_file, 'w', encoding='utf-8') as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 80)
        print(f"✓ パース完了")
        print(f"  処理成功: {success_count}/{len(exam_pairs)}回")
        print(f"  総問題数: {len(all_questions)}問")
        print(f"  個別ファイル: {OUTPUT_DIR.absolute()}")
        print(f"  統合ファイル: {all_file.name}")
        print("=" * 80)
        print("\n次のステップ:")
        print("  1. parsed_questions/all_questions.json を確認")
        print("  2. python categorize_questions.py（問題の分類）")
        print("  3. python upload_to_firebase.py（Firebaseアップロード）")
    else:
        print("\n✗ パースに失敗しました")
        print("  PDFの形式を確認してください")

if __name__ == "__main__":
    main()