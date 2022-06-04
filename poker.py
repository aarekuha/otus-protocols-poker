#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools
import collections

SUIT: int = 1  # Индекс масти
RANK: int = 0  # Индекс ранга(веса) карты
JOKER_RANK: str = '?'

WEIGHTS: dict = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
    '?': 15,
}


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand: list[str]) -> list[str]:
    """
        Возвращает список рангов (его числовой эквивалент),
            отсортированный от большего к меньшему
        >>> card_ranks("TD TC TH 7C 7D 8C 8S".split())
        ['T', 'T', 'T', '8', '8', '7', '7']
        >>> card_ranks("6C 7C ?R 9C TC 5C ?B".split())
        ['?', '?', 'T', '9', '7', '6', '5']
    """
    sorted_hand: list[str] = sorted(hand, key=lambda card: WEIGHTS[card[RANK]], reverse=True)
    return [card[RANK] for card in sorted_hand]


def flush(hand: list[str]) -> bool:
    """
        Возвращает True, если все карты одной масти
        >>> flush("TD TC TH 7C 7D 8C 8S".split())
        False
        >>> flush("6C 7C ?R 9C TC 5C ?B".split())
        True
        >>> flush("6C 7S 2C 9C TD 5C 3C".split())
        True
        >>> flush("6C 7S ?R 9C TD 5C 2C".split())
        False
        >>> flush("6C 7S ?B 9C TD 5C 2C".split())
        True
    """
    clean_hand: list[str] = hand.copy()
    # Заменить джокеры на две карты каждой масти
    if '?B' in clean_hand:
        clean_hand.remove('?B')
        clean_hand += ['?C', '?S']
    if '?R' in clean_hand:
        clean_hand.remove('?R')
        clean_hand += ['?H', '?D']
    # Посчитать количество карт каждой масти
    groupped_cards: collections.Counter = collections.Counter(card[SUIT] for card in clean_hand)
    most_common_count: int = next(iter(groupped_cards.most_common()))[1]
    return most_common_count >= 5


def straight(sorted_ranks: list[str]) -> bool:
    """
        Возвращает True, если отсортированные ранги формируют последовательность 5ти,
            где у 5ти карт ранги идут по порядку (стрит)
        >>> straight("A K Q J T".split())
        True
        >>> straight("A Q J T 9 8 2".split())
        True
        >>> straight("? A Q J T 2 3".split())
        True
        >>> straight("? ? Q J T 8 7".split())
        True
        >>> straight("? ? Q J 7 2 2".split())
        False
    """
    return False


def kind(n: int, sorted_ranks: list[str]) -> str | None:
    """
        Возвращает первый ранг, который n раз встречается в данной руке.
        Возвращает None, если ничего не найдено
        >>> kind(2, "A A K Q J T 9 8".split())
        'A'
        >>> kind(2, "A K Q J J T 9 8".split())
        'J'
        >>> kind(2, "A K Q J T 9 8 7".split()) is None
        True
        >>> kind(2, "? ? K Q J T 9 8".split())
        '?'
        >>> kind(2, "? K Q J T 9 8 2".split())
        'K'
        >>> kind(3, "? K Q J T T 8 2".split())
        'T'
        >>> kind(4, "? K Q J T 2 2 2".split())
        '2'
    """
    ranks_counter: collections.Counter = collections.Counter(rank for rank in sorted_ranks)
    jokers_count: int = sorted_ranks.count(JOKER_RANK)
    for rank in ranks_counter:
        hit_pure: bool = (ranks_counter[rank] == n)
        hit_with_jokers: bool = (ranks_counter[rank] + jokers_count >= n) and (rank != JOKER_RANK)
        if hit_pure or hit_with_jokers:
            return rank

    return None


def two_pair(sorted_ranks: list[str]) -> list[str] | None:
    """
        Если есть две пары, то возврщает два соответствующих ранга,
            иначе возвращает None
        >>> two_pair("A A K Q J T 9 9".split())
        ['A', '9']
        >>> two_pair("A K K Q J T 9 9".split())
        ['K', '9']
        >>> two_pair("A K K Q J T 9 9".split())
        ['K', '9']
        >>> two_pair("A K K Q J J 9 9".split())
        ['K', 'J']
        >>> two_pair("? K K Q J T 9 8".split())
        ['K', 'Q']
        >>> two_pair("? ? K J T 9 8 2".split())
        ['K', 'J']
        >>> two_pair("K Q J T 9 8 7 6".split()) is None
        True
        >>> two_pair("? Q J T 9 8 7 6".split()) is None
        True
    """
    ranks_counter: collections.Counter = collections.Counter(rank for rank in sorted_ranks)
    jokers_count: int = sorted_ranks.count(JOKER_RANK)
    # Дополнить количество джокерами
    for rank, count in ranks_counter.items():
        if rank == JOKER_RANK:
            continue
        if not jokers_count:
            break
        if count == 1:
            ranks_counter[rank] = 2
            jokers_count -= 1
    pair_ranks: dict = {rank: count for rank, count in ranks_counter.items() if count > 1 and rank != JOKER_RANK}
    if len(pair_ranks) > 1:
        # Элементов может быть больше 2, вернуть только первые два
        return [rank for rank in itertools.islice(pair_ranks, 2)]

    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    return


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    return


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    assert (sorted(best_wild_hand("6C 7C ?R 9C TC 5C ?B".split()))
            == ['7C', '?R', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TC 7C 2C 2S ?R JC ?B".split()))
            == ['?C', '?S', '?H', '?B', 'TC'])
    print('OK')


def joker_free_hand(sorted_ranks: list[str]) -> list[str]:
    """
        Возвращает "руку" без джокеров
        >>> joker_free_hand(card_ranks("TC 7C 2C 2S ?R JC ?B".split()))
        ['J', 'T', '7', '2', '2']
        >>> joker_free_hand(card_ranks("TC 7C 2C 2S 2H JC 2B".split()))
        ['J', 'T', '7', '2', '2', '2', '2']
    """
    return list(itertools.dropwhile(lambda rank: rank == JOKER_RANK, sorted_ranks))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # test_best_hand()
    # test_best_wild_hand()
