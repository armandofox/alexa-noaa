PYTHON = python
ZIP = zip
TARGET = lambda

zip:
	rm $(TARGET).zip
	cd lambda && $(ZIP) -qr ../$(TARGET).zip *

skill/utterances.txt: skill/utterances.txt.glob
	@$(PYTHON) lambda/ask/unglob_intent.py $^ > $@
