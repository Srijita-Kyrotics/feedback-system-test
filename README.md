# Aaliah University Survey Processing System

This repository contains the complete automated pipeline for processing student satisfaction survey forms from handwritten images into standardized reports.

## Project Overview

The system automates the extraction and aggregation of student feedback. It uses a vision-based AI model to read scores and metadata from handwritten survey forms, calculates averages for each teacher across multiple students, and generates a formatted CSV report.

## Directory Structure

- input: Folder for storing raw handwritten survey images (JPEG format).
- output: Folder containing report templates and sample outputs.
- olm_ocr_project: The core OCR engine and processing logic.
- survey_system: Main automation scripts and generated reports.
- survey_system/process_surveys.py: The main script that runs the entire pipeline.
- survey_system/logic.md: Detailed documentation of the mapping and calculation logic.
- survey_reports.csv: The final generated report.

## Requirements

The project requires Python 3.10+ and several specialized libraries for OCR and data processing:
- torch
- transformers
- qwen-vl-utils
- pandas
- openpyxl

A GPU is recommended for the actual OCR extraction part of the pipeline.

## Usage

### Running the Full Pipeline
To process all images in the input directory and update the report:
1. Place images in the input folder.
2. Run the following command:
   python survey_system/process_surveys.py

### Running in Mock Mode
If you are in an environment without a GPU or the required AI models, you can verify the processing logic and mapping using the mock flag:
   python survey_system/process_surveys.py --mock

This will use simulated data instead of reading from images but will follow the exact same calculation and mapping rules.

## Scoring Logic

The system identifies 14 questions on the survey form but only tracks the first 7 questions for the final report categories:
1. Preparation and Organization for Class
2. Subject knowledge and Expertise
3. Explanation and Empathy to student
4. Discipline and Punctuality
5. Regularity and Timeliness
6. Encouragement to Participative Learning
7. Teacher availability beyond classroom

Questions 8 through 14 are ignored during the report generation.
