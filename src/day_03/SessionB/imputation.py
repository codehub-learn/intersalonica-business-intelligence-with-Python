import csv

input_file = "your_file.csv"
output_file = "imputed_file.csv"
fill_value = "0"  # You can change this to "N/A", "Unknown", etc.

with open(input_file, "r", newline="", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows = list(reader)

imputed_rows = []
missing_counts = [0] * len(header)

for row in rows:
    new_row = []
    for i, value in enumerate(row):
        if value.strip() == "":  # Detect empty cell
            missing_counts[i] += 1
            new_row.append(fill_value)
        else:
            new_row.append(value)
    imputed_rows.append(new_row)

# Summary
print("Missing values replaced per column:")
for col, count in zip(header, missing_counts):
    print(f"{col}: {count}")

# Write to new file
with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)
    writer.writerows(imputed_rows)

print(f"\nImputed file saved as '{output_file}'")
