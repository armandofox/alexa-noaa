PYTHON = python
ZIP = zip
TARGET = lambda

.PHONY: all
all: zip skill/utterances.txt

zip:
	rm -f $(TARGET).zip
	cd lambda && $(ZIP) -qr ../$(TARGET).zip *

skill/utterances.txt: skill/utterances.txt.glob
	@$(PYTHON) lambda/ask/unglob_intent.py $^ > $@
