# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

일본어 단어장 플래시카드 앱. 순수 HTML/CSS/JS 단일 파일로 구성되며, 브라우저에서 바로 실행 가능. TTS 음성 재생, 북마크, 가중치 랜덤 테스트 기능 포함.

## 작업 관리 정책

### TODO 리스트 자동 확인

**대화 시작 시 자동 동작:**
- 매 대화 시작 시 [TDLs/TDLs.md](TDLs/TDLs.md) 파일을 자동으로 확인
- 파일 내용 중 다음 항목을 확인:
  - "새 작업 추가" 섹션에 작성된 새 작업
  - 대기 상태 `[ ]` 또는 진행중 상태 `[▶️]`인 작업
- 새 작업이나 미완료 작업이 있으면 사용자에게 알림 후 작업 시작 여부 확인

**TODO 확인 기록:**
- 확인 시 "Claude 마지막 확인" 섹션에 시간(초 단위)과 상태 기록
- 형식: `YYYY-MM-DD HH:MM:SS`
- "새 작업 추가" 섹션의 내용을 정리하여 "진행 중인 작업" 섹션으로 이동
- 이동 후 "새 작업 추가" 섹션은 비움

**사용자 입력 간편 명령:**
- **"." 입력**: 문맥에 따라 다른 의미
  - **질문에 대한 응답**: "ok" (동의/진행)
  - **대화 없음 또는 종료 후**: TODO 리스트 확인
    - TDLs/TDLs.md의 미완료/새 작업 확인
    - 작업이 있으면 진행, 없으면 현재 상태 보고

**작업 진행 규칙:**
- 작업 시작 전 TodoWrite 도구로 작업 목록 생성
- 각 작업 완료 시 즉시 완료 표시 (배치 처리 금지)
- 작업 완료 후 [TDLs/TDLs_Done.md](TDLs/TDLs_Done.md)로 이동 (완료 시간, 커밋 해시 기록)
- [TDLs/TDLs.md](TDLs/TDLs.md): 미완료 작업만 관리
- [TDLs/TDLs_Done.md](TDLs/TDLs_Done.md): 완료된 작업 히스토리

## 기술 스택

- **순수 HTML/CSS/JS** (단일 파일, 프레임워크 없음)
- **브라우저 내장 TTS** (speechSynthesis API, ja-JP)
- **localStorage** (북마크/학습 데이터 저장)
- 메인 파일: [Cards/japanese-flashcard.html](Cards/japanese-flashcard.html)

## 프로젝트 구조

```
Cards/
  japanese-flashcard.html   ← 메인 앱 (단일 파일)
  project-summary.md        ← 프로젝트 요약
TDLs/
  TDLs.md                   ← TODO 리스트
  TDLs_Done.md              ← 완료 히스토리
```

## 자동 정리

- 프로젝트 루트에 `nul` 파일이 존재하면 발견 즉시 삭제 (Windows 아티팩트)

## 코드 컨벤션

- 한글 주석/로그 사용
- 단일 HTML 파일 내 `<style>`, `<script>` 인라인 구성
- CSS 변수(`:root`)로 테마 관리

## 파일 참조 규칙

코드 참조 시 **반드시** 다음 형식을 사용:
- 파일: `[japanese-flashcard.html](Cards/japanese-flashcard.html)`
- 특정 라인: `[japanese-flashcard.html:79](Cards/japanese-flashcard.html#L79)`
- 폴더: `[Cards/](Cards/)`
- **절대 경로 금지**, 프로젝트 루트 기준 상대 경로 사용
- **백틱 금지**: 파일 참조는 markdown link 형식

## Git 커밋 정책

작업 완료 후 자동으로 커밋을 수행합니다:
- **시점**: 각 TODO 작업 완료 직후
- **대상 브랜치**: 현재 작업 중인 브랜치 (새 브랜치 생성 없음)
- **커밋 메시지 형식**:
  ```
  <type>: <간결한 설명>

  - 변경 사항 1
  - 변경 사항 2

  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
  ```
- **Type 종류**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- **Push**: 커밋 후 즉시 자동 push 수행 (확인 없이 바로 실행)

## 단어장 생성 규칙

대본(스크립트)을 받으면 다음 규칙으로 단어장 파일을 생성:

- **Day 구분**: 단어(명사, 동사, 형용사 등)와 표현(문장, 관용구)을 별도 Day로 분리
- **단어 수**: 최대한 많이 추출 (초보 수준이므로 기본 단어도 포함)
- **표현 수**: 실용적인 표현도 최대한 많이 포함
- **형식**: `{h:"히라가나/카타카나", r:"romaji", m:"[품사] 뜻"}` 구조 유지
- **카테고리 오프셋**: 기초(0), 중급(100), 미친맛집(200) 등 100 단위

## 참고 문서

- [Cards/project-summary.md](Cards/project-summary.md): 프로젝트 요약 및 기능 목록
- [TDLs/TDLs.md](TDLs/TDLs.md): TODO 리스트
