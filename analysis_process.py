import sys
from collections import defaultdict

def extract_k(filename):
    parts = filename.split('_')
    if len(parts) < 3:
        raise ValueError(f"Could not extract k from filename: {filename}")
    k_str = parts[-3]
    if not k_str.isdigit():
        raise ValueError(f"3rd-from-last token '{k_str}' is not a number in: {filename}")
    return int(k_str)

def count_partitions(filepath):
    filename = filepath.split('/')[-1]
    k = extract_k(filename)
    print(f"Filename : {filename}")
    print(f"k        : {k}  (partitions 0 to {k})")
    print()

    with open(filepath, 'r') as f:
        total_lines = sum(1 for line in f if line.strip())

    print(f"Total lines: {total_lines}")
    print()

    checkpoints = {}
    for pct in range(10, 101, 10):
        line_num = max(1, round(total_lines * pct / 100))
        checkpoints[line_num] = pct

    counts = defaultdict(int)
    results = {}

    with open(filepath, 'r') as f:
        for i, line in enumerate(f, start=1):
            val = line.strip()
            if not val:
                continue
            counts[val] += 1
            if i in checkpoints:
                pct = checkpoints[i]
                results[pct] = dict(counts)

    # Print table
    header = f"{'Partition':<12}" + "".join(f"{p:>8}%" for p in range(10, 101, 10))
    print(header)
    print("-" * len(header))

    for partition in range(k + 1):
        row = f"{str(partition):<12}"
        for pct in range(10, 101, 10):
            snapshot = results.get(pct, {})
            row += f"{snapshot.get(str(partition), 0):>9}"
        print(row)

    print()
    print(f"{'Lines read':<12}", end="")
    for pct in range(10, 101, 10):
        line_num = max(1, round(total_lines * pct / 100))
        print(f"{line_num:>9}", end="")
    print()

    # Build 2D array: rows = partitions (0..k), cols = checkpoints (10%..100%)
    array_rows = []
    for partition in range(k + 1):
        row = []
        for pct in range(10, 101, 10):
            snapshot = results.get(pct, {})
            row.append(snapshot.get(str(partition), 0))
        array_rows.append(row)

    # Format as numpy array literal
    inner = ",\n         ".join(
        "[" + ", ".join(str(v) for v in row) + "]"
        for row in array_rows
    )
    np_str = (
        f'data = np.array([{inner}])'
        f'  # columns = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]'
    )

    # Write to output file
    out_path = filepath.rsplit('.', 1)[0] + '_partition_counts.py'
    with open(out_path, 'w') as f:
        f.write(np_str + '\n')

    print(f"\nArray written to: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python count_partitions.py <filepath>")
        sys.exit(1)
    count_partitions(sys.argv[1])