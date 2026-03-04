# Quick Reference Card

## 📋 System Overview
**Survey Processing System** that takes images → extracts data → aggregates responses → outputs CSV reports

## 🚀 Quick Start Commands

### Test the System
```bash
cd "Aaliah University 1\Aaliah University\survey_system"
python process_surveys.py --mock
```

### Process Real Surveys
```bash
python process_surveys.py --input_dir ../input --output_csv survey_reports.csv
```

### Manual Entry
```bash
python survey_cli.py
```

## 📊 The Math Behind Aggregation

**For each teacher:**
```
Final Score per Category = Average of all student ratings for that category
Example: If 5 students rate Teacher with [4,5,3,2,1] for Q1
         Category 1 score = (4+5+3+2+1) / 5 = 3.0
```

**Final Report:**
```
Total: Sum of all 7 category averages (max 35)
Percentage: (Total / 35) × 100
```

## 📁 File Structure
```
survey_system/
├── process_surveys.py          ← Main OCR processing script
├── survey_cli.py               ← Manual entry tool
├── survey_reports.csv          ← Output (auto-generated)
├── config.json                 ← System configuration
├── USAGE_GUIDE.md              ← Full documentation
├── IMPLEMENTATION_NOTES.md     ← How it works
└── README.md                   ← Original docs
```

## 🎯 Processing Steps

1. **Input**: Images or manual entry with 14 questions
2. **Extraction**: OCR reads survey forms
3. **Grouping**: Groups by Department + Teacher
4. **Selection**: Uses only Q1-Q7 (ignores Q8-Q14)
5. **Aggregation**: Averages all student responses
6. **Output**: CSV with teacher evaluation metrics

## 📋 7 Evaluation Categories (out of 14 questions)

| From Q | Category | Score |
|--------|----------|-------|
| Q1 | Preparation & Organization | 0-5 |
| Q2 | Subject Knowledge & Expertise | 0-5 |
| Q3 | Explanation & Empathy | 0-5 |
| Q4 | Discipline & Punctuality | 0-5 |
| Q5 | Regularity & Timeliness | 0-5 |
| Q6 | Encouragement to Learning | 0-5 |
| Q7 | Teacher Availability | 0-5 |
| **TOTAL** | | **0-35** |

## 🔢 Example Calculation

**Scenario**: Soma Das rated by 4 students

| Student | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 |
|---------|----|----|----|----|----|----|-----|
| Vote 1: | 4  | 5  | 3  | 2  | 1  | 5  | 4   |
| Vote 2: | 3  | 2  | 3  | 2  | 2  | 3  | 3   |
| Vote 3: | 5  | 5  | 5  | 5  | 5  | 5  | 5   |
| Vote 4: | 1  | 1  | 2  | 1  | 1  | 2  | 1   |
| **Avg**: | 3.25 | 3.25 | 3.25 | 2.5 | 2.25 | 3.75 | 3.25 |

**Total Score**: 3.25 + 3.25 + 3.25 + 2.5 + 2.25 + 3.75 + 3.25 = 21.5 / 35
**Percentage**: (21.5 / 35) × 100 = **61.43%**

## 💾 CSV Output Format

```
Name of the Teacher,Cat1 Avg,Cat2 Avg,Cat3 Avg,Cat4 Avg,Cat5 Avg,Cat6 Avg,Cat7 Avg,Total (35),Percentage
Dr. Rumi Sen,5.0,5.0,5.0,5.0,5.0,5.0,5.0,35.0,100.00%
Soma Das,3.25,3.25,3.25,2.5,2.25,3.75,3.25,21.5,61.43%
```

## 🔧 Key Features

✅ **Multi-Student Aggregation** - Handles multiple votes per teacher  
✅ **Smart Grouping** - Groups by Department + Teacher automatically  
✅ **Score Validation** - Clamps scores to 0-5 range  
✅ **Error Handling** - Handles missing/invalid data gracefully  
✅ **Professional Output** - Formatted CSV with headers and metadata  
✅ **Mock Testing** - Test without OCR model loaded

## 📝 Input Requirements

For OCR Processing:
- Clear, readable survey images (JPEG/PNG)
- Handwritten responses to questions 1-14
- Teacher name field
- Department field

For Manual Entry:
- Interactive CLI prompts
- Enter scores as space-separated numbers
- Auto-calculates averages

## ⚠️ Important Notes

- **Only Q1-Q7 used** in calculations (Q8-Q14 ignored)
- **Scores clamped** to 0-5 (invalid inputs → 0)
- **Grouped by teacher** - same teacher across multiple surveys = one average row
- **Appends to CSV** - doesn't overwrite existing data
- **Department preserved** in report header

## 🔗 Dependencies

**For OCR (optional):**
- transformers
- torch
- qwen-vl-utils
- pillow

**Core (always needed):**
- pandas
- csv (built-in)
- json (built-in)

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| OCR model not loading | Ensure GPU available or use survey_cli.py |
| Empty CSV output | Check Q1-Q7 scores are valid (0-5) |
| Images not processed | Verify input/ folder path and image format |
| Duplicate entries | System appends records; filter CSV if needed |

## 📞 File Reference

- **process_surveys.py** → OCR-based automated processing
- **survey_cli.py** → Manual data entry
- **survey_reports.csv** → Final output (auto-created)
- **USAGE_GUIDE.md** → Complete documentation
- **config.json** → Configuration settings

---

**Status**: ✅ Ready to use with test data
**Next**: Load real survey images and run `python process_surveys.py`
