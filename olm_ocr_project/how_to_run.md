# How to Run OLM OCR Project

This guide explains how to set up the environment and run the OCR processor.

## Prerequisites

- Python 3.10 or higher
- Git (for installing `olmocr`)

## Setup

1.  **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

2.  **Activate the Virtual Environment:**

    -   **Windows:**
        ```powershell
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the OCR Processor

The `ocr_processor.py` script extracts text from images in a directory and saves the results to an Excel file.

### Basic Usage

```bash
python ocr_processor.py --input_dir "path/to/your/images"
```

### Arguments

-   `--input_dir`: **(Required)** The root directory containing subfolders with images.
-   `--model`: The HuggingFace model ID to use. Default is `Qwen/Qwen2-VL-7B-Instruct`.
-   `--template`: Path to the Excel template file. Default is `template.xlsx`.
-   `--mock`: Run in mock mode (does not load the model) for testing the Excel output logic.

### Example

```bash
python ocr_processor.py --input_dir "D:/Data/Forms" --model "Qwen/Qwen2-VL-7B-Instruct"
```

### Example

```bash
cd olm_ocr_project
./venv/Scripts/python ocr_processor.py --input_dir "D:/Aaliah University/image"
```

This will generate an Excel file with dummy data.
