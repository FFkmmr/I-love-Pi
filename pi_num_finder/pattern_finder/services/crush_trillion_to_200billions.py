# services/crush_trillion_to_200billions.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,  'data','unsorted_trillions')

CHUNK_COUNT = 5 

def clean_line(line: str, filename: str):
    if filename == 'trillion_00.txt':
        return line.replace("3.", "")
    return line

def crush_trillion():
    for filename in os.listdir(DATA_DIR):
        if not filename.startswith("trillion_") or not filename.endswith(".txt"):
            continue

        input_path = os.path.join(DATA_DIR, filename)
        base_name = filename[:-4]
        output_dir = os.path.join(DATA_DIR, base_name)
        os.makedirs(output_dir, exist_ok=True)

        with open(input_path, 'r') as f:
            lines = [clean_line(line, filename) for line in f]

        chunk_size = len(lines) // CHUNK_COUNT
        for i in range(CHUNK_COUNT):
            chunk = lines[i*chunk_size:(i+1)*chunk_size] if i < CHUNK_COUNT - 1 else lines[i*chunk_size:]
            chunk_path = os.path.join(output_dir, f'200billions_{i}.txt')
            with open(chunk_path, 'w') as out:
                out.writelines(chunk)

# if __name__ == "__main__":
#     crush_trillion()
