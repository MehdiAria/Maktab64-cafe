def alias_to_model(res, reverse_alias: dict):
    for i in reverse_alias.keys():
        if i in res.keys():
            value = res[i]
            res.pop(i)
            res[reverse_alias[i]] = value
    return res
