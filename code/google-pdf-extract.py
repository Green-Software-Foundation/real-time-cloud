#!/usr/bin/env python3
"""
Google Sustainability Report PDF Extractor

This script downloads Google's annual Environmental Report PDF and extracts
relevant data tables containing PUE, WUE, and other sustainability metrics
for Google Cloud regions.

Usage:
    python google-pdf-extract.py --year 2024
    python google-pdf-extract.py --pdf path/to/report.pdf
    python google-pdf-extract.py --url https://example.com/report.pdf
"""

import pandas as pd
import requests
import sys
import argparse
import os
import re
from io import BytesIO
import pdfplumber
from datetime import datetime

# Known Google Environmental Report URLs
GOOGLE_REPORT_URLS = {
    2024: 'https://sustainability.google/reports/google-2024-environmental-report.pdf',
    2023: 'https://sustainability.google/reports/google-2023-environmental-report.pdf',
    2022: 'https://sustainability.google/reports/google-2022-environmental-report.pdf',
    2021: 'https://sustainability.google/reports/google-2021-environmental-report.pdf',
}

def download_pdf(url):
    """
    Download a PDF from a URL.
    
    Args:
        url (str): URL to the PDF file
        
    Returns:
        BytesIO: PDF content as bytes
    """
    print(f"Downloading PDF from {url}...")
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        # Verify it's a PDF
        content_type = response.headers.get('content-type', '')
        if 'pdf' not in content_type.lower():
            print(f"Warning: Content-Type is '{content_type}', expected PDF")
        
        pdf_bytes = BytesIO(response.content)
        print(f"✓ Downloaded {len(response.content):,} bytes")
        return pdf_bytes
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading PDF: {e}")
        raise

def extract_tables_from_pdf(pdf_source, search_keywords=None):
    """
    Extract all tables from a PDF that match search keywords.
    
    Args:
        pdf_source: File path, BytesIO, or file-like object
        search_keywords (list): Keywords to search for in text near tables
        
    Returns:
        list: List of tuples (page_num, table_dataframe, context_text)
    """
    if search_keywords is None:
        search_keywords = ['pue', 'power usage effectiveness', 'wue', 'water usage effectiveness',
                          'data center', 'datacenter', 'cloud region', 'efficiency']
    
    print(f"\nExtracting tables from PDF...")
    extracted_tables = []
    
    try:
        with pdfplumber.open(pdf_source) as pdf:
            print(f"PDF has {len(pdf.pages)} pages")
            
            for page_num, page in enumerate(pdf.pages, start=1):
                # Extract text for context
                text = page.extract_text() or ""
                text_lower = text.lower()
                
                # Check if page contains relevant keywords
                has_keywords = any(keyword.lower() in text_lower for keyword in search_keywords)
                
                # Extract tables from this page
                tables = page.extract_tables()
                
                if tables:
                    print(f"  Page {page_num}: Found {len(tables)} table(s)", end='')
                    
                    if has_keywords:
                        print(" [Contains relevant keywords]")
                        for table_idx, table in enumerate(tables):
                            if table and len(table) > 0:
                                # Convert to DataFrame
                                try:
                                    df = pd.DataFrame(table[1:], columns=table[0])
                                    # Clean column names
                                    df.columns = [str(col).strip() if col else f'Column_{i}' 
                                                 for i, col in enumerate(df.columns)]
                                    
                                    # Get surrounding text as context
                                    context = text[:500] if len(text) > 500 else text
                                    
                                    extracted_tables.append({
                                        'page': page_num,
                                        'table_index': table_idx,
                                        'dataframe': df,
                                        'context': context,
                                        'full_text': text
                                    })
                                except Exception as e:
                                    print(f"\n    Warning: Could not convert table {table_idx} to DataFrame: {e}")
                    else:
                        print()
        
        print(f"\n✓ Extracted {len(extracted_tables)} relevant tables")
        return extracted_tables
        
    except Exception as e:
        print(f"✗ Error extracting tables: {e}")
        raise

def identify_pue_wue_tables(tables):
    """
    Identify which extracted tables contain PUE or WUE data.
    
    Args:
        tables (list): List of table dictionaries
        
    Returns:
        dict: Categorized tables by type
    """
    print("\nIdentifying table types...")
    
    categorized = {
        'pue': [],
        'wue': [],
        'combined': [],
        'other': []
    }
    
    for table_info in tables:
        df = table_info['dataframe']
        context = (table_info['context'] + ' '.join(df.columns)).lower()
        
        has_pue = 'pue' in context or 'power usage' in context
        has_wue = 'wue' in context or 'water usage' in context
        has_region = 'region' in context or 'data center' in context or 'datacenter' in context
        
        # Look for year columns or region identifiers
        has_data = any('20' in str(col) for col in df.columns) or has_region
        
        if has_data:
            if has_pue and has_wue:
                categorized['combined'].append(table_info)
                print(f"  Page {table_info['page']}: Combined PUE/WUE table")
            elif has_pue:
                categorized['pue'].append(table_info)
                print(f"  Page {table_info['page']}: PUE table")
            elif has_wue:
                categorized['wue'].append(table_info)
                print(f"  Page {table_info['page']}: WUE table")
            else:
                categorized['other'].append(table_info)
                print(f"  Page {table_info['page']}: Other relevant table")
    
    return categorized

def save_tables_to_csv(categorized_tables, output_dir, year=None):
    """
    Save extracted tables to CSV files.
    
    Args:
        categorized_tables (dict): Categorized tables
        output_dir (str): Output directory
        year (int): Year of the report (for filename)
        
    Returns:
        list: List of saved file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    year_str = f"{year}_" if year else ""
    saved_files = []
    
    print(f"\nSaving tables to {output_dir}/...")
    
    for category, tables in categorized_tables.items():
        if not tables:
            continue
        
        for idx, table_info in enumerate(tables):
            df = table_info['dataframe']
            page = table_info['page']
            
            filename = f"google_{year_str}{category}_page{page}_table{idx}.csv"
            filepath = os.path.join(output_dir, filename)
            
            df.to_csv(filepath, index=False)
            saved_files.append(filepath)
            print(f"  ✓ {filename} ({len(df)} rows, {len(df.columns)} columns)")
            
            # Also save a metadata file
            meta_filename = f"google_{year_str}{category}_page{page}_table{idx}_meta.txt"
            meta_filepath = os.path.join(output_dir, meta_filename)
            
            with open(meta_filepath, 'w') as f:
                f.write(f"Table from Page {page}\n")
                f.write(f"Category: {category}\n")
                f.write(f"Rows: {len(df)}\n")
                f.write(f"Columns: {', '.join(df.columns)}\n\n")
                f.write("Context:\n")
                f.write(table_info['context'])
            
            saved_files.append(meta_filepath)
    
    print(f"\n✓ Saved {len(saved_files)} files total")
    return saved_files

def main():
    """Main function to orchestrate PDF extraction."""
    parser = argparse.ArgumentParser(
        description='Extract sustainability data tables from Google Environmental Report PDFs'
    )
    
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        '--year',
        type=int,
        help='Year of Google Environmental Report to download (e.g., 2024)'
    )
    source_group.add_argument(
        '--url',
        type=str,
        help='URL to a specific PDF file'
    )
    source_group.add_argument(
        '--pdf',
        type=str,
        help='Path to a local PDF file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='google_extracted_tables',
        help='Directory to save extracted CSV files (default: google_extracted_tables)'
    )
    
    parser.add_argument(
        '--keywords',
        type=str,
        nargs='+',
        help='Additional keywords to search for (default: PUE, WUE, data center, etc.)'
    )
    
    args = parser.parse_args()
    
    try:
        # Determine PDF source
        pdf_source = None
        year = None
        
        if args.pdf:
            # Local file
            if not os.path.exists(args.pdf):
                print(f"✗ Error: File not found: {args.pdf}", file=sys.stderr)
                sys.exit(1)
            print(f"Using local PDF: {args.pdf}")
            pdf_source = args.pdf
            
            # Try to extract year from filename
            year_match = re.search(r'20\d{2}', args.pdf)
            if year_match:
                year = int(year_match.group())
                print(f"Detected year from filename: {year}")
        
        elif args.url:
            # Download from URL
            pdf_source = download_pdf(args.url)
            
            # Try to extract year from URL
            year_match = re.search(r'20\d{2}', args.url)
            if year_match:
                year = int(year_match.group())
                print(f"Detected year from URL: {year}")
        
        elif args.year:
            # Use known URL for year
            if args.year not in GOOGLE_REPORT_URLS:
                print(f"✗ Error: No known URL for year {args.year}", file=sys.stderr)
                print(f"Available years: {', '.join(map(str, GOOGLE_REPORT_URLS.keys()))}")
                print(f"Use --url to specify a custom PDF URL")
                sys.exit(1)
            
            year = args.year
            url = GOOGLE_REPORT_URLS[year]
            pdf_source = download_pdf(url)
        
        else:
            # Default to most recent year
            year = max(GOOGLE_REPORT_URLS.keys())
            print(f"No source specified, using most recent report ({year})")
            url = GOOGLE_REPORT_URLS[year]
            pdf_source = download_pdf(url)
        
        # Extract tables
        search_keywords = args.keywords if args.keywords else None
        tables = extract_tables_from_pdf(pdf_source, search_keywords)
        
        if not tables:
            print("\n⚠️  No relevant tables found in PDF")
            print("Try different keywords or check if the PDF contains table data")
            sys.exit(0)
        
        # Categorize tables
        categorized = identify_pue_wue_tables(tables)
        
        # Save to CSV
        saved_files = save_tables_to_csv(categorized, args.output_dir, year)
        
        print(f"\n✓ Success! Extracted data from Google {year if year else ''} Environmental Report")
        print(f"\nNext steps:")
        print(f"  1. Review extracted CSV files in {args.output_dir}/")
        print(f"  2. Identify which tables contain region-specific PUE/WUE data")
        print(f"  3. Manually clean and format data as needed")
        print(f"  4. Integrate relevant data into Cloud_Region_Metadata.csv")
        
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"\n✗ Error: {e}", file=sys.stderr)
        print(f"\nFull traceback:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

