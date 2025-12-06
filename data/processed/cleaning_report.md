# Data Cleaning Report

**Generated:** 2025-12-06 15:53:27

---

## Summary

- **Files Processed:** 5
- **Cleaning Operations:** Standardization, Missing value handling, Type validation
- **Output Location:** `data/processed/`

## Dataset 2: Match Results

- **Records:** 57,865
- **Date Range:** 1993-07-23 to 2025-11-09
- **Unique Teams:** 244
- **Leagues:** bundesliga, la-liga, ligue-1, premier-league, serie-a

### Cleaning Operations

1. **Team Names:** Standardized to lowercase, removed special characters
2. **Dates:** Parsed and validated (DD/MM/YY format)
3. **Missing Cards:** Filled with 0
4. **Result Validation:** Verified FTR matches FTHG vs FTAG
5. **Season Column:** Added based on match date

## Dataset 1 Files

- **Teams:** 4,104 records
- **Team Stats:** 99,665 records
- **Standings:** 6,024 records
- **Leagues:** 1,084 records

---

## Next Steps

1. Run `03_integrate.py` to merge datasets
2. Team name matching will be performed during integration
3. Quality assessment in `04_quality.py`

