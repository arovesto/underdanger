def probability_range(items_dict):
    assert sum(p for p in items_dict) <= 1, 'probability > 100%'
    lower_bound = 0
    proba = {}
    for p in items_dict:
        proba[(lower_bound, lower_bound + p)] = items_dict[p]
        lower_bound += p
    return proba


def get_item(probability, prob_range):
    try:
        return next(i for prob, i in prob_range.items() if probability > prob[0] and probability <= prob[1])
    except StopIteration:
        return None
