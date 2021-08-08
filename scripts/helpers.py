import requests
import os
import io
import pandas as pd

# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class Colors:
    GREEN   = "\033[92m"
    YELLOW = "\033[93m"
    CYAN    = "\033[96m"
    END     = "\033[0m"


class GetData(Colors):
    def __init__(self, directory, url, file_name):
        if file_name is None:
            file_name = url.split("/")[-1].split(".")[0]

        self.directory = directory
        self.url = url
        self.file_name = file_name
        self.data = None
        self.old_data = None

    def pprint(self, color, text):
        print(color + text + self.END)

    def make_dir(self):
        os.makedirs(self.directory, exist_ok=True)

    def import_data(self):
        print(self.GREEN, f"Downloading data for: {self.file_name}")
        data = requests.get(self.url)
        data.raise_for_status()
        data = pd.read_csv(io.StringIO(data.content.decode("utf-8")), index_col=0)
        data = data.fillna(0)
        self.data = data

    def __str__(self):
        return str(self.data.head())

    def set_old_data(self):
        old_filepath = f"{self.directory}/{self.file_name}.csv"
        if os.path.isfile(old_filepath) is True:
            self.old_data = pd.read_csv(old_filepath)

    def save_data(self):
        self.set_old_data()
        if self.old_data is None:
            self.save_to_file()
            return
        if len(self.data) > len(self.old_data) or len(self.data.columns) > len(self.old_data.columns):
            self.save_to_file()
            return
        self.pprint(self.CYAN, f"{self.file_name} has not yet updated. Skipping")

    def save_to_file(self):
        self.pprint(self.GREEN, f"Writing {self.file_name} to file")
        self.data.to_csv(f"{self.directory}/{self.file_name}.csv", na_rep="0")

    def download_data(self):
        self.pprint(self.YELLOW, "===================================================")
        self.make_dir()
        self.import_data()
        self.save_data()
        self.pprint(self.YELLOW, "===================================================")

def download_data(directory, url, file_name=None):
    data = GetData(directory, url, file_name)
    data.download_data()

def get_directory_path(directory):
    directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", directory))
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

if __name__ == "__main__":
    csv_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "csv"))
    url = input("Input download URL: ")
    data = GetData(csv_dir, url)
    data.download_data()