import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.function import sentence_parser, new_language, pattern_language, month_exception, phone_number, tag_correction
from src.util import transform_index, pos

def korean2num(sentence: str) -> str:
    """worker function"""

    if sentence.strip() == "":
        return sentence

    nominative_case_pos_tags = ["JKS", "JKC", "JX", "JKO" ] #JKG (?)
    nominative_case_pos_keys = ["이", "을", "를", "가", "은", "는"]
    sentence_pos = tag_correction.apply_tag_correction(sentence, pos.get_pos(sentence))

    # print(sentence_pos)

    split_sentence = []
    result_sentence = ""
    sentence_start_index = 0
    sentence_end_index = 0
    for pos_index, pos_element in enumerate(sentence_pos):
        if any(nominative_case_pos_key == pos_element[0] for nominative_case_pos_key in nominative_case_pos_keys) and any(nominative_case_pos_tag == pos_element[1] for nominative_case_pos_tag in nominative_case_pos_tags):
            sentence_end_index = transform_index.get_txt_ind_impr(sentence, pos_index) + 2
            split_sentence.append(sentence[sentence_start_index:sentence_end_index])
            sentence_start_index = sentence_end_index
    split_sentence.append(sentence[sentence_start_index:])

    for i in range(len(split_sentence)):

        sentence_pos = pos.get_pos(split_sentence[i])
        # print(pos.get_pos(split_sentence[i]))
        # print(split_sentence[i])
        split_sentence[i] = pattern_language.apply_regular_expression(split_sentence[i])
        # print(split_sentence[i])
        split_sentence[i] = phone_number.phone_number_exception(split_sentence[i], sentence_pos)
        # print(split_sentence[i])
        split_sentence[i] = new_language.apply_dictionary(split_sentence[i])
        # print(split_sentence[i])
        split_sentence[i] = pattern_language.apply_regular_expression_before_convert(split_sentence[i])
        # print(split_sentence[i])
        split_sentence[i] = sentence_parser.PutNumber(split_sentence[i], sentence_pos)
        # print(split_sentence[i])
        split_sentence[i] = month_exception.get_month_exception(split_sentence[i], sentence_pos)
        # print(split_sentence[i])
        split_sentence[i] = new_language.revert_error_words(split_sentence[i])
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
        "그렇게 받아들이기로 했고 이천이십일년도 부터는 강제사항이 되었습니다.",
        # "금정구 국민의 국회의원 백종현입니다.",
        # "오히려 그 당시에 국민들이 그렇게 반대하던 한일정상회담을 야당 정치인으로서 유일하게 찬성한다.","더민주당 위원님이 이야기했듯이 뚜렷한 역사관 또 백 범의 문화대국이라는 그런.",
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
        "철인 삼 종 폭력피해 선수 자살사건 경과보고 이게 여기 깔려 있나요?",
        "조사단은 대한체육회 대한철인삼종협회 등에 대하여 제보사항 처리과정의 적정성과 선수인권보호시스템 전반에 대해 감사조사를 실시할 예정이며 책임있는 관련자들을 일벌백계함은 물론 재발방지대책도 마련할 계획입니다.",
        "제사항에서 ",
        "십시일반",
        "그 조건일시에 적용했다",
        "그 조건 일시에 적용했다",
        "그 조건일 시에 적용했다",
        "그 조건 일 시에 적용했다",
        "내 눈은 사 시가 아니다.",
        ""
    ]
    for item in text:
        # print(item)
        
        print(tag_correction.apply_tag_correction(item, pos.get_pos(item)))
        item = korean2num(item)
        print(item)
        print()