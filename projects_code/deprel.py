import stanza
stanza.download('ru')

ppln = stanza.Pipeline('ru', processors='tokenize,pos,lemma,depparse')
txt = """
ТЦ «Авиапарк» в Москве пригрозили закрыть за нарушения масочного режима
В России вновь выявили более 22 тыс. случаев заражения COVID-19
В Удмуртии и Пермском крае введут QR-коды, коронавирусные ограничения также ужесточили Саратовская и Курская области
Мурашко напомнил о высоком риске смерти в течение полугода после COVID-19
В России за сутки от COVID умерло рекордное число больных
Минобороны заявило о планах ВСУ повторить в Лисичанске провокацию в Буче
... нанесении ударов по объектам гражданской инфраструктуры, добавили в Минобороны России. [ РБК ] Путин сравнил Бучу с «фейками о применении химоружия» в Сирии ... , пока они контролировали город, «ни один местный житель не пострадал». [ РБК ] Захарова заявила о подготовке силами НАТО провокаций на Украине Глава ...
ТЦ «Авиапарк» в Москве пригрозили закрыть за нарушения масочного режима
В России вновь выявили более 22 тыс. случаев заражения COVID-19
Мурашко напомнил о высоком риске смерти в течение полугода после COVID-19
В России за сутки от COVID умерло рекордное число больных
МВД сообщило о снижении ущерба от преступлений почти на 9%
Зеленский сравнил коронавирус с аварией на Чернобыльской АЭС
МВД сообщило о 1250 протоколах на нарушителей самоизоляции
Путин подписал закон об уголовной ответственности за нарушение карантина
Путин утвердил штрафы за нарушение карантина и фейки о коронавирусе
Путин заявил об ухудшении ситуации с коронавирусом в России
Мосгордума приняла закон о штрафах для нарушителей самоизоляции
Врачи объяснили высокую смертность в Италии последствиями эпидемии гриппа
"""

doc = ppln(txt)

print(*[f'word: {word.text}\thead: {snt.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}'
        for snt in doc.sentences for word in snt.words], sep='\n')