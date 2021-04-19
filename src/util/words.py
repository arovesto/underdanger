
genitive_end_mapping = {
    "а": "у",
    "я": "ю",
    "й": "я",
}


def name_to_genitive(name: str):
    for m, e in sorted(genitive_end_mapping.items(), key=lambda x: len(x[0])):
        if name.endswith(m):
            return name.replace(m, e)
    return name + "а" # TODO иногда здесь я, иногда здесь нужно убирать мягкий знак