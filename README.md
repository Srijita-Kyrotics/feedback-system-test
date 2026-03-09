# Student Feedback Survey Processing System 

This repository contains an automated pipeline for processing student satisfaction survey forms using Vision AI. It converts handwritten feedback images into a standardized CSV report.

## 🚀 Key Features & Optimizations

- **Vision AI Core**: Uses the **Qwen2-VL-7B** model for high-accuracy OCR of handwritten text and survey markings.
- **VRAM Optimization**: Implements **4-bit Quantization** (via `bitsandbytes`) to allow the 7B model to run on GPUs with ~22GB VRAM (e.g., RTX 3090/4090).
- **Sequential Image Processing**: Multi-page forms are processed one-by-one to prevent CUDA Out Of Memory (OOM) errors during batch inference.
- **Robust Data Aggregation**: Implements a sophisticated merge logic that combines data from multiple images (e.g., Page 1 and Page 2) while intelligently filtering out "Not Provided" or "Unknown" fallbacks to ensure no data loss.
- **Fail-safe JSON Parsing**: Built-in robust parsing to extract structured JSON data even when the AI provides conversational or markdown-wrapped responses.

## 📁 Project Structure

- `input/`: Storage for raw handwritten survey images (JPEG/PNG).
- `survey_system/`: 
  - `process_surveys.py`: **Main Automation Entry Point**. Orchestrates the OCR and report generation.
  - `survey_reports.csv`: Final persistent ledger of teacher evaluations.
- `olm_ocr_project/`:
  - `ocr_processor.py`: Core AI logic handling model loading, quantization, and sequential inference.

## 🛠️ Technical Logic

### 1. Extraction Pipeline
The system identifies the following from each form:
- **Header Metadata**: Department, Semester, Year, Teacher Name, Course Name.
- **Categorical Scores (Q1-Q14)**: Interprets "tick" marks across Likert scale columns (1-5).
- **Open Feedback (Q15)**: Transcribes handwritten comments.

### 2. Calculation Logic
The university report focuses on the **first 7 questions**:
- **Averaging**: Calculates the mean score for each of the 7 categories across all student responses for a teacher.
- **Totaling**: Sums the 7 category averages (Max 35.0).
- **Percentage**: `(Total / 35.0) * 100`.

## 📦 Requirements

- Python 3.10+
- `torch`, `transformers`, `accelerate`, `bitsandbytes`
- `qwen-vl-utils`, `torchvision`, `pandas`, `openpyxl`

## 🏃 How to Run

1. **Place images**: Add survey JPEGs to the `input/` folder.
2. **Execute Pipeline**:
   ```bash
   python survey_system/process_surveys.py --input_dir input
   ```
3. **Mock Mode (Testing)**:
   ```bash
   python survey_system/process_surveys.py --mock
   ```

## 📊 Output
Results are appended to `survey_reports.csv` with full university-standard headers and teacher/department categorization.
