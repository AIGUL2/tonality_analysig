import stanza
stanza.download('ru')


ppln = stanza.Pipeline('ru', processors='tokenize,pos')
txt = """
Путин рассказал о работе по улучшению условий для женщин с детьми
Фонд Круг добра обеспечил лекарствами почти 1,6 тысячи детей
Голикова рассказала о привилегиях для COVID-free-регионов
Путин поблагодарил тех, кто помогал восстановить собор в Волгограде
Гурцкая считает, что голосование для инвалидов стало комфортнее и доступнее
Фальков заявил о важности психологического благополучия студентов
России важны и хорошие дороги, и хорошая армия, заявил Песков
Фертильность у женщин: как рассчитать лучший день для зачатия ребенка
Названы продукты, улучшающие работу мозга
Путин призвал выделять деньги на создание правильного образа учителя
Путин подчеркнул важность возврата соцвыплат, списанных на кредиты
Названо безопасное количество мяса для человека

"""

doc = ppln(txt)
# print(*[f'word: {word.text}\tupos: {word.upos}\tfeats: {word.feats if word.feats else "_"}'
#         for snt in doc.sentences for word in snt.words], sep='\n')

# print(*[f'upos: {word.upos}\tfeats: {word.feats if word.feats else "_"}'
#         for snt in doc.sentences for word in snt.words], sep='\n')

print(*[f'upos: {word.upos}'
        for snt in doc.sentences for word in snt.words], sep='\n')