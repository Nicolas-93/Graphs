from collections import defaultdict

def invert_dict(dico: dict) -> dict:
    res = defaultdict(list)

    for k, v in dico.items():
        res[v].append(k)

    return dict(res)
