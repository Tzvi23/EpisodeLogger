def flatten_json(y):
    # From https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def flat_dict(x):
    """
    :param x: dict type variable with 3 nested levels
    :return: list of dictionaries
    """
    out = list()
    for s_number in x.keys():
        for e_number in x[s_number]:
            out.append({'season': int(s_number), 'episode': int(e_number), 'name': x[s_number][e_number]['name'], 'air_date': x[s_number][e_number]['air_date'], 'watched': x[s_number][e_number]['watched']})
    return out