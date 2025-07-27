import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR,'data', 'unsorted_billion', 'pi_billion_00.txt')
OUTPUT_DIR = os.path.join(BASE_DIR,'data', 'unsorted_billion', 'pi_billion_00')
CHUNK_SIZE = 200_000_000
CHUNK_COUNT = 5

def split_billion():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_PATH, 'r') as f:
        digits = f.read().strip()

    if len(digits) != 1_000_000_000:
        print(f"Warning: Expected 1,000,000,000 digits, got {len(digits)}")
        digits = digits[2:]

    for i in range(CHUNK_COUNT):
        start = i * CHUNK_SIZE
        end = (i + 1) * CHUNK_SIZE
        chunk = digits[start:end]
        output_file = os.path.join(OUTPUT_DIR, f'200millions_{i}.txt')
        with open(output_file, 'w') as f_out:
            f_out.write(chunk)
        print(f"Saved: {output_file} ({len(chunk)} digits)")

if __name__ == '__main__':
    split_billion()