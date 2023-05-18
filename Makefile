.DEFAULT_GOAL := main
MAKEFLAGS += --silent

main: 
	python3 gestion_dossier_medical.py
	find . -type d -name '__pycache__' -exec rm -rf {} +

setup:
	gestion_db/./setup_db.sh

init:
	python3 gestion_db/init_db.py
	find . -type d -name '__pycache__' -exec rm -rf {} +

print:
	python3 gestion_db/print_db.py

clean:
	python3 gestion_db/clear_db.py



