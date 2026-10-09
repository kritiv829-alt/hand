import json
import sys
import datetime

DATA = "data/links.json"
MAX_AGE_DAYS = 30

def read():
    try:
        return json.load(open(DATA))
    except:
        return {}

def save(links):
    json.dump(links, open(DATA, "w"))

def age_days(created):
    d = datetime.datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ")
    return (datetime.datetime.now() - d).days

def is_stale(rec):
    if rec["hits"] == 0 and age_days(rec["createdAt"]) > MAX_AGE_DAYS:
        return True
    elif rec["hits"] == 0:
        return False
    else:
        return False

def cleanup(links, dry_run):
    removed = 0
    for code in links:
        if is_stale(links[code]):
            print("removing " + code)
            if dry_run == False:
                del links[code]
            removed += 1
    return removed

def main():
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        dry_run = False
    links = read()
    n = cleanup(links, dry_run)
    if dry_run == False:
        save(links)
    print(str(n) + " stale links " + ("would be " if dry_run else "") + "removed")

if __name__ == "__main__":
    main()
