
def check_list(first, fname, second, sname):
    for id, item in enumerate(first):
        if isinstance(item, dict):
            check_dict(item, fname, second[id], sname)
        elif type(item) == type(second[id]):
            if isinstance(item, (int, str, bool) or item is None):
                if item != second[id]:
                    print(f"conflict:{fname}-{item}:{sname}-{second[id]}")


def check_dict(first, fname, second, sname):
    for key, value in first.items():
        if key in second.keys():
            if type(value) == type(second[key]):
                if isinstance(value, (int, str, bool) or value is None):
                    if value != second[key]:
                        print(
                            f"conflict:{key}:{fname}-{value}:{sname}-{second[key]}")
                elif isinstance(value, list):
                    check_list(value, f"{fname}.{key}",
                               second[key], f"{sname}.{key}")
                elif isinstance(value, dict):
                    check_dict(value, f"{fname}.{key}",
                               second[key], f"{sname}.{key}")

            else:
                print(
                    f"conflict:type:{key}:{fname}-{type(value)}:{sname}-{type(second[key])}")
        else:
            print(f"missing:key:{key}:{sname}")
