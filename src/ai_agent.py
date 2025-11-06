import json
import os
from sentence_transformers import SentenceTransformer, util

EMBED_PATH = os.path.join(os.path.dirname(__file__), '../data/embeddings.json')
model = SentenceTransformer('all-MiniLM-L6-v2')

# 埋め込みデータのロード
with open(EMBED_PATH, 'r') as f:
    dataset = json.load(f)

texts = [item['text'] for item in dataset]
embeddings = [item['embedding'] for item in dataset]

# ユーザーの質問に最も近いメッセージを返す

def search_similar_message(query, top_k=3):
    query_emb = model.encode(query)
    scores = util.cos_sim(query_emb, embeddings)[0]
    top_results = scores.argsort(descending=True)[:top_k]
    return [texts[i] for i in top_results]

# テスト用
if __name__ == '__main__':
    q = input('質問を入力してください: ')
    results = search_similar_message(q)
    print('類似メッセージ:')
    for r in results:
        print('-', r)
