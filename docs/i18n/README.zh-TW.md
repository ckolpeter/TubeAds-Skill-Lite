# TubeAds Skill Lite 1.0.0｜繁體中文

[← 回到主 README](../../README.md)

YouTube 影片廣告規劃：多種開場、口播腳本、分鏡、拍攝清單與單一變因素材測試。

## 能做什麼

- 使用本地模板產生可人工審查的廣告企劃初稿。
- 保留未知資訊，不捏造帳號、成效、價格、權限或平台能力。
- 可由 Codex／Claude Code 等承載模型依工作流改寫內容，再執行本地驗證。

## 不會做什麼

Lite 不登入廣告帳號、不保存憑證、不呼叫廣告平台 API、不讀取即時帳號資料，也不建立、發布或修改廣告。PLAN_READY 只代表本地規劃資料可供人工審查。

## 快速開始

```bash
python3 scripts/toolkit.py plan examples/brief.synthetic.json --out-dir output/demo
python3 scripts/toolkit.py validate output/demo/plan.json
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py
```

需求：Python 3.10+。套件本身不需要 API key、npm 或 Docker。

## 語言與安全

文件提供繁體中文、簡體中文、English、日本語、한국어。Agent 產出應沿用使用者語言；未提供的事實維持未知。請勿把未去識別的客戶個資或廣告憑證交給模型。

AI Ads Academy：https://www.ai-ads.academy

授權：Apache-2.0。
