import unittest

from pipeline_drugs_pub.src.feature_journal import get_maps_journals_drugs, count_for_journal_most_drugs


class FeatureJournalTest(unittest.TestCase):
    def test_get_maps_journals_drugs(self):
        expected_maps = {"Journal 1": {"D1", "D3"}, "Journal 2": {"D1", "D4"}, "Journal 3": {"D1", "D2", "D3"}}

        self.assertEqual(get_maps_journals_drugs(get_sample_json()), expected_maps)

    def test_count_for_journal_most_drugs(self):
        maps_only_one = {"Journal 1": {"D1", "D3"}, "Journal 2": {"D1", "D4"}, "Journal 3": {"D1", "D2", "D3"}}
        maps_multi = {
            "Journal 1": {"D1", "D3"},
            "Journal 2": {"D1", "D4"},
            "Journal 3": {"D1", "D2", "D3"},
            "Journal 4": {"D4", "D2", "D3"}
        }

        expected_only_one = ["Journal 3"]
        expected_multi = ["Journal 3", "Journal 4"]
        self.assertEqual(count_for_journal_most_drugs(maps_only_one), expected_only_one)
        self.assertEqual(count_for_journal_most_drugs(maps_multi), expected_multi)


def get_sample_json():
    return {
        "context": {
            "drugs": {
                "D1": {
                    "drug": "DRUG1"
                },
                "D2": {
                    "drug": "DRUG2"
                },
                "D3": {
                    "drug": "DRUG3"
                },
                "D4": {
                    "drug": "DRUG4"
                }
            },
            "publications": {
                "1": {
                    "type": "pubmed",
                    "title": "Title with DRUG1, DRUG3",
                    "date": "2020-01-01",
                    "journal": "Journal 1",
                    "old_id": 9
                },
                "2": {
                    "type": "pubmed",
                    "title": "Title with DRUG1",
                    "date": "2020-01-01",
                    "journal": "Journal 1",
                    "old_id": 10
                },
                "3": {
                    "type": "pubmed",
                    "title": "Title with DRUG1, DRUG4",
                    "date": "2020-01-01",
                    "journal": "Journal 2",
                    "old_id": "11"
                },
                "4": {
                    "type": "pubmed",
                    "title": "Title with DRUG1, DRUG2",
                    "date": "2020-03-01",
                    "journal": "Journal 3",
                    "old_id": "12"
                },
                "5": {
                    "type": "pubmed",
                    "title": "Title with DRUG3",
                    "date": "2020-03-01",
                    "journal": "Journal 3",
                    "old_id": ""
                }
            }
        },
        "assossiation_dp": [
            {
                "atccode": "D1",
                "pub_id": "1"
            },
            {
                "atccode": "D3",
                "pub_id": "1"
            },
            {
                "atccode": "D1",
                "pub_id": "2"
            },
            {
                "atccode": "D1",
                "pub_id": "3"
            },
            {
                "atccode": "D4",
                "pub_id": "3"
            },
            {
                "atccode": "D1",
                "pub_id": "4"
            },
            {
                "atccode": "D2",
                "pub_id": "4"
            },
            {
                "atccode": "D3",
                "pub_id": "5"
            }
        ]
    }


if __name__ == '__main__':
    unittest.main()
