import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.main import main

def korean2num(sent: str) -> str:
    """worker function"""
    return main(sent)

if __name__ == "__main__":
    # start = time.time()
    print(korean2num("어 전체 확진자의 구십구점오프로는 무증상 경증의 재택 치료자분들입니다 대면 진료나 목내 처방을 받는데 불편함이 없도록 이십사시간 의료상담과 대응체계를 구축하겠습니다."))
    print(korean2num("만 이십 세 이상의 대인은 만 원이에요."))
    print(korean2num("난 단 만이십원 있다."))
    # print("time :", (time.time() - start))