import json
from typing import Dict, List


def get_journal_with_most_drugs(json_file_path: str) -> List:
    """
    Get from json file the journal(s) that mentions the most different drugs.
    :param json_file_path: the path of the json file to treat
    :return: list of journal(s) name(s)
    """

    with open(json_file_path, encoding='utf-8') as file_handler:
        content = json.load(file_handler)

    journals_drugs = get_maps_journals_drugs(content)

    return count_for_journal_most_drugs(journals_drugs)


def get_maps_journals_drugs(content: Dict) -> Dict:
    """
    Get a maps with the drugs mentions for each journal.
    :param content: the content from json file
    :return: a maps with key : journal name and value : set of drugs
    """

    journals_drugs = {}

    for asso in content["assossiation_dp"]:
        publi = content["context"]["publications"][asso["pub_id"]]

        if journals_drugs.get(publi["journal"]) is None:
            journals_drugs[publi["journal"]] = {asso["atccode"]}
        else:
            journals_drugs[publi["journal"]].add(asso["atccode"])

    return journals_drugs


def count_for_journal_most_drugs(journals_drugs: Dict) -> List:
    """
    From the 'maps' count and return the journal(s) with most drugs mentions
    :param journals_drugs: a maps with key : journal name and value : set of drugs
    :return: list of journal(s) name(s)
    """

    res = []
    for key in journals_drugs:
        journals_drugs[key] = len(journals_drugs[key])

    max_drugs = (max(journals_drugs.values()))
    for key, value in journals_drugs.items():
        if value == max_drugs:
            res.append(key)

    return res
