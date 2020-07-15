import os
from pathlib import Path
from typing import Dict, Iterable, Iterator


class FU(object):

    @classmethod
    def get_file_info(cls, path: str) -> Dict:
        result = {"path": path, "parent": "", "base": "", "name": "", "ext": "",
                  "parts": list(), "parents": list(), "suffixes": list()}
        if cls.is_valid_file(path):
            result["path"] = str(Path(path).absolute())
            result["parent"] = str(Path(path).parent)
            result["base"] = Path(path).name
            result["name"] = Path(path).stem
            result["ext"] = Path(path).suffix
            result["parts"] = list(Path(path).parts)
            result["parents"] = [str(ps) for ps in Path(path).parents]
            result['suffixes'] = [suf.strip(".") for suf in Path(path).suffixes]
        return result

    @classmethod
    def is_valid_dir(cls, source: str) -> bool:
        """
        Validate directory with source files.
        :param source: Directory name
        :return:   boolean
        """
        result = False
        try:
            if os.path.exists(source) and os.path.isdir(source)\
                    and os.access(source, os.R_OK) and os.listdir(source):
                result = True
            else:
                raise IOError("Bad directory <{}>".format(source))
        except IOError as e:
            logger.error(e)
        return result

    @classmethod
    def is_valid_file(cls, source: str) -> bool:
        """
        Validate file.
        :param source: file name
        :return:   boolean
        """
        return os.path.exists(source) and os.path.isfile(source) and os.access(source, os.R_OK)

    @staticmethod
    def get_files(dr, sort=False) -> Iterable[str]:
        """
        Extract files from current directory
        :param sort: Sort flag
        :param path: Directory path
        :return result: List of files
        """
        result = []
        try:
            if FU.is_valid_dir(dr):
                for item in os.scandir(dr):
                    fn = os.path.join(dr, item)
                    if os.path.isfile(fn):
                        name = Path(fn).name
                        if "pi" in name:
                            result.append(fn)
                result = sorted(result)
        except Exception as exc:
            print(exc)
        return result
