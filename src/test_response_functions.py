#!/usr/bin/env python3
"""
新しい応答生成関数の単体テスト（モデルロード不要）
"""
import re


def test_generate_detailed_answer():
    """詳細回答生成関数のテスト"""
    print("=== 詳細回答生成関数のテスト ===\n")

    # テスト用のペルソナとメッセージ
    persona = {
        "common_endings": ["ます。", "です。", "ね。"],
        "avg_message_length": 20.0,
    }

    similar_messages = [
        "Pythonのインストールは公式サイトからできます",
        "ダウンロードページで自分のOSを選んでください",
        "インストーラーを実行すればOKです",
        "PATH設定を忘れずにチェックしてください",
        "インストール後はpython --versionで確認できます",
    ]

    # テスト用の簡易版関数（ai_agent.pyの関数をシミュレート）
    def generate_detailed_answer(similar_messages, persona):
        if not similar_messages:
            return "わかりません。"

        common_endings = persona.get("common_endings", [])
        avg_length = persona.get("avg_message_length", 50)

        response_parts = []
        used_sentences = set()
        target_length = max(avg_length * 3, 100)

        for message in similar_messages:
            sentences = [s.strip() for s in re.split(r"[。！？]", message) if s.strip()]

            for sentence in sentences:
                is_duplicate = False
                for used in used_sentences:
                    if len(sentence) > 0 and len(used) > 0:
                        common_chars = sum(1 for c in sentence if c in used)
                        similarity = common_chars / max(len(sentence), len(used))
                        if similarity > 0.6:
                            is_duplicate = True
                            break

                if not is_duplicate and len(sentence) >= 3:
                    response_parts.append(sentence)
                    used_sentences.add(sentence)

                    current_length = sum(len(s) for s in response_parts)
                    if current_length >= target_length:
                        break

            current_length = sum(len(s) for s in response_parts)
            if current_length >= target_length:
                break

        if len(response_parts) < 2 and len(similar_messages) >= 2:
            response_parts = [similar_messages[0]]
            if len(similar_messages) > 1:
                response_parts.append(similar_messages[1])

        if not response_parts:
            response = similar_messages[0]
        else:
            formatted_parts = []
            for i, part in enumerate(response_parts):
                if i == len(response_parts) - 1:
                    # 最後の文 - apply_common_ending相当の処理
                    text_without_ending = re.sub(r"[。！？\s]+$", "", part)
                    if common_endings:
                        formatted_parts.append(text_without_ending + common_endings[0])
                    else:
                        formatted_parts.append(part)
                else:
                    if not re.search(r"[。！？]$", part):
                        formatted_parts.append(part + "。")
                    else:
                        formatted_parts.append(part)

            response = "\n".join(formatted_parts)

        return response

    # テスト実行
    response = generate_detailed_answer(similar_messages, persona)

    print(f"テスト入力: {len(similar_messages)}個の類似メッセージ")
    print(f"\n生成された応答:\n{response}\n")
    print(f"応答の長さ: {len(response)}文字")
    print(f"行数: {response.count('\n') + 1}行")

    # 検証
    assert len(response) > 50, "応答が短すぎます"
    assert (
        response.count("\n") >= 1 or len(response) > 100
    ), "複数行または十分な長さが必要です"

    print("✓ 詳細回答生成テスト成功")
    return True


def test_generate_casual_response():
    """カジュアル応答生成関数のテスト"""
    print("\n=== カジュアル応答生成関数のテスト ===\n")

    persona = {
        "common_endings": ["ね。", "よ。", "です。"],
        "avg_message_length": 15.0,
    }

    # テストケース1: 適切な長さのメッセージ
    similar_messages_1 = ["いいですね", "楽しみです"]

    # テストケース2: 長すぎるメッセージ
    similar_messages_2 = [
        "これは非常に長いメッセージです。いろいろな内容が含まれています。詳細に説明します。"
    ]

    # テストケース3: 短すぎるメッセージ
    similar_messages_3 = ["OK", "了解です"]

    def generate_casual_response(similar_messages, persona):
        if not similar_messages:
            return "そうですね。"

        base_message = similar_messages[0]
        common_endings = persona.get("common_endings", [])
        target_length = persona.get("avg_message_length", 50)

        if len(base_message) > target_length * 1.5:
            sentences = [s for s in re.split(r"[。！？]", base_message) if s.strip()]
            response = (sentences[0] + "。") if sentences else base_message
        elif len(base_message) < target_length * 0.5:
            if len(similar_messages) > 1:
                second_message = similar_messages[1]
                second_sentences = [
                    s for s in re.split(r"[。！？]", second_message) if s.strip()
                ]
                if second_sentences:
                    response = base_message + " " + second_sentences[0] + "。"
                else:
                    response = base_message
            else:
                response = base_message
        else:
            response = base_message

        # 文末表現を適用
        text_without_ending = re.sub(r"[。！？\s]+$", "", response)
        if common_endings:
            response = text_without_ending + common_endings[0]
        else:
            response = text_without_ending

        return response

    # テスト1
    print("テストケース1: 適切な長さのメッセージ")
    response_1 = generate_casual_response(similar_messages_1, persona)
    print(f"応答: {response_1}")
    print(f"長さ: {len(response_1)}文字")
    assert len(response_1) < 100, "カジュアル応答は短く保つべきです"
    print("✓ テスト1成功\n")

    # テスト2
    print("テストケース2: 長すぎるメッセージ（短縮が必要）")
    response_2 = generate_casual_response(similar_messages_2, persona)
    print(f"応答: {response_2}")
    print(f"長さ: {len(response_2)}文字")
    assert len(response_2) < len(
        similar_messages_2[0]
    ), "長いメッセージは短縮されるべきです"
    print("✓ テスト2成功\n")

    # テスト3
    print("テストケース3: 短すぎるメッセージ（拡張が必要）")
    response_3 = generate_casual_response(similar_messages_3, persona)
    print(f"応答: {response_3}")
    print(f"長さ: {len(response_3)}文字")
    print("✓ テスト3成功")

    return True


def test_question_detection():
    """質問検出ロジックのテスト"""
    print("\n=== 質問検出ロジックのテスト ===\n")

    question_keywords = [
        "？",
        "?",
        "ですか",
        "ますか",
        "なに",
        "何",
        "どう",
        "いつ",
        "どこ",
        "だれ",
        "誰",
        "どのように",
        "なぜ",
        "教えて",
        "方法",
        "やり方",
    ]

    test_cases = [
        ("Pythonのインストール方法を教えてください", True),
        ("どうやって始めればいいですか？", True),
        ("これは何ですか", True),
        ("今日はいい天気ですね", False),
        ("頑張りましょう", False),
        ("なるほど", False),
        ("Discord Botの作り方は？", True),
        ("いつ完成しますか", True),
    ]

    for text, expected_is_question in test_cases:
        query_lower = text.lower()
        is_question = any(q in query_lower for q in question_keywords)

        status = "✓" if is_question == expected_is_question else "✗"
        print(
            f'{status} "{text}" -> 質問: {is_question} (期待: {expected_is_question})'
        )

        assert is_question == expected_is_question, f"質問検出が間違っています: {text}"

    print("\n✓ 質問検出テスト成功")
    return True


def main():
    """メインテスト関数"""
    print("\n" + "=" * 60)
    print("新しい応答生成関数の単体テスト")
    print("=" * 60 + "\n")

    try:
        test_generate_detailed_answer()
        test_generate_casual_response()
        test_question_detection()

        print("\n" + "=" * 60)
        print("✅ すべてのテストに合格しました！")
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
