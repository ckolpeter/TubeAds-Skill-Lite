# TubeAds Skill Lite 1.0.0｜简体中文

[← 返回主 README](../../README.md)

YouTube 视频广告规划：多种开场、口播脚本、分镜、拍摄清单与单一变量素材测试。

## 可以做什么

- 使用本地模板生成可人工审核的广告规划初稿。
- 保留未知信息，不编造账号、效果、价格、权限或平台能力。
- 可由 Codex／Claude Code 等宿主模型依照工作流改写内容，再执行本地验证。

## 不会做什么

Lite 不登录广告账号、不保存凭证、不调用广告平台 API、不读取实时账号数据，也不创建、发布或修改广告。PLAN_READY 只表示本地规划数据可供人工审核。

## 快速开始

```bash
python3 scripts/toolkit.py plan examples/brief.synthetic.json --out-dir output/demo
python3 scripts/toolkit.py validate output/demo/plan.json
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py
```

要求：Python 3.10+。套件本身不需要 API key、npm 或 Docker。

## 语言与安全

文档提供繁体中文、简体中文、English、日本語、한국어。Agent 输出应沿用用户语言；未提供的事实保持未知。请勿把未经匿名化的客户个人信息或广告凭证提交给模型。

AI Ads Academy：https://www.ai-ads.academy

许可证：Apache-2.0。
