#  script to run aizynthcli on a single SMILES file
CONFIG_FILE="/custom_config.yml"

INPUT_FILE="1K_SMILES.smi"
OUTPUT_LOG_FILE="1K_SMILES.log"

# Run aizynthcli
echo "Running aizynthcli on: $INPUT_FILE"
aizynthcli --config "$CONFIG_FILE" --smiles "$INPUT_FILE" > "$OUTPUT_LOG_FILE" 2>&1

echo "Done. Output written to $OUTPUT_LOG_FILE"
