import math
def get_split(index, total, splits_config):
    # simple deterministic split
    train = splits_config.get("train", 85)
    val = splits_config.get("validation", 10)
    test = splits_config.get("test", 5)
    total_ratio = train + val + test
    
    ratio = index / total * total_ratio
    if ratio < train:
        return "train"
    elif ratio < train + val:
        return "validation"
    else:
        return "test"
