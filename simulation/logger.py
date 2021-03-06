import csv
from typing import List


class Logger:
    def __init__(self, log_addr: str, header: List[str], reset_log_file: bool = True):
        self.log_addr = log_addr
        self.header = header
        self._init_log_file(reset_log_file)

    def _init_log_file(self, reset: bool = True):
        with open(self.log_addr, ("w" if reset else "a"), newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",")
            spamwriter.writerow(self.header)

    def write_to_log_file(self, vals: List[str]):
        if len(vals) != len(self.header):
            print("Number of log values differente of header size. Passing.")
            return False
        with open(self.log_addr, "a", newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",")
            spamwriter.writerow(vals)

if __name__ == "__main__":
    pass
