import os
import sys
import time
from functools import partial
from pathlib import Path
# from concurrent.futures import ProcessPoolExecutor
from .core.fileu import FU as fu

"""
    Launch example: 
    python3.8 __main__.py /bigfiles/test '0011453'
    python3.8 project_name '/bigfiles/test' '0011453'
"""

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class Main:
    @staticmethod
    def findall(pos, string):
        match = string.find(pos)
        while match != -1:
            yield match
            match = string.find(pos, match + 1)

    @staticmethod
    def find_in_file(substr, fname, mode="rb", buff_size=100000000):
        """
        Find substr in big (1gb+) string stored in file. Return all position founded.
        :param substr: Needle string
        :param fname:  File name
        :param mode:   File open mode
        :param buff_size: Buffer size. For default 100MB
        :return:
        """
        with open(fname, mode) as bfo:
            chunk = iter(partial(bfo.read, buff_size), b'')
            for s in chunk:
                s = s.decode('ascii')
                for x in Main.findall(substr, s):
                    yield x

    @staticmethod
    def find_in_file_it(substr, fname, buff_size=100_000_000):
        """
        Find substr in big (1gb+) string stored in file. Return all position founded.
        :param substr: Needle string
        :param fname:  File name
        :param mode:   File open mode
        :param buff_size: Buffer size. For default 100MB
        :return:
        """
        with open(fname, "rb") as bfo:
            chunk = iter(partial(bfo.read, buff_size), b'')
            for s in chunk:
                s = s.decode('ascii')
                for x in Main.findall(substr, s):
                    yield x


    @staticmethod
    def process_files(pattern, dpath):
        buff_size = 100_000_000
        file_offset = 0
        total_count = 0
        matches = {}

        stm = time.perf_counter()

        for f in fu.get_files(dpath):
            print('[DEBUG] ВЗЯТ ФАЙЛ')
            file_nums_count = 0
            file_matches = {}
            for n in Main.find_in_file_it(pattern, f):
                file_nums_count += 1
                total_count += 1
                file_matches[file_nums_count] = n + file_offset
            if file_matches: 
                matches[os.path.basename(f)] = {
                    'matches': file_matches,
                    'count': file_nums_count,
                }

            file_offset += buff_size

        se = time.perf_counter() - stm
        matches['runtime'] = f"This query took {se:.4f} seconds."
        matches['summary'] = f"Found {total_count} entries in {len(matches)} file(s) at {se:.4f} sec."

        return matches

    

    @staticmethod
    def process_file(pattern, fn):
        stm = time.perf_counter()
        count = 0
        for n in Main.find_in_file(pattern, fn):
            count += 1
            print(f"{count} - {n}")
        se = time.perf_counter() - stm
        print(f"Founded {count} entries at {se:.4f} sec.")


if __name__ == "__main__":
    dpath = sys.argv[1] if 1 < len(sys.argv) else os.path.join(BASE_PATH, 'data')
    pattern = sys.argv[2] if 2 < len(sys.argv) else '74012'
    fn = "/media/efanchiс/mobile/bigfiles/test/pi_dec_1t_0000.txt"

    Main.process_files(pattern, dpath)

# def process_file(pattern, fn):
#     result = []
#     for n in Main.find_in_file(pattern, fn):
#         result.append(n)
#     return result


# def future_callback(future):
#     print(future.result())


# def process_file_pool(pattern):
#     with ProcessPoolExecutor(10) as pool:
#         for fn in fu.get_files(dpath):
#             future = pool.submit(process_file, pattern, fn)
#             future.add_done_callback(future_callback)



    #Main.process_file(pattern, fn)
    # stm = time.perf_counter()
    # count = 0
    # process_file_pool(pattern)
    # se = time.perf_counter() - stm
    # print(f"Founded {count} entries at {se:.4f} sec.")