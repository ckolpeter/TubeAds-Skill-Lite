# TubeAds Skill Lite 1.0.0 | English

[← Back to the main README](../../README.md)

Offline YouTube ad planning for hooks, voiceover scripts, storyboards, shot lists, and single-variable creative tests.

## What it does

- Produces a local, human-reviewable advertising-planning draft from supplied information.
- Keeps unknown facts unknown instead of inventing account state, performance, pricing, permissions, or platform capabilities.
- Can be used with a host model such as Codex or Claude Code for language refinement, followed by local validation.

## What it does not do

Lite does not sign in to ad accounts, store credentials, call advertising-platform APIs, read live account data, or create, publish, and mutate live ads. PLAN_READY means the local planning artifact is ready for human review only.

## Quick start

```bash
python3 scripts/toolkit.py plan examples/brief.synthetic.json --out-dir output/demo
python3 scripts/toolkit.py validate output/demo/plan.json
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py
```

Requirement: Python 3.10+. The package itself needs no API key, npm, or Docker.

## Languages and safety

Documentation is available in Traditional Chinese, Simplified Chinese, English, Japanese, and Korean. Agent output should follow the user's language. Do not provide unredacted customer personal data or advertising credentials to a model.

AI Ads Academy: https://www.ai-ads.academy

License: Apache-2.0.
