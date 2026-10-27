# Publishing the repository on GitHub

1. Create a **public**, empty GitHub repository named `tracerag-evidence-lab`. Do **not** initialize it with a README, `.gitignore`, or license; these files are already included.
2. Extract the ZIP and open the `tracerag-evidence-lab` directory. Make sure hidden files and directories such as `.github/` and `.gitignore` are included.
3. From a terminal in that directory, run:

```bash
git init
git add -A
git commit -m "Initial release: offline retrieval and evidence audit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tracerag-evidence-lab.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Alternatively, use **Add file → Upload files** in the empty repository and upload the extracted project contents (not the ZIP itself). Browser upload may not preserve hidden directories on some systems; verify `.github/workflows/ci.yml` is present after upload.

Suggested GitHub topics: `rag`, `information-retrieval`, `bm25`, `tfidf`, `nlp`, `evaluation`, `mlops`, `python`, `github-actions`.

After the first push, open the **Actions** tab to confirm the CI workflow runs. Inspect `reports/index.html` locally for the benchmark dashboard. Avoid claiming the synthetic benchmark demonstrates production-level accuracy.
