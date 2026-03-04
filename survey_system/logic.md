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

## Automated Pipeline Workflow

The process follow these steps when running `python process_surveys.py`:

1.  **Image Discovery**: The script scans the `input/` folder for images.
2.  **OCR Extraction**: Each image is processed by `ocr_processor.py` (using the Qwen2-VL vision model) to extract data into a JSON format containing labels like `Q1`, `Q2`, etc.
3.  **Data Mapping**: The extracted scores are passed through the mapping logic to convert raw question data into report categories.
4.  **CSV Update**: The mapped results are appended to `survey_reports.csv` along with calculated totals and percentages.

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
