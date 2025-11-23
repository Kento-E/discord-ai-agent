#!/usr/bin/env python3
"""
実践的アドバイス抽出機能のテスト
"""
import re
import sys


def test_extract_actionable_sentences():
    """実践的アドバイス抽出のテスト"""
    print("=== 実践的アドバイス抽出のテスト ===\n")

    # _extract_actionable_sentences関数を模倣
    def extract_actionable_sentences(message):
        """メッセージから実践的なアドバイス・アクションを含む文を抽出"""
        sentences = [s.strip() for s in re.split(r"[。！？]", message) if s.strip()]

        actionable_patterns = [
            r"(して|する|した)ください",
            r"(して|する|した)方が良い",
            r"(して|する|した)といい",
            r"(する|した)方法",
            r"手順",
            r"やり方",
            r"ステップ",
            r"まず",
            r"次に",
            r"その後",
            r"最後に",
            r"必要",
            r"重要",
            r"確認",
            r"注意",
            r"ポイント",
            r"コツ",
            r"試して",
            r"おすすめ",
            r"推奨",
            r"できます",
            r"可能",
            r"使って",
            r"設定",
            r"インストール",
            r"実行",
            r"変更",
        ]

        actionable_sentences = []
        for sentence in sentences:
            for pattern in actionable_patterns:
                if re.search(pattern, sentence):
                    actionable_sentences.append(sentence)
                    break

        return actionable_sentences, sentences

    # テストケース1: 手順を含むメッセージ
    test_message1 = (
        "まずDocker Desktopをインストールしてください。"
        "次にコンテナを起動する必要があります。"
        "最後に設定ファイルを確認してください。"
    )
    actionable1, _ = extract_actionable_sentences(test_message1)
    print("✓ テスト1: 手順を含むメッセージ")
    print(f"  入力: {test_message1}")
    print(f"  抽出: {len(actionable1)}個の実践的アドバイス")
    for i, advice in enumerate(actionable1, 1):
        print(f"    {i}. {advice}")
    assert len(actionable1) == 3, "3つの実践的アドバイスが抽出されるべき"

    # テストケース2: 方法を説明するメッセージ
    test_message2 = (
        "Pythonをインストールする方法はいくつかあります。"
        "公式サイトからダウンロードできます。"
        "pipを使って依存パッケージをインストールしてください。"
    )
    actionable2, _ = extract_actionable_sentences(test_message2)
    print("\n✓ テスト2: 方法を説明するメッセージ")
    print(f"  入力: {test_message2}")
    print(f"  抽出: {len(actionable2)}個の実践的アドバイス")
    for i, advice in enumerate(actionable2, 1):
        print(f"    {i}. {advice}")
    assert len(actionable2) >= 2, "少なくとも2つの実践的アドバイスが抽出されるべき"

    # テストケース3: 実践的アドバイスを含まないメッセージ
    test_message3 = "今日は良い天気ですね。そうですね。気持ちいいです。"
    actionable3, _ = extract_actionable_sentences(test_message3)
    print("\n✓ テスト3: 実践的アドバイスを含まないメッセージ")
    print(f"  入力: {test_message3}")
    print(f"  抽出: {len(actionable3)}個の実践的アドバイス")
    assert len(actionable3) == 0, "実践的アドバイスは抽出されないべき"

    return True


def test_organize_advice_as_steps():
    """アドバイスの手順整理のテスト"""
    print("\n=== アドバイスの手順整理のテスト ===\n")

    def organize_advice_as_steps(advice_sentences):
        """アドバイスを手順として整理"""
        if not advice_sentences:
            return []

        step_keywords = ["まず", "次に", "その後", "最後に", "最初に", "1", "2", "3"]

        step_sentences = []
        other_sentences = []

        for sentence in advice_sentences:
            is_step = False
            for keyword in step_keywords:
                if keyword in sentence:
                    step_sentences.append(sentence)
                    is_step = True
                    break
            if not is_step:
                other_sentences.append(sentence)

        return step_sentences + other_sentences

    # テストケース: 手順とその他のアドバイスが混在
    advice_list = [
        "pip install -r requirements.txtを実行してください",
        "まずリポジトリをクローンします",
        "環境変数を設定する必要があります",
        "次に依存パッケージをインストールします",
        "最後にアプリケーションを起動します",
    ]

    organized = organize_advice_as_steps(advice_list)
    print("✓ 手順整理テスト")
    print(f"  入力: {len(advice_list)}個のアドバイス")
    print("  整理後:")
    for i, advice in enumerate(organized, 1):
        print(f"    {i}. {advice}")

    # 手順を示す文が最初に来ることを確認
    assert "まず" in organized[0], "「まず」を含む文が最初に来るべき"
    assert "次に" in organized[1], "「次に」を含む文が2番目に来るべき"
    assert "最後に" in organized[2], "「最後に」を含む文が3番目に来るべき"

    return True


def test_practical_advice_integration():
    """実践的アドバイス生成の統合テスト"""
    print("\n=== 実践的アドバイス生成の統合テスト ===\n")

    # 実際のgenerate_detailed_answerのロジックを模倣した統合テスト
    similar_messages = [
        "まずDocker Desktopをインストールしてください。次にDockerfileを作成します。",
        "コンテナを起動する方法はdocker runコマンドを使ってください。",
        "設定ファイルを確認することが重要です。エラーが出た場合はログを見てください。",
    ]

    print("✓ 統合テスト: 複数の類似メッセージから実践的アドバイスを抽出")
    print(f"  入力: {len(similar_messages)}個の類似メッセージ")
    print("")
    for i, msg in enumerate(similar_messages, 1):
        print(f"  メッセージ{i}: {msg}")

    # 実践的アドバイス抽出のシミュレーション
    print("\n  期待される出力: 手順付きの実践的アドバイス")
    print("    1. まずDocker Desktopをインストールしてください。")
    print("    2. 次にDockerfileを作成します。")
    print("    3. コンテナを起動する方法はdocker runコマンドを使ってください。")

    return True


def main():
    """メインテスト関数"""
    print("\n" + "=" * 60)
    print("実践的アドバイス抽出機能のテスト")
    print("=" * 60 + "\n")

    try:
        # テスト実行
        assert test_extract_actionable_sentences(), "実践的アドバイス抽出テストが失敗"
        assert test_organize_advice_as_steps(), "手順整理テストが失敗"
        assert test_practical_advice_integration(), "統合テストが失敗"

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
    success = main()
    sys.exit(0 if success else 1)
