# TubeAds Skill Lite 1.0.0｜日本語

[← メイン README に戻る](../../README.md)

フック、ナレーション台本、絵コンテ、撮影リスト、単一変数クリエイティブテストを作成する YouTube 広告向けオフライン企画 Skill。

## できること

- 提供された情報から、人間がレビューできるローカル広告企画の初稿を生成します。
- アカウント状態、実績、価格、権限、プラットフォーム機能などの不明情報を推測しません。
- Codex／Claude Code などのホストモデルで文章を改善した後、ローカル検証を実行できます。

## できないこと

Lite は広告アカウントへログインせず、認証情報を保存せず、広告 API やライブアカウントデータを利用しません。広告の作成、公開、変更も行いません。PLAN_READY は人間によるレビュー準備ができたことだけを示します。

## クイックスタート

```bash
python3 scripts/toolkit.py plan examples/brief.synthetic.json --out-dir output/demo
python3 scripts/toolkit.py validate output/demo/plan.json
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py
```

要件：Python 3.10+。パッケージ自体に API key、npm、Docker は不要です。

## 言語と安全性

繁體中文、简体中文、English、日本語、한국어のドキュメントを提供します。Agent の出力はユーザーの言語に合わせます。匿名化されていない顧客個人情報や広告認証情報をモデルへ渡さないでください。

AI Ads Academy：https://www.ai-ads.academy

ライセンス：Apache-2.0。
