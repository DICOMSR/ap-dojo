"""
Firestoreにサンプルデータをアップロードするスクリプト（デバッグ版）
"""

import json
from pathlib import Path
import sys

print("=" * 80)
print("Firestore データアップロード（デバッグ版）")
print("=" * 80)

# Step 1: Firebase Admin SDKのインポート
print("\n[1] Firebase Admin SDKをインポート中...")
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    print("  ✓ インポート成功")
except ImportError as e:
    print(f"  ✗ インポートエラー: {e}")
    print("  pip install firebase-admin を実行してください")
    sys.exit(1)

# Step 2: serviceAccountKey.jsonの確認
print("\n[2] serviceAccountKey.jsonを確認中...")
cred_path = Path("serviceAccountKey.json")

if not cred_path.exists():
    print(f"  ✗ serviceAccountKey.jsonが見つかりません")
    print(f"  場所: {cred_path.absolute()}")
    sys.exit(1)
else:
    print(f"  ✓ ファイルが存在します: {cred_path.absolute()}")

# Step 3: Firebaseの初期化
print("\n[3] Firebaseを初期化中...")
try:
    # 既に初期化されている場合はスキップ
    if firebase_admin._apps:
        print("  ⚠ 既に初期化されています。既存の接続を使用します")
        app = firebase_admin.get_app()
    else:
        cred = credentials.Certificate(str(cred_path))
        app = firebase_admin.initialize_app(cred)
        print("  ✓ 初期化成功")
    
    db = firestore.client()
    print("  ✓ Firestoreに接続しました")
except Exception as e:
    print(f"  ✗ 初期化エラー: {e}")
    sys.exit(1)

# Step 4: データファイルの確認
print("\n[4] データファイルを確認中...")
data_file = Path("sample_questions.json")

if not data_file.exists():
    print(f"  ✗ sample_questions.jsonが見つかりません")
    print(f"  場所: {data_file.absolute()}")
    
    # 代替ファイルを探す
    alt_file = Path("parsed_questions/all_questions.json")
    if alt_file.exists():
        print(f"  ⚠ 代わりに {alt_file} を使用します")
        data_file = alt_file
    else:
        print("  ✗ 代替ファイルも見つかりません")
        sys.exit(1)
else:
    print(f"  ✓ ファイルが存在します: {data_file.absolute()}")

# Step 5: JSONファイルの読み込み
print("\n[5] JSONファイルを読み込み中...")
try:
    with open(data_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    print(f"  ✓ {len(questions)}問を読み込みました")
except Exception as e:
    print(f"  ✗ 読み込みエラー: {e}")
    sys.exit(1)

# Step 6: Firestoreにアップロード
print(f"\n[6] {len(questions)}問をアップロード中...")
success_count = 0
error_count = 0

for i, question in enumerate(questions, 1):
    try:
        doc_ref = db.collection('questions').document(question['questionId'])
        doc_ref.set(question)
        success_count += 1
        
        if i % 10 == 0:
            print(f"  {i}/{len(questions)}問完了...")
    except Exception as e:
        error_count += 1
        print(f"  ✗ {question['questionId']}のアップロード失敗: {e}")

print(f"\n✓ アップロード完了: {success_count}成功 / {error_count}失敗")
print("=" * 80)