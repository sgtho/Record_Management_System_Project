import json


class FlightRepository:
    """
    FlightRepository is responsible for managing flight records, which are stored in JSONL format.
    It provides methods to create, read, update, and delete (CRUD) records in a JSONL file.
    """

    def __init__(self, filename: str):
        """
        Initializes the repository with the specified file and loads the existing records.

        :param filename: The name of the JSONL file where flight records are stored.
        """
        self.filename = filename
        self.records = self.load_records()

    def load_records(self):
        """
        Loads flight records from the specified JSONL file.

        :return: A list of dictionaries, each representing a flight record.
        """
        records = []
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    records.append(json.loads(line.strip()))
        except FileNotFoundError:
            return []
        return records

    def save_records(self):
        """
        Saves all flight records back to the JSONL file.
        Each record is written as a separate line in JSON format.
        """
        with open(self.filename, "w") as file:
            for record in self.records:
                file.write(json.dumps(record) + "\n")  # Write each record as a new line

    def create(self, record: dict):
        """
        Adds a new flight record to the repository and saves it to the JSONL file.

        :param record: The flight booking number record to add (as a dictionary).
        """
        record["ID"] = len(self.records) + 1
        record["Type"] = "Flight"
        self.records.append(record)
        self.save_records()

    def list(self):
        """
        Lists all flight records.

        :return: A list of all flight records.
        """
        return self.records

    def get(self, id: int):
        """
        Retrieves a flight record by its Booking Number.

        :param id: The Booking Number of the flight to retrieve.
        :return: The flight record if found, otherwise None.
        """
        for record in self.records:
            if record["ID"] == id:
                return record
        return None

    def search_by_client_id(self, client_id: str):
        """
        Searches for flight records by Client ID.

        :param client_id: The partial or full Client ID to search for.
        :return: A list of flight records that match the provided Client ID.
        """
        if len(client_id) == 0:
            return self.records
        filtered = []
        for record in self.records:
            if str(record["Client_ID"]).startswith(client_id):
                filtered.append(record)
        return filtered

    def search_by_id(self, id: int):
        """
        Searches for flight records by partial or full Booking Number.

        :param id: The partial or full ID to search for.
        :return: A list of flight records that match the provided Booking Number.
        """
        if len(id) == 0:
            return self.records
        filtered = []
        for record in self.records:
            if str(record["ID"]).startswith(id):
                filtered.append(record)
        return filtered

    def update(self, updated_record: dict):
        """
        Updates an existing flight record.

        :param updated_record: The updated flight record (as a dictionary).
        """
        for idx, flight in enumerate(self.records):
            if flight["ID"] == updated_record["ID"]:
                self.records[idx] = updated_record
                break
        self.save_records()

    def delete(self, record: dict):
        """
        Deletes a flight record from the repository.

        :param record: The flight record to delete (as a dictionary).
        """
        for idx, flight in enumerate(self.records):
            if flight["ID"] == record["ID"]:
                del self.records[idx]
                break
        self.save_records()
