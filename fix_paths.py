# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 17:34:21 2026

@author: cartin
"""

import glob
import re

html_files = glob.glob("**/*.html", recursive=True)

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove all <base> tags completely
    content = re.sub(r'<base href="[^"]*">\s*', '', content)

    # 2. Strip hardcoded root domain
    content = content.replace('https://dcartin.github.io/', '/')

    # 3. Clean up double repository names
    content = content.replace('NAPS-Intermediate-Physics/NAPS-Intermediate-Physics/', 'NAPS-Intermediate-Physics/')

    # 4. Standardize asset paths (_static) to absolute subfolder paths
    content = re.sub(r'href=["\'](\.\./)*_static/', 'href="/NAPS-Intermediate-Physics/_static/', content)
    content = re.sub(r'src=["\'](\.\./)*_static/', 'src="/NAPS-Intermediate-Physics/_static/', content)
    content = re.sub(r'href=["\']/_static/', 'href="/NAPS-Intermediate-Physics/_static/', content)
    content = re.sub(r'src=["\']/_static/', 'src="/NAPS-Intermediate-Physics/_static/', content)

    # 5. Standardize notebook page links to absolute subfolder paths
    content = re.sub(r'href=["\'](\.\./)*notebooks/', 'href="/NAPS-Intermediate-Physics/notebooks/', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Successfully processed {len(html_files)} HTML files.")