# Survey System Usage Guide

## Overview
This system processes student satisfaction surveys, extracts data from images, groups responses by teacher/department, calculates category averages, and generates CSV reports.

## System Architecture

### Key Features
1. **Image Input Processing** - Accepts survey images from the input folder
2. **OCR Data Extraction** - Extracts survey responses using Qwen2-VL model
3. **Student Response Aggregation** - Groups all student votes for each teacher
4. **Average Calculation** - Computes category averages across students
5. **CSV Report Generation** - Outputs structured evaluation reports

## Quick Start

### 1. Manual CLI Entry (No OCR)
For manually digitizing survey data without processing images:

```bash
python survey_cli.py
```

**Workflow:**
- Enter department name
- Enter teacher name
- Enter number of students
- For each of 7 categories, input student scores (space-separated)
- System auto-calculates averages and saves to CSV

### 2. Automated OCR Processing

#### For Testing (Mock Mode)
```bash
python process_surveys.py --mock
```
Processes sample data with multiple student responses for demonstration.

#### For Production (Real Images)
```bash
python process_surveys.py --input_dir ../input --output_csv survey_reports.csv
```

**Requirements:**
- Qwen2-VL model installed (`transformers` library)
- GPU available (or sufficient CPU RAM)
- Survey images in JPEG/PNG format in the input folder

## Data Structure

### Input Format
Each survey image extracted by OCR contains:
```json
{
  "Department": "Computer Science",
  "Semester": "6th",
  "Year": "2025",
  "CourseCode": "CS401",
  "CourseName": "Database Systems",
  "TaughtBy": "Dr. Rumi Sen",
  "Q1": "5",  // Preparation & Organization
  "Q2": "5",  // Subject Knowledge
  "Q3": "5",  // Explanation & Empathy
  "Q4": "5",  // Discipline & Punctuality
  "Q5": "5",  // Regularity & Timeliness
  "Q6": "5",  // Encouragement to Learning
  "Q7": "5"   // Teacher Availability
  // Q8-Q14 are extracted but ignored in calculations
}
```

### Output CSV Format
```csv
Name of the Teacher,Preparation & Organization for Class (5),Subject knowledge & Expertise (5),...,Total (35),Percentage of score
Dr. Rumi Sen,5.0,5.0,5.0,5.0,5.0,5.0,5.0,35.0,100.00%
Soma Das,3.0,4.0,3.5,2.5,2.0,4.5,3.5,23.0,65.71%
```

## How Aggregation Works

### Example Scenario
**Teacher: Professor A, Department: CSE**

**Student 1 Response:**  Q1=4, Q2=5, Q3=3, Q4=2, Q5=1, Q6=5, Q7=4

**Student 2 Response:** Q1=3, Q2=4, Q3=4, Q3=3, Q5=3, Q6=4, Q7=3

**Aggregation Process:**
```
Category 1 (Preparation & Organization): Average of (4, 3) = 3.5
Category 2 (Subject Knowledge): Average of (5, 4) = 4.5
Category 3 (Explanation & Empathy): Average of (3, 4) = 3.5
Category 4 (Discipline & Punctuality): Average of (2, 3) = 2.5
Category 5 (Regularity & Timeliness): Average of (1, 3) = 2.0
Category 6 (Encouragement to Learning): Average of (5, 4) = 4.5
Category 7 (Teacher Availability): Average of (4, 3) = 3.5

Total Score: 3.5 + 4.5 + 3.5 + 2.5 + 2.0 + 4.5 + 3.5 = 24.0
Percentage: (24.0 / 35) × 100 = 68.57%
```

## Processing Flow

```
Input Images (input/ folder)
    ↓
OCR Extraction (Qwen2-VL Model)
    ↓
Parse Student Responses (Q1-Q7)
    ↓
Group by Teacher + Department
    ↓
Calculate Averages per Category
    ↓
CSV Output (survey_reports.csv)
```

## Category Mapping (7 out of 14 Questions)

Only the first 7 questions are used for evaluation metrics:

| # | Category | Max Score |
|---|----------|-----------|
| 1 | Preparation & Organization for Class | 5 |
| 2 | Subject knowledge & Expertise | 5 |
| 3 | Explanation & Empathy to student | 5 |
| 4 | Discipline & Punctuality | 5 |
| 5 | Regularity & Timeliness | 5 |
| 6 | Encouragement to Participative Learning | 5 |
| 7 | Teacher availability beyond classroom | 5 |
| **Total** | | **35** |

Questions 8-14 are extracted by OCR but ignored in calculations.

## Practical Workflow

### Step 1: Prepare Survey Images
- Place scanned survey forms in `../input` folder
- Ensure images are clear and readable
- Supported formats: JPEG, PNG

### Step 2: Run OCR Processing
```bash
python process_surveys.py
```

### Step 3: Review Results
- Open `survey_reports.csv` generated in the survey_system folder
- Analyze teacher performance metrics
- Department-wise aggregation is handled automatically

## Installation Requirements

### For OCR Processing:
```bash
pip install transformers torch pillow qwen-vl-utils
```

### For CLI/CSV Processing Only:
```bash
pip install pandas openpyxl
```

## Troubleshooting

### Issue: "Model cannot be loaded"
- **Solution**: Ensure GPU available or use `transformers>=4.38` with sufficient RAM
- **Alternative**: Use manual CLI entry (`survey_cli.py`) instead

### Issue: Images not processed
- **Check**: Ensure images are in `../input` folder with correct format
- **Check**: Image quality - handwritten text must be legible

### Issue: Empty CSV output
- **Check**: Verify input data contains valid Q1-Q7 scores (0-5)
- **Check**: Ensure "TaughtBy" field identifies the teacher

## Customization

To modify scoring categories, edit the mapping in `process_surveys.py`:
```python
# Mapping in calculate_averages_for_teacher():
# Q1 → Preparation & Organization
# Q2 → Subject Knowledge
# ... (customize as needed)
```

To change CSV headers, modify the `headers` list in `update_csv()`.

---

**For Questions or Issues**: Review the README.md or check the mock test with `python process_surveys.py --mock`
