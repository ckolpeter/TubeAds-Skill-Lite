"""TubeAds Skill Lite storyboard planning only; no video generation or publishing."""
IS_TIKTOK = False


def build(brief: dict) -> dict:
    duration = brief["video_duration_seconds"] or 30
    offer = brief["offer"]
    facts = brief["facts"]
    proof = facts[0]["text"] if facts else f"先看看{offer}的完整介紹，再判斷是否符合目前需求。"
    evidence = [facts[0]["id"]] if facts else []
    if IS_TIKTOK:
        hooks = [f"先別急著決定，看看{offer}有哪些內容。", "選擇方案前，先確認這幾件事。", "把介紹講清楚，從這裡開始。"]
        points = [0, max(1, round(duration * .1)), round(duration * .45), round(duration * .83), duration]
        visuals = ["近景口播或產品實拍；不要冒充真實用戶見證。", "手持展示或螢幕示範；畫面必須是真實可提供的內容。",
                   "以字幕整理待確認的使用情境與條件。", "顯示品牌與單一行動入口；不要杜撰限時優惠。"]
    else:
        hooks = [f"正在了解{offer}？先看清楚內容再決定。", "比較不同方案時，哪些資訊值得先確認？", "從具體內容，了解一個選擇。"]
        points = [0, max(1, round(duration * .17)), round(duration * .45), round(duration * .78), duration]
        visuals = ["展示主題與品牌；不要延後到最後才說明內容。", "拍攝可核實的內容導覽或操作示範。",
                   "列出選擇條件；未知條件保留待確認。", "品牌收尾搭配單一行動入口。"]
    voice = [hooks[0], proof, "先確認內容與適用情境，再決定是否符合你的需求。", "查看完整介紹，了解下一步。"]
    segments = [{"start": points[i], "end": points[i + 1], "role": role,
                 "voiceover": voice[i], "visual": visuals[i],
                 "evidence_ids": evidence if i == 1 else []}
                for i, role in enumerate(["hook", "explanation", "consideration", "cta"])]
    result = {
        "duration_seconds": duration,
        "duration_source": "user_supplied" if brief["video_duration_seconds"] else "starter_assumption",
        "hook_variants": [{"id": f"local-hook-{i}", "text": text} for i, text in enumerate(hooks, 1)],
        "segments": segments,
        "shot_list": visuals,
        "cta": "查看完整介紹，了解下一步。",
        "test_plan": [{"id": "local-test-1", "variable": "opening_hook",
                       "variants": [f"local-hook-{i}" for i in range(1, 4)],
                       "hold_constant": ["後續腳本與總時長", "CTA", "素材形式", "客群與量測口徑"],
                       "decision_rule": "先比對觀看與成功行動的完整路徑；觀看率高不等於轉換較好，資料不足時不選贏家。",
                       "budget_allocation": None}],
        "review_notes": ["秒數是分鏡規劃，不是配音實測；拍攝前須試讀，過長時縮短文案。",
                         "預設 30 秒只是起稿假設，不是平台要求；素材規格與活動支援須於上線前確認。",
                         "腳本不是影片檔；未生成、下載、上傳任何影片、音樂或創作者素材。"],
    }
    if IS_TIKTOK:
        result["creator_brief"] = {"tone": "自然解說，不冒充親身使用者或未授權代言人。",
                                  "must_show": ["可核實的內容", "清楚字幕", "單一行動入口"],
                                  "avoid": ["偽造見證", "未提供的價格或倒數", "未授權音樂或貼文"],
                                  "spark_authorization": "NOT_VERIFIED", "music_rights": "NOT_VERIFIED"}
    else:
        result["campaign_note"] = "YouTube 影片投放屬 Google Ads 規劃範圍；本工具僅負責影片企劃，不建立活動。"
    return result


def validate(value: dict, brief: dict) -> list[str]:
    errors = []
    duration = value["duration_seconds"]
    if brief["video_duration_seconds"] is not None:
        if duration != brief["video_duration_seconds"] or value["duration_source"] != "user_supplied":
            errors.append("duration: must match the supplied brief")
    elif value["duration_source"] != "starter_assumption":
        errors.append("duration_source: unspecified input must remain an assumption")
    ids = [item["id"] for item in value["hook_variants"]]
    if len(ids) != len(set(ids)):
        errors.append("hook_variants: duplicate local IDs")
    previous = 0
    for segment in value["segments"]:
        if segment["start"] != previous or segment["end"] <= segment["start"]:
            errors.append("segments: time intervals must be positive and continuous from zero")
        previous = segment["end"]
    if previous != duration:
        errors.append("segments: final end must equal duration_seconds")
    if value["segments"][0]["role"] != "hook" or value["segments"][-1]["role"] != "cta":
        errors.append("segments: storyboard must start with hook and end with cta")
    for test in value["test_plan"]:
        if any(ref not in ids for ref in test["variants"]):
            errors.append("test_plan: unknown hook reference")
    return errors
