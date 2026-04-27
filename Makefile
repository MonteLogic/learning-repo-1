# ── Variables ─────────────────────────────────────────────────────────────────
PYTHON   := python3
VENV     := .venv
PIP      := $(VENV)/bin/pip
RUNNER   := $(VENV)/bin/python

SCRIPT_MD  := audiobook_JCMNS_Vol40.md
CLEAN_TXT  := audiobook_clean.txt
OUTPUT_MP3 := audiobook_JCMNS_Vol40.mp3

# edge-tts voice / rate / pitch — override on the command line:
#   make mp3 VOICE=en-US-JennyNeural RATE=+15%
VOICE  := en-US-GuyNeural
RATE   := +10%
PITCH  := -2Hz

# ── Targets ───────────────────────────────────────────────────────────────────
.PHONY: all mp3 clean-audio setup help

all: mp3

## mp3 : generate the audiobook MP3 (default target)
mp3: setup $(SCRIPT_MD)
	@echo "→ Generating $(OUTPUT_MP3) ..."
	$(RUNNER) generate_audiobook.py \
		--voice "$(VOICE)" \
		--rate  "$(RATE)"  \
		--pitch "$(PITCH)"

## setup : create virtualenv and install dependencies
setup: $(VENV)/bin/edge_tts

$(VENV)/bin/edge_tts: requirements.txt
	@echo "→ Setting up virtual environment ..."
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip --quiet
	$(PIP) install -r requirements.txt --quiet
	@touch $(VENV)/bin/edge_tts

## clean-audio : remove generated files (keeps the PDF and markdown script)
clean-audio:
	@echo "→ Removing generated files ..."
	rm -f $(CLEAN_TXT) $(OUTPUT_MP3)

## help : show this help
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'
