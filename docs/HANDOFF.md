# 桌面 Codex／Claude Code 交接

## 目前狀態

版本 1.0.0：最基礎可執行離線工作流。`plan` 用固定規則起稿；SKILL.md 指導承載模型改寫。
已交付專用輸出、去識別資料模板、本地驗證、範例、測試與來源紀錄。
實測結果以 TEST_REPORT.md 為準；未聲稱桌面安裝、模型路由或廣告平台驗收已完成。

## 第一個桌面任務：先驗收，不擴充

```text
你是這個 Lite Skill 的接手工程師。先讀 AGENTS.md、SKILL.md、README.md、
references/data-contract.md、docs/TEST_REPORT.md。
先不要增加功能，也不要連線廣告平台或更改 GitHub。
1. 確認資料夾、Python 與版本。
2. 執行 tests、release_gate，以及合成 brief 的 plan/validate/render。
3. 檢查生成內容是否符合這個平台，不得只看測試數量。
4. 在桌面端執行 evals/manual-cases.md，明確區分 PASS、FAIL、NOT_RUN。
5. 回報問題、證據、最小修正與下一個功能建議。不要修改其他 Skill 或上傳 GitHub。
```

## 接著做的單一功能

v1.1 首選：增加長短版腳本改寫與人工試讀紀錄；不得把估算語速宣稱為實測配音時長。

```text
根據這個專案的 AGENTS.md，只實作 docs/HANDOFF.md 推薦的下一個單一功能。
先交代輸入、輸出與驗收條件，再用最小差異修改，新增正常、缺資料與錯誤資料測試。
保持零 runtime 網路依賴、不收憑證、不新增 live 操作。
若要變更輸出契約，先說明相容性；不要未經授權改寫整個共用框架。
完成後執行測試與範例，更新版本／CHANGELOG／文件，最後才更新發行 manifest。
不得宣稱未執行的桌面或平台測試通過。
```

## 建議操作端

實作：Codex Desktop，使用你目前已驗證可用的 coding 模型；契約與除錯使用高推理。
獨立審查：Claude Code 的另一個對話；先做唯讀審查，不和實作 Agent 同時寫相同檔案。
此包不修改你的模型供應商、API 設定或工具權限。
