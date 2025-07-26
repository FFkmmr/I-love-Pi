# services/crush_200billions_to_10billions.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'unsorted_trillions')

CHUNK_COUNT = 20

def crush_200billions():
    for dir_name in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, dir_name)
        if not os.path.isdir(dir_path):
            continue

        for file in os.listdir(dir_path):
            if not file.startswith('200billions_') or not file.endswith('.txt'):
                continue

            input_path = os.path.join(dir_path, file)
            base_name = file[:-4]
            out_dir = os.path.join(dir_path, base_name)
            os.makedirs(out_dir, exist_ok=True)

            with open(input_path, 'r') as f:
                lines = f.readlines()

            chunk_size = len(lines) // CHUNK_COUNT
            for i in range(CHUNK_COUNT):
                chunk = lines[i*chunk_size:(i+1)*chunk_size] if i < CHUNK_COUNT - 1 else lines[i*chunk_size:]
                output_path = os.path.join(out_dir, f'10billions_{i}.txt')
                with open(output_path, 'w') as out:
                    out.writelines(chunk)

# if __name__ == "__main__":
#     crush_200billions()
