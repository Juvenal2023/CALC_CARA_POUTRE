import os
import json
import shutil
import subprocess
from time import time
from Const import SIF_PATH


def copy_files(old_dir: str, new_dir: str, files: str, ext: str=None) -> None:
    if files == "" or files == [] or files == ():
        raise Exception("No file to copy.")
    if isinstance(files, str):
        files = (files)
    l_file_nom = []
    for file in files:
        file_nom = file if ext is None or file.endswith(ext) else file + "." + ext
        l_file_nom.append(file_nom)
        old_path = os.path.join(old_dir, file_nom)
        new_path = os.path.join(new_dir, file_nom)
        if not os.path.exists(old_path) or not os.path.isfile(old_path):
            raise Exception(f"Template file {old_path} does not exist.")
        shutil.copyfile(old_path, new_path)
    return l_file_nom


def read_write_file(file_path: str, file_type: str="json", mode: str="r", encoding: str="utf-8", obj=None, lst=False):
    if file_type not in ["json", "txt"]:
        raise Exception("Invalid file type.")
    try:
        with open(file_path, mode=mode, encoding=encoding) as f:
            if mode == "r":
                return json.load(f) if file_type == "json" else (f.readlines() if lst is True else f.read())
            elif mode == "w" and obj is not None:
                json.dump(obj, f, indent=4) if file_type == "json" else f.write(obj)
                return True
            else:
                raise Exception("Invalid mode or object.")
    except FileNotFoundError:
        raise Exception(f"File {file_path} does not exist.")
    except json.JSONDecodeError:
        raise Exception(f"Failed to decode JSON from file {file_path}.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def replace_keyword(file_path: str, key_word: str, new_word: str) -> None:
    old_cont = read_write_file(file_path, file_type="txt")
    new_cont = old_cont.replace(key_word, new_word)
    read_write_file(file_path, file_type="txt", mode="w", obj=new_cont)


def run_aster(export_path: str) -> None:
    if not (os.path.exists(SIF_PATH) and os.path.isfile(SIF_PATH)):
        raise Exception("Code aster sif file not found.")

    aster_failed = False
    command = f"singularity exec {SIF_PATH} run_aster {export_path}"

    aster_start = time()
    result = subprocess.run(command, shell=True, capture_output=True)
    aster_failed = b"NOOK  AUTRE_ASTER" in result.stdout or (
        b"DIAGNOSTIC JOB : <A>_ALARM" not in result.stdout
        and b"NOOK" not in result.stdout
    )
    aster_end = time()

    if aster_failed:
        raise Exception("MACR_CARA_POUTRE failed.")
    else:
        return aster_end - aster_start