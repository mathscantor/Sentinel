import glob
import os
import subprocess
import json
import csv
from utils.messenger import messenger

class Converter:

    def __init__(self):
        self.csv_header_set = set()
        self.concatenated_keys = ""
        self.sentinel_repo_path = os.path.dirname(os.path.abspath(__file__))
        self.operating_system = self.check_operating_system()

    def check_operating_system(self) -> str:
        allowed_os = ["nt", "posix"]
        if os.name in allowed_os:
            return os.name
        else:
            messenger(2, "Unable to run evtxdump on '{}'".format(os.name))
            exit(1)

    def convert_evtx_to_json(self):
        evtx_list = glob.glob(pathname=os.path.join(self.sentinel_repo_path, "datasets/windows/evtx/*.evtx"))
        os.makedirs(os.path.dirname(os.path.join(self.sentinel_repo_path, "datasets/windows/json")), exist_ok=True)
        for evtx_path in evtx_list:
            print("Converting: {}".format(evtx_path))
            json_path = os.path.join(self.sentinel_repo_path,
                                     "datasets/windows/json/{}.json".format(os.path.basename(evtx_path).split(".evtx")[0]))
            if self.operating_system == "nt":
                subprocess.run([os.path.join(self.sentinel_repo_path, "binaries/windows/evtxdump_windows.exe"),
                                "--no-confirm-overwrite",
                                "--separate-json-attributes",
                                "--format", "jsonl",
                                "--output", json_path,
                                evtx_path])

            elif self.operating_system == "posix":
                subprocess.run([os.path.join(self.sentinel_repo_path, "binaries/linux/evtxdump_linux"),
                                "--no-confirm-overwrite",
                                "--separate-json-attributes",
                                "--format", "jsonl",
                                "--output", json_path,
                                evtx_path])
        return

    def convert_evtx_to_xml(self):
        evtx_list = glob.glob(pathname=os.path.join(self.sentinel_repo_path, "datasets/windows/evtx/*.evtx"))
        os.makedirs(os.path.dirname(os.path.join(self.sentinel_repo_path, "datasets/windows/xml")), exist_ok=True)
        for evtx_path in evtx_list:
            print("Converting: {}".format(evtx_path))
            xml_path = os.path.join(self.sentinel_repo_path,
                                    "datasets/windows/xml/{}.xml".format(os.path.basename(evtx_path).split(".evtx")[0]))
            if self.operating_system == "nt":
                subprocess.run([os.path.join(self.sentinel_repo_path, "binaries/windows/evtxdump_windows.exe"),
                                "--no-confirm-overwrite",
                                "--dont-show-record-number",
                                "--format", "xml",
                                "--output", xml_path,
                                evtx_path])

            elif self.operating_system == "posix":
                subprocess.run([os.path.join(self.sentinel_repo_path, "binaries/linux/evtxdump_linux"),
                                "--no-confirm-overwrite",
                                "--dont-show-record-number",
                                "--format", "xml",
                                "--output", xml_path,
                                evtx_path])
        return

    def update_csv_header_set(self, json_obj: dict):

        # Iterative way to get csv header. It is silly but it works.
        # Currently, works for json objects with at most 4 levels deep!
        # Future Task: Make it more elegant with recursion
        for key_1 in json_obj.keys():
            if not isinstance(json_obj[key_1], dict):
                self.csv_header_set.update({key_1})
                continue
            for key_2 in json_obj[key_1].keys():
                if not isinstance(json_obj[key_1][key_2], dict):
                    self.csv_header_set.update({key_1 + "." + key_2})
                    continue
                for key_3 in json_obj[key_1][key_2].keys():
                    if not isinstance(json_obj[key_1][key_2][key_3], dict):
                        self.csv_header_set.update({key_1 + "." + key_2 + "." + key_3})
                        continue
                    for key_4 in json_obj[key_1][key_2][key_3].keys():
                        if not isinstance(json_obj[key_1][key_2][key_3][key_4], dict):
                            self.csv_header_set.update({key_1 + "." + key_2 + "." + key_3 + "." + key_4})
                            continue

        return

    def convert_json_to_csv(self):
        null_value = None
        tmp_data_row = []
        json_list = glob.glob(pathname=os.path.join(self.sentinel_repo_path, "datasets/windows/json/*.json"))
        for json_path in json_list:
            print("Converting: {}".format(json_path))
            csv_path = os.path.join(self.sentinel_repo_path,
                                    "datasets/windows/csv/{}.csv".format(os.path.basename(json_path).split(".json")[0]))
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            f_csv = open(csv_path, "w", newline='', encoding="utf8")
            csv_writer = csv.writer(f_csv)

            f_json = open(json_path, "r")

            # Set the header by crawling through every field in every data row to ensure consistency
            for json_str in f_json:
                json_obj = json.loads(json_str)
                self.update_csv_header_set(json_obj=json_obj["Event"])
            csv_header = sorted(list(self.csv_header_set))
            # Move the Time attribute to the first column for clarity
            csv_header.insert(0, csv_header.pop(csv_header.index("System.TimeCreated_attributes.SystemTime")))

            # Crawl through the data based on our previously known fields
            f_json.seek(0)
            is_first_line = True
            for json_str in f_json:
                json_obj = json.loads(json_str)
                if is_first_line:
                    is_first_line = False
                    csv_writer.writerow(csv_header)
                    f_csv.flush()

                for field in csv_header:
                    field_tokens = field.split(".")
                    if len(field_tokens) == 1:
                        if field_tokens[0] not in json_obj["Event"].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        value = json_obj["Event"][field_tokens[0]]

                    elif len(field_tokens) == 2:
                        if field_tokens[0] not in json_obj["Event"].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        if field_tokens[1] not in json_obj["Event"][field_tokens[0]].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        value = json_obj["Event"][field_tokens[0]][field_tokens[1]]

                    elif len(field_tokens) == 3:
                        if field_tokens[0] not in json_obj["Event"].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        if field_tokens[1] not in json_obj["Event"][field_tokens[0]].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        if field_tokens[2] not in json_obj["Event"][field_tokens[0]][field_tokens[1]].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        value = json_obj["Event"][field_tokens[0]][field_tokens[1]][field_tokens[2]]

                    elif len(field_tokens) == 4:
                        if field_tokens[0] not in json_obj["Event"].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        if field_tokens[1] not in json_obj["Event"][field_tokens[0]].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        if field_tokens[2] not in json_obj["Event"][field_tokens[0]][field_tokens[1]].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        if field_tokens[3] not in json_obj["Event"][field_tokens[0]][field_tokens[1]][field_tokens[2]].keys():
                            value = null_value
                            tmp_data_row.append(value)
                            continue
                        value = json_obj["Event"][field_tokens[0]][field_tokens[1]][field_tokens[2]][field_tokens[3]]

                    tmp_data_row.append(value)

                csv_writer.writerow(tmp_data_row)
                f_csv.flush()
                tmp_data_row.clear()
            self.csv_header_set.clear()

        f_json.close()
        f_csv.close()
        return


if __name__ == "__main__":
    converter = Converter()
    messenger(3, "Converting EVTX to XML Format...")
    converter.convert_evtx_to_xml()
    messenger(0, "Successfully converted EVTX to XML Format!\n")

    messenger(3, "Converting EVTX to JSON Format...")
    converter.convert_evtx_to_json()
    messenger(0, "Successfully converted EVTX to JSON Format!\n")

    messenger(3, "Converting JSON to CSV Format...")
    converter.convert_json_to_csv()
    messenger(0, "Successfully converted JSON to CSV Format!\n")
