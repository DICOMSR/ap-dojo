"""
Firestoreの全questionsデータを削除
"""

import firebase_admin
from firebase_admin import credentials, firestore

def delete_collection(db, collection_name, batch_size=500):
    """コレクションの全ドキュメントを削除"""
    collection_ref = db.collection(collection_name)
    
    deleted = 0
    while True:
        # batch_size件ずつ取得
        docs = collection_ref.limit(batch_size).stream()
        docs_list = list(docs)
        
        if not docs_list:
            break
        
        # バッチで削除
        batch = db.batch()
        for doc in docs_list:
            batch.delete(doc.reference)
            deleted += 1
        
        batch.commit()
        print(f"  {deleted}件削除...")
    
    return deleted

def main():
    print("=" * 80)
    print("Firestore データ削除")
    print("=" * 80)
    
    # 初期化
    cred_path = "serviceAccountKey.json"
    
    try:
        # 既に初期化されている場合はスキップ
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("✓ Firebaseに接続しました\n")
        
        # 確認
        print("⚠️  警告: questionsコレクションの全データを削除します")
        print("この操作は取り消せません。\n")
        
        response = input("続行しますか？ (yes/no): ").strip().lower()
        
        if response != "yes":
            print("\n✗ 削除をキャンセルしました")
            return
        
        # 削除実行
        print("\n削除中...")
        deleted = delete_collection(db, "questions")
        
        print(f"\n✓ {deleted}件のドキュメントを削除しました")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ エラー: {e}")

if __name__ == "__main__":
    main()