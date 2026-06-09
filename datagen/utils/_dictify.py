def dictify(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if hasattr(v, "to_dict") and callable(getattr(v, "to_dict")):
            out[k] = v.to_dict()
        else:
            out[k] = v
    return out