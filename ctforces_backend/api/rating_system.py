import math


class RatingSystem:
    @staticmethod
    def __get_probability(a, b):
        return 1.0 / (1.0 + math.pow(10.0, (b - a) / 5000.0))

    @staticmethod
    def __get_geometrical_mean(a, b):
        return math.sqrt(a * b)

    def __init__(self, ratings):
        self.ratings = ratings

    def __get_seed(self, rating):
        ret = 1

        for r in self.ratings:
            if r[0] != rating[0]:
                ret += self.__get_probability(r[1], rating[1])

        return ret

    def __get_satisfaction(self, s, p):
        left = 0
        right = 200000
        for iteration in range(100):
            mid = (left + right) / 2
            if self.__get_seed((p, mid)) < s:
                right = mid
            else:
                left = mid
        return left

    def calculate(self):
        if len(self.ratings) == 0:
            return []

        for i in range(len(self.ratings)):
            if self.ratings[i][0] != 1:
                break
        else:
            return [0 for _ in range(len(self.ratings))]

        delta = [0 for _ in range(len(self.ratings))]

        place = 1
        last_team_size = 0
        for i in range(len(self.ratings)):
            if i > 0 and self.ratings[i][0] != self.ratings[i - 1][0]:
                place += last_team_size
                last_team_size = 0
            last_team_size += 1

            s = self.__get_seed(self.ratings[i])
            m = self.__get_geometrical_mean(s, place)
            R = self.__get_satisfaction(m, self.ratings[i][0])

            delta[i] = (R - self.ratings[i][1]) / 2

        dec = sum(delta) / len(delta)

        for i in range(len(delta)):
            delta[i] -= dec

        not_top_cnt = 0

        for i in range(len(delta)):
            if self.ratings[i][0] == 1:
                delta[i] = max(delta[i], 1)
            else:
                not_top_cnt += 1

        dec = sum(delta) / not_top_cnt

        for i in range(len(delta)):
            if self.ratings[i][0] != 1:
                delta[i] -= dec

        for i in range(len(delta)):
            delta[i] = int(delta[i])

        return delta


if __name__ == "__main__":
    import random

    for test in range(100):
        print(f'Test {test}')
        data = []
        teams_cnt = random.randint(1, 50)
        for team in range(teams_cnt):
            members_cnt = random.randint(1, 10)
            for member in range(members_cnt):
                rating = random.randint(1, 10000)
                data.append((team + 1, rating))
        rs = RatingSystem(data)
        delta = rs.calculate()

        for i in range(len(data)):
            for j in range(len(data)):
                cur_state = f'{data[i]} {data[j]} {delta[i]} {delta[j]}'
                if data[i][0] > data[j][0] and data[i][1] < data[j][1]:
                    assert data[i][1] + delta[i] <= data[j][1] + delta[j], cur_state
                if data[i][0] < data[j][0] and data[i][1] < data[j][1]:
                    assert delta[i] >= delta[j], cur_state

        for i in range(len(data)):
            if data[i][0] == 1:
                cur_state = f'{data[i][0]} {delta[i]}'
                assert delta[i] >= 0, cur_state
