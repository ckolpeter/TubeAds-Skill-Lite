# tubeads.plan@1.0

這是離線企劃資料，不是平台 API payload。完整欄位與型別見 `schemas/plan.schema.json`。

固定 producer 為 tubeads-skill-lite／1.0.0／lite；所有本地 ID 以 local- 開頭。F1 等 ID 只引用 input.facts。
unknown 欄位會被拒絕；要擴充契約，必須同時更新 schema、驗證器、範例、測試及版本說明。

`status` 永遠為 PLAN_READY；`review_status` 永遠為 HUMAN_REVIEW_REQUIRED。這兩個欄位可同時成立：
前者僅代表可被本地流程消費的結構，後者表示尚無人核准投放。
`publish_authorized`、`external_reads`、`external_writes` 必須為布林 false，不接受字串 false 或數字 0。

`input` 保存去識別商業簡報。`budget` 是輸入總額的算術摘要，不自動拆預算給素材。
`measurement` 的追蹤狀態是 NOT_VERIFIED；baseline／target／attribution_window 保留 null，v1.0 不分析真實成效。
`deliverables` 僅收此 Skill 的專用欄位，不接受其他平台結果冒充本平台。

`generation_mode` 區分 deterministic_starter 與 agent_assisted；工具不會自動呼叫模型。
`validation_scope=local_structure_only`；通過不能證明事實真實、政策合規或 live 能力存在。

## 本地 JSON Schema 檢查範圍

實作使用 Python 標準函式庫，支持本包使用的 type、const、enum、required、properties、additionalProperties、
minLength、maxLength、pattern、minItems、maxItems、items、minimum、maximum。
不是完整 JSON Schema 引擎；$schema 僅標示文件格式。時間、證據 ID、預算一致性、影片時間軸等另以程式檢查。
禁止重複 JSON key、NaN／Infinity、超過 1 MB 的 JSON 與過深結構。
敏感欄位與常見憑證樣式檢查只是防呆，不能當作完整 DLP；輸入仍需人工去識別。
