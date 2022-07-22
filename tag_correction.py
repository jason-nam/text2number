import pos

def num_two_correction(sentence):
    if sentence.replace(" ",'') =='':
        return pos.get_pos(sentence)
    sen_pos = pos.get_pos(sentence)
    newList =[]
    place = 0
    for i in range(len(sen_pos)-1):
        if sen_pos[i]==('이', 'JKS'):
            if sen_pos[i+1][1]=='NR':
                for a in range(place, len(sentence)):
                    if sentence[a:a+2]=='이'+sen_pos[i+1][0]:
                       newList.append(('이', 'NR'))
                       place = a
                       break
            else: newList.append(sen_pos[i])
        else: newList.append(sen_pos[i])
    newList.append(sen_pos[len(sen_pos)-1])
    return newList