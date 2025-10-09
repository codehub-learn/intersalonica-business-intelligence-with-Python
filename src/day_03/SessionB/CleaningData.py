import csv

input_file = "your_file.csv"
output_file = "cleaned_file.csv"

# Read the CSV and detect missing values
with open(input_file, "r", newline="", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    header = next(reader)
    rows = list(reader)

print("Checking for missing values...\n")

# Count missing values per column
missing_counts = [0] * len(header)
clean_rows = []

for row in rows:
    has_missing = False
    for i, value in enumerate(row):
        if value.strip() == "":
            missing_counts[i] += 1
            has_missing = True
    if not has_missing:
        clean_rows.append(row)

# Print missing value summary
print("Missing values per column:")
for col, count in zip(header, missing_counts):
    print(f"{col}: {count}")

print(f"\nOriginal rows: {len(rows)}")
print(f"Rows after removing missing values: {len(clean_rows)}")

# Write cleaned data
with open(output_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)
    writer.writerows(clean_rows)

print(f"\nCleaned file saved as '{output_file}'")
