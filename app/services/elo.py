def calculate_elo(rating, opponent_rating, result, k=32):
    expected = 1 / (1 + 10 ** ((opponent_rating - rating) / 400))
    return int(rating + k * (result - expected))