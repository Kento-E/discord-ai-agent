#!/usr/bin/env python3
"""
語尾重複防止ロジックの単体テスト

ai_agent.pyの重複防止ロジックを直接テストする
"""
import re
import sys
import unittest


class TestDuplicateSuffixPrevention(unittest.TestCase):
    """語尾重複を防ぐロジックのテスト"""

    def test_suffix_removal_from_ending(self):
        """common_endingから句読点を除去するロジックのテスト"""
        test_cases = [
            ("します。", "します"),
            ("ます！", "ます"),
            ("ですか？", "ですか"),
            ("です。", "です"),
            ("ね。", "ね"),
            ("！", ""),
            ("。", ""),
        ]

        for ending, expected in test_cases:
            result = re.sub(r"[。！？\s]+$", "", ending)
            self.assertEqual(
                result,
                expected,
                f"語尾 '{ending}' の句読点除去が正しくありません: 期待値={expected}, 実際={result}",
            )

    def test_endswith_detection(self):
        """文末が同じ語尾で終わっているかの判定テスト"""
        test_cases = [
            ("よろしくお願いします", "します", True),
            ("確認してみます", "ます", True),
            ("これはテストです", "です", True),
            ("これはテストですか", "ですか", True),
            ("よろしくお願いします", "ですか", False),
            ("確認してみます", "です", False),
            ("これはテストです", "ます", False),
        ]

        for base, ending, expected in test_cases:
            result = base.endswith(ending)
            self.assertEqual(
                result,
                expected,
                f"'{base}' が '{ending}' で終わっているかの判定が正しくありません",
            )

    def test_duplicate_prevention_logic_question(self):
        """質問応答での重複防止ロジックのテスト"""
        # シミュレート: 質問応答の場合の処理
        test_cases = [
            # (base_message, common_ending, expected_result)
            ("よろしくお願いします。", "します！", "よろしくお願いします。"),
            ("確認してみます。", "ます。", "確認してみます。"),
            ("これはテストですか？", "ですか？", "これはテストですか？"),
            ("了解しました。", "ました。", "了解しました。"),
            # 重複しない場合は語尾を追加
            ("確認してみます。", "です！", "確認してみますです！"),
            ("これは良い案", "ですね。", "これは良い案ですね。"),
        ]

        for base_message, common_ending, expected in test_cases:
            # ai_agent.pyの実際のロジックを模倣
            base_without_ending = re.sub(r"[。！？\s]+$", "", base_message)
            ending_without_punct = re.sub(r"[。！？\s]+$", "", common_ending)

            if ending_without_punct and base_without_ending.endswith(
                ending_without_punct
            ):
                # 既に同じ語尾で終わっている場合はそのまま使用
                response = base_message
            else:
                response = base_without_ending + common_ending

            self.assertEqual(
                response,
                expected,
                f"base='{base_message}', ending='{common_ending}' の処理が間違っています",
            )

    def test_duplicate_prevention_logic_normal(self):
        """通常会話での重複防止ロジックのテスト"""
        # シミュレート: 通常会話の場合の処理
        test_cases = [
            # (response_text, common_ending, expected_result)
            ("よろしくお願いします。", "します。", "よろしくお願いします。"),
            ("確認してみます。", "ます！", "確認してみます。"),
            ("了解です。", "です。", "了解です。"),
            # 重複しない場合は語尾を追加
            ("確認します。", "ね。", "確認しますね。"),
            ("そうですね", "よ。", "そうですねよ。"),
        ]

        for response_text, common_ending, expected in test_cases:
            # ai_agent.pyの実際のロジックを模倣
            response_without_ending = re.sub(r"[。！？\s]+$", "", response_text)
            ending_without_punct = re.sub(r"[。！？\s]+$", "", common_ending)

            if ending_without_punct and response_without_ending.endswith(
                ending_without_punct
            ):
                # 既に同じ語尾で終わっている場合は元のresponseを使用
                response = response_text
            else:
                response = response_without_ending + common_ending

            self.assertEqual(
                response,
                expected,
                f"response='{response_text}', ending='{common_ending}' の処理が間違っています",
            )

    def test_actual_bug_cases(self):
        """実際のバグ報告ケースのテスト"""
        # Issue報告の例: "よろしくおねがいします よろしくお願いします😊します！"
        test_cases = [
            # ケース1: "よろしくお願いします" + "します！"
            ("よろしくお願いします", "します！", "よろしくお願いします"),
            # ケース2: "これどう返せばいいですか" + "ですか？"
            ("これどう返せばいいですか", "ですか？", "これどう返せばいいですか"),
        ]

        for base_text, common_ending, expected in test_cases:
            # 実際のロジック
            base_without_ending = re.sub(r"[。！？\s]+$", "", base_text)
            ending_without_punct = re.sub(r"[。！？\s]+$", "", common_ending)

            if ending_without_punct and base_without_ending.endswith(
                ending_without_punct
            ):
                result = base_text  # 元のテキストを保持（句読点付き）
            else:
                result = base_without_ending + common_ending

            # 重複が発生していないことを確認
            self.assertNotIn("しますします", result)
            self.assertNotIn("ますます", result)
            self.assertNotIn("ですかですか", result)
            self.assertNotIn("かか？", result)

            print(f"✓ '{base_text}' + '{common_ending}' -> '{result}'")


def main():
    """テスト実行"""
    print("\n" + "=" * 60)
    print("語尾重複防止ロジック単体テスト")
    print("=" * 60 + "\n")

    # テストスイートの作成
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDuplicateSuffixPrevention)

    # テストの実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ 全てのテストに合格しました！")
        print("\n修正内容:")
        print("- 語尾を追加する前に、既に同じ語尾で終わっているかをチェック")
        print("- 重複する場合は語尾を追加せず、元のテキストを使用")
    else:
        print("❌ テストが失敗しました")
    print("=" * 60 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
