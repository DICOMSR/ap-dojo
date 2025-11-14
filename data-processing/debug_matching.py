"""
解答PDFの抽出内容を確認
"""

from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
import re

# Tesseractのパス
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\10074256\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Users\10074256\Desktop\ap-dojo\poppler\Library\bin'

def extract_text_from_answer_pdf(pdf_path):
    """解答PDFからテキストを抽出"""
    print(f"PDFを処理中: {pdf_path.name}")
    
    images = convert_from_path(
        str(pdf_path),
        dpi=300,
        poppler_path=POPPLER_PATH
    )
    
    text = ""
    for image in images:
        page_text = pytesseract.image_to_string(image, lang='jpn')
        text += page_text + "\n"
    
    return text

def parse_answers(text):
    """解答を抽出（デバッグ版）"""
    print("\n【抽出されたテキスト（最初の1000文字）】")
    print("=" * 80)
    print(text[:1000])
    print("=" * 80)
    
    print("\n【正規表現でのマッチング】")
    
    patterns = [
        (r'問\s*(\d+)\s+([アイウエ])', "パターン1: 問\\s*(\\d+)\\s+([アイウエ])"),
        (r'(\d+)\s+([アイウエ])', "パターン2: (\\d+)\\s+([アイウエ])"),
        (r'問(\d+)[\\s　]*([アイウエ])', "パターン3: 問(\\d+)[\\s　]*([アイウエ])"),
    ]
    
    for pattern, desc in patterns:
        matches = re.findall(pattern, text)
        print(f"\n{desc}")
        print(f"  マッチ数: {len(matches)}")
        if matches:
            print(f"  最初の10個:")
            for i, match in enumerate(matches[:10]):
                print(f"    {i+1}. {match}")

def main():
    # R07秋期の解答PDFを確認
    answer_pdf = Path("downloaded_pdfs/R07_秋期_午前解答.pdf")
    
    if not answer_pdf.exists():
        print(f"✗ ファイルが見つかりません: {answer_pdf}")
        return
    
    text = extract_text_from_answer_pdf(answer_pdf)
    parse_answers(text)

if __name__ == "__main__":
    main()