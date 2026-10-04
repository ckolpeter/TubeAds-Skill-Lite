# v1.0.0 實測報告

發行日期：2026-10-05。測試環境：Linux x86_64／CPython 3.13.5。

## 已實際執行

| 項目 | 結果 |
|---|---|
| `python3 -m unittest discover -s tests -v` | PASS；67 tests；3.350 秒（本次執行） |
| CLI plan → validate → render | PASS；測試涵蓋完整輸出與含空白／中文路徑 |
| 缺資料、錯誤型別、禁止欄位、假憑證與輸出覆寫 | 回歸測試 PASS |
| 內附 synthetic 範例 | 本地 schema 與平台結構檢查 PASS |
| 標準 JSON Schema 引擎獨立檢查 | 範例與 schema PASS；該引擎不屬 runtime 依賴 |

原始測試輸出見 `test-output.txt`。本包含 54 項共用測試，不能把四包的加總當成同等數量的獨特廣告能力。
輸入指令注入測試只證明 Python 把字串當作資料，不代表已完成 LLM 注入攻擊測試。

## 未執行／不在此版範圍

- Codex Desktop／Claude Code 的實際 UI 安裝、自然語句觸發與模型產出品質：NOT_RUN。
- macOS、Windows、WSL、Python 3.10 及 GitHub Actions 執行：NOT_RUN。程式按 Python 3.10+ 語法撰寫，不等於各環境已測。
- 真實廣告帳號、API、追蹤、素材權利、政策審核與投放成效：NOT_RUN／不支援。

`release_gate.py` 可重現靜態檢查與 SHA256 完整性檢查。完整性不等於程式安全簽章或平台認證。
任何後續修改都應重跑測試，並在檢視差異後重新產生 manifest。
