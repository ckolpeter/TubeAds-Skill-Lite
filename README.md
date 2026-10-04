# TubeAds Skill Lite v1.0.0

[繁體中文](docs/i18n/README.zh-TW.md) · [简体中文](docs/i18n/README.zh-CN.md) · [English](docs/i18n/README.en.md) · [日本語](docs/i18n/README.ja.md) · [한국어](docs/i18n/README.ko.md)

**AI Ads Academy／AI 廣告學院｜最基礎離線版**

YouTube 影片廣告：三種開場、分鏡、口播、拍攝清單與單一變因測試。

## 已完成與沒有完成

這包包含可運作的固定規則起稿工具、可被 Agent 讀取的 SKILL.md、繁中說明、嚴格本地格式檢查、合成範例及自動測試。
不是四份換名字的提示詞；`scripts/platform_rules.py` 與輸出 schema 各自不同。

不包含：廣告帳號連線、API/OAuth、即時數據、網站抓取、上傳／發布、圖片／影片生成、平台審核或投放成效驗證。

**兩種使用方式**：直接跑 Python 會產生固定規則初稿；把 Skill 載入 Codex／Claude Code 後，承載模型可以依專用流程改寫與完善內容。套件沒有內建 LLM，也不需 API key。
模型端可能使用雲端服務並產生用量；「離線」指套件腳本及廣告平台存取，不代表整個 AI 應用都離線。

## 最快試跑

需求：Python 3.10 以上；不需 pip、npm、Docker 或環境變數。
在本資料夾開啟終端：

```bash
python3 scripts/toolkit.py plan examples/brief.synthetic.json --out-dir output/demo
python3 scripts/toolkit.py validate output/demo/plan.json
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py
```

Windows 可將 `python3` 換成 `py -3`；實際測試環境請看 `docs/TEST_REPORT.md`，不把未跑過的系統宣稱為已驗證。

輸出為 `output/demo/plan.json`、`report.md`、`validation.json`。同名輸出存在會拒絕覆寫，重跑請改成 `output/demo-2`。

`examples/expected/` 已附產出的完整 JSON／Markdown，不用執行也能先閱讀。範例品牌、預算、課程全部為合成資料，不是學院的真實承諾或投放成果。

## 用自己的資料

複製 `templates/brief.json` 到另一個工作資料夾，填入 `offer`，其他未知資料保留 null。資料已由使用者提供就不要重問；不要加真實帳號 ID、授權碼或個資。
`facts` 每筆需要 `id`（如 F1）、`text`、`source`；來源可為使用者提供的文件描述。
`goal` 可為 awareness／traffic／leads／sales，僅為本地規劃標籤，不是平台 enum。
金額是使用者提供的總額；給了 total_budget 就必須給三碼大寫 currency。

generation_mode 為 deterministic_starter 時內容來自固定模板；用 Agent 改寫後改成 agent_assisted，再執行 validate 與 render。
字串檢查不能證明商品主張真實、證據足夠或策略有效，仍須人工驗收。

## 在桌面工具中使用／繼續開發

讀取 `docs/INSTALLATION.md`。只要開啟此資料夾並要求讀取 SKILL.md，也能先明確使用工作流；這不等於安裝或自動路由測試已完成。
後續擴充請直接把 `docs/HANDOFF.md` 裡的提示詞交給桌面 Codex／Claude Code。

## 檔案位置

| 位置 | 用途 |
|---|---|
| SKILL.md | Agent 的專用任務說明與觸發範圍 |
| scripts/toolkit.py | plan／validate／render／utm 本地命令 |
| scripts/platform_rules.py | 這個平台的基礎產出與檢查邏輯 |
| schemas/ | brief 與 plan 的資料格式 |
| templates/、examples/ | 輸入模板、合成案例與完整輸出 |
| tests/、evals/ | 自動化測試及尚待桌面端執行的手動情境 |
| AGENTS.md、CLAUDE.md、docs/HANDOFF.md | 後續開發交接 |

## 信任邊界

PLAN_READY 表示**本地格式完成、等待人工審查**，並非可直接投放。
禁止 external reads／writes；所有素材與文字只保存在你選擇的本地路徑。
格式驗證與靜態 import 檢查不是完整安全沙箱。不要把未去識別的真實客戶資料傳給模型。

來源與核對狀態見 `references/official-sources.md`。套件不是任何廣告平台的官方產品，也不代表平台背書。

授權：Apache-2.0；版本紀錄見 CHANGELOG.md。
