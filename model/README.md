# Instructions sensitivity analysis

1. Open 'sobol.ipynb' and choose the number of samples, and replicates to perform the saltelli sampling.
After the 'out.csv' file has been created close the notebook.
2. Head over to your local cluster of choice or personal slurm workload manager and submit para.sh to the job system
3. A file 'data_int_on.csv' will be created which contains the data needed for the sensitivity analysis.
4. Make sure the column names are defined as in e.g. 'data/data_int_off.csv'
5. Reopen the 'sobol.ipynb' and run the remaining cells, which output the sobol indices.
