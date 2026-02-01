#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
복습이 필요한 단어를 추출하는 스크립트
복습 열에 1이 있는 단어들을 모아서 복습.md 파일을 생성합니다.
"""

import re
import os

def extract_review_words(file_path, file_type):
    """
    마크다운 파일에서 복습 열에 1이 있는 단어를 추출합니다.

    Args:
        file_path: 마크다운 파일 경로
        file_type: 파일 유형 ('hiragana', 'katakana', 'kanji')

    Returns:
        dict: 카테고리별 복습 단어 딕셔너리
    """
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    review_words = {}
    current_category = None
    in_table = False

    for line in lines:
        line = line.strip()

        # 카테고리 헤더 찾기 (### 로 시작)
        if line.startswith('### '):
            current_category = line[4:].strip()
            in_table = False
            continue

        # 테이블 헤더 확인
        if '| 한국어 |' in line and '| 일본어 |' in line:
            in_table = True
            continue

        # 구분선 스킵
        if line.startswith('|---'):
            continue

        # 섹션 끝
        if line.startswith('[↑ 맨 위로]') or line.startswith('---'):
            in_table = False
            continue

        # 테이블 행 처리
        if in_table and line.startswith('|') and current_category:
            parts = [p.strip() for p in line.split('|')]
            # parts[0]은 빈 문자열, parts[-1]도 빈 문자열
            if len(parts) >= 4:
                # 복습 열 확인 (마지막에서 두 번째)
                review_col = parts[-2] if len(parts) >= 3 else ''

                if '1' in review_col:
                    if current_category not in review_words:
                        review_words[current_category] = []

                    # 파일 타입에 따라 다른 형식
                    if file_type == 'kanji':
                        # 한자는 4열: 한국어, 일본어, 한자, 복습
                        if len(parts) >= 5:
                            korean = parts[1]
                            japanese = parts[2]
                            kanji = parts[3]
                            review_words[current_category].append({
                                'korean': korean,
                                'japanese': japanese,
                                'kanji': kanji
                            })
                    else:
                        # 히라가나/카타카나는 3열: 한국어, 일본어, 복습
                        if len(parts) >= 4:
                            korean = parts[1]
                            japanese = parts[2]
                            review_words[current_category].append({
                                'korean': korean,
                                'japanese': japanese
                            })

    return review_words

def generate_review_markdown(hiragana_words, katakana_words, kanji_words, output_file):
    """
    복습 단어들을 마크다운 파일로 생성합니다.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# 복습 단어장\n\n')
        f.write('복습이 필요한 단어들만 모아놓았습니다.\n\n')

        # 하나의 통합 테이블 생성
        f.write('| 한국어 | 일본어 | 한자 | 복습 |\n')
        f.write('|--------|--------|------|------|\n')

        # 히라가나 단어
        for category, words in hiragana_words.items():
            for word in words:
                f.write(f"| {word['korean']} | {word['japanese']} |  | 1 |\n")

        # 카타카나 단어
        for category, words in katakana_words.items():
            for word in words:
                f.write(f"| {word['korean']} | {word['japanese']} |  | 1 |\n")

        # 한자 단어
        for category, words in kanji_words.items():
            for word in words:
                f.write(f"| {word['korean']} | {word['japanese']} | {word['kanji']} | 1 |\n")

        f.write('\n')

def main():
    """메인 함수"""
    # 현재 스크립트 디렉토리
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 파일 경로
    hiragana_file = os.path.join(script_dir, '히라가나.md')
    katakana_file = os.path.join(script_dir, '카타카나.md')
    kanji_file = os.path.join(script_dir, '한자.md')
    output_file = os.path.join(script_dir, '복습.md')

    # 복습 단어 추출
    print('히라가나 단어 추출 중...')
    hiragana_words = extract_review_words(hiragana_file, 'hiragana')

    print('카타카나 단어 추출 중...')
    katakana_words = extract_review_words(katakana_file, 'katakana')

    print('한자 단어 추출 중...')
    kanji_words = extract_review_words(kanji_file, 'kanji')

    # 통계 출력
    total_hiragana = sum(len(words) for words in hiragana_words.values())
    total_katakana = sum(len(words) for words in katakana_words.values())
    total_kanji = sum(len(words) for words in kanji_words.values())
    total = total_hiragana + total_katakana + total_kanji

    print(f'\n복습 단어 통계:')
    print(f'  히라가나: {total_hiragana}개')
    print(f'  카타카나: {total_katakana}개')
    print(f'  한자: {total_kanji}개')
    print(f'  총합: {total}개')

    if total == 0:
        print('\n복습이 필요한 단어가 없습니다.')
        print('단어장에서 복습 열에 1을 입력하면 해당 단어가 복습.md에 추가됩니다.')
        # 빈 파일이라도 생성
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('# 복습 단어장\n\n')
            f.write('복습이 필요한 단어가 없습니다.\n\n')
            f.write('단어장에서 복습 열에 1을 입력하면 해당 단어가 여기에 표시됩니다.\n')
    else:
        # 마크다운 파일 생성
        print(f'\n{output_file} 생성 중...')
        generate_review_markdown(hiragana_words, katakana_words, kanji_words, output_file)
        print('완료!')

if __name__ == '__main__':
    main()
