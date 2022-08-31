from contextlib import AbstractAsyncContextManager
import os
from re import A
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.function import lang_dict, sentence_parser, pattern_language, month_exception, phone_number, tag_correction
from src.util import transform_index, pos

def korean2num(sentence: str) -> str:
    """worker function"""

    if sentence.strip() == "":
        return sentence

    nominative_case_pos_tags = ["JKS", "JKC", "JX", "JKO" ] #JKG (?)
    nominative_case_pos_keys = ["이", "을", "를", "가", "은", "는"]
    sentence_pos = tag_correction.correct_tags(sentence,  pos.get_pos(sentence))

    # print(sentence_pos)

    split_sentence = []
    result_sentence = ""
    sentence_start_index = 0
    sentence_end_index = 0
    for pos_index, pos_element in enumerate(sentence_pos):
        if (
            any(nominative_case_pos_key == pos_element[0] for nominative_case_pos_key in nominative_case_pos_keys) 
            and any(nominative_case_pos_tag == pos_element[1] for nominative_case_pos_tag in nominative_case_pos_tags)
        ):
            sentence_end_index = transform_index.get_txt_ind_impr(sentence, pos_index) + 2
            split_sentence.append(sentence[sentence_start_index:sentence_end_index])
            sentence_start_index = sentence_end_index
    
    split_sentence.append(sentence[sentence_start_index:])

    for i in range(len(split_sentence)):
        # sentence_pos = pos.get_pos(split_sentence[i])
        # print(pos.get_pos(split_sentence[i]))
        # print(split_sentence[i])
        split_sentence[i] = pattern_language.convert_regular_expression(split_sentence[i])
        # print(split_sentence[i])
        # split_sentence[i] = phone_number.phone_number_exception(split_sentence[i], sentence_pos)
        # print(split_sentence[i])
        split_sentence[i] = lang_dict.apply_dictionary(split_sentence[i])
        # print(split_sentence[i])
        sentence_pos = pos.get_pos(split_sentence[i])
        split_sentence[i] = sentence_parser.PutNumber(split_sentence[i], sentence_pos)
        # print(split_sentence[i])
        # split_sentence[i] = month_exception.get_month_exception(split_sentence[i], sentence_pos)
        # print(split_sentence[i])
        split_sentence[i] = lang_dict.revert_error_words(split_sentence[i])
        # print(split_sentence[i])
        split_sentence[i] = pattern_language.convert_text_regular_expression(split_sentence[i])
        # print(split_sentence[i])
        split_sentence[i] = pattern_language.revert_regular_expression(split_sentence[i])

        # 변환

        # print(split_sentence[i])
        result_sentence += split_sentence[i]

    return result_sentence

if __name__ == '__main__':
    text = [
        # '내 전화번호는 공일공 이이이이 오오오오입니다. 니 전화번호는 뭐니?',
        # '나는 이번 유 월 사일에 본 시험에서 구점 사점을 받았어.',
        # '기상청에서는 올 이월에도 꽃샘추위가 몇 차례 찾아올 것이라고 전망하였다',
        # "허리나 요충사업원 또는 요추",
        # "내 인천 동구미추홀구 갑 허종식 의원입니다.",
        # "그렇게 받아들이기로 했고 이천이십일년도 부터는 강제사항이 되었습니다.",
        # "금정구 국민의 국회의원 백종현입니다.",
        # "오히려 그 당시에 국민들이 그렇게 반대하던 한일정상회담을 야당 정치인으로서 유일하게 찬성한다.",
        # "더민주당 위원님이 이야기했듯이 뚜렷한 역사관 또 백 범의 문화대국이라는 그런.",
        # "떨어져 일 때를 대비해서",
        # "구월 사일에 태어났다.",
        # "백범 김구선생님은 고구려 여행을 가셨다.",
        # "나는 백제유물을 가지고있어",
        # "이 박보균 후보자는 육왕 생일 축하연에",
        # "떨어져 일 때 나는 죽었어",
        # "나는 담배 스무갑을 피웠어",
        # "나는 전과 구범 이야.",
        # "여기서 누구가 전과 백범 이야?",
        # "여기서 누구가 전과 이십오범 이야?",
        # "여기서 누구가 전과 구천구백구십구범 이야?",
        # "여기서 누구가 영범 이야?",
        # "네 그~ 코로나일구로 지금 거의 오륙 개월 정도 국민들께서 많이 외부 활동을 못하시고",
        # "철인 삼 종 폭력피해 선수 자살사건 경과보고 이게 여기 깔려 있나요?",
        # "조사단은 대한체육회 대한철인삼종협회 등에 대하여 제보사항 처리과정의 적정성과 선수인권보호시스템 전반에 대해 감사조사를 실시할 예정이며 책임있는 관련자들을 일벌백계함은 물론 재발방지대책도 마련할 계획입니다.",
        # "제사항에서 ",
        # "십시일반",
        # "그 조건일시에 적용했다",
        # "그 조건 일시에 적용했다",
        # "그 조건일 시에 적용했다",
        # "그 조건 일 시에 적용했다",
        # "내 눈은 사 시가 아니다.",
        # "나는 이공삼공 세대에서 ",
        # "지금은 삼시 사십분 이야",
        # "매뉴얼 육만천팔백구십육다시일을 한번 봐봐",
        # "일일히 확인했다.",
        # "일일이 전화해봐",
        # "광고 회사의 사업자등록번호를 조회하니 공 공 일 다시 공 공 다시 사 삼 이 이 오 가 조회 결과로 나왔다. 또 사십삼년 전에도",
        # " 육쪽입니까? 확인해보세요 보시면 이십삼쪽에 나와있다고 하네요. 그러면 백제문화유산인데 그래도 되나요?",
        # "이 시간부터 코딩을 해보겠습니다.",
        # "메달이 정해진 순간, 은메달 선수의 행복도는 십 점 중 사 점 팔 점, 동메달 선수는 칠 점 일 점이라는 분석이 있다",
        # "광고 회사의 사업자등록번호를 조회하니 공공일다시공공다시사삼이이오가 조회 결과로 나왔다.",
        # "이천 이십 년 전 세계 경제회복을 위한 예산 지출의 오 분의 일 가량만 탄소 감축 예산으로 배정된 것으로 나타났다.",
        # "이월달에 이월했다.",
        # "나는 십이월 일일에 출소했어",
        # "나는 십이월 삼십일일에 출소했어",
        
        # "어 국민들께서 우려하고 계신데 어 제가 봐 온 복지는 위기앞에 여야가 없었습니 이번에도 두분 간사님께서 지혜를 잘 모아 주실 거라고 생각합니다.",
        # "보건복지부 간사 선임해 주신 것에 감사드립니다 제가 사실은 간사 간사로 선임은 받았습니다만 일시 사 일 신상의 이유로 당분간 직무대행을 좀 지정하고 어 운영",
        # "보니까 여야가 동서로 두분씩이 바뀐 것 같아요 두 분 씩이 새로 오신 분이고 또 정의 당의 우리 또 강인인 모시고 해서 다섯분이 이제 전반기와 다르게 새로운 분이 오신 것 같아요.",
        # "하반기에 구십육만 명물을 추가로 도입하여 일 확진자 삼십 명 부분까지 충분히 대응할 수 있도록 준비하고 있습니다.",
        # "어 전체 확진자의 구십구점오프로는 무증상 경증의 재택 치료자분들입니다 대면 진료나 목내 처방을 받는데 불편함이 없도록 이십사시간 의료상담과 대응체계를 구축하겠습니다.",
        # "포스트 오미크론 어 시기에는 일상회복을 추진하되",
        # "이거 잘못된 거 아닙니까 삼십인 미만이라는 거는 숫자로 기업을",
        # "어 아직 어 못 만났습니다 앞으로 코백회 협의체를 만나시면서 피해자들의",
        # "이만 어 이십오만 건이기 때문에 아 이천오백만 건이기 때문에 스토탈",
        # "이 말씀이신 거죠 알겠습니다 오십대 백신접종 확대에 관해서 어 어 질의하도록 하겠습니다.",
        # "내 이메일 주소는 제이오이골뱅이지메일닷컴이야",
        # "내 점수는 오십오점이야",
        # "오점이야",
        "만 이십 세 이상의 대인은 만 원이에요.",
        # "난 단 만이십원 있다."
    ]
    for item in text:
        # print(item)
        print(item)
        print(tag_correction.FilterNone_toNR(item,tag_correction.FilterNR_toNone(item,  pos.get_pos(item))))
        start = time.time()
        item = korean2num(item)
        print("time :", (time.time() - start))
        print(item)
        print()
