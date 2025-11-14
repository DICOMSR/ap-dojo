"""
IPA過去問PDFから問題を抽出（pytesseract版）
"""

import re
import json
from pathlib import Path
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Tesseractのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\10074256\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Popplerのパスを設定
POPPLER_PATH = r'C:\Users\10074256\Desktop\ap-dojo\poppler\Library\bin'  # ← 実際のパスに変更

INPUT_DIR = Path("downloaded_pdfs")
OUTPUT_DIR = Path("parsed_questions")
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """PDFからテキストを抽出（OCR対応）"""
    try:
        # まずPyPDF2で試す
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # テキストが十分に抽出できた場合
        if len(text.strip()) > 1000:
            print(f"    ✓ PyPDF2で抽出成功")
            return text
        else:
            print(f"    ⚠ テキストPDFではない、OCR実行中...")
            return extract_with_ocr(pdf_path)
            
    except Exception as e:
        print(f"    ⚠ エラー: {e}")
        print(f"    OCR実行中...")
        return extract_with_ocr(pdf_path)

def extract_with_ocr(pdf_path):
    """OCRでPDFからテキストを抽出"""
    try:
        print(f"    OCR処理中（時間がかかります）...")
        
        # PDFを画像に変換
        images = convert_from_path(
            str(pdf_path),
            dpi=300,  # 高解像度で変換
            poppler_path=POPPLER_PATH,
            first_page=1,
            last_page=None  # すべてのページ
        )
        
        print(f"    {len(images)}ページを処理中...")
        
        text = ""
        for i, image in enumerate(images):
            # 日本語OCR
            page_text = pytesseract.image_to_string(
                image,
                lang='jpn',  # 日本語
                config='--psm 6'  # ページセグメンテーションモード
            )
            text += page_text + "\n"
            
            if (i + 1) % 10 == 0:
                print(f"      {i + 1}/{len(images)}ページ完了")
        
        print(f"    ✓ OCRで{len(text)}文字を抽出")
        return text
        
    except Exception as e:
        print(f"    ✗ OCRエラー: {e}")
        return None

def parse_am_questions(text, year, season):
    """問題データを抽出"""
    questions = []
    
    pattern = r'問\s*(\d+)\s+'
    splits = re.split(pattern, text)
    
    for i in range(1, len(splits), 2):
        if i + 1 >= len(splits):
            break
        
        question_num = splits[i].strip()
        question_content = splits[i + 1]
        
        choices = extract_choices(question_content)
        
        if choices and len(choices) == 4:
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
                "correctAnswer": None,
                "category": None,
                "subcategory": None,
                "difficulty": None,
                "explanation": None,
            }
            questions.append(question_data)
    
    return questions

def extract_choices(text):
    """選択肢を抽出"""
    choices = []
    markers = ['ア', 'イ', 'ウ', 'エ']
    
    for i, marker in enumerate(markers):
        if i < len(markers) - 1:
            next_marker = markers[i + 1]
            pattern = f'{marker}[\\s　]+(.+?)(?={next_marker}|\\Z)'
        else:
            pattern = f'{marker}[\\s　]+(.+?)(?=\\n\\n|\\Z)'
        
        match = re.search(pattern, text, re.DOTALL)
        if match:
            choice_text = match.group(1).strip()
            choice_text = re.sub(r'\s+', ' ', choice_text)
            choices.append(choice_text)
    
    return choices

def clean_question_text(full_text, choices):
    """問題文を抽出"""
    idx = full_text.find('ア')
    if idx != -1:
        question_text = full_text[:idx].strip()
        question_text = re.sub(r'\s+', ' ', question_text)
        return question_text
    return full_text.strip()

def parse_am_answers(text, year, season):
    """正解を抽出"""
    answers = {}
    
    patterns = [
        r'問\s*(\d+)\s+([アイウエ])',
        r'(\d+)\s+([アイウエ])',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            for question_num, answer in matches:
                question_id = f"{year}_{season}_Q{question_num.zfill(2)}"
                answer_map = {"ア": "a", "イ": "b", "ウ": "c", "エ": "d"}
                answers[question_id] = answer_map.get(answer)
            break
    
    return answers

def merge_questions_and_answers(questions, answers):
    """正解を設定"""
    for question in questions:
        question_id = question["questionId"]
        if question_id in answers:
            question["correctAnswer"] = answers[question_id]
    return questions

def process_exam_pair(year, season):
    """1回分を処理"""
    print(f"\n【{year} {season}】")
    
    question_pdf = INPUT_DIR / f"{year}_{season}_午前問題.pdf"
    answer_pdf = INPUT_DIR / f"{year}_{season}_午前解答.pdf"
    
    if not question_pdf.exists() or not answer_pdf.exists():
        print(f"  ✗ PDFが見つかりません")
        return None
    
    print(f"  問題PDFを処理中...")
    question_text = extract_text_from_pdf(question_pdf)
    
    print(f"  解答PDFを処理中...")
    answer_text = extract_text_from_pdf(answer_pdf)
    
    if not question_text or not answer_text:
        return None
    
    print(f"  問題をパース中...")
    questions = parse_am_questions(question_text, year, season)
    print(f"    ✓ {len(questions)}問を抽出")
    
    print(f"  解答をパース中...")
    answers = parse_am_answers(answer_text, year, season)
    print(f"    ✓ {len(answers)}問の正解を抽出")
    
    questions = merge_questions_and_answers(questions, answers)
    
    with_answer = sum(1 for q in questions if q['correctAnswer'])
    print(f"    ✓ {with_answer}/{len(questions)}問に正解を設定")
    
    output_file = OUTPUT_DIR / f"{year}_{season}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ 保存完了: {output_file.name}")
    
    return questions

def main():
    """メイン処理"""
    print("=" * 80)
    print("IPA過去問 PDFパース処理（pytesseract版）")
    print("=" * 80)
    
    pdf_files = list(INPUT_DIR.glob("*_午前問題.pdf"))
    
    if not pdf_files:
        print("\n✗ PDFファイルが見つかりません")
        return
    
    print(f"\n{len(pdf_files)}回分の試験を発見しました")
    
    # 全回分を処理
    exam_pairs = []
    for pdf_file in pdf_files:  # 全部処理
        filename = pdf_file.stem
        parts = filename.split('_')
        if len(parts) >= 2:
            exam_pairs.append((parts[0], parts[1]))

    exam_pairs = list(set(exam_pairs))
    exam_pairs.sort(reverse=True)  # 新しい順

    
    all_questions = []
    success_count = 0

    for year, season in exam_pairs:
        questions = process_exam_pair(year, season)
        if questions and len(questions) > 0:
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
        print(f"  統合ファイル: {all_file.name}")
        print("=" * 80)
    else:
        print("\n✗ パースに失敗しました")

if __name__ == "__main__":
    main()