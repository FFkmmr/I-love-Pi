# services/crush_10billions_to_500millions.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'unsorted_trillions')

CHUNK_COUNT = 20

def crush_10billions():
    for trillion_dir in os.listdir(DATA_DIR):
        trillion_path = os.path.join(DATA_DIR, trillion_dir)
        if not os.path.isdir(trillion_path):
            continue

        for bill_dir in os.listdir(trillion_path):
            bill_path = os.path.join(trillion_path, bill_dir)
            if not os.path.isdir(bill_path) or not bill_dir.startswith('200billions_'):
                continue

            for ten_file in os.listdir(bill_path):
                if not ten_file.startswith('10billions_') or not ten_file.endswith('.txt'):
                    continue

                input_path = os.path.join(bill_path, ten_file)
                with open(input_path, 'r') as f:
                    lines = f.readlines()

                chunk_size = len(lines) // CHUNK_COUNT
                for i in range(CHUNK_COUNT):
                    chunk = lines[i*chunk_size:(i+1)*chunk_size] if i < CHUNK_COUNT - 1 else lines[i*chunk_size:]
                    output_path = os.path.join(bill_path, f'500millions_{i}.txt')
                    with open(output_path, 'w') as out:
                        out.writelines(chunk)

# if __name__ == "__main__":
#     crush_10billions()
