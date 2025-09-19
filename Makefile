 .PHONY: up translate gate render adopt
up:        ## bootstrap tools & pre-commit, run smoke checks
	./scripts/nexus-up.sh
translate: ## spec-kit → artifacts
	python -m tools.nexus translate
gate:      ## local PR gate
	python -m tools.nexus gate
render:    ## fix diagrams
	python -m tools.nexus render
adopt:     ## adopt a repo (provide repo=...)
	python -m tools.nexus adopt $(repo)
