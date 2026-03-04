# OLM OCR Extraction Project

This project uses the Qwen2-VL model (the base for OLM OCR) to extract text from images of forms and save the data to Excel files.

## Prerequisites

- **NVIDIA GPU**: Highly recommended (16GB+ VRAM for 7B model).
- **Conda**: For environment management.

## Setup

1.  **Create the Conda Environment:**
    ```bash
    conda env create -f environment.yml
    ```

2.  **Activate the Environment:**
    ```bash
    conda activate olm_ocr_env
    ```

## Usage

1.  **Prepare your Input:**
    Organize your images in folders. For example:
    ```
    data/
      form1/
        page1.jpg
        page2.jpg
      form2/
        page1.jpg
        page2.jpg
    ```

2.  **Run the Script:**
    ```bash
    python ocr_processor.py --input_dir /path/to/your/data
    ```

3.  **Output:**
    The script will generate an `extracted_data.xlsx` file in each processed folder containing the extracted information.

## Troubleshooting

-   **OOM (Out of Memory) Errors**: If you run out of GPU memory, try using a smaller model or enabling CPU offloading (automatically handled by `device_map="auto"` but effectively slower).
-   **Model Not Found**: Ensure you have internet access to download the model from Hugging Face on the first run.
-   **JSON Errors**: If the model output isn't perfect JSON, the script will save a `raw_output.txt` file for you to inspect.
