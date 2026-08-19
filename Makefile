.PHONY: audit sync enrich upstream-check upstream-apply install-standard bundle assets weekly discover prune finance-suite publish

weekly:
	./scripts/weekly_cycle.sh

discover:
	python3 scripts/weekly_curation.py discover --import-approved

prune:
	python3 scripts/weekly_curation.py prune --apply

finance-suite:
	python3 scripts/generate_finance_suite.py

publish:
	./scripts/publish_weekly.sh

audit:
	python3 scripts/audit_skills.py

sync:
	./scripts/sync-upstream.sh

enrich:
	python3 scripts/generate_enriched_catalog.py

upstream-check:
	python3 scripts/check_upstream_updates.py

upstream-apply:
	python3 scripts/check_upstream_updates.py --apply

install-standard:
	./scripts/install-standard-bundle.sh --dry-run

bundle:
	./scripts/build-bundle.sh

assets:
	python3 scripts/generate_assets.py
