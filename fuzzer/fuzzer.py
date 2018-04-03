#!/usr/bin/env python3.6

import json
from copy import deepcopy


def get_keys(data):
    """Generate list of keys to all (nested) attributes of data.

    Example: data({'a': 1, 'b': [1, 2]})
    -> [('a',), ('b',), ('b',0), ('b',1)]
    """
    keys = []

    if isinstance(data, dict):
        for k in data:
            keys.append((k,))
            subkeys = get_keys(data[k])
            for sk in subkeys:
                keys.append((k,) + sk)

    elif isinstance(data, list):
        for i, val in enumerate(data):
            keys.append((i,))
            subkeys = get_keys(val)
            for sk in subkeys:
                keys.append((i,) + sk)

    return keys


#: Unique object for deletion in mutation list
DELETE = []


def mutations(value):
    """Generate list of possible mutations for value."""

    results = [DELETE]

    results += [0, 1, -1, 319723912739871239872193871289 ** 40, None, '', '#',
                'asd', -0.0, 0.0, True, False, [], [1], {}, {'a': 1}]

    if isinstance(value, str):
        results += [value * 2, value * 100, 'asd' * 800, '@', '&', '\n', '{}',
                    '\u20bf']
        if '2018' in value:
            results.append(value.replace('2018', '1018'))
            results.append(value.replace('2018', '3018'))
    if isinstance(value, (int, float)):
        # TODO: int coded as string: '5' -> '-5', '4', '6'
        results += [-value, value + 1, value - 1]
    return results


class Fuzzer():
    def __init__(self, input_json):
        self.input = json.loads(input_json)
        self.keys = get_keys(self.input)

        self.key_idx = 0
        self.mutation_idx = 0
        self.mutations = None

    def fuzz(self):
        if self.key_idx >= len(self.keys):
            raise StopIteration

        key = self.keys[self.key_idx]

        copy = deepcopy(self.input)

        # generate mutation list when we start mutating a different attribute
        if self.mutation_idx == 0:
            value = copy
            for k in key:
                value = value[k]

            self.mutations = mutations(value)

        # select next mutation for the current attribute
        mut = self.mutations[self.mutation_idx]

        # retrieve the direct container of the mutated attribute
        value = copy
        for k in key[:-1]:
            value = value[k]

        # perform mutation
        if mut is DELETE:
            del value[key[-1]]
        else:
            value[key[-1]] = mut

        # select next mutation (used on the next call to fuzz)
        self.mutation_idx += 1
        # select next attribute when all mutations are exhausted for the current
        # attribute
        if self.mutation_idx >= len(self.mutations):
            self.key_idx += 1
            self.mutation_idx = 0

        return json.dumps(copy)
