from __future__ import annotations
import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import core, platform_rules


class VideoTests(unittest.TestCase):
    def setUp(self):
        self.plan = core.make_plan(core.load_json(ROOT / "examples/brief.synthetic.json"), platform_rules.build)

    def test_three_hooks(self):
        self.assertEqual(len(self.plan["deliverables"]["hook_variants"]), 3)

    def test_default_duration_assumption(self):
        p = core.make_plan({"offer": "課程"}, platform_rules.build)
        self.assertEqual(p["deliverables"]["duration_seconds"], 30)
        self.assertEqual(p["deliverables"]["duration_source"], "starter_assumption")

    def test_duration_grid(self):
        for duration in (6, 7, 8, 15, 30, 60, 90, 300):
            with self.subTest(duration=duration):
                p = core.make_plan({"offer": "課程", "video_duration_seconds": duration}, platform_rules.build)
                self.assertTrue(core.validate_plan(p, platform_rules.validate)["valid"])

    def test_time_gap(self):
        self.plan["deliverables"]["segments"][1]["start"] += 1
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_time_overlap(self):
        self.plan["deliverables"]["segments"][1]["start"] = 0
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_zero_duration_segment(self):
        self.plan["deliverables"]["segments"][0]["end"] = 0
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_final_end(self):
        self.plan["deliverables"]["segments"][-1]["end"] = 29
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_duration_mismatch(self):
        self.plan["deliverables"]["duration_seconds"] = 31
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_wrong_role(self):
        self.plan["deliverables"]["segments"][0]["role"] = "explanation"
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_bad_hook_reference(self):
        self.plan["deliverables"]["test_plan"][0]["variants"][0] = "local-unknown"
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_duplicate_hook_id(self):
        hooks = self.plan["deliverables"]["hook_variants"]
        hooks[1]["id"] = hooks[0]["id"]
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_evidence_unknown(self):
        self.plan["deliverables"]["segments"][1]["evidence_ids"] = ["F999"]
        with self.assertRaises(core.InputError):
            core.validate_plan(self.plan, platform_rules.validate)

    def test_platform_specific_fields(self):
        v = self.plan["deliverables"]
        if core.config()["id"] == "tikads-skill-lite":
            self.assertEqual(v["creator_brief"]["spark_authorization"], "NOT_VERIFIED")
            v["creator_brief"]["spark_authorization"] = "APPROVED"
            with self.assertRaises(core.InputError):
                core.validate_plan(self.plan, platform_rules.validate)
        else:
            self.assertIn("Google Ads", v["campaign_note"])
            self.assertNotIn("creator_brief", v)
