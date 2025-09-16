all: process_data

fetch_data:
	@echo "--- Fetching data ---"
	bash ./fetch_data.sh

process_data: fetch_data
	@echo "--- Processing data ---"
	bash ./process_data.sh
	@echo "--- Pipeline complete ---"

clean:
	@echo "--- Cleaning up ---"
	rm -f breeds.json
