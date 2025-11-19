# リンターツールのセットアップと使用方法

## 概要

このプロジェクトでは、コード品質を保つためにリンターとフォーマッターを使用します。これらのツールは、コミット前に自動的に実行され、未使用のインポートや変数を削除し、コードスタイルを統一します。

## インストール

### 1. リンターツールのインストール

```bash
pip install -r requirements.txt
```

以下のツールがインストールされます：

- **flake8**: Pythonコードの静的解析
- **pylint**: より詳細なコード品質チェック
- **autoflake**: 未使用importの自動削除
- **isort**: import文の自動整形
- **black**: コードの自動フォーマット
- **pre-commit**: Git pre-commitフックの管理

### 2. Pre-commitフックのセットアップ

```bash
pre-commit install
```

このコマンドにより、コミット前に自動的にリンターが実行されるようになります。

## 使用方法

### 自動実行（推奨）

Pre-commitフックをインストールすると、`git commit` 時に自動的にリンターが実行されます：

```bash
git add .
git commit -m "コミットメッセージ"
```

リンターがコードを自動的に修正した場合：

1. 修正内容を確認
2. 再度 `git add .` で修正を追加
3. 再度 `git commit` を実行

### 手動実行

コミット前にリンターを手動で実行することもできます：

```bash
# 全てのファイルに対してpre-commitフックを実行
pre-commit run --all-files

# 特定のフックのみ実行
pre-commit run autoflake --all-files
pre-commit run isort --all-files
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

### 個別ツールの実行

各ツールを個別に実行することもできます：

```bash
# autoflake - 未使用importの削除
autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive src/

# isort - import文の整形
isort src/

# black - コードフォーマット
black src/

# flake8 - 静的解析
flake8 src/

# pylint - 詳細な品質チェック
pylint src/
```

## 設定ファイル

### `.pre-commit-config.yaml`

Pre-commitフックの設定ファイル。実行するツールとそのオプションを定義しています。

### `setup.cfg`

flake8、isort、pylintの設定ファイル。

### `pyproject.toml`

blackとisortの設定ファイル（setup.cfgと併用）。

## リンターが修正する内容

### autoflake

- 未使用のimport文を削除
- 未使用の変数を削除
- `import *` を展開

**例:**

```python
# 修正前
import os
import sys
from typing import *

def hello():
    print("Hello")
```

```python
# 修正後
def hello():
    print("Hello")
```

### isort

- import文をアルファベット順にソート
- 標準ライブラリ、サードパーティ、ローカルimportを分離

**例:**

```python
# 修正前
from typing import List
import os
from discord import Client
import sys
```

```python
# 修正後
import os
import sys
from typing import List

from discord import Client
```

### black

- コードスタイルを統一（インデント、スペース、改行など）
- 行の長さを88文字に制限

**例:**

```python
# 修正前
def function(arg1,arg2,arg3):
    result=arg1+arg2+arg3
    return result
```

```python
# 修正後
def function(arg1, arg2, arg3):
    result = arg1 + arg2 + arg3
    return result
```

### flake8

- コードスタイルの問題を検出（エラーは出すが修正はしない）
- 未使用の変数やimportを警告
- PEP 8準拠のチェック

## トラブルシューティング

### Pre-commitフックが実行されない

```bash
# フックを再インストール
pre-commit uninstall
pre-commit install
```

### リンターのエラーを無視したい場合

特定の行でリンターを無効化：

```python
# flake8を無効化
import sys  # noqa: F401

# pylintを無効化
import sys  # pylint: disable=unused-import
```

### Pre-commitをスキップしてコミット

緊急時のみ使用してください：

```bash
git commit --no-verify -m "メッセージ"
```

## ベストプラクティス

1. **コミット前に必ずリンターを実行**: Pre-commitフックを活用
2. **定期的にコード全体をチェック**: `pre-commit run --all-files`
3. **リンターの警告を無視しない**: 問題があれば修正する
4. **IDEのリンター統合を活用**: VS CodeやPyCharmのリンター機能を有効化

## 参考リンク

- [flake8 ドキュメント](https://flake8.pycqa.org/)
- [pylint ドキュメント](https://pylint.pycqa.org/)
- [autoflake GitHub](https://github.com/PyCQA/autoflake)
- [isort ドキュメント](https://pycqa.github.io/isort/)
- [black ドキュメント](https://black.readthedocs.io/)
- [pre-commit ドキュメント](https://pre-commit.com/)
