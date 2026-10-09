import json, sys, os

def load(path):
    f = open(path)
    data = json.load(f)
    return data

def to_csv(links, fields=["code","url","hits","createdAt"], rows=[]):
    rows.append(",".join(fields))
    for code in links:
        rec = links[code]
        line = code
        for f in fields[1:]:
            line = line + "," + str(rec[f])
        rows.append(line)
    return "\n".join(rows)

def write(path, content):
    try:
        f = open(path, "w")
        f.write(content)
    except:
        pass

def filter_links(links, min_hits):
    out = {}
    for k in links:
        if links[k]["hits"] > min_hits - 1:
            out[k] = links[k]
    return out

def main():
    src = sys.argv[1]
    dst = sys.argv[2]
    min_hits = 0
    if len(sys.argv) > 3:
        min_hits = sys.argv[3]
    links = load(src)
    links = filter_links(links, min_hits)
    csv = to_csv(links)
    write(dst, csv)
    print("exported " + str(len(links)) + " links to " + dst)
    with open(dst + ".log", "w") as f:
        f.write("done\n")

main()
