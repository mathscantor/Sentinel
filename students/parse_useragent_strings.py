import httpagentparser
import pandas as pd
import json

def main():

    df = pd.read_csv("datasets/splunk/http_user_agent_dataset.csv")
    http_user_agent_to_info_map = dict()

    for http_user_agent in df["http_user_agent"].values:
        json_result = httpagentparser.detect(agent=http_user_agent)
        http_user_agent_to_info_map.update({http_user_agent: json_result})

    pretty_print(mapping=http_user_agent_to_info_map)
    return 0

def pretty_print(mapping: dict):

    i = 1
    for key in mapping:
        print("{}. User Agent: {}".format(i, key))

        print("Operating System: {}".format(mapping[key]["platform"]["name"]), end="")
        if mapping[key]["platform"]["version"] is not None:
            print(" " + mapping[key]["platform"]["version"])
        else:
            print("")
        if "browser" in mapping[key]:
            print("Browser: {}".format(mapping[key]["browser"]["name"]), end="")
            if mapping[key]["browser"]["version"] is not None:
                print(" " + mapping[key]["browser"]["version"])
            else:
                print("")
        else:
            print("Browser: Unknown Browser")

        print("")
        i += 1
    return


if __name__ == "__main__":
    main()