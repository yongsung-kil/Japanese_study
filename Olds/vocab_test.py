import re
from datetime import datetime
import os
import random

def parse_markdown_table(file_path):
    """마크다운 파일에서 단어 테이블 파싱"""
    words = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    for line in lines:
        # 테이블 헤더 감지
        if '| 한국어 | 일본어 |' in line:
            in_table = True
            continue

        # 테이블 구분선 스킵
        if in_table and '|---' in line:
            continue

        # 테이블 행 파싱
        if in_table and line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            # parts: ['', '한국어', '일본어', '복습', '']
            if len(parts) >= 4 and parts[1] and parts[2]:
                korean = parts[1]
                japanese = parts[2]
                if korean and japanese and korean != '한국어':  # 헤더가 아닌 경우
                    words.append({'korean': korean, 'japanese': japanese})

        # 테이블 끝 감지
        elif in_table and line.strip() and not line.strip().startswith('|'):
            in_table = False

    return words

def select_file():
    """학습할 파일 선택"""
    print("\n=== 일본어 단어 테스트 ===")
    print("1. 히라가나.md")
    print("2. 카타카나.md")
    print("3. 한자.md")

    while True:
        choice = input("\n파일을 선택하세요 (1-3): ").strip()
        if choice == '1':
            return '히라가나.md'
        elif choice == '2':
            return '카타카나.md'
        elif choice == '3':
            return '한자.md'
        else:
            print("잘못된 입력입니다. 1-3 중 선택하세요.")

def select_mode():
    """테스트 모드 선택"""
    print("\n=== 테스트 모드 선택 ===")
    print("1. 한국어 → 일본어 (한국어를 보고 일본어 떠올리기)")
    print("2. 일본어 → 한국어 (일본어를 보고 한국어 떠올리기)")

    while True:
        choice = input("\n모드를 선택하세요 (1-2): ").strip()
        if choice in ['1', '2']:
            return int(choice)
        else:
            print("잘못된 입력입니다. 1 또는 2를 선택하세요.")

def run_test(words, mode, output_file):
    """단어 테스트 실행"""
    wrong_count = 0

    print(f"\n=== 테스트 시작 (총 {len(words)}개 단어) ===")
    print("0: 알고 있음 | 1: 모르겠음")
    print("-" * 50)

    for idx, word in enumerate(words, 1):
        # 질문과 가려진 정답 표시
        if mode == 1:
            question = word['korean']
            answer = word['japanese']
            print(f"\n[{idx}/{len(words)}] {question}{'='*30}정답: {answer}")
        else:
            question = word['japanese']
            answer = word['korean']
            print(f"\n[{idx}/{len(words)}] {question}{'='*30}정답: {answer}")

        # 사용자 입력
        while True:
            user_input = input("0(알고있음) / 1(모름): ").strip()
            if user_input in ['0', '1']:
                break
            else:
                print("0 또는 1을 입력하세요.")

        # 모르는 단어는 바로 파일에 저장
        if user_input == '1':
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"| {word['korean']} | {word['japanese']} |  |\n")
            wrong_count += 1

    return wrong_count

def initialize_result_file(mode, file_name):
    """결과 파일 초기화 (헤더 작성)"""
    # 복습 폴더 생성 (없으면)
    review_dir = os.path.join(os.path.dirname(__file__), "복습")
    if not os.path.exists(review_dir):
        os.makedirs(review_dir)

    # 날짜 형식: YYMMDD
    date_str = datetime.now().strftime("%y%m%d")
    output_file = os.path.join(review_dir, f"test결과_{date_str}.md")

    mode_str = "한국어 → 일본어" if mode == 1 else "일본어 → 한국어"

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## {file_name} - {mode_str} (테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
        f.write("| 한국어 | 일본어 | 복습 |\n")
        f.write("|--------|--------|------|\n")

    return output_file

def print_results(wrong_count, output_file):
    """테스트 결과 출력"""
    print(f"\n=== 테스트 완료 ===")
    if wrong_count == 0:
        print("모든 단어를 알고 계십니다! 🎉")
    else:
        print(f"틀린 단어: {wrong_count}개")
        print(f"결과 저장: {output_file}")

def main():
    # 파일 선택
    file_name = select_file()
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    # 단어 파싱
    words = parse_markdown_table(file_path)

    if not words:
        print("단어를 찾을 수 없습니다.")
        return

    print(f"\n{len(words)}개의 단어를 찾았습니다.")

    # 단어 순서 섞기
    random.shuffle(words)

    # 모드 선택
    mode = select_mode()

    # 결과 파일 초기화 (헤더 작성)
    output_file = initialize_result_file(mode, file_name)

    # 테스트 실행 (1을 누를 때마다 바로 파일에 저장됨)
    wrong_count = run_test(words, mode, output_file)

    # 결과 출력
    print_results(wrong_count, output_file)

if __name__ == "__main__":
    main()
