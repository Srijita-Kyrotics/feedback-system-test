# Survey Processing System - Technical Logic

This document explains the architecture, directory structure, and the logic used to process handwritten survey forms into standardized reports.

## Directory Structure

```
Aaliah University/
├── input/                  # Input handwritten survey images (*.jpeg)
├── output/                 # Reference templates and sample reports
├── olm_ocr_project/        # Core OCR processing module
│   └── ocr_processor.py    # Handles vision-model interaction & extraction
├── survey_system/          # Automation and CLI tools
│   ├── process_surveys.py  # MAIN SCRIPT: Automates the entire pipeline
│   ├── survey_cli.py       # Manual CLI tool for score entry
│   └── survey_reports.csv  # Final generated report database
└── requirements.txt        # System dependencies
```

## Data Flow: Image to Report

The system is designed to be **fully automated**. No manual data entry is required in the final pipeline.

1.  **Image Discovery**: The `process_surveys.py` script automatically finds handwritten survey images in the `input/` folder.
2.  **AI Extraction**: It uses the `ocr_processor.py` engine (Qwen2-VL AI) to "read" the handwritten scores, teacher names, and departments directly from the JPEG files.
3.  **JSON Conversion**: The AI turns the visual data into a digital JSON format (e.g., Q1: "5", Q2: "4").
4.  **Logical Mapping**: The script maps these results to the 7-column report categories.
5.  **Final CSV**: The system appends the result to `survey_reports.csv`.

## Scoring & Mapping Logic

The survey form contains 14 handwritten questions, but the report requires 7 standardized categories. As per the latest requirements, the system uses a **direct mapping** for the first 7 questions and excludes the rest.

### Category Mapping (1-to-1)

| Report Parameter | Source Question from Image |
| :--- | :--- |
| **Preparation & Organization** | Q1 |
| **Subject Knowledge & Expertise** | Q2 |
| **Explanation & Empathy** | Q3 |
| **Discipline & Punctuality** | Q4 |
| **Regularity & Timeliness** | Q5 |
| **Encouragement to Learning** | Q6 |
| **Teacher Availability** | Q7 |

*Note: Questions **Q8 through Q14** are extracted by the OCR but are intentionally **ignored** during report generation.*

### Calculations

- **Total Score**: Sum of Category 1 to Category 7 (Max 35.00).
- **Percentage**: `(Total Score / 35.00) * 100`.

## How to Verify
Run the pipeline in mock mode to see the mapping logic in action:
```powershell
cd survey_system
python process_surveys.py --mock
```
This will add a "Dr. Verification Test" entry to the CSV using the direct Q1-Q7 mapping logic.
