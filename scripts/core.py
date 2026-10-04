"""Offline planning primitives. Python 3.10+; standard library only.

This module never contacts a network or advertising account. Its schema checker
implements only the keywords used by the bundled schemas, not all JSON Schema.
"""
from __future__ import annotations

import html
import json
import math
import re
import unicodedata
import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAX_INPUT_BYTES = 1_000_000
MAX_DEPTH = 24
MAX_NODES = 20_000


class InputError(ValueError):
    """Invalid or unsafe local input; messages never echo the input value."""


def _reject_constant(_value: str) -> None:
    raise InputError("JSON must not contain NaN or Infinity")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise InputError("Duplicate JSON keys are not allowed")
        result[key] = value
    return result


def load_json(path: str | Path) -> Any:
    p = Path(path)
    try:
        with p.open("rb") as handle:
            raw = handle.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise InputError("JSON input exceeds the 1 MB local limit")
        value = json.loads(raw.decode("utf-8-sig"), parse_constant=_reject_constant,
                           object_pairs_hook=_unique_object)
        inspect_data(value)
        return value
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError(f"Cannot read valid UTF-8 JSON ({type(exc).__name__})") from exc


def normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


FORBIDDEN_KEYS = {
    "apikey", "accesstoken", "refreshtoken", "authtoken", "authorization",
    "bearertoken", "clientsecret", "password", "secret", "cookie", "cookies",
    "credentials", "accountid", "adaccountid", "customerid", "campaignid",
    "adgroupid", "adsetid", "adid", "uploadid", "pixelid", "connectorpayload",
    "livepayload", "liveschema", "privatekey", "sparkcode", "authorizationcode",
}
SECRET_TEXT = re.compile(
    r"(?:\bsk-[A-Za-z0-9_-]{16,}|\bgh[pousr]_[A-Za-z0-9]{20,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"(?i:bearer)\s+[A-Za-z0-9._~-]{16,}|"
    r"(?i:api[_ -]?key|access[_ -]?token|client[_ -]?secret|password)\s*[:=]\s*\S{6,})"
)


def inspect_data(value: Any) -> None:
    count = 0

    def walk(item: Any, depth: int) -> None:
        nonlocal count
        count += 1
        if depth > MAX_DEPTH or count > MAX_NODES:
            raise InputError("Input is too deeply nested or too large")
        if isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise InputError("Object keys must be strings")
                if normalized_key(key) in FORBIDDEN_KEYS:
                    raise InputError("Credential or live-resource field is forbidden")
                walk(key, depth + 1)
                walk(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                walk(child, depth + 1)
        elif isinstance(item, str):
            if SECRET_TEXT.search(item):
                raise InputError("Secret-like content is forbidden; supply sanitized input")
            if any((ord(c) < 32 and c not in "\n\r\t") or 0xD800 <= ord(c) <= 0xDFFF for c in item):
                raise InputError("Unsupported control or surrogate character")
        elif isinstance(item, float) and not math.isfinite(item):
            raise InputError("Non-finite numbers are forbidden")
        elif item is not None and not isinstance(item, (bool, int, float)):
            raise InputError("Only JSON-compatible values are accepted")

    walk(value, 0)


def schema_errors(value: Any, schema: dict, path: str = "$") -> list[str]:
    """Strict subset: type, required, properties, additionalProperties, const,
    enum, pattern, min/maxLength, min/maxItems, items, minimum/maximum.
    """
    errors: list[str] = []
    kinds = schema.get("type")
    if kinds is not None:
        kinds = [kinds] if isinstance(kinds, str) else kinds
        matches = {
            "null": value is None, "boolean": type(value) is bool,
            "object": isinstance(value, dict), "array": isinstance(value, list),
            "string": isinstance(value, str), "integer": type(value) is int,
            "number": type(value) in (int, float) and math.isfinite(value),
        }
        if not any(matches.get(k, False) for k in kinds):
            return [f"{path}: invalid type; expected {'/'.join(kinds)}"]
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append(f"{path}: does not match required constant")
    if "enum" in schema and not any(type(value) is type(v) and value == v for v in schema["enum"]):
        errors.append(f"{path}: unsupported value")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required field missing")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(schema_errors(item, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unknown field rejected")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", 10_000):
            errors.append(f"{path}: invalid number of entries")
        if "items" in schema:
            for i, item in enumerate(value):
                errors.extend(schema_errors(item, schema["items"], f"{path}[{i}]"))
    elif isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", 100_000):
            errors.append(f"{path}: invalid text length")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: invalid text format")
        if schema.get("minLength", 0) > 0 and not value.strip():
            errors.append(f"{path}: blank text is not allowed")
    elif type(value) in (int, float):
        if value < schema.get("minimum", -math.inf) or value > schema.get("maximum", math.inf):
            errors.append(f"{path}: number out of range")
    return errors


def config() -> dict:
    return load_json(ROOT / "skill.json")


def require_schema(value: Any, filename: str) -> None:
    inspect_data(value)
    errors = schema_errors(value, load_json(ROOT / "schemas" / filename))
    if errors:
        raise InputError("\n".join(errors[:30]))


def validate_url(url: str) -> None:
    if len(url) > 4096 or any(c.isspace() for c in url) or "\\" in url:
        raise InputError("URL contains unsupported characters")
    try:
        parts = urlsplit(url)
        if parts.scheme not in {"https", "http"} or not parts.hostname:
            raise InputError("Use a complete HTTP(S) URL")
        if parts.username is not None or parts.password is not None:
            raise InputError("Credentials in URLs are forbidden")
        _ = parts.port
        for key, _value in parse_qsl(parts.query, keep_blank_values=True):
            if normalized_key(key) in FORBIDDEN_KEYS | {"token", "key", "email", "phone", "signature", "sig"}:
                raise InputError("Sensitive URL parameters are forbidden")
    except ValueError as exc:
        if isinstance(exc, InputError):
            raise
        raise InputError("Malformed URL") from exc


def normalize_brief(value: dict) -> dict:
    require_schema(value, "brief.schema.json")
    brief = {
        "brand": None, "offer": None, "audience": None, "market": None,
        "goal": None, "success_action": None, "landing_page_url": None,
        "landing_page_text": None, "currency": None, "total_budget": None,
        "duration_days": None, "video_duration_seconds": None,
        "facts": [], "constraints": [], "data_label": "user_supplied",
    }
    brief.update(value)
    for key, item in brief.items():
        if isinstance(item, str):
            brief[key] = item.strip()
    if brief["landing_page_url"]:
        validate_url(brief["landing_page_url"])
    if brief["total_budget"] is not None and not brief["currency"]:
        raise InputError("currency is required when total_budget is supplied")
    ids = [fact["id"] for fact in brief["facts"]]
    if len(ids) != len(set(ids)):
        raise InputError("Fact IDs must be unique")
    return brief


def budget_summary(brief: dict) -> dict:
    total, days = brief["total_budget"], brief["duration_days"]
    average = None
    if total is not None and days:
        average = float((Decimal(str(total)) / Decimal(days)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    return {
        "currency": brief["currency"], "total_limit": total,
        "duration_days": days, "daily_average": average,
        "note": "僅為總額除以天數的規劃均值，不是平台每日預算設定；不得直接四捨五入後乘回作為支出承諾。",
    }


def missing_questions(brief: dict) -> list[str]:
    labels = {"brand": "品牌名稱", "audience": "目標客群", "market": "投放市場",
              "goal": "商業目標", "success_action": "可觀察的成功行動",
              "landing_page_url": "落地頁網址", "total_budget": "預算上限",
              "duration_days": "測試天數"}
    questions = [f"待確認：{label}" for key, label in labels.items() if brief[key] is None]
    if not brief["facts"]:
        questions.append("待確認：可引用的商品事實及來源；不得補寫價格、保證或成效")
    if brief["landing_page_text"] is None:
        questions.append("未提供落地頁文字；未讀取網站，無法核對訊息一致性")
    return questions


def make_plan(brief_raw: dict, deliverable_builder) -> dict:
    cfg = config()
    brief = normalize_brief(brief_raw)
    return {
        "contract_name": cfg["contract_name"], "contract_version": "1.0",
        "producer": {"skill_id": cfg["id"], "version": "1.0.0", "edition": "lite"},
        "plan_id": "local-" + uuid.uuid4().hex[:16],
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "platform": cfg["platform"], "scope": cfg["scope"], "status": "PLAN_READY",
        "publish_authorized": False, "external_reads": False, "external_writes": False,
        "review_status": "HUMAN_REVIEW_REQUIRED", "generation_mode": "deterministic_starter",
        "input": brief, "budget": budget_summary(brief),
        "deliverables": deliverable_builder(brief),
        "measurement": {
            "success_action": brief["success_action"], "tracking_status": "NOT_VERIFIED",
            "baseline": None, "target": None, "attribution_window": None,
        },
        "assumptions": [
            "這是固定規則產生的企劃起稿；訊息角度是待驗證假設，不是成效預測。",
            "輸入事實由使用者提供，未經本工具外部查證；合成範例不得當作真實案例。",
            "平台目標與素材規格未作 live 驗證；人工上線前須在實際帳號確認。",
        ],
        "open_questions": missing_questions(brief),
        "validation_scope": "local_structure_only",
    }


def validate_plan(plan: dict, platform_validator) -> dict:
    require_schema(plan, "plan.schema.json")
    errors: list[str] = []
    brief = normalize_brief(plan["input"])
    if plan["budget"] != budget_summary(brief):
        errors.append("budget: summary must match the supplied brief")
    if plan["measurement"]["success_action"] != brief["success_action"]:
        errors.append("measurement: success_action must match the brief")
    try:
        stamp = datetime.fromisoformat(plan["created_at"].replace("Z", "+00:00"))
        if stamp.utcoffset() is None:
            raise ValueError
    except ValueError:
        errors.append("created_at: ISO timestamp must include timezone")
    fact_ids = {fact["id"] for fact in brief["facts"]}

    def fact_refs(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "evidence_ids" and any(item not in fact_ids for item in child):
                    errors.append("deliverables: unknown evidence reference")
                fact_refs(child)
        elif isinstance(value, list):
            for child in value:
                fact_refs(child)

    fact_refs(plan["deliverables"])
    errors.extend(platform_validator(plan["deliverables"], brief))
    if errors:
        raise InputError("\n".join(errors[:30]))
    warnings = list(dict.fromkeys(missing_questions(brief) + plan["open_questions"]))
    warnings += ["尚未驗證模型路由、廣告審核、素材授權或實際投放成效。",
                 "通過僅表示本地結構檢查；商品真實性與廣告策略須人工審查。"]
    return {"valid": True, "validation_scope": "local_structure_only", "warnings": warnings}


def save_text(path: str | Path, text: str) -> None:
    """Create a new local file; never silently replace existing user work."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    except FileExistsError as exc:
        raise InputError("Output already exists; choose a new file or directory") from exc


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def safe_md(value: Any) -> str:
    if value is None:
        return "待確認"
    if isinstance(value, bool):
        return "true" if value else "false"
    text = html.escape(str(value), quote=False).replace("\r", "").replace("\n", " / ")
    for char in ("\\", "`", "*", "_", "[", "]", "|", "#"):
        text = text.replace(char, "\\" + char)
    return text


def render_report(plan: dict, result: dict) -> str:
    title = config()["title"]
    out = [f"# {title}｜離線企劃初稿", "", "> 尚未投放、未查詢帳號或網站；所有建議須人工確認。", "",
           f"版本：1.0.0｜資料：{safe_md(plan['input']['data_label'])}｜產生方式：{safe_md(plan['generation_mode'])}",
           f"狀態：PLAN_READY（僅本地結構）｜人工審查：HUMAN_REVIEW_REQUIRED", ""]

    def walk(value: Any, depth: int = 0) -> None:
        indent = "  " * min(depth, 8)
        if isinstance(value, dict):
            for key, child in value.items():
                if isinstance(child, (dict, list)):
                    out.append(f"{indent}- **{safe_md(key)}**")
                    walk(child, depth + 1)
                else:
                    out.append(f"{indent}- **{safe_md(key)}**：{safe_md(child)}")
        elif isinstance(value, list):
            if not value:
                out.append(indent + "- 未提供／未設定")
            for i, child in enumerate(value):
                if isinstance(child, (dict, list)):
                    out.append(f"{indent}- 項目 {i + 1}")
                    walk(child, depth + 1)
                else:
                    out.append(indent + "- " + safe_md(child))

    for heading, value in [("1. 商業資料與證據", plan["input"]), ("2. 預算算術摘要", plan["budget"]),
                           ("3. 平台專用產出", plan["deliverables"]), ("4. 量測待辦", plan["measurement"]),
                           ("5. 假設", plan["assumptions"]), ("6. 檢查與待確認", result)]:
        out += ["## " + heading, ""]
        walk(value)
        out.append("")
    return "\n".join(out) + "\n"


def make_utm(url: str, campaign: str, content: str | None = None) -> str:
    inspect_data([url, campaign, content])
    validate_url(url)
    if not campaign.strip() or len(campaign) > 200 or (content is not None and len(content) > 200):
        raise InputError("Campaign/content must be short, non-sensitive labels")
    cfg = config()
    parts = urlsplit(url)
    pairs = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
    pairs += [("utm_source", cfg["utm_source"]), ("utm_medium", cfg["utm_medium"]),
              ("utm_campaign", campaign.strip())]
    if content:
        pairs.append(("utm_content", content.strip()))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(pairs), parts.fragment))


def google_width(text: str) -> int:
    """Conservative local heuristic, not Google's official counting engine.
    NFC-normalized CJK/wide/fullwidth = 2; other code points = 1.
    Emoji, joiners and combining characters require platform re-check.
    """
    return sum(2 if unicodedata.east_asian_width(c) in {"W", "F"} else 1
               for c in unicodedata.normalize("NFC", text))


def rsa_check(payload: dict) -> dict:
    inspect_data(payload)
    if not isinstance(payload, dict) or set(payload) != {"headlines", "descriptions"}:
        raise InputError("Copy input must contain exactly headlines and descriptions")
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[dict] = []
    for key, minimum, maximum, width in (("headlines", 3, 15, 30), ("descriptions", 2, 4, 90)):
        values = payload[key]
        if not isinstance(values, list) or not all(isinstance(v, str) and v.strip() for v in values):
            raise InputError("Copy fields must be nonempty string arrays")
        if len(values) < minimum or len(values) > maximum:
            errors.append(f"{key}: expected {minimum}..{maximum} entries")
        if len(set(unicodedata.normalize("NFC", v).strip().casefold() for v in values)) != len(values):
            errors.append(f"{key}: duplicate copy")
        for i, text in enumerate(values):
            measured = google_width(text)
            rows.append({"field": key, "index": i, "width": measured, "limit": width, "within_limit": measured <= width})
            if measured > width:
                errors.append(f"{key}[{i}]: exceeds local character limit")
            if text != text.strip() or "\n" in text or "\r" in text:
                errors.append(f"{key}[{i}]: whitespace requires cleanup")
            if any(unicodedata.category(c).startswith("M") or unicodedata.category(c) == "Cf" or ord(c) >= 0x1F000 for c in text):
                warnings.append(f"{key}[{i}]: complex Unicode requires platform verification")
    return {"valid": not errors, "errors": errors, "warnings": warnings, "fields": rows,
            "scope": "local_RSA_counts_only_not_ad_approval"}
