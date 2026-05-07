# Double-Blind Anonymization Checklist

Before creating the anonymous GitHub repository:

- [ ] No real author names in README, commits, config, docs, or file paths.
- [ ] No institution names, lab names, personal websites, or project-internal URLs.
- [ ] No `.git/` history from a private or identifiable repository.
- [ ] No raw logs containing usernames, hostnames, or absolute paths.
- [ ] No paper PDF with author metadata.
- [ ] No hidden files such as `.DS_Store`, `.idea`, `.vscode/settings.json`, or notebook checkpoint folders.
- [ ] Git identity set to anonymous values before first commit.

Recommended check:

```bash
grep -RniE "(name|university|gmail|outlook|users/|C:\\|/home/)" . \
  --exclude-dir=.git --exclude=ANONYMIZATION_CHECKLIST.md
```
