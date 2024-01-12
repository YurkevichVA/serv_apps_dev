import json

def main() -> None:
    try:
        with open("sample.json") as f:
            j = json.load(f)
    except:
        print("JSON load error")
        return
    
    print(type(j), j)

    for k in j:
        print(k, j[k], type(j[k]))

    j['newItem1'] = 'Hi, All'
    j['newItem2'] = 'Вітання'
    print(j)
    print(json.dumps(j, ensure_ascii=False, indent=4))

    key = "arr"
    if key in j:
        print(key, "exists")
    else:
        print(key, "does not exist")

    try:
        with open("sample2.json", "w", encoding="utf-8") as f:
            json.dump(j, f, ensure_ascii=False)
    except:
        print("Write fail")
    else:
        print("Write OK")


if __name__ == "__main__":
    main()