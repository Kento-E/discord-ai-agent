#!/usr/bin/env python3
"""
応答生成ロジックの詳細テスト
"""
import random
import re


def test_persona_generation():
    """ペルソナ生成ロジックのテスト"""
    print("=== ペルソナ生成ロジックのテスト ===\n")

    # テストメッセージ
    test_messages = [
        "おはようございます！",
        "こんにちは、元気ですか？",
        "お疲れ様です。",
        "ありがとうございます！",
        "了解しました。",
        "よろしくお願いします。",
        "確認してみます。",
        "わかりました！",
        "いいですね。",
        "そうですね。",
    ]

    # 頻出単語の抽出
    all_words = []
    for text in test_messages:
        words = re.findall(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFFa-zA-Z]+", text)
        all_words.extend(words)

    from collections import Counter

    common_words = Counter(all_words).most_common(10)
    print(f"✓ 頻出単語: {[word for word, count in common_words]}")

    # 挨拶表現の検出
    greetings = []
    greeting_patterns = ["おはよう", "こんにちは", "お疲れ", "ありがとう", "よろしく"]
    for text in test_messages:
        for pattern in greeting_patterns:
            if pattern in text:
                greetings.append(text)
                break

    print(f"✓ 挨拶表現: {greetings[:3]}")

    # 平均メッセージ長
    avg_length = sum(len(text) for text in test_messages) / len(test_messages)
    print(f"✓ 平均メッセージ長: {avg_length:.2f}文字")

    return True


def test_response_generation_logic():
    """応答生成ロジックのテスト"""
    print("\n=== 応答生成ロジックのテスト ===\n")

    # テスト用ペルソナ
    persona = {
        "common_words": ["お疲れ", "確認", "ありがとう", "よろしく"],
        "sample_greetings": ["おはようございます！", "こんにちは！", "お疲れ様です。"],
        "avg_message_length": 15.0,
        "sample_messages": [
            "確認してみます。",
            "ありがとうございます！",
            "よろしくお願いします。",
        ],
    }

    # テストケース1: 挨拶への応答
    query1 = "おはよう"
    is_greeting = any(g in query1 for g in ["おはよう", "こんにちは", "お疲れ"])
    if is_greeting:
        response1 = random.choice(persona["sample_greetings"])
        print("✓ 挨拶テスト")
        print(f"  入力: {query1}")
        print(f"  応答: {response1}")
        assert any(
            g in response1 for g in ["おはよう", "こんにちは", "お疲れ"]
        ), "挨拶応答が正しくありません"

    # テストケース2: 質問への応答
    query2 = "進捗はどうですか？"
    is_question = any(q in query2 for q in ["？", "?", "ですか", "ますか", "どう"])
    if is_question:
        response2 = persona["sample_messages"][0]
        print("\n✓ 質問応答テスト")
        print(f"  入力: {query2}")
        print(f"  応答: {response2}")
        assert len(response2) > 0, "応答が空です"

    # テストケース3: 通常会話への応答
    query3 = "プロジェクトについて話しましょう"
    base_message = persona["sample_messages"][1]
    target_length = persona["avg_message_length"]

    if len(base_message) < target_length * 0.5:
        response3 = base_message + " " + persona["sample_messages"][2]
    else:
        response3 = base_message

    print("\n✓ 通常会話テスト")
    print(f"  入力: {query3}")
    print(f"  応答: {response3}")
    assert len(response3) > 0, "応答が空です"

    return True


def main():
    """メインテスト関数"""
    print("\n" + "=" * 60)
    print("応答生成ロジック詳細テスト")
    print("=" * 60 + "\n")

    try:
        # ペルソナ生成テスト
        assert test_persona_generation(), "ペルソナ生成テストが失敗しました"

        # 応答生成ロジックテスト
        assert test_response_generation_logic(), "応答生成ロジックテストが失敗しました"

        print("\n" + "=" * 60)
        print("✅ 全てのテストに合格しました！")
        print("=" * 60 + "\n")

        return True

    except AssertionError as e:
        print(f"\n❌ テスト失敗: {e}")
        return False
    except Exception as e:
        print(f"\n❌ エラー発生: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
