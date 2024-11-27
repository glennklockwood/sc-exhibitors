#!/usr/bin/env python3

import ezdxf
import csv
import argparse
import yaml

def main(dwg_file_path, output_file=None):
    # Load the DXF file
    doc = ezdxf.readfile(dwg_file_path)
    msp = doc.modelspace()

    # Initialize variables to store the current booth number and area
    current_booth_number = None
    current_booth_area = None

    # List to store extracted data
    booth_data = []

    # Process entities in order
    for entity in msp:
        if entity.dxftype() in ["TEXT", "MTEXT"]:
            layer = entity.dxf.layer
            text = entity.plain_text() if entity.dxftype() == "MTEXT" else entity.dxf.text

            if layer == "BOOTH_NUMBER":
                current_booth_number = text
            elif layer == "BOOTH_AREA":
                current_booth_area = text
                if current_booth_area.endswith(' Sqft'):
                    current_booth_area = int(current_booth_area[:-5])
                else:
                    raise ValueError(f"Unexpected format for booth area: {current_booth_area}")
            elif layer == "COMPANY_NAME":
                # When a company name is encountered, assume the previous booth number and area apply
                booth_data.append({
                    "company_name": text,
                    "booth_number": current_booth_number,
                    "booth_area_sqft": current_booth_area
                })
                # Reset the booth number and area for the next record
                current_booth_number = None
                current_booth_area = None

    # Output the results as pretty-printed YAML
    print(yaml.dump(booth_data, sort_keys=False, default_flow_style=False))

    # Optionally save to CSV
    if output_file:
        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["company name", "booth number", "booth area sqft"])
            for booth in booth_data:
                writer.writerow([booth["company_name"], booth["booth_number"], booth["booth_area_sqft"]])
        print(f"Data written to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract booth data from a DXF file.")
    parser.add_argument("dwg_file_path", help="Path to the DXF file")
    parser.add_argument("--output_file", help="Path to the output CSV file", default=None)
    args = parser.parse_args()
    main(args.dwg_file_path, args.output_file)
