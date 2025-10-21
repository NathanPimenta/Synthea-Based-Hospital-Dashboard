#!/bin/bash
set -e  # exit on error

NUMBER_OF_PATIENTS=${1:-2000}

# --- Initialize paths ---
PROJ_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "📁 Project Directory: $PROJ_DIR"

REPO_URL="https://github.com/synthetichealth/synthea.git"
SYNTHEA_DIR="$HOME/synthea"
DATASET_DIR="$PROJ_DIR/Datasets"

# --- Clone or update Synthea ---
if [ ! -d "$SYNTHEA_DIR" ]; then
    echo "🔄 Cloning Synthea repository into $SYNTHEA_DIR..."
    git clone "$REPO_URL" "$SYNTHEA_DIR"
else
    echo "📦 Synthea repo already exists. Pulling latest changes..."
    cd "$SYNTHEA_DIR" || exit
    git pull
fi

# --- Ensure CSV export is enabled ---
PROPERTIES_FILE="$SYNTHEA_DIR/src/main/resources/synthea.properties"
echo "⚙️  Configuring Synthea for CSV export..."

# Make sure the properties file exists
if [ ! -f "$PROPERTIES_FILE" ]; then
    echo "❌ ERROR: synthea.properties not found in $PROPERTIES_FILE"
    exit 1
fi

# Modify export settings using sed
sed -i 's/^exporter.fhir.export *= *.*/exporter.fhir.export = false/' "$PROPERTIES_FILE"
sed -i 's/^exporter.csv.export *= *.*/exporter.csv.export = true/' "$PROPERTIES_FILE"
sed -i 's/^exporter.csv.append_mode *= *.*/exporter.csv.append_mode = true/' "$PROPERTIES_FILE"
sed -i "s|^exporter.baseDirectory *= *.*|exporter.baseDirectory = $DATASET_DIR|" "$PROPERTIES_FILE"

# --- Ensure output directory exists ---
mkdir -p "$DATASET_DIR"

# --- Generate CSV data ---
cd "$SYNTHEA_DIR" || exit

# -- doing a clean build to ensure everything is up to date --
./gradlew build 

# --- synthea stores the o/p under the csv dir if above options are set --- 
echo "🚀 Generating CSV data for 2000 patients..."
./run_synthea -p "$NUMBER_OF_PATIENTS"

# cp output/csv/* "$DATASET_DIR"
echo "✅ CSV datasets generated in: $DATASET_DIR"