import csv

input_file = "1K_SMILES.log" 
output_file = "1K_SMILES_with_AiZynthFinder_Score.csv"

results = []

with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("Done with "):
            try:
                smiles = line.split("Done with ")[1].split(" in ")[0].strip()
                solved = "not solved" not in line
                results.append({
                    "SMILES": smiles,
                    "Solved_with_AiZynthFinder": solved
                })
            except Exception as e:
                print(f"Skipping malformed line: {line}")
                continue

# Save to CSV
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ["SMILES", "Solved_with_AiZynthFinder"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Parsed {len(results)} lines. Results saved to {output_file}")
