# 安裝與試用

## 先明確呼叫，不依賴自動觸發

在 Codex Desktop 或 Claude Code 打開這個資料夾，貼上：

```text
請讀取此資料夾的 SKILL.md，依範圍執行 examples/brief.synthetic.json 的示範。
使用實際存在的 Python 版本，輸出到新的 output 目錄，不要連線、發布廣告或修改任何外部帳號。
最後顯示 report.md 的重點、驗證結果與未確認事項。
```

這是直接讀檔方式，尚未驗證工具的自動選擇行為。

## 安裝為本地 Skill

Codex 本地目錄：`~/.agents/skills/tubeads-skill-lite/SKILL.md`。
Claude Code 本地目錄：`~/.claude/skills/tubeads-skill-lite/SKILL.md`。
專案範圍可使用專案下的 `.agents/skills/` 或 `.claude/skills/`。
請複製**整個 tubeads-skill-lite 資料夾**，不要只複製 SKILL.md；遇同名資料夾先停下備份與比較，不要覆蓋。

Codex 可明確選擇 `$tubeads-skill-lite`；Claude Code 可用 `/tubeads-skill-lite`。自動觸發請依 evals 檔案測試。
路徑依官方文件整理，參見 references/official-sources.md。管理政策或不同應用版本可能影響載入。

Claude Code 的本地 Skill 不等於 Claude Cowork／雲端帳號的 Skill。此包不宣稱已驗證 Cowork 安裝。

## 開發與安裝副本

後續程式修改應在原始專案資料夾進行，不要同時修改原始碼與兩個安裝副本。
同名副本不自動同步；驗收新版本後再由使用者明確替換。
整套 ZIP 附有安全的 `install_skills.py`：只建立缺少的專案安裝資料夾、預設不覆寫，可先 dry-run。
