
from collections import Counter

from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from pymorphy2.tokenizers import simple_word_tokenize
from pymystem3 import Mystem
from tqdm import tqdm
from wordcloud import WordCloud

import nltk
nltk.download('stopwords')
stops = stopwords.words("russian")
meaningful_pos = ["A", "ADV", "S", "V"]
mystem = Mystem()


def parse_lines(lines, mystem, stops):
    ready_lines = []
    for line in lines:
        good_tokens = []

        for word_analysis in mystem.analyze(line):
            if word_analysis.get("analysis"):
                lemma = word_analysis["analysis"][0]["lex"]
                pos = word_analysis["analysis"][0]["gr"].split("=")[0].split(",")[0]
                if (lemma not in stops) and (pos in meaningful_pos):
                    good_tokens.append(lemma)
        if good_tokens:
            ready_lines.append(" ".join(good_tokens))
    return ready_lines

with open("C:/Users/Айгуль/PycharmProjects/"
          "Project_dep_1/project_data_in/negative_lines_lemmas_ria.txt", "r", encoding="utf-8") as f_pos:
    neg_lines = parse_lines(f_pos.readlines(), mystem, stops)

negative_c = Counter()

for line in tqdm(neg_lines):
    tokens = simple_word_tokenize(line)
    negative_c.update(tokens)

print(negative_c.most_common(100))

#
# wordcloud = WordCloud(background_color="white").generate(" ".join(neg_lines))
# wordcloud = wordcloud.to_file('C:/Users/Айгуль/PycharmProjects/Project_dep_1/images/.wordcloud_ria_neg.png')

# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.savefig("C:/Users/Айгуль/PycharmProjects/Project_dep_1/images/wordcloud_negative_ria.png")



# Positive

with open("C:/Users/Айгуль/PycharmProjects/"
          "Project_dep_1/project_data_in/positive_lines_lemmas_ria.txt", "r", encoding="utf-8") as f:
    pos_lines = parse_lines(f.readlines(), mystem, stops)

positive_c = Counter()

for line in tqdm(pos_lines):
    tokens = simple_word_tokenize(line)
    positive_c.update(tokens)

print(positive_c.most_common(100))

# wordcloud = WordCloud(background_color="white").generate(" ".join(pos_lines))
# wordcloud = wordcloud.to_file('C:/Users/Айгуль/PycharmProjects/Project_dep_1/images/.wordcloud_ria_pos.png')

# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.savefig("C:/Users/Айгуль/PycharmProjects/Project_dep_1/images/wordcloud_pos_ria.png")

# _______________________________________
# Are there any words that are in both lists?

lemmas_both = set(positive_c.elements()) & set(negative_c.elements())
len_positive = len(simple_word_tokenize(" ".join(pos_lines)))
len_negative = len(simple_word_tokenize(" ".join(neg_lines)))

len(lemmas_both), len_positive, len_negative

pos_freqs = []
neg_freqs = []
for em_lemma in lemmas_both:
    pos_freqs.append(positive_c[em_lemma])
    neg_freqs.append(negative_c[em_lemma])

plt.hist(pos_freqs, bins=100)
plt.savefig("C:/Users/Айгуль/PycharmProjects/Project_dep_1/images/plt_hist_both.png")


print(Counter(pos_freqs))
