import unittest
import json
import os
from src.data.airline_repository import AirlineRepository


class TestAirlineRepository(unittest.TestCase):

    def setUp(self):
        """
        This method is called before each test. It sets up a temporary file and initial records for testing.
        """
        self.filename = "test_airlines.jsonl"

        # records have other fields as well but we only set ID and Name as this is all we need for the tests
        self.initial_records = [
            {"ID": 1, "Type": "Airline", "Company_Name": "Global Airline"},
            {"ID": 2, "Type": "Airline", "Company_Name": "WingAir"},
        ]
        with open(self.filename, "w") as file:
            for record in self.initial_records:
                file.write(json.dumps(record) + "\n")
        self.repo = AirlineRepository(self.filename)

    def tearDown(self):
        """
        This method is called after each test. It cleans up by removing the temporary test file.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_load_records(self):
        """
        Test that records are loaded correctly from the file.
        """
        records = self.repo.load_records()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["Company_Name"], "Global Airline")
        self.assertEqual(records[1]["Company_Name"], "WingAir")

    def test_create_record(self):
        """
        Test that a new record is added successfully.
        """
        new_record = {"Type": "Airline", "Company_Name": "Space Air"}
        self.repo.create(new_record)

        records = self.repo.list()
        self.assertEqual(len(records), 3)
        self.assertIn(new_record, records)

    def test_list_records(self):
        """
        Test that all records are listed correctly.
        """
        records = self.repo.list()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["Company_Name"], "Global Airline")
        self.assertEqual(records[1]["Company_Name"], "WingAir")

    def test_get_record_by_id(self):
        """
        Test that a record can be retrieved by its ID.
        """
        record = self.repo.get(1)
        self.assertIsNotNone(record)
        self.assertEqual(record["Company_Name"], "Global Airline")

        record = self.repo.get(999)  # Non-existing ID
        self.assertIsNone(record)

    def test_search_by_name(self):
        """
        Test that records can be searched by name.
        """
        result = self.repo.search_by_name("Glo")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Company_Name"], "Global Airline")

        result = self.repo.search_by_name("Nonexistent")
        self.assertEqual(len(result), 0)

    def test_search_by_id(self):
        """
        Test that records can be searched by ID.
        """
        result = self.repo.search_by_id("1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["ID"], 1)

        result = self.repo.search_by_id("999")  # Non-existing ID
        self.assertEqual(len(result), 0)

    def test_update_record(self):
        """
        Test that an existing record is updated correctly.
        """
        updated_record = {"ID": 1, "Type": "Airline", "Company_Name": "Worldwide Airline"}
        self.repo.update(updated_record)

        record = self.repo.get(1)
        self.assertEqual(record["Company_Name"], "Worldwide Airline")

    def test_delete_record(self):
        """
        Test that a record is deleted successfully.
        """
        record_to_delete = {"ID": 1, "Type": "Airline", "Company_Name": "Global Airline"}
        self.repo.delete(record_to_delete)

        records = self.repo.list()
        self.assertEqual(len(records), 1)
        self.assertNotIn(record_to_delete, records)


if __name__ == "__main__":
    unittest.main()
