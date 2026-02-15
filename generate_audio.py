"""
일본어/한국어 단어 MP3 생성 스크립트
gTTS를 사용하여 모든 단어의 오디오 파일을 생성합니다.
"""
import os
import re
import json
import time
from pathlib import Path
from gtts import gTTS

SCRIPT_DIR = Path(__file__).parent
CARDS_DIR = SCRIPT_DIR / "Cards"
AUDIO_DIR = SCRIPT_DIR / "audio"

JS_FILES = [
    CARDS_DIR / "기초단어.js",
    CARDS_DIR / "중급단어.js",
    CARDS_DIR / "미친맛집.js",
]

def sanitize_filename(text):
    """파일명에 사용할 수 없는 문자 제거"""
    # / \ : * ? " < > | 를 _로 대체
    return re.sub(r'[/\\:*?"<>|]', '_', text).strip()

def extract_words(js_file):
    """JS 파일에서 h(일본어)와 m(한국어 뜻) 추출"""
    content = js_file.read_text(encoding='utf-8')
    words = []

    # {h:"...",  또는 h: "..." 패턴 매칭
    h_pattern = re.findall(r'h\s*:\s*"([^"]*)"', content)
    m_pattern = re.findall(r',\s*m\s*:\s*"([^"]*)"', content)

    for i in range(min(len(h_pattern), len(m_pattern))):
        words.append({'h': h_pattern[i], 'm': m_pattern[i]})

    return words

def clean_korean(text):
    """[품사] 태그 제거"""
    return re.sub(r'^\[.*?\]\s*', '', text).strip()

def collect_all_words():
    """모든 JS 파일에서 단어 수집 및 중복 제거"""
    ja_texts = set()
    ko_texts = set()

    for js_file in JS_FILES:
        if not js_file.exists():
            print(f"  SKIP: {js_file.name} not found")
            continue
        words = extract_words(js_file)
        print(f"  {js_file.name}: {len(words)} words")
        for w in words:
            # 일본어: " / "로 분리된 경우 각각 추가
            h = w['h']
            if ' / ' in h:
                for part in h.split(' / '):
                    part = part.strip()
                    if part:
                        ja_texts.add(part)
            else:
                ja_texts.add(h)

            # 한국어: [품사] 제거 후 추가
            m_clean = clean_korean(w['m'])
            if m_clean and len(m_clean) > 0:
                ko_texts.add(m_clean)

    return sorted(ja_texts), sorted(ko_texts)

def generate_mp3(text, lang, output_path, retries=2):
    """gTTS로 MP3 생성"""
    for attempt in range(retries + 1):
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(str(output_path))
            return True
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
            else:
                print(f"    FAIL: {text} -> {e}")
                return False
    return False

def build_manifest(ja_texts, ko_texts):
    """텍스트 → 파일명 매핑 JSON 생성"""
    manifest = {"ja": {}, "ko": {}}
    for t in ja_texts:
        manifest["ja"][t] = sanitize_filename(t) + ".mp3"
    for t in ko_texts:
        manifest["ko"][t] = sanitize_filename(t) + ".mp3"
    return manifest

def main():
    print("=== MP3 Audio Generator ===\n")

    # 1. 단어 수집
    print("[1/4] Collecting words...")
    ja_texts, ko_texts = collect_all_words()
    print(f"  Japanese: {len(ja_texts)} unique words")
    print(f"  Korean: {len(ko_texts)} unique meanings\n")

    # 2. 디렉토리 생성
    ja_dir = AUDIO_DIR / "ja"
    ko_dir = AUDIO_DIR / "ko"
    ja_dir.mkdir(parents=True, exist_ok=True)
    ko_dir.mkdir(parents=True, exist_ok=True)

    # 3. 매니페스트 생성
    manifest = build_manifest(ja_texts, ko_texts)

    # 4. 일본어 MP3 생성
    print(f"[2/4] Generating Japanese MP3s ({len(ja_texts)})...")
    ja_done = 0
    ja_skip = 0
    for i, text in enumerate(ja_texts):
        fname = sanitize_filename(text) + ".mp3"
        fpath = ja_dir / fname
        if fpath.exists():
            ja_skip += 1
            continue
        if generate_mp3(text, 'ja', fpath):
            ja_done += 1
        if (i + 1) % 50 == 0:
            print(f"    {i+1}/{len(ja_texts)}...")
            time.sleep(0.5)  # rate limit 방지
    print(f"  Done: {ja_done} generated, {ja_skip} skipped (already exist)\n")

    # 5. 한국어 MP3 생성
    print(f"[3/4] Generating Korean MP3s ({len(ko_texts)})...")
    ko_done = 0
    ko_skip = 0
    for i, text in enumerate(ko_texts):
        fname = sanitize_filename(text) + ".mp3"
        fpath = ko_dir / fname
        if fpath.exists():
            ko_skip += 1
            continue
        if generate_mp3(text, 'ko', fpath):
            ko_done += 1
        if (i + 1) % 50 == 0:
            print(f"    {i+1}/{len(ko_texts)}...")
            time.sleep(0.5)
    print(f"  Done: {ko_done} generated, {ko_skip} skipped (already exist)\n")

    # 6. 매니페스트 저장
    manifest_path = AUDIO_DIR / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[4/4] Manifest saved: {manifest_path}")

    # 7. 용량 계산
    total_size = 0
    for dirpath, _, filenames in os.walk(AUDIO_DIR):
        for fname in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, fname))
    print(f"\nTotal size: {total_size / 1024 / 1024:.1f} MB")
    print("Done!")

if __name__ == "__main__":
    main()
