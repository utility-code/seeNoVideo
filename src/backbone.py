import re
import subprocess
from pathlib import Path
from shutil import copyfile

from tqdm import tqdm

from .helpers import *


def replacers(x, p1, p2=""):
    return x.replace(p1, p2).strip()


def space_remover(x):
    return replacers(x, " ").strip()


def nl_remover(x):
    return replacers(x, "\n").strip()


def curly_split(x):
    return re.findall(r"\{(.*?)\}", x, re.MULTILINE | re.DOTALL)


def between_curlies(x):
    return re.findall(r"\}(.*?)\{", x, re.MULTILINE | re.DOTALL)


def comma_split(x):
    return [y.split(",") for y in x]


def single_to_dict(x):
    tmp_dict = {}
    for i in x:
        if len(i) == 0:
            break
        split_string = i.split(":")
        tmp_dict[split_string[0]] = split_string[1]
    return tmp_dict


def multiple_to_dict(x):
    return [single_to_dict(y) for y in x]


def preprocess_input(x):
    return compose(
        x, [space_remover, nl_remover, curly_split, comma_split, multiple_to_dict]
    )


def preprocess_merges(x):
    return compose(x, [space_remover, nl_remover, between_curlies])


def exec_ffmpeg_com(vid_path, tmp_path, comm, noop=False):
    part_tmp_path = Path(tmp_path.with_name("temp_" + tmp_path.name))
    if noop == True:
        copyfile(vid_path, tmp_path)
        return tmp_path
    else:
        try:
            if not Path.exists(tmp_path):
                gi = subprocess.getoutput(
                    f"yes|ffmpeg -i {str(vid_path)} {comm} {str(tmp_path)}"
                )
                print(gi)
                vid_path = tmp_path
                return tmp_path

            else:

                subprocess.getoutput(
                    f"yes|ffmpeg -i {str(tmp_path)} {comm} {str(part_tmp_path)}"
                )
                #         Path.unlink(tmp_path)
                try:
                    Path.rename(part_tmp_path, tmp_path)
                except FileNotFoundError:
                    pass
                return tmp_path
        except:
            return tmp_path


def vidstab(
    val,
    vid_path,
    tmp_path,
):
    try:
        if int(val) == 1:
            tfile = vid_path.parent / "tfs.trf"
            comm = f"-vf vidstabdetect=shakiness=10:accuracy=15:result={tfile} -f"
            ex = subprocess.getoutput(f"yes|ffmpeg -i {str(vid_path)} {comm} null -")
            ex = exec_ffmpeg_com(
                vid_path, tmp_path, f'-vf vidstabtransform=zoom=5:input="{tfile}"'
            )

    except ValueError:
        ex = tmp_path

    return ex


def remove_audio(
    val,
    vid_path,
    tmp_path,
):
    if len(str(val)) > 2:
        tv = Path(vid_path.parent / val)
        if Path.exists(tv):
            print(f"Replacing audio with {tv}")
            ex = exec_ffmpeg_com(
                vid_path,
                tmp_path,
                f"-i {str(tv)} -c:v copy -map 0:v:0 -map 1:a:0 -shortest",
            )
    else:
        ex = tmp_path
    try:
        if int(val) == 0:
            ex = exec_ffmpeg_com(vid_path, tmp_path, "-c copy -an")
    except ValueError:
        ex = tmp_path

    return ex


def rescale_video(
    val,
    vid_path,
    tmp_path,
):
    if len(val) > 2:
        ex = exec_ffmpeg_com(
            vid_path, tmp_path, f'-vf scale={":".join(val.split(";"))}'
        )
    else:
        ex = tmp_path
    return ex


def trim_video(
    val,
    vid_path,
    tmp_path,
):
    _order = 1
    val_p = val.split(";")
    val_p = [x.replace("-", ":") for x in val_p]
    if len(val_p) == 2:
        ex = exec_ffmpeg_com(
            vid_path,
            tmp_path,
            f"-vcodec copy -acodec copy -ss {val_p[0]} -to {val_p[1]}",
        )
    else:
        ex = tmp_path
    return ex


def speed_video(val, vid_path, tmp_path):
    val = int(val)
    if val != 0:
        ex = exec_ffmpeg_com(vid_path, tmp_path, f"-filter:v 'setpts=PTS/{val}'")
    else:
        ex = tmp_path
    return ex


def namer(val, vid_path, tmp_path):
    ex = exec_ffmpeg_com(vid_path, tmp_path, f"", noop=True)
    return ex


def speed_audio(val, vid_path, tmp_path):
    val = float(val)
    if val >= 2.0:
        val = 2.0
    elif val <= 0:
        val = 0.5
    if val != 0:
        ex = exec_ffmpeg_com(vid_path, tmp_path, f"-filter:a 'atempo={val}' -vn")
    else:
        ex = tmp_path
    return ex


def concat_video(lis, fpath, merge_name):
    f1, f2 = lis[0].name, lis[1].name
    with open(fpath / "tmp_vid_list.txt", "w+") as f:
        f.write(f"file '{str(f1)}'\nfile '{str(f2)}'")

    ou1 = subprocess.getoutput(
        f"yes|ffmpeg -f concat -safe 0 -i {fpath/'tmp_vid_list.txt'} -c copy {fpath/merge_name}"
    )

    return fpath / merge_name


dic_procs = {
    "A": remove_audio,
    "resize": rescale_video,
    "+": concat_video,
    "trim": trim_video,
    "speedA": speed_audio,
    "speedV": speed_video,
    "stabilize": vidstab,
    "name": namer,
}


def process_video(dic, fpath):
    name = dic["name"]
    vid_path = fpath / name
    tmp_path = fpath / f"tmp_{name}"

    for key in dic.keys():
        print(f"Executing: {dic_procs[key]}")
        out = dic_procs[key](dic[key], vid_path, tmp_path)

        #  if key != "name":
        #      print(f"Executing: {dic_procs[key]}")
        #      out = dic_procs[key](dic[key], vid_path, tmp_path)
    return tmp_path


def run_process(string, fpath, merge_name="final_output.mp4"):
    pi = preprocess_input(string)
    try:
        pm = preprocess_merges(string)
    except IndexError:
        pm = None
    executed_vid_list = []
    # run process for all files
    for i, vid in tqdm(enumerate(pi), total=len(pi)):
        out = process_video(vid, fpath)
        print(out)
        executed_vid_list.append(out)
    #     print(executed_vid_list)
    lex = len(executed_vid_list)
    if lex >= 2:
        if lex % 2 == 0:
            assert len(pm) == (lex / 2)
        else:
            assert len(pm) == (lex % 2 + 1)
        concat_video(executed_vid_list, fpath, merge_name)
