def filter_dict(
    d: dict, 
    fnone: bool = True,
    fint: bool = True, 
    fstr: bool = True, 
    flen: bool = True,
) -> dict:

    out = d
    out = {**out}

    if fnone:
        out = {k: v for k, v in out.items() if v is not None}
    if fint:
        out = {k: v for k, v in out.items() if v != 0}
    if fstr:
        out = {k: v for k, v in out.items() if v != ""}
    if flen:
        out = {k: v for k, v in out.items() if hasattr(v, "__len__") and len(v) > 0}
    return out