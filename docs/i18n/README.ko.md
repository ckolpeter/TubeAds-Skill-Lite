# TubeAds Skill Lite 1.0.0｜한국어

[← 메인 README로 돌아가기](../../README.md)

후크, 보이스오버 스크립트, 스토리보드, 촬영 목록 및 단일 변수 크리에이티브 테스트를 위한 YouTube 광고 오프라인 기획 Skill.

## 할 수 있는 일

- 제공된 정보로 사람이 검토할 수 있는 로컬 광고 기획 초안을 만듭니다.
- 계정 상태, 성과, 가격, 권한 또는 플랫폼 기능처럼 알 수 없는 사실을 임의로 만들지 않습니다.
- Codex／Claude Code 같은 호스트 모델로 문구를 보완한 뒤 로컬 검증을 실행할 수 있습니다.

## 하지 않는 일

Lite는 광고 계정에 로그인하지 않고 자격 증명을 저장하지 않으며 광고 플랫폼 API나 실시간 계정 데이터를 사용하지 않습니다. 광고 생성, 게시 또는 수정도 수행하지 않습니다. PLAN_READY는 로컬 기획 결과가 사람의 검토를 받을 준비가 되었다는 뜻일 뿐입니다.

## 빠른 시작

```bash
python3 scripts/toolkit.py plan examples/brief.synthetic.json --out-dir output/demo
python3 scripts/toolkit.py validate output/demo/plan.json
python3 -m unittest discover -s tests -v
python3 scripts/release_gate.py
```

요구 사항: Python 3.10+. 패키지 자체에는 API key, npm 또는 Docker가 필요하지 않습니다.

## 언어 및 안전

번체 중국어, 간체 중국어, English, 日本語, 한국어 문서를 제공합니다. Agent 출력은 사용자의 언어를 따릅니다. 익명화되지 않은 고객 개인정보나 광고 자격 증명을 모델에 제공하지 마세요.

AI Ads Academy：https://www.ai-ads.academy

라이선스: Apache-2.0.
