# import stanza
# stanza.download('ru')
#
# ppln = stanza.Pipeline('ru', processors='tokenize,pos')
# txt = """Без справки вход воспрещен: с какими болезнями не пускают в бассейн
# В Удмуртии сократилось количество госпитализаций заболевших COVID-19
# В Москве нашли нарушения антиковидных мер на 118 объектах
# Минздрав предложил запретить частным клиникам выдавать медсправки на оружие
# """
#
# doc = ppln(txt)
# print(*[f'word: {word.text}\tupos: {word.upos}\tfeats: {word.feats if word.feats else "_"}'
#         for snt in doc.sentences for word in snt.words], sep='\n')


with open("C:/Users/Айгуль/PycharmProjects/Project_dep_1/project_data_in/pos_deprel/negative_line_for_pos_deprel.txt", "r", encoding="utf-8") as f:
        phrase_list = [x.strip('"') for x in f.readlines()]
        print(phrase_list)


# infile = open("C:/Users/Айгуль/PycharmProjects/Project_dep_1/"
#               "project_data_in/pos_deprel/negative_line_for_pos_deprel.txt", "r+")
# line = infile.readline()
# print(line)
#
# line  = line.replace('"', '')