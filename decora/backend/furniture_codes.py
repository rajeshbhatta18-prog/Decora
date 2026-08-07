CATEGORY_CODE_TO_NAME = {
    "bed": {"db": "double_bed", "sb": "single_bed", "kb": "kingsize_bed"},
    "table": {"lt": "large_table", "mt": "medium_table"},
    "chair": {"pc": "plastic_chair", "mc": "metal_chair", "ac": "adjustable_chair"},
    "wardrobe": {"fw": "fabric_wardrobe", "hw": "hanger_wardrobe", "ww": "wooden_wardrobe"},
    "bookshelf": {"wb": "wooden_bookshelf", "bb": "bamboo_bookshelf"},
    "bedsidetable": {"bt": "bedside_table"},
    "dresser": {"dr": "dresser"},
    "dustbin": {"di": "dustbin"},
    "mirror": {"mr": "mirror"},
}

NAME_TO_CATEGORY = {
    name: category
    for category, code_map in CATEGORY_CODE_TO_NAME.items()
    for name in code_map.values()
}
NAME_TO_CATEGORY.update({category: category for category in CATEGORY_CODE_TO_NAME})


def code_to_name(category: str, code: str):
    return CATEGORY_CODE_TO_NAME.get(category, {}).get(code)
