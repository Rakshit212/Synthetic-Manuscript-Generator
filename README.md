# Synthetic Manuscript Generator

## Project Overview
This project is an automated, end-to-end Python pipeline that synthesizes realistic historical manuscript folio images from raw Indic-script text and generates fully synchronized ground-truth annotation files. It is designed to generate datasets for training modern OCR models.

## Assignment Objective
The objective is to produce 300 realistic manuscript folios across 3 Indic scripts (Devanagari, Modi, Sharada) with matching markdown annotations preserving the ground truth layout and text.

## Features
- **Extensible Architecture:** Configuration-driven script definitions
- **Realistic Backgrounds:** Aged handmade paper and palm-leaf simulations
- **Physical Effects:** Text rotation, slant, baseline variation, ink bleed, and deformation
- **Accurate Ground Truth:** Exact markdown annotations paired with images to prevent loss of GT

## Supported Scripts
- Devanagari
- Modi
- Sharada

## Dataset Distribution
- Total Images: 300
- Train: 255 (85 per script)
- Validation: 30 (10 per script)
- Test: 15 (5 per script)

## Requirements
- Python 3.9+
- See `requirements.txt`

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## Font Setup
**IMPORTANT**: Due to licensing, fonts are not included. Place compatible `.ttf` or `.otf` fonts in:
- `fonts/devanagari/`
- `fonts/modi/`
- `fonts/sharada/`

## Configuration
Adjust settings in `config/config.yaml`.

## CLI Usage
```bash
# Get help
python generate.py --help

# Generate a small sample
python generate.py --script devanagari --count 1

# Generate the full assignment
python generate.py --script all --count 100
```

## Validation
```bash
python validate_dataset.py
```

## Hugging Face Dataset
The generated dataset is hosted and publicly available on Hugging Face:
👉 https://huggingface.co/datasets/Rakshit212/Synthetic-Manuscript-Generator
