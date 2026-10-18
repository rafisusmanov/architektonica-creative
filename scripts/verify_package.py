#!/usr/bin/env python3
"""Read-only checks for Architektonica Creative Engine package."""
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
skills=sorted((root/'skills').glob('architektonica-*/SKILL.md'))
expected={'architektonica-creative-director','architektonica-reader-insight','architektonica-idea-lab','architektonica-narrative-design','architektonica-copy-studio','architektonica-psycholinguistic-editor','architektonica-critical-editor','architektonica-search-visibility','architektonica-engine-mapper','architektonica-portfolio-case-writer'}
found={p.parent.name for p in skills}
errors=[]
if found!=expected:errors.append(f'Skill dirs mismatch: {expected^found}')
for f in skills:
 s=f.read_text(encoding='utf-8')
 if not s.startswith('---\n'):errors.append(f'{f.name}: no yaml header')
 for k in ('name:','description:'):
  if k not in s.split('---',2)[1]:errors.append(f'{f.name}: missing {k}')
 for rel in re.findall(r'`(\.\./\.\./(?:references|methods)/[^`]+)`',s):
  candidate=(f.parent/rel).resolve()
  if not candidate.exists(): errors.append(f'{f.parent.name}: broken relative path {rel}')
for f in skills:
 dest=root/'.agents'/'skills'/f.parent.name/'SKILL.md'
 if not dest.exists() or dest.read_bytes()!=f.read_bytes():errors.append(f'Missing or stale .agents mirror: {f.parent.name}')
critical=[root/'methods/portfolio-case-workflow.md',root/'samples/05_portfolio_from_one_message.md',root/'PROJECT_SYSTEM_PROMPT.md',root/'QUICK_START.md',root/'methods/research-evidence-map.md',root/'references/research/Architektonica_реестры_исследования.xlsx',root/'references/template/Тексты шаблона Architektonica (Engine).xlsx']
for f in critical:
 if not f.exists():errors.append('Missing: '+str(f.relative_to(root)))
print(f'Skills: {len(skills)}; required files: {len(critical)}; errors: {len(errors)}')
for e in errors:print('ERROR',e)
raise SystemExit(bool(errors))
