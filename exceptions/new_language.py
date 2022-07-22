from typing  import Dict

#defined_dictionary = ['코로나일구','이공삼공','일월','삼월','사월','오월','유월','칠월','팔월','구월','시월','십일월','십이월','육이오','삼일절','사일구혁명','지세번']
#changed_dictionary = ['코로나19','2030','1월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월','6.25','3.1절','4.19혁명','G7']

DICTIONARY: Dict[str, str] = {
    "코로나일구" : "코로나19",
    "이공삼공" : "2030",
    "육이오" : "6.25",
    "삼일절" : "3.1절",
    "사일구혁명" : "4.19혁명",
    "지세번" : "G7"
}


def apply_dictionary(sentence: str) -> str:
    if not any(dictionary_key in sentence for dictionary_key in DICTIONARY):
        return sentence
    for dictionary_key in DICTIONARY:
        sentence = sentence.replace(dictionary_key, DICTIONARY[dictionary_key]) 
    return sentence



#레아를 활용해야 할듯
#NNG  mecab

#lea에서 nng인거를 가져와서 그것을 설치로 찾고 있으면 형태소와 맞는지 확인하고 만약 다르게 나왔다. nr꼴로 나와있었다. 그럼 형태소두개를 한개로 합쳐서 다시넣어준다.

