# GitHub Actions ワークフロー

このディレクトリには、リポジトリの自動化を行うGitHub Actionsワークフローが含まれています。

## ワークフロー一覧

### 1. 知識データのRelease自動アップロード (`upload-knowledge-to-release.yml`)

「知識データの生成と保存」ワークフローで作成された暗号化知識データを、GitHub Releaseとして自動的に公開するワークフローです。

詳細なアーキテクチャ、利点、使用方法、トラブルシューティングについては [docs/RELEASE_FLOW.md](../../docs/RELEASE_FLOW.md) を参照してください。

**トリガー**: `workflow_run` (「知識データの生成と保存」完了時)  
**権限**: `contents: write`

### 2. 知識データの生成と保存 (`generate-knowledge-data.yml`)

Discordサーバーからメッセージを取得し、AI学習用の埋め込みデータを生成して暗号化するワークフローです。

詳細な動作、実行時間、環境変数については [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md#知識データの生成と保存) を参照してください。

**トリガー**: `workflow_dispatch`（手動実行）、定期実行  
**権限**: `contents: read`

### 3. Discord Botの実行 (`run-discord-bot.yml`)

Discord AIエージェントBotを起動するワークフローです。最新のGitHub Releaseから暗号化された知識データをダウンロードし、復号化してBotを実行します。

詳細な動作、環境変数、注意事項については [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md#discord-botの実行) を参照してください。

**トリガー**: `workflow_dispatch`（手動実行）  
**権限**: `contents: read`

### 4. Auto Merge on Approval (`auto-merge.yml`)

PRが承認されたときに、GitHubの自動マージ機能を有効化するワークフローです。承認とステータスチェックが完了すると、GitHubが自動的にSquash and Mergeを実行します。

詳細な動作フロー、トラブルシューティングについては [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md#auto-merge-on-approval) を参照してください。

**トリガー**: `pull_request_review` (Approved時)  
**権限**: `contents: write`, `pull-requests: write`

### 5. Auto Delete Branch on Merge (`auto-delete-branch.yml`)

PRがマージされた後、ソースブランチを自動的に削除するワークフローです。`auto-merge.yml`のバックアップとして機能します。

詳細な動作、注意事項については [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md#auto-delete-branch-on-merge) を参照してください。

**トリガー**: `pull_request` (closed、merged時)  
**権限**: `contents: write`

### 6. Update Other PRs After Merge (`update-other-prs.yml`)

PRがmainブランチにマージされたときに、同じベースブランチを対象とする他のオープンなPRを自動的に更新するワークフローです。

詳細な動作、メリット、注意事項については [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md#update-other-prs-after-merge) を参照してください。

**トリガー**: `pull_request` (closed、main、merged時)  
**権限**: `contents: write`, `pull-requests: write`

### 7. Secrets疎通テスト (`test-secrets.yml`)

Discord BotとGemini APIの認証情報（Secrets）の疎通を確認するワークフローです。DISCORD_TOKEN、TARGET_GUILD_ID、GEMINI_API_KEYの有効性を検証し、APIへの接続を確認します。

詳細な動作、環境変数、注意事項については [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md#secrets疎通テスト) を参照してください。

**トリガー**: `workflow_dispatch`（手動実行）、`push`（main、対象ファイル変更時）  
**権限**: `contents: read`  
**注**: Gemini APIテストは手動実行時のみオプションで有効化可能（無料枠保護のため）。

## 詳細情報

各ワークフローの詳細な仕様、トラブルシューティング、カスタマイズ方法については [docs/WORKFLOWS.md](../../docs/WORKFLOWS.md) を参照してください。
