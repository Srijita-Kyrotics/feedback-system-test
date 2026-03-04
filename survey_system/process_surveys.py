import os
import json
import csv
import argparse
import sys
from collections import defaultdict

# Add the olm_ocr_project to path so we can import ocr_processor
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "olm_ocr_project"))
import ocr_processor

def parse_score(value):
    """
    Parse a score value, handling various input formats.
    Returns float between 0-5, or 0 if invalid.
    """
    try:
        val = str(value).strip().split()[0]
        score = float(val)
        # Clamp to 0-5 range
        return max(0, min(5, score))
    except (ValueError, IndexError, AttributeError):
        return 0.0

def calculate_averages_for_teacher(student_responses):
    """
    Calculate category averages for a teacher across multiple student responses.
    
    Args:
        student_responses: List of dictionaries, each containing Q1-Q7 scores
    
    Returns:
        Tuple of (category_averages, total_score, percentage)
    
    Mapping:
    1. Preparation & Organization (Q1)
    2. Subject knowledge & Expertise (Q2)
    3. Explanation & Empathy (Q3)
    4. Discipline & Punctuality (Q4)
    5. Regularity & Timeliness (Q5)
    6. Encouragement to Learning (Q6)
    7. Teacher availability (Q7)
    """
    if not student_responses:
        return [0] * 7, 0, 0
    
    # Initialize lists to store all scores for each category
    category_scores = [[] for _ in range(7)]
    
    # Collect scores from all students
    for response in student_responses:
        for category_idx in range(7):
            q_key = f"Q{category_idx + 1}"
            score = parse_score(response.get(q_key, 0))
            category_scores[category_idx].append(score)
    
    # Calculate average for each category
    cat_avgs = []
    for category_idx in range(7):
        if category_scores[category_idx]:
            avg = sum(category_scores[category_idx]) / len(category_scores[category_idx])
            cat_avgs.append(avg)
        else:
            cat_avgs.append(0.0)
    
    total_score = sum(cat_avgs)
    percentage = (total_score / 35.0) * 100
    return cat_avgs, total_score, percentage

def calculate_averages(data):
    """
    Legacy function for single data entry compatibility.
    Maps the first 7 handwritten survey questions (Q1-Q7) directly to 
    the 7 standardized report categories.
    """
    student_responses = [data]
    return calculate_averages_for_teacher(student_responses)

def update_csv(csv_file, dept, teacher, cat_avgs, total_score, percentage):
    """
    Update CSV with teacher evaluation report.
    """
    file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
    headers = [
        "Name of the Teacher",
        "Preparation & Organization for Class (5)",
        "Subject knowledge & Expertise (5)",
        "Explanation & Empathy to student (5)",
        "Discipline & Punctuality (5)",
        "Regularity & Timeliness (5)",
        "Encouragement to Participative Learning (5)",
        "Teacher availability beyond classroom (5)",
        "Total (35)",
        "Percentage of score"
    ]
    
    row = [teacher] + [round(a, 2) for a in cat_avgs] + [round(total_score, 2), f"{percentage:.2f}%"]

    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Students' Satisfaction Survey Report for the 2025 Odd (Autumn) Semester"])
            writer.writerow([f"Department of {dept}"])
            writer.writerow(["Feedback Regarding Teacher"])
            writer.writerow([])
            writer.writerow(headers)
        writer.writerow(row)

def process_ocr_data(extracted_data_list):
    """
    Process OCR extracted data and group by department/teacher.
    
    Args:
        extracted_data_list: List of extracted survey data from OCR
    
    Returns:
        Dictionary with structure: {(dept, teacher): [responses]}
    """
    teacher_groups = defaultdict(list)
    
    for data in extracted_data_list:
        teacher = data.get("TaughtBy", "Unknown")
        dept = data.get("Department", "General")
        
        # Extract only Q1-Q7 responses
        student_response = {}
        for i in range(1, 8):
            q_key = f"Q{i}"
            student_response[q_key] = data.get(q_key, 0)
        
        teacher_groups[(dept, teacher)].append(student_response)
    
    return teacher_groups

def main():
    parser = argparse.ArgumentParser(description="Automated Survey Processing Pipeline")
    parser.add_argument("--input_dir", type=str, default="../input", help="Directory with survey images")
    parser.add_argument("--output_csv", type=str, default="survey_reports.csv", help="Output CSV file")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_csv = os.path.abspath(args.output_csv)

    print(f"Starting pipeline processing for input: {input_dir}")

    if args.mock:
        print("Running in MOCK mode...")
        # Simulating multiple students voting for same teachers
        mock_data = [
            {
                "Department": "Computer Science",
                "Semester": "6th",
                "Year": "2025",
                "CourseCode": "CS401",
                "CourseName": "Database Systems",
                "TaughtBy": "Dr. Rumi Sen",
                "FullPart": "Full",
                "Q1": "5", "Q2": "5", "Q3": "5", "Q4": "5", "Q5": "5",
                "Q6": "5", "Q7": "5",  # Student 1 votes for Dr. Rumi Sen
                "Q8": "0", "Q9": "0", "Q10": "0", "Q11": "0", "Q12": "0", "Q13": "0", "Q14": "0",
            },
            {
                "Department": "Computer Science",
                "Semester": "6th",
                "Year": "2025",
                "CourseCode": "CS401",
                "CourseName": "Database Systems",
                "TaughtBy": "Dr. Rumi Sen",
                "FullPart": "Full",
                "Q1": "5", "Q2": "5", "Q3": "5", "Q4": "5", "Q5": "5",
                "Q6": "5", "Q7": "5",  # Student 2 votes for Dr. Rumi Sen
                "Q8": "0", "Q9": "0", "Q10": "0", "Q11": "0", "Q12": "0", "Q13": "0", "Q14": "0",
            },
            {
                "Department": "Computer Science",
                "Semester": "6th",
                "Year": "2025",
                "CourseCode": "CS402",
                "CourseName": "Data Structures",
                "TaughtBy": "Soma Das",
                "FullPart": "Full",
                "Q1": "4", "Q2": "5", "Q3": "3", "Q4": "2", "Q5": "1",
                "Q6": "5", "Q7": "4",  # Student 1 votes for Soma Das
                "Q8": "0", "Q9": "0", "Q10": "0", "Q11": "0", "Q12": "0", "Q13": "0", "Q14": "0",
            },
            {
                "Department": "Computer Science",
                "Semester": "6th",
                "Year": "2025",
                "CourseCode": "CS402",
                "CourseName": "Data Structures",
                "TaughtBy": "Soma Das",
                "FullPart": "Full",
                "Q1": "2", "Q2": "3", "Q3": "4", "Q4": "3", "Q5": "3",
                "Q6": "4", "Q7": "3",  # Student 2 votes for Soma Das
                "Q8": "0", "Q9": "0", "Q10": "0", "Q11": "0", "Q12": "0", "Q13": "0", "Q14": "0",
            },
        ]
        extracted_data_list = mock_data
    else:
        # For production: process actual images from input_dir
        print("Initializing OCR model (this may take a moment and requires GPU)...")
        try:
            model, processor = ocr_processor.load_model()
            extracted_data_list = []
            
            # The ocr_processor.py expects images in subfolders.
            # If images are in the root of input_dir, we process that folder directly.
            # Otherwise, we walk the subdirectories.
            
            subdirs = [os.path.join(input_dir, d) for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
            folder_to_process = subdirs if subdirs else [input_dir]
            
            for folder in folder_to_process:
                print(f"Extracting data from folder: {folder}")
                extraction_result = ocr_processor.process_folder(folder, model, processor, None)
                if extraction_result:
                    try:
                        # Clean and parse the OCR output (which is often wrapped in markdown blocks)
                        cleaned_json = extraction_result.strip()
                        if cleaned_json.startswith("```json"):
                            cleaned_json = cleaned_json[7:]
                        if cleaned_json.endswith("```"):
                            cleaned_json = cleaned_json[:-3]
                        
                        data = json.loads(cleaned_json.strip())
                        extracted_data_list.append(data)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Failed to parse JSON from {folder}: {e}")
        except Exception as e:
            print(f"Error in OCR pipeline: {e}")
            print("Ensure you have the required dependencies and hardware (GPU) to run the model.")
            return

    # Group data by teacher/department and aggregate responses
    teacher_groups = process_ocr_data(extracted_data_list)
    
    print(f"Processing {len(teacher_groups)} teacher(s)...")
    
    # Process each teacher's aggregated responses
    for (dept, teacher), student_responses in teacher_groups.items():
        print(f"  {teacher} ({dept}): {len(student_responses)} student response(s)")
        
        # Calculate averages across all student responses
        cat_avgs, total_score, percentage = calculate_averages_for_teacher(student_responses)
        
        print(f"    -> Total: {total_score:.2f}/35 ({percentage:.2f}%)")
        update_csv(output_csv, dept, teacher, cat_avgs, total_score, percentage)

    print(f"\nPipeline complete. Results saved to {output_csv}")

if __name__ == "__main__":
    main()
