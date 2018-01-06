# STARR-seq Analysis Pipeline
This project contains a STARR-seq analysis pipeline based on the tool ```mka```, ```starcode```, and ```drmr```. In addition to a template file for ```mka```, the project contains the ```starrseq``` module that must be loaded that contains helper scripts for running the pipeline. 

# Getting Started
In order to run the pipeline if you're on the lab server, you must load the ```starrseq``` and ```starcode``` modules, while also either sourcing ```/lab/sw/bin/pl``` or preceding the mka command with ```MKA_TEMPLATES = /lab/sw/lib/mka/templates```. The reason for the extra steps is that in its current state, the pipeline is not very general and thus the files reside in the lab's directory for custom templates. Regardless, the necessary imports can all be handled automatically by adding the following to your ```.bashrc``` and restarting the shell:
```
loadmodule starrcode
loadmodule starrseq 
. /lab/sw/bin/pl
```

# Renaming the input files
The sequencing core should povide metadata in the form of a .csv file alongside the fastq files. To ensure that the fastq files containing the input DNA are correctly labeled and handled by the pipeline, the description for each of the input DNA files within the .csv should contain the word "input". Once this condition is met, run the command 
```
starr_screname /path/to/metadata.csv /path/to/sample/directories /path/to/data/destination
```

# Generating the pipeline
Once the files are renamed, mka is ready to be run. When running mka, make sure that only the fastq files containing cDNA and DNA are specified, and not sub-assemblies. The pipeline is currently equipped to create count tables for exactly 3 replicates, though it will be updated to handle more or less than 3 replicates soon. If you need more than 3 replicates, you can run the counts in batches of 3. If you need less than 3 replicates, you can put in the same library twice, and simply remove the extra column from the count table once finished. To set up the pipeline, do the following: 
```
mka --analysis-type  starr-seq --description 'Random STARR-seq pipeline' -a /path/to/analysis /path/to/control /path/to/dna_cdna/fq_files/*
```

# Making and running the pipeline
Once the commands file is generated, switch to the commands directory and run the command, then specify the reference genome as hg19. Set IONICE to the maximum number of commands that you wish to have running concurrently (probably ok to leave at 0):
```
make pipeline
```
Finally, go to the analysis directory and run the command:
```
drmr pipeline
```
and the job scheduler will handle the tasks associated with the pipeline. 

# Finding Results
The final counts table can be found in 
```
/path/to/analysis/work/final_counts_table.txt.gz
```
