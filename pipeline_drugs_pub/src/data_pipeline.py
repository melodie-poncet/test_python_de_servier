import csv
import json
import logging
import re
from datetime import datetime
from typing import Dict, List

from pipeline_drugs_pub.src import feature_journal

LOGGER = logging.getLogger(__name__)


def csv_to_json(path_file_csv: str, path_file_json: str):
    """Transform the csv file on json file."""
    content_file = []
    with open(path_file_csv, 'r', encoding='utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)

        for rows in csv_reader:
            content_file.append(rows)

    with open(path_file_json, 'w', encoding='utf-8') as json_file_handler:
        json_file_handler.write(json.dumps(content_file, ensure_ascii=False, indent=2))


def clean_file_publication(path_file_json: str):
    """Clean publications on JSON file."""
    try:
        with open(path_file_json, "r", encoding='utf-8') as json_file_handler:
            content_file = json.load(json_file_handler)

        if "pubmed" in path_file_json:
            content_formatted = content_transform(content_file, "pubmed", "title")
        else:
            content_formatted = content_transform(content_file, "clinical_trials", "scientific_title")

        with open(path_file_json, "w", encoding='utf-8') as json_file_handler:
            json_file_handler.write(json.dumps(content_formatted, ensure_ascii=False, indent=2))
    except json.decoder.JSONDecodeError as err:
        LOGGER.warning(f"JSONDecodeError : {err} \n "
                       f"file ignored : {path_file_json}")


def content_transform(content_file: List[Dict], type_content: str, title_field: str) -> List[Dict]:
    """
    Clean publications.
    :param content_file: list of publications
    :param type_content: type of publication pubmed or clinical trials
    :param title_field: title field depending on type of publication
    :return: cleaning publications
    """
    content_formatted = []
    for item in content_file:
        try:
            item_formatted = {
                "id": item.get("id", ""),
                "type": type_content,
                "title": get_clean_str(item, title_field),
                "date": get_clean_date(item),
                "journal": get_clean_str(item, "journal")
            }
            content_formatted.append(item_formatted)
        except ValueError as err:
            ignored_row = {
                "id": item.get("id", ""),
                "type": type_content,
                "title": item.get(title_field),
                "date": item.get("date"),
                "journal": item.get("journal")
            }
            LOGGER.warning(f"ValueError : {err} \n "
                           f"ignored row : {ignored_row}")

    return content_formatted


def get_clean_str(item: Dict, field: str) -> str:
    """
    Clean a string field
    :param item: a publication
    :param field: the field to treat
    :return: the cleaning field
    """
    if item.get(field) is None or len(item.get(field).strip()) == 0:
        raise ValueError(field + " is not valid")

    str_striped = item[field].strip()

    try:
        # In case of character in latin-1
        if '\\xc3' in str_striped:
            try:
                # force to traduct char to utf-8
                return bytes(str_striped, 'utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
            except ValueError:
                # if the character not really exist, it is deleted
                return re.sub("\\\\xc3\\\\x.{2}", "", str_striped)

        return str_striped
    except ValueError:
        raise ValueError(field + " is not valid")


def get_clean_date(item: Dict) -> str:
    """
    Clean the date of publication
    :param item: a publication
    :return: the cleaning date in string
    """
    date_str = item.get("date")
    if date_str is None:
        raise ValueError("Invalid date")

    try:
        if '/' in date_str:
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        elif '-' in date_str:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        elif ' ' in date_str:
            return datetime.strptime(date_str, "%d %B %Y").strftime("%Y-%m-%d")
        else:
            raise ValueError
    except ValueError:
        raise ValueError("Unrecognized date format")


def add_association(asso: List, drugs: Dict, pub_id: int, title: str):
    """
    Add all associations find between drugs_list and title
    :param asso: the list of associations
    :param drugs_list: map of all drugs
    :param pub_id: the current publication generated id
    :param title: the title of publication
    """
    for code in drugs.keys():
        if drugs[code]["drug"].lower() in title.lower():
            asso.append({"atccode": code, "pub_id": pub_id})


def construct_final_json(drugs_file: str, list_publi_files: List[str]):
    """
    Construct the final JSON result.
    :param drugs_file: the path of drugs file
    :param list_publi_files: list of all files of publications
    """
    context = {}
    asso = []
    with open(drugs_file, encoding='utf-8') as drugs_file_handler:
        drugs = json.load(drugs_file_handler)

    context["drugs"] = {}
    for drug in drugs:
        context["drugs"][drug["atccode"]] = {"drug": drug["drug"]}

    generated_id = 1
    context["publications"] = {}
    for file in list_publi_files:
        with open(file, encoding='utf-8') as publi_file_handler:
            publis = json.load(publi_file_handler)
            for pub in publis:
                publi = {
                    "type": pub["type"],
                    "title": pub["title"],
                    "date": pub["date"],
                    "journal": pub["journal"],
                    "old_id": pub.get("id", "")
                }
                context["publications"][generated_id] = publi
                add_association(asso, context["drugs"], str(generated_id), pub["title"])
                generated_id += 1

    with open("../data/res/result.json", "w", encoding='utf-8') as json_file_handler:
        json_file_handler.write(json.dumps({"context": context, "assossiation_dp": asso}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    csv_to_json("../data/csv/drugs.csv", "../data/json/drugs.json")
    csv_to_json("../data/csv/clinical_trials.csv", "../data/json/clinical_trials.json")
    csv_to_json("../data/csv/pubmed.csv", "../data/json/pubmed2.json")
    clean_file_publication("../data/json/clinical_trials.json")
    clean_file_publication("../data/json/pubmed.json")
    clean_file_publication("../data/json/pubmed_malformed.json")
    clean_file_publication("../data/json/pubmed2.json")

    construct_final_json(
        "../data/json/drugs.json",
        ["../data/json/pubmed.json", "../data/json/pubmed2.json", "../data/json/clinical_trials.json"]
    )

    list_journals = feature_journal.get_journal_with_most_drugs("../data/res/result.json")
    LOGGER.warning("The journal(s) that mentions the most different drugs are : \n" + "\n".join(list_journals))
