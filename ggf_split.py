FILENAME = "Othello.latest.ggf"
LINE_COUNT = 10000

with open(FILENAME, "r", encoding="utf-8") as f:
    line_count = 0
    file_count = 0
    lines = ""
    for line in f.readlines():
        lines += line.replace(")(", ")\n(")
        line_count += 1

        if line_count == LINE_COUNT:
            with open(f"ggf_files/ggf ({file_count}).ggf", "w",encoding="utf-8") as wf:
                wf.write(lines)
            file_count += 1
            line_count = 0
            lines = ""

