import os
import pandas as pd
from pymystem3 import Mystem
from tqdm import tqdm


def load_phrase_list():
    """Loads ria_data.txt for the experiment.

    :returns phrase_list (str) - list of data
    """
    with open("C:/Users/Айгуль/PycharmProjects/Project_dep_1/project_data_in/rbc_data.txt", "r", encoding="utf-8") as f:
        phrase_list = [x.strip('"') for x in f.readlines()]
    return phrase_list


def prepare_lexicons():
    """Loads lexicons for the experiment.

    :returns lexicons_dict (dict) - dictionary with all lexicons used
    """
    path_to_lexicons = "C:/Users/Айгуль/PycharmProjects/Project_dep_1/sentiment_datasets"
    lexicons = [lex[:-4] for lex in os.listdir(path_to_lexicons) if lex.endswith(".csv")]
    lexicons_dict = {}
    for lexicon in lexicons:
        lex_df = pd.read_csv("C:/Users/Айгуль/PycharmProjects/Project_dep_1/sentiment_datasets/{}.csv".format(lexicon),
                             sep=";", encoding="utf-8")
        lexicons_dict[lexicon] = lex_df
    return lexicons_dict


def evaluate_phrase_polarity(phrase, lexicon, mystem):
    """Calculates polarity for the whole phrase.

    :arg phrase (str) - phrase to evaluate
    :arg lexicon (pandas.DataFrame) - lexicon to check the lemmas
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns sign(phrase_sum) (int) - calculated polarity
    """
    sign = lambda x: x and (1, -1)[int(x) < 0]
    phrase_sum = 0
    lemmas = [parse["analysis"][0]["lex"] for parse in mystem.analyze(phrase) if parse.get("analysis")]

    for lemma in lemmas:
        if lemma in lexicon["lemma"].values:
            lemma_polarity = lexicon[lexicon["lemma"] == lemma].iloc[0]["sentiment"]
            phrase_sum += lemma_polarity
    return sign(phrase_sum)


def analyse_line_all_lexicons(dict_by_line, phrase, phrase_list, lexicons_dict, mystem):
    """Analyses one line against all lexicons, saves changes to a dataframe.

    :arg dict_by_line (dict) - storage for all results
    :arg phrase (str)
    :arg phrase_list (list of str) - lines to analyse
    :arg lexicons_dict (dict) - storage of all lexicons
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns dict_by_line (dict) - parsed lines
    """
    dict_by_line["line"].append(phrase)
    phrase_lemmas = " ".join(
        [parse["analysis"][0]["lex"] for parse in mystem.analyze(phrase) if parse.get("analysis")])
    dict_by_line["line, lemmas"].append(phrase_lemmas)
    for lexicon_name in lexicons_dict.keys():
        lexicon = lexicons_dict[lexicon_name]
        polarity = evaluate_phrase_polarity(phrase_lemmas, lexicon, mystem)
        dict_by_line[lexicon_name].append(polarity)
    return dict_by_line


def analysis_by_line(lexicons_dict, phrase_list, mystem):
    """Pipeline for analysingphrases line-by-line.

    :arg lexicons_dict (dict) - lexicons to use
    :arg phrase_list (list of str)
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns None
    """
    dict_by_line = {
        "phrase": [],
        "line": [],
        "line, lemmas": [],
        "RuSentiLex": [],
        "EmoLex": [],
        "LinisCrowd": [],
        "ChenSkiena": [],
        "ProductSentiRus": [],
        "SentiRusColl": []
    }
    for phrase in tqdm(phrase_list):
        dict_by_line = analyse_line_all_lexicons(dict_by_line, phrase, phrase_list, lexicons_dict, mystem)
    df_by_line = pd.DataFrame.from_dict(dict_by_line, orient='index')
    # df_by_line = pd.DataFrame.from_dict(dict_by_line)
    df_by_line = df_by_line.transpose()
    df_by_line.to_csv("C:/Users/Айгуль/PycharmProjects/Project_dep_1/projects_data_output/"
                      "lexicons_to_line_for_rbc_data.csv")


def analyse_type(phrases, lexicon, mystem, lexicon_name):
    """Pipeline for sentiment analysis of all phrases of a given type in a phrase.

    :param lexicon_name:
    :arg phrases (list of str) - phrase lines
    :arg lexicon (pandas.DataFrame) - lexicon to check the lemmas
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns type_total (int) - line count
    :returns type_positive (int) - count of positively evaluated lines
    :returns type_negative (int) - count of negatively evaluated lines
    """
    type_total = len(phrases)
    type_positive = 0
    type_negative = 0
    for phrase in phrases:
        sent = evaluate_phrase_polarity(phrase, lexicon, mystem)
        if sent > 0:
            type_positive += 1
        else:
            type_negative += 1

    lists = [type_total, type_positive, type_negative, lexicon_name]
    return lists


def analyse_phrase(overall_dict, phrase, tpe):
    """Analyses phrase in general.

    :param tpe:
    :arg overall_dict (dict) - storage for all results
    :arg phrase (str) -phrase name to access TXT files
    # :arg lexicon_name (str) - lexicon name
    # :arg lexicon (pandas.DataFrame) - lexicon and polarity values
    # :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns overall_dict (dict) - updated dict
    """

    overall_dict["phrase"].append(phrase)
    overall_dict["lexicon"].append(tpe[3])
    overall_dict["polatity, total"].append(tpe[0])
    overall_dict["polatity positive"].append(tpe[1])
    overall_dict["polatity positive, %"].append(tpe[1] / tpe[0] * 100)
    overall_dict["polatity negative"].append(tpe[2])
    overall_dict["polatity negative, %"].append(tpe[2] / tpe[0] * 100)

    return overall_dict


def analysis_by_phrase(lexicons_dict, phrase_list, mystem):
    """Pipeline for analysis by phrase.

    :arg lexicons_dict (dict) - lexicons to use
    :arg phrase_list (list of str)
    :arg mystem (pymystem3.mystem.Mystem) - an instance of morphological analyzer

    :returns None
    """
    tpes = []
    overall_dict = {
        "phrase": [],
        "lexicon": [],
        "polatity, total": [],
        "polatity positive": [],
        "polatity positive, %": [],
        "polatity negative": [],
        "polatity negative, %": []
    }
    for lexicon_name in lexicons_dict:
        tpes.append(analyse_type(phrase_list, lexicons_dict[lexicon_name], mystem, lexicon_name))

    for phrase in tqdm(phrase_list):
        for tpe in tpes:
            overall_dict = analyse_phrase(overall_dict, phrase, tpe)
    df = pd.DataFrame.from_dict(overall_dict)
    df.to_csv("C:/Users/Айгуль/PycharmProjects/Project_dep_1/projects_data_output/lexicons_experiment_for_rbc.csv")


def main():
    lexicons_dict = prepare_lexicons()
    phrase_list = load_phrase_list()
    mystem = Mystem()
    analysis_by_line(lexicons_dict, phrase_list, mystem)
    analysis_by_phrase(lexicons_dict, phrase_list, mystem)


if __name__ == "__main__":
    main()


