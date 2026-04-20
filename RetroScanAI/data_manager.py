import pandas as pd
import os

class DataManager:
    """Manages saving and loading of processed RetroScan AI data."""

    def __init__(self, filename="retroscan_data.csv"):
        print("DataManager initialized.")
        self.filename = filename
        self.data = pd.DataFrame()
        if os.path.exists(self.filename):
            self.data = pd.read_csv(self.filename)

    def save_records(self, records):
        """Appends new records to the DataFrame and saves to CSV.

        Args:
            records (list): A list of dictionaries, each representing a processed record.
        """
        if records:
            new_data = pd.DataFrame(records)
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.data.to_csv(self.filename, index=False)
            print(f"Saved {len(records)} records to {self.filename}")

    def load_data(self):
        """Loads all data from the CSV file.

        Returns:
            pd.DataFrame: A DataFrame containing all processed data.
        """
        if os.path.exists(self.filename):
            self.data = pd.read_csv(self.filename)
        return self.data
