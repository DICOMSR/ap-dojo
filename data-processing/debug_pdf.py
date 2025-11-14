"""
PDFの内容を確認するデバッグスクリプト
"""

from pathlib import Path
from PyPDF2 import PdfReader

INPUT_DIR = Path("downloaded_pdfs")

def check_pdf_content():
    # 最初のPDFファイルを確認
    pdf_files = list(INPUT_DIR.glob("*_午前問題.pdf"))
    
    if not pdf_files:
        print("PDFファイルが見つかりません")
        return
    
    # 最初のファイルを選択
    pdf_file = pdf_files[0]
    print(f"確認するファイル: {pdf_file.name}")
    print("=" * 80)
    
    try:
        reader = PdfReader(pdf_file)
        print(f"総ページ数: {len(reader.pages)}")
        print()
        
        # 最初の3ページの内容を表示
        for i in range(min(3, len(reader.pages))):
            print(f"\n--- ページ {i+1} ---")
            text = reader.pages[i].extract_text()
            # 最初の1000文字だけ表示
            print(text[:1000])
            print("...")
            print()
        
        # 解答PDFも確認
        answer_file = str(pdf_file).replace('問題', '解答')
        answer_path = Path(answer_file)
        
        if answer_path.exists():
            print("\n" + "=" * 80)
            print(f"解答ファイル: {answer_path.name}")
            print("=" * 80)
            
            reader = PdfReader(answer_path)
            print(f"総ページ数: {len(reader.pages)}")
            
            # 最初のページの内容を表示
            text = reader.pages[0].extract_text()
            print(text[:1000])
            print("...")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    check_pdf_content()