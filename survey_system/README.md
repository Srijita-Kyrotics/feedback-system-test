# Student Satisfaction Survey System

Automated and manual feedback processing system designed to streamline teacher evaluation reports.

##  Overview

This system automates the transition from handwritten student satisfaction surveys to structured data reports. It supports both manual data entry (via CLI) and automated processing (via OCR).

##  Core Logic & Mapping

The survey form contains 14 questions, but as per the reporting requirements, only the first 7 are used for the official teacher performance metrics.

### Mapping Flow
Scores from the survey (Q1 - Q7) are mapped directly to the following 7 categories:

1.  **Preparation & Organization** (Mapped from Q1)
2.  **Subject Knowledge & Expertise** (Mapped from Q2)
3.  **Explanation & Empathy** (Mapped from Q3)
4.  **Discipline & Punctuality** (Mapped from Q4)
5.  **Regularity & Timeliness** (Mapped from Q5)
6.  **Encouragement to Learning** (Mapped from Q6)
7.  **Teacher Availability** (Mapped from Q7)

*Questions 8 through 14 are currently ignored in the final score calculation.*

### Scoring Metrics
- **Individual Category Score**: 0 to 5.
- **Total Score**: Sum of the 7 category averages (Maximum 35).
- **Percentage**: (Total Score / 35) * 100.

##  Project Structure

- `survey_cli.py`: A Python terminal interface for manual score entry. Ideal for high-accuracy manual data digitization.
- `process_surveys.py`: An automated pipeline utilizing OCR (Optical Character Recognition) to extract scores from scanned survey images.
- `survey_reports.csv`: The master ledger where all processed results are appended.
- `status.md`: Tracks the development and verification status of the system.

##  Usage

### Manual CLI Entry
Run the following command to start entering data manually:
```bash
python survey_cli.py
```

### Automated OCR Processing (Mock Mode)
To test the pipeline logic without a GPU/Loaded Model:
```bash
python process_surveys.py --mock
```

##  Output Format
The results are saved in `survey_reports.csv` with the following headers:
- Name of the Teacher
- 7 Category Averages
- Total (Max 35)
- Percentage of Score

---

