#
# Makefile for Parker Lab analysis run_1890_pipeline_test
#

#
# This analysis was generated with this mka command:
#
# /lab/sw/ve/pl3/bin/mka --analysis-type 'atac-seq' --description 'test' /lab/work/collinwa/scifair_1718/run_1890_pipeline_test /lab/work/collinwa/scifair_1718/data_2/________1___Rep1.1.fastq.gz /lab/work/collinwa/scifair_1718/data_2/________1___Rep1.2.fastq.gz /lab/work/collinwa/scifair_1718/data_2/________2___Rep1.1.fastq.gz /lab/work/collinwa/scifair_1718/data_2/________2___Rep1.2.fastq.gz
#
# run in this directory:
#
# /lab/work/collinwa/scifair_1718
#

ANALYSIS_NAME = run_1890_pipeline_test
DESCRIPTION = test
CONTROL_PATH = /lab/work/collinwa/scifair_1718/run_1890_pipeline_test
ANALYSIS_PATH = /lab/work/collinwa/scifair_1718/run_1890_pipeline_test
DATA_PATH = /lab/work/collinwa/scifair_1718/run_1890_pipeline_test/data
WORK_PATH = /lab/work/collinwa/scifair_1718/run_1890_pipeline_test/work

.PHONY: run cancel clean all_clean clean_data clean_pipeline clean_work github_repo

pipeline: $(ANALYSIS_PATH)/pipeline

work_directory:
	mkdir -p ${WORK_PATH}

$(ANALYSIS_PATH)/pipeline: $(CONTROL_PATH)/commands
	@mkdir -p $(ANALYSIS_PATH) && cd $(ANALYSIS_PATH) && chmod +x $(CONTROL_PATH)/commands && $(CONTROL_PATH)/commands

run: $(ANALYSIS_PATH)/pipeline
	@cd $(WORK_PATH) && drmr -j $(ANALYSIS_NAME) --mail-at-finish --mail-on-error $(ANALYSIS_PATH)/pipeline

cancel: $(CANCEL_SCRIPT)
	@drmrm -j $(ANALYSIS_NAME)

clean:
	@read -p "Enter 'yes' if you really want to delete your pipeline and work directory: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(ANALYSIS_PATH)/pipeline $(WORK_PATH) && echo "All clean." || echo "OK, not deleting anything."

all_clean:
	@read -p "Enter 'yes' if you really want to delete your pipeline, data and work: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(ANALYSIS_PATH)/pipeline $(DATA_PATH) $(WORK_PATH) && echo "All clean." || echo "OK, not deleting anything."

clean_data:
	@read -p "Enter 'yes' if you really want to delete your data staging directory: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(DATA_PATH) && echo "Data staging directory deleted." || echo "OK, not deleting anything."

clean_pipeline:
	@rm -f $(ANALYSIS_PATH)/pipeline && echo "Pipeline script deleted."

clean_work:
	@read -p "Enter 'yes' if you really want to delete your work tree: " ANSWER && test "yesx" = "$${ANSWER}x" && rm -rf $(WORK_PATH) && echo "Work tree deleted." || echo "OK, not deleting anything."

github_repo:
	@hub create -p ParkerLab/$(ANALYSIS_NAME) -d "$(DESCRIPTION)" && git push --set-upstream origin master