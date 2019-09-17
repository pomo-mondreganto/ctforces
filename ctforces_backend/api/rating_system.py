import math


class RatingSystem:

    @staticmethod
    def __get_probability(a, b):
        return 1.0 / (1.0 + math.pow(10.0, (b - a) / 3000.0))

    @staticmethod
    def __get_geometrical_mean(a, b):
        return math.sqrt(a * b)

    def __init__(self, ratings):
        self.ratings = ratings

    def __get_seed(self, rating):
        ret = 1

        for r in self.ratings:
            ret += self.__get_probability(r, rating)

        return ret - 0.5

    def __get_satisfaction(self, s):
        left = 0
        right = 50000
        for iteration in range(300):
            mid = (left + right) / 2
            if self.__get_seed(mid) < s:
                right = mid
            else:
                left = mid
        return left

    def calculate(self):
        if len(self.ratings) == 0:
            return []

        delta = [0 for _ in range(len(self.ratings))]

        for i in range(len(self.ratings)):
            m = self.__get_geometrical_mean(self.__get_seed(self.ratings[i]), i + 1)
            R = self.__get_satisfaction(m)

            delta[i] = (R - self.ratings[i]) / 2

        sum_deltas = sum(delta)

        inc = -sum_deltas / len(delta) - 1

        for i in range(len(delta)):
            delta[i] += inc

        top_group = int(max(min(float(len(delta)), 4 * math.sqrt(len(delta))), 1))

        sum_top_deltas = sum(delta[:top_group])

        inc = min(max(-sum_top_deltas / top_group, -80), 0)

        for i in range(len(delta)):
            delta[i] += inc

        delta = [int(i - 1) for i in delta]

        return delta
