import unittest
import data_pipeline
import pytest


class DataPipelineTest(unittest.TestCase):
    def test_get_clean_date(self):
        scenarios_ok = [
            [{"date": "31/01/2023"}, "2023-01-31"],
            [{"date": "2023-01-31"}, "2023-01-31"],
            [{"date": "31 January 2023"}, "2023-01-31"]
        ]
        scenarios_ko = [
            {"date": "2023-31-01"},
            {"date": "20230131"},
            {"no_date": "2023-01-31"},
            {"date": None},
            {"date": ""}
        ]

        for senario in scenarios_ok:
            self.assertEqual(data_pipeline.get_clean_date(senario[0]), senario[1])

        for senario in scenarios_ko:
            with pytest.raises(ValueError):
                data_pipeline.get_clean_date(senario)

    def test_get_clean_str(self):
        scenarios_ok = [
            [{"title": " a title "}, "title", "a title"],
            [{"title": " a \\xc3\\xb1 title \\xc3\\xb9 "}, "title", "a ñ title ù"],
            [{"title": " a title "}, "title", "a title"],
            [{"title": " a\\xc3\\x28title\\xc3\\x35"}, "title", "atitle"],
            [{"title": "a title"}, "title", "a title"],
        ]
        scenarios_ko = [
            [{"title": None}, "title"],
            [{"title": " a title"}, "journal"],
            [{"title": " "}, "title"],
            [{"title": ""}, "title"],
        ]

        for senario in scenarios_ok:
            self.assertEqual(data_pipeline.get_clean_str(senario[0], senario[1]), senario[2])

        for senario in scenarios_ko:
            with pytest.raises(ValueError):
                data_pipeline.get_clean_str(senario[0], senario[1])

    def test_add_association(self):
        asso = []
        drugs = {
            "1": {
                "drug": "d1"
            },
            "2": {
                "drug": "d2"
            },
            "3": {
                "drug": "d3"
            },
            "4": {
                "drug": "d4"
            },
            "5": {
                "drug": "d5"
            }
        }

        data_pipeline.add_association(asso, drugs, "1", "a title who contains d1 and D5 and other")

        expected_asso1 = [
            {"atccode": "1", "pub_id": "1"},
            {"atccode": "5", "pub_id": "1"}
        ]

        self.assertEqual(asso, expected_asso1)

        data_pipeline.add_association(asso, drugs, "2", "a title without drugs")

        self.assertEqual(asso, expected_asso1)

        data_pipeline.add_association(asso, drugs, "3", "a title contains d3 and D5")

        expected_asso2 = [
            {"atccode": "1", "pub_id": "1"},
            {"atccode": "5", "pub_id": "1"},
            {"atccode": "3", "pub_id": "3"},
            {"atccode": "5", "pub_id": "3"}
        ]
        self.assertEqual(asso, expected_asso2)

    def test_content_transform(self):

        content = [
            {
                "id": "NCT01967433",
                "scientific_title": "Use of Diphenhydramine as an Adjunctive Sedative",
                "date": "1 January 2020",
                "journal": "Journal of emergency nursing"
            },
            {
                "id": "NCT01967433",
                "scientific_title": "Use of Diphenhydramine as an Adjunctive Sedative",
                "date": "1 January 2020",
                "journal": " "
            }
        ]

        expected_content_formatted = [
            {
                "id": "NCT01967433",
                "type": "clinical_trials",
                "title": "Use of Diphenhydramine as an Adjunctive Sedative",
                "date": "2020-01-01",
                "journal": "Journal of emergency nursing"
            }
        ]

        self.assertEqual(
            data_pipeline.content_transform(content, "clinical_trials", "scientific_title"),
            expected_content_formatted
        )


if __name__ == '__main__':
    unittest.main()
