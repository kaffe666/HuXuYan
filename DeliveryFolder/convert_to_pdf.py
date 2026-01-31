#!/usr/bin/env python3
"""
Convert ITD_Document.md to PDF using markdown and browser print.
This script generates an HTML file that can be printed to PDF.
"""

import markdown
import os

def convert_md_to_html():
    # Read the markdown file
    with open('ITD_Document.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )
    
    # Create full HTML document with styling
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ITD Document - Best Bike Paths (BBP)</title>
    <style>
        @media print {{
            body {{ font-size: 11pt; }}
            h1 {{ page-break-before: always; }}
            h1:first-of-type {{ page-break-before: avoid; }}
            table {{ page-break-inside: avoid; }}
            pre {{ page-break-inside: avoid; }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        
        h1 {{
            color: #1a365d;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
            margin-top: 40px;
        }}
        
        h2 {{
            color: #1e40af;
            border-bottom: 1px solid #93c5fd;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        
        h3 {{
            color: #1e3a8a;
            margin-top: 25px;
        }}
        
        h4 {{
            color: #3730a3;
            margin-top: 20px;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        
        th, td {{
            border: 1px solid #d1d5db;
            padding: 10px 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #1e40af;
            color: white;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background-color: #f3f4f6;
        }}
        
        tr:hover {{
            background-color: #e5e7eb;
        }}
        
        code {{
            background-color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
            color: #1e40af;
        }}
        
        pre {{
            background-color: #1e293b;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 0.85em;
            line-height: 1.5;
        }}
        
        pre code {{
            background-color: transparent;
            color: inherit;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #2563eb;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #eff6ff;
            color: #1e40af;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 30px 0;
        }}
        
        a {{
            color: #2563eb;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        ul, ol {{
            padding-left: 25px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        .cover-page {{
            text-align: center;
            padding: 60px 0;
            border-bottom: 3px solid #2563eb;
            margin-bottom: 40px;
        }}
        
        .cover-page h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            border: none;
        }}
        
        .cover-page h2 {{
            font-size: 1.5em;
            color: #64748b;
            border: none;
            margin-top: 0;
        }}
        
        /* Status indicators */
        td:contains("✅") {{ color: #16a34a; }}
        td:contains("❌") {{ color: #dc2626; }}
    </style>
</head>
<body>
{html_content}

<footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #64748b; font-size: 0.9em;">
    <p>Implementation and Test Deliverable (ITD) - Best Bike Paths (BBP)</p>
    <p>Software Engineering 2 - Politecnico di Milano</p>
    <p>Generated: January 30, 2026</p>
</footer>
</body>
</html>'''
    
    # Write HTML file
    with open('ITD_Document.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print("✅ HTML file created: ITD_Document.html")
    print("")
    print("📄 To create PDF:")
    print("   1. Open ITD_Document.html in your browser (Chrome recommended)")
    print("   2. Press Ctrl+P (or Cmd+P on Mac)")
    print("   3. Select 'Save as PDF' as destination")
    print("   4. Click 'Save' and choose the filename")
    print("")
    print("   Or use Microsoft Edge/Chrome's built-in 'Print to PDF' feature")
    
    return 'ITD_Document.html'

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    output_file = convert_md_to_html()
    
    # Try to open in browser
    import webbrowser
    webbrowser.open('file://' + os.path.abspath(output_file))
