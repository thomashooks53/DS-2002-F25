.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "Starting fetch step: retrieving METAR data..."
	./fetch_metars.sh
	@echo "Fetch complete. Raw JSON data stored in raw_metars/."

analyze: fetch
	@echo "Starting analysis step: processing METAR data..."
	./analyze_data.sh
	@echo "Analysis complete. Results saved in weather_report.csv."
	@echo "Pipeline completed successfully!"

clean:
	@echo "Cleaning up generated files..."
	rm -rf raw_metars weather_report.csv
	@echo "Cleanup complete. Workspace reset."

