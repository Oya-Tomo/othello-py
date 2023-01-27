import pprint
import pandas

def extract_from_csv(filename: str) -> list:
    file = pandas.read_csv(filename)
    return file["transcript"].to_list()

def extract_from_ggf(filename: str) -> list:
    with open(filename, "r", encoding="utf-8") as f:
        data_str = f.read().splitlines()

    transcripts = []
    count = 0
    for line in data_str:
        count += 1
        sep = line.find("---- *]B[")
        raw = line[sep:]
        transcript = ""
        while True:
            pos = raw.find("[")
            if pos == -1:
                break
            pos += 1
            raw = raw[pos:]
            move = raw[:2]
            if move == "pa" or move == "PA":
                pass
            else:
                transcript += move.lower()
        if len(transcript) < 10:
            continue
        transcripts.append(transcript)

    return transcripts

def extract(filename: str) -> list:
    if filename[-3:] == "csv":
        return extract_from_csv(filename)
    else:
        return extract_from_ggf(filename)

if __name__ == "__main__":
    # pprint.pprint(extract_from_csv("csv_files/wthor (0).csv"))
    pprint.pprint(extract_from_ggf("ggf_files/ggf (0).ggf"))