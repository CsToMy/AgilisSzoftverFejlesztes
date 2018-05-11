#!/usr/bin/env python3.6

from copy import deepcopy
import json
import random


def get_keys(data):
    """Generate list of keys to all (nested) attributes of data.

    Example: get_keys({'a': 1, 'b': [1, 2]})
    -> [('a',), ('b',), ('b', 0), ('b', 1)]
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


def possible_mutations(value):
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

    if not isinstance(value, str):
        results.append(str(value))

    # if value is a number type, or an str with a number value
    try:
        try:
            value = int(value)
        except (ValueError, TypeError):
            value = float(value)
        vals = [-value, value + 1, value - 1]
        results += vals
        results += map(str, vals)
    except (ValueError, TypeError):
        pass

    return results


def resolve_keypath(value, key_path):
    """Get contained object by using keys.

    Example: resolve_keypath({'a': [[[['x']]]]}, ['a', 0, 0, 0, 0]) -> 'x'
    """
    for k in key_path:
        value = value[k]
    return value


def apply_mutations(original_json, mutations):
    """Apply specified mutations to object.

    Args:
        original_json: Object to be modified.
        mutations: Keypath+mutation pairs.
    """
    copy = deepcopy(original_json)

    for key_path, mut in mutations:
        # retrieve the direct container of the mutated attribute
        value = copy
        try:
            value = resolve_keypath(value, key_path[:-1])
        except (KeyError, IndexError):
            # container has been replaced or deleted
            continue

        if not isinstance(value, (dict, list)):
            # container has been modified to a non-composite value
            continue

        last_key = key_path[-1]
        if mut is DELETE:
            try:
                del value[last_key]
            except (KeyError, IndexError):
                pass
        else:
            try:
                value[last_key] = mut
            except IndexError:
                value.append(mut)
    return copy


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

        key_path = self.keys[self.key_idx]

        # generate mutation list when we start mutating a different attribute
        if self.mutation_idx == 0:
            value = resolve_keypath(self.input, key_path)

            self.mutations = possible_mutations(value)

        # select next mutation for the current attribute
        mut = self.mutations[self.mutation_idx]

        result = apply_mutations(self.input, [(key_path, mut)])

        # select next mutation (used on the next call to fuzz)
        self.mutation_idx += 1
        # select next attribute when all mutations are exhausted for the current
        # attribute
        if self.mutation_idx >= len(self.mutations):
            self.key_idx += 1
            self.mutation_idx = 0

        return json.dumps(result)

    def fuzz_random(self, mut_num=2):
        attributes = random.sample(self.keys, mut_num)
        mutations = []
        for key_path in attributes:
            value = resolve_keypath(self.input, key_path)
            mutation = random.choice(possible_mutations(value))
            mutations.append((key_path, mutation))

        return apply_mutations(self.input, mutations)
