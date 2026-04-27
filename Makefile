# Makefile for Dev Hub tasks
.PHONY: regenerate-docs
regenerate-docs:
	python3 scripts/generate_docs_index.py

.PHONY: regen-projects regen-projects-discover
regen-projects:
	python3 scripts/generate_project_pages.py

regen-projects-discover:
	python3 scripts/generate_project_pages.py --discover


.PHONY: regen-projects-commit
regen-projects-commit:
	python3 scripts/generate_project_pages.py
	git -C /home/hn3t add -A dev_hub/dist/projects_data.js dev_hub/dist/projects dev_hub/Makefile dev_hub/projects.json
	git -C /home/hn3t commit -m "Rebuild dashboards: update generated project pages and projects_data.js" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" || echo "No changes to commit"

