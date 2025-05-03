input_file = "combined_history_dataset.txt"
train_file = "train.txt"
eval_file = "eval.txt"

# Change this if you want different splits
train_lines = 2000
eval_lines = 500

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Optional: shuffle if needed
# import random
# random.shuffle(lines)

# Write train set
with open(train_file, "w", encoding="utf-8") as f:
    f.writelines(lines[:train_lines])

# Write eval set
with open(eval_file, "w", encoding="utf-8") as f:
    f.writelines(lines[-eval_lines:])

print(f"✅ Split completed: {train_file} ({train_lines} lines), {eval_file} ({eval_lines} lines)")
