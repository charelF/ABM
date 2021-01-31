Aleksander Janczewski, Charel Felten, Mario van Rooij, Mehmet Ege Arkin

# Agent-based modelling

Agent-based model to simulate EU policy, wealth disparities and economic convergence.

Developed to answer the research question: *How can we sustain cooperation and economic convergence in the European Union?*

## Files

### Model

- ```model.py```: contains the model class
- ```agent.py```: contains the agent class
- ```server.py```: contains some code to create a local webserver to run the model

### Other

- ```batcher.py, para.sh, data/*, data_int_on.csv, errorplot.m```: for sensitivity analysis and plots
- ```sobol.ipynb, test.ipynb, out.csv```: jupyter notebooks used to investigate model and create plots for sensitivity analysis
- ```nuts_rg_60M_2013_lvl_2.geojson```: regions dataset
- ```run.py```: file from mesa
- ```LICENSE, README.md, web_interface_screenshot.png```: readme and license
- ```__init__.py```: to make the folder a python module

## Execution

In the ```model``` directory, run the command ```mesa runserver``` or ```python server.py``` to launch the web-interace on localhost. The model can also be ran from a class by initialising it and then manually calling ```model.step()``` to progress it.

## Sensitivity analysis

1. Open 'sobol.ipynb' and choose the number of samples, and replicates to perform the saltelli sampling.
After the 'out.csv' file has been created close the notebook.
2. Head over to your local cluster of choice or personal slurm workload manager and submit para.sh to the job system
3. A file 'data_int_on.csv' will be created which contains the data needed for the sensitivity analysis.
4. Make sure the column names are defined as in e.g. 'data/data_int_off.csv'
5. Reopen the 'sobol.ipynb' and run the remaining cells, which output the sobol indices.

## Web-Interface

![screenshot of the web interface](web_interface_screenshot.png)


## Acknowledgment

The model is an extension of the Schelling example from mesa geo: https://github.com/Corvince/mesa-geo






