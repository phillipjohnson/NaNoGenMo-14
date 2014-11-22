import random
import numpy as np
from scipy import stats

nanogenmoseed = 727272
np.random.RandomState(nanogenmoseed)
np.random.seed(nanogenmoseed)
random.seed(nanogenmoseed)

concordance_cache = {}

line_lengths = {1: 0.37012475970532455, 2: 0.13680991884813376, 3: 0.05066508405475493, 4: 0.019468706859848535, 5: 0.00896670064121586, 6: 0.004683327097498355, 7: 0.002425524777767743, 8: 0.001535305577416816, 9: 0.0010579416583880582, 10: 0.0003741500986982157, 11: 0.0005289708291940291, 12: 0.0003096414609916268, 13: 0.0001419190029544956, 14: 7.74103652479067e-05, 15: 0.00012901727541317782, 16: 6.450863770658891e-05, 17: 5.160691016527113e-05, 18: 0.00010321382033054225, 19: 5.160691016527113e-05, 20: 3.870518262395335e-05, 21: 1.2901727541317782e-05, 22: 3.870518262395335e-05, 23: 2.5803455082635563e-05, 24: 1.2901727541317782e-05, 26: 1.2901727541317782e-05, 34: 1.2901727541317782e-05, 37: 1.2901727541317782e-05}
sentence_lengths = {1: 0.2617742283617526, 2: 0.1997625728469674, 3: 0.2009712928987697, 4: 0.19697819987049428, 5: 0.17209151737535075, 6: 0.14213252751996547, 7: 0.11187135765162962, 8: 0.08644506799050292, 9: 0.06440751133175049, 10: 0.04871573494496007, 11: 0.037686164472264194, 12: 0.02831858407079646, 13: 0.02421756960932441, 14: 0.01804446363047701, 15: 0.015756529246708395, 16: 0.012238290524498166, 17: 0.009086984675156486, 18: 0.0075545003237643, 19: 0.006367364558601338, 20: 0.0051370602201597235, 21: 0.004619037340815886, 22: 0.003453485862292251, 23: 0.002762788689833801, 24: 0.002352687243686596, 25: 0.0019210015109000647, 26: 0.0013598100582775739, 27: 0.0009928771854090222, 28: 0.001251888625080941, 29: 0.0005827757392618173, 30: 0.0006906971724584503, 31: 0.0005611914526224909, 32: 0.000453270019425858, 33: 0.00032376429958989856, 34: 0.00034534858622922514, 35: 0.00032376429958989856, 36: 0.00019425857975393913, 37: 0.00015109000647528598, 38: 0.00019425857975393913, 39: 0.00017267429311461257, 40: 8.633714655730629e-05, 41: 6.475285991797971e-05, 42: 6.475285991797971e-05, 43: 6.475285991797971e-05, 44: 2.158428663932657e-05, 45: 8.633714655730629e-05, 46: 4.316857327865314e-05, 47: 6.475285991797971e-05, 48: 4.316857327865314e-05, 49: 4.316857327865314e-05, 52: 2.158428663932657e-05, 53: 2.158428663932657e-05, 54: 2.158428663932657e-05, 56: 2.158428663932657e-05, 62: 2.158428663932657e-05, 75: 2.158428663932657e-05}
sentence_types = {'2': 0.11148124313888784, '1': 0.665568888720647, '3': 0.2229498681404651}


def create_probability(d):
    return stats.rv_discrete(a=1, values=(list(d.keys()), list(d.values())))


def create_concordance_probability(d):
    word_list = list(d.keys())
    freq_list = list(d.values())
    word_order_list = [x for x in range(len(word_list))]
    probs = stats.rv_discrete(a=0, values=(word_order_list, freq_list))

    return CacheResult(word_list, probs)


sentence_length_prob = create_probability(sentence_lengths)
line_length_prob = create_probability(line_lengths)
sentence_type_prob = create_probability(sentence_types)


def get_line_length():
    return get_rand_from_prob(line_length_prob)


def get_sentence_length():
    return get_rand_from_prob(sentence_length_prob)


def get_sentence_type():
    return get_rand_from_prob(sentence_type_prob)


def get_rand_from_prob(prob):
    return prob.rvs(size=1)[0]


def put_word_in_cache(word, concordances):
    cache_result = create_concordance_probability(concordances)
    concordance_cache[word] = cache_result


def get_concordance_from_cache(word):
    if not concordance_cache.get(word):
        return None
    return concordance_cache.get(word).get_next_word()


class CacheResult:
    def __init__(self, word_list, frequency_dictionary):
        self.word_list = word_list
        self.frequency_dictionary = frequency_dictionary

    def get_next_word(self):
        word_ordinal = get_rand_from_prob(self.frequency_dictionary)
        return self.word_list[word_ordinal]