from pathlib import Path


def listify(o):
    """
    Convert to list
    """
    if o is None:
        return []
    if isinstance(o, list):
        return o
    if isinstance(o, str):
        return [o]
    return [o]


def compose(x, funcs, *args, order_key="_order", **kwargs):
    """
    Chain functions
    """
    key = lambda o: getattr(o, order_key, 0)
    for f in sorted(listify(funcs), key=key):
        x = f(x, **kwargs)
    return x


def remove_only_if_there(fpath):
    if Path.exists(fpath):
        Path.unlink(fpath)


def clean_up_fully(fpath):
    for i in [x for x in fpath.iterdir()]:
        if "tmp_" in i.name:
            remove_only_if_there(i)
    remove_only_if_there(fpath / "tmp_vid_list.txt")
    remove_only_if_there(fpath / "final_output.mp4")
    remove_only_if_there(fpath / "tfs.trf")


def clean_up(fpath):
    remove_only_if_there(fpath / "tmp_vid_list.txt")
