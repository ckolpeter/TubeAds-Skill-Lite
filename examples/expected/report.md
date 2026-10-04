# TubeAds Skill Lite｜離線企劃初稿

> 尚未投放、未查詢帳號或網站；所有建議須人工確認。

版本：1.0.0｜資料：synthetic｜產生方式：deterministic\_starter
狀態：PLAN_READY（僅本地結構）｜人工審查：HUMAN_REVIEW_REQUIRED

## 1. 商業資料與證據

- **brand**：範例學院
- **offer**：廣告入門課程
- **audience**：想練習廣告規劃的初學者
- **market**：台灣
- **goal**：leads
- **success\_action**：提交課程諮詢表單
- **landing\_page\_url**：https://example.com/course
- **landing\_page\_text**：合成範例：頁面介紹課程內容，設有課程諮詢表單。未提供價格、保證、開課日或真實成效。
- **currency**：TWD
- **total\_budget**：6000
- **duration\_days**：14
- **video\_duration\_seconds**：30
- **facts**
  - 項目 1
    - **id**：F1
    - **text**：課程內容包含廣告規劃練習。
    - **source**：合成教學範例，不是 AI Ads Academy 的真實課程承諾。
- **constraints**
  - 不得宣稱保證收益。
  - 未提供價格，不得補寫優惠。
- **data\_label**：synthetic

## 2. 預算算術摘要

- **currency**：TWD
- **total\_limit**：6000
- **duration\_days**：14
- **daily\_average**：428.57
- **note**：僅為總額除以天數的規劃均值，不是平台每日預算設定；不得直接四捨五入後乘回作為支出承諾。

## 3. 平台專用產出

- **duration\_seconds**：30
- **duration\_source**：user\_supplied
- **hook\_variants**
  - 項目 1
    - **id**：local-hook-1
    - **text**：正在了解廣告入門課程？先看清楚內容再決定。
  - 項目 2
    - **id**：local-hook-2
    - **text**：比較不同方案時，哪些資訊值得先確認？
  - 項目 3
    - **id**：local-hook-3
    - **text**：從具體內容，了解一個選擇。
- **segments**
  - 項目 1
    - **start**：0
    - **end**：5
    - **role**：hook
    - **voiceover**：正在了解廣告入門課程？先看清楚內容再決定。
    - **visual**：展示主題與品牌；不要延後到最後才說明內容。
    - **evidence\_ids**
      - 未提供／未設定
  - 項目 2
    - **start**：5
    - **end**：14
    - **role**：explanation
    - **voiceover**：課程內容包含廣告規劃練習。
    - **visual**：拍攝可核實的內容導覽或操作示範。
    - **evidence\_ids**
      - F1
  - 項目 3
    - **start**：14
    - **end**：23
    - **role**：consideration
    - **voiceover**：先確認內容與適用情境，再決定是否符合你的需求。
    - **visual**：列出選擇條件；未知條件保留待確認。
    - **evidence\_ids**
      - 未提供／未設定
  - 項目 4
    - **start**：23
    - **end**：30
    - **role**：cta
    - **voiceover**：查看完整介紹，了解下一步。
    - **visual**：品牌收尾搭配單一行動入口。
    - **evidence\_ids**
      - 未提供／未設定
- **shot\_list**
  - 展示主題與品牌；不要延後到最後才說明內容。
  - 拍攝可核實的內容導覽或操作示範。
  - 列出選擇條件；未知條件保留待確認。
  - 品牌收尾搭配單一行動入口。
- **cta**：查看完整介紹，了解下一步。
- **test\_plan**
  - 項目 1
    - **id**：local-test-1
    - **variable**：opening\_hook
    - **variants**
      - local-hook-1
      - local-hook-2
      - local-hook-3
    - **hold\_constant**
      - 後續腳本與總時長
      - CTA
      - 素材形式
      - 客群與量測口徑
    - **decision\_rule**：先比對觀看與成功行動的完整路徑；觀看率高不等於轉換較好，資料不足時不選贏家。
    - **budget\_allocation**：待確認
- **review\_notes**
  - 秒數是分鏡規劃，不是配音實測；拍攝前須試讀，過長時縮短文案。
  - 預設 30 秒只是起稿假設，不是平台要求；素材規格與活動支援須於上線前確認。
  - 腳本不是影片檔；未生成、下載、上傳任何影片、音樂或創作者素材。
- **campaign\_note**：YouTube 影片投放屬 Google Ads 規劃範圍；本工具僅負責影片企劃，不建立活動。

## 4. 量測待辦

- **success\_action**：提交課程諮詢表單
- **tracking\_status**：NOT\_VERIFIED
- **baseline**：待確認
- **target**：待確認
- **attribution\_window**：待確認

## 5. 假設

- 這是固定規則產生的企劃起稿；訊息角度是待驗證假設，不是成效預測。
- 輸入事實由使用者提供，未經本工具外部查證；合成範例不得當作真實案例。
- 平台目標與素材規格未作 live 驗證；人工上線前須在實際帳號確認。

## 6. 檢查與待確認

- **valid**：true
- **validation\_scope**：local\_structure\_only
- **warnings**
  - 尚未驗證模型路由、廣告審核、素材授權或實際投放成效。
  - 通過僅表示本地結構檢查；商品真實性與廣告策略須人工審查。

