PYTHON = python

skill/utterances.txt: skill/utterances.txt.glob
	@$(PYTHON) lambda/ask/unglob_intent.py $^ > $@
