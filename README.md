# AgilisSzoftverFejlesztes
[![Build Status](https://travis-ci.org/CsToMy/AgilisSzoftverFejlesztes.svg?branch=master)](https://travis-ci.org/CsToMy/AgilisSzoftverFejlesztes)

This is the repo for source files, documentation and research materials
for accomplishing the Agile Network Service Development (Agilis
szoftverfejlesztés) subject.

## Example JSON used for testing:

```json
{
    "a": "kismacska",
    "b": "almafa",
    "THIS_IS_A_DICTIONARY": {
        "dictelem1": 23,
        "dictelem2": true
    },
    "A_LIST": ["alma", "retek", "cseresznye"],
    "B_LIST": [23.5, false, {"x": true, "y":false, "f": 3.1415}],
    "szam": 6
}
```

## Unittest
* Run `python3 -m unittest discover`command in the root directory.
* This will run all tests in `test` folder, which match the `test*.py` pattern.

## Flake8
* Run `flake8 .` command in root directory.
* This will recursively check all files in current directory.
