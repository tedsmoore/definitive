import numpy as np
from random import shuffle
from collections import OrderedDict


class PageRank(object):

    def __init__(self, items, participant_matchup_results):
        self.items = items
        self.participant_matchup_results = participant_matchup_results
        self._scores = None
        self._ranks = None
        self._pagerank = None
        self._wins_matrix = None
        self._loss_matrix = None

    @property
    def wins_matrix(self):
        if self._wins_matrix is not None:
            return self._wins_matrix

        opponent_list = [0 for _ in range(len(self.items))]
        wins_matrix_list = [opponent_list.copy() for _ in range(len(self.items))]

        for matchup_results in self.participant_matchup_results:
            winner = matchup_results[0]
            loser = matchup_results[1] if winner == matchup_results[2] else matchup_results[2]
            winner_index = self.items.index(winner)
            loser_index = self.items.index(loser)
            wins_matrix_list[winner_index][loser_index] += 1

        wins_matrix = np.array(wins_matrix_list)

        self._wins_matrix = wins_matrix
        return wins_matrix

    @property
    def loss_matrix(self):
        if self._loss_matrix is not None:
            return self._loss_matrix

        loss_matrix = np.transpose(self.wins_matrix)

        self._loss_matrix = loss_matrix
        return loss_matrix

    @property
    def pagerank(self, eps=1.0e-8, d=0.85):
        if self._pagerank is not None:
            return self._pagerank

        w = self.wins_matrix + 1.0e-10
        m = w / w.sum(axis=0, keepdims=1)
        n = m.shape[1]
        v = np.random.rand(n, 1)
        v = v / np.linalg.norm(v, 1)
        last_v = np.ones((n, 1), dtype=np.float32) * 1.e10
        m_hat = (d * m) + (((1 - d) / n) * np.ones((n, n), dtype=np.float32))

        while np.linalg.norm(v - last_v, 2) > eps:
            last_v = v
            v = np.matmul(m_hat, v)

        pagerank_list = [item for sublist in v for item in sublist]

        self._pagerank = pagerank_list
        return pagerank_list

    @property
    def scores(self):
        if self._scores is not None:
            return self._scores

        pagerank = self.pagerank

        average = sum(pagerank) / len(pagerank)
        scores = []
        for score in self.pagerank:
            index = 100 * score / average
            scores.append(index)

        self._scores = scores
        return scores

    def summary_data(self):
        summary_data = []

        for item in self.items:
            item_index = self.items.index(item)
            item_data = OrderedDict()
            item_data.update({
                'rank': 0,
                'score': self.scores[item_index],
                'item': item,
                'wins': sum(self.wins_matrix[item_index]),
                'losses': sum(self.loss_matrix[item_index])
            })
            summary_data.append(item_data)

        sorted_summary_data = sorted(summary_data, key=lambda k: k['score'], reverse=True)

        rank = 0
        for data in sorted_summary_data:
            rank += 1
            data['rank'] = rank

        return sorted_summary_data

    def all_output(self):
        all_data = []

        for item in self.items:
            item_index = self.items.index(item)
            item_data = OrderedDict()
            item_data.update({
                'raw_score': self.pagerank[item_index],
                'score': self.scores[item_index],
                'item': item,
                'wins': sum(self.wins_matrix[item_index]),
                'losses': sum(self.loss_matrix[item_index])
            })
            all_data.append(item_data)

        sorted_all_data = sorted(all_data, key=lambda k: k['score'], reverse=True)

        return sorted_all_data

    def wins_table(self):
        wins_table = []
        for item in self.items:
            item_index = self.items.index(item)
            item_data = OrderedDict({'item': item})

            for opp in self.items:
                item_data[opp] = self.wins_matrix[item_index, self.items.index(opp)]

            wins_table.append(item_data)

        return wins_table

    def win_loss_table(self):
        win_loss_table = []

        for item in self.items:
            item_index = self.items.index(item)
            item_data = OrderedDict({'item': item})

            for opp in self.items:
                wins = str(self.wins_matrix[item_index, self.items.index(opp)])
                losses = str(self.loss_matrix[item_index, self.items.index(opp)])
                item_data[opp] = "+" + wins + " | -" + losses

            win_loss_table.append(item_data)

        return win_loss_table


def create_matchup_data():
    # A helper fcn to create some fake user data

    items = [2, 3, 4, 5, 6, 7, 8, 9]

    matchup_results = []
    a = {2: 0, 3: 23, 4: 27, 5: 19, 6: 21, 7: 11, 8: 17, 9: 13}
    b = {2: 16, 3: 0, 4: 11, 5: 6, 6: 15, 7: 25, 8: 11, 9: 12}
    c = {2: 16, 3: 14, 4: 0, 5: 11, 6: 10, 7: 13, 8: 17, 9: 13}
    d = {2: 15, 3: 22, 4: 32, 5: 0, 6: 21, 7: 22, 8: 25, 9: 22}
    e = {2: 28, 3: 19, 4: 18, 5: 30, 6: 0, 7: 22, 8: 25, 9: 29}
    f = {2: 20, 3: 18, 4: 13, 5: 8, 6: 23, 7: 0, 8: 16, 9: 15}
    g = {2: 27, 3: 26, 4: 26, 5: 29, 6: 25, 7: 20, 8: 0, 9: 28}
    h = {2: 13, 3: 21, 4: 18, 5: 14, 6: 11, 7: 25, 8: 19, 9: 0}
    all_dicts = [a, b, c, d, e, f, g, h]

    for wins_dict in all_dicts:
        dict_name_index = all_dicts.index(wins_dict)
        dict_name = items[dict_name_index]
        for opponent in wins_dict:
            repeats = wins_dict[opponent]
            repetition = 0
            while repetition < repeats:
                matchup = [dict_name, opponent, dict_name]
                matchup_results.append(matchup)
                repetition += 1

    shuffle(matchup_results)
    participant_matchup_results = []
    start_index = 0
    end_index = 10

    while end_index < len(matchup_results):
        sublist = matchup_results[start_index:end_index + 1]
        participant_matchup_results.append(sublist)
        start_index += 11
        end_index += 11

    return items, participant_matchup_results


if __name__ == "__main__":
    example_items, participant_results = create_matchup_data()
    pass
