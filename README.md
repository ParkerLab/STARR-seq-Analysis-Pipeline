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
In order for mka to run correctly, a bit of setup is necessary to encode metadata in the name of the files such that ```mka``` knows how to iterate over the files. To do this, a simple csv must be written that has metadata about the information. Here is an example csv file (make sure read 1 comes first, read 3 comes second):

```
       inputDNA     ,       rep1       ,        rep2       ,  ....
       
      inputDNA.read1.fq.gz   ,   rep1.read1.fq.gz  ,   rep2.read1.fq.gz  , ....

      inputDNA.read3.fq.gz   ,   rep1.read3.fq.gz  ,   rep2.read3.fq.gz  , ....
```

Next, run the command:

```
starr_screname_custom analysis_name /path/to/metadata.csv /path/to/data/directories /path/to/data/destination
```

Provided the right format for the csv, this will create a data directory with files that have symbolic links with ```mka's``` naming conventions to the correct data files. Here are the example contents of the directory:

```
lrwxrwxrwx  1 collinwa parkerlab-users 84 Jan  1 18:05 83213_modSTARRseq_121917___inputDNA___L001___inputDNA.1.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/scp1-STARRseq_inputDNA_120717.read1.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 84 Jan  1 18:05 83213_modSTARRseq_121917___inputDNA___L001___inputDNA.2.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/scp1-STARRseq_inputDNA_120717.read3.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 85 Jan  1 18:05 83213_modSTARRseq_121917___rep1___L001___rep1.1.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/83213_scp1-STARRseq_cDNA_rep_1.read1.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 85 Jan  1 18:05 83213_modSTARRseq_121917___rep1___L001___rep1.2.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/83213_scp1-STARRseq_cDNA_rep_1.read3.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 85 Jan  1 18:05 83213_modSTARRseq_121917___rep2___L001___rep2.1.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/83213_scp1-STARRseq_cDNA_rep_2.read1.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 85 Jan  1 18:10 83213_modSTARRseq_121917___rep2___L001___rep2.2.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/83213_scp1-STARRseq_cDNA_rep_2.read3.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 85 Jan  1 18:05 83213_modSTARRseq_121917___rep3___L001___rep3.1.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/83213_scp1-STARRseq_cDNA_rep_3.read1.fq.gz
lrwxrwxrwx  1 collinwa parkerlab-users 85 Jan  1 18:05 83213_modSTARRseq_121917___rep3___L001___rep3.2.fq.gz -> /home/ykyono/data/83213_modSTARRseq_121917/83213_scp1-STARRseq_cDNA_rep_3.read3.fq.gz
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
