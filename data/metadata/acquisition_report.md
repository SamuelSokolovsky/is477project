# Data Acquisition Report

**Generated:** 2025-12-06 15:49:00

---

## Summary

- **Total Files Processed:** 5
- **Total Size:** 17.72 MB
- **Verification Status:** Complete
- **Purpose:** Key files for data integration only

## Dataset 1: ESPN Soccer Data (Kaggle)

- **Files Processed:** 4
- **Source:** https://www.kaggle.com/datasets/excel4soccer/espn-soccer-data
- **License:** Check Kaggle dataset page

### Files

- `teams.csv` - 503.40 KB
- `teamStats.csv` - 11.24 MB
- `standings.csv` - 637.52 KB
- `leagues.csv` - 138.28 KB

## Dataset 2: Football-Data.co.uk

- **Files Processed:** 1
- **Source:** https://github.com/datasets/football-datasets
- **License:** PDDL 1.0 (Public Domain)

### Files

- `all_leagues_all_seasons.csv` - 5.23 MB
  - **Primary integration file**
  - Contains: All 5 leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)
  - Time span: 1999-2025

---

## File Details

| File | Size | Checksum (SHA-256) |
|------|------|-----------|
| `teams.csv` | 503.40 KB | `69a836fbba90e275...` |
| `teamStats.csv` | 11.24 MB | `a9f233ba3ad7f6e2...` |
| `standings.csv` | 637.52 KB | `e872ee06d5f31ab0...` |
| `leagues.csv` | 138.28 KB | `7677d3fe20eebe56...` |
| `all_leagues_all_seasons.csv` | 5.23 MB | `ca14e991b2b6cb6a...` |

---

## Verification

All files have been verified with SHA-256 checksums.
See `checksums.txt` for complete checksum listing.

## Notes

- Only processing key files needed for data integration
- Dataset 2: Using consolidated `all_leagues_all_seasons.csv` only
- Ignored files with [invalid] prefix
- Ignored individual season files (using consolidated version)

