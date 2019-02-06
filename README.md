# Analysis Tools for State-Sponsored Trolls on Twitter 

This repository contain the source code for reproducing the results from the paper "Who Let The Trolls Out? Towards Understanding State-Sponsored troll accounts on Twitter" (see https://arxiv.org/abs/1811.03130 for detailed description on the results).

## Prerequisites

##### Packages
The code relies on the following Python packages:
```
Pandas (https://github.com/pandas-dev/pandas)
Numpy (https://github.com/numpy/numpy)
Matplotlib (https://github.com/matplotlib/matplotlib)
tldextract (https://github.com/john-kurkowski/tldextract)
Gensim (https://github.com/RaRe-Technologies/gensim)
Networkx (https://github.com/networkx/networkx)
twitter-text-python (https://github.com/edmondburnett/twitter-text-python)
pigeo (https://github.com/afshinrahimi/pigeo)
NLTK (https://github.com/nltk/nltk)
stop-words (https://pypi.org/project/stop-words/)
```

##### Other requirements

```
sudo apt-get install libgeos-3.5.0
sudo apt-get install libgeos-dev
sudo pip install https://github.com/matplotlib/basemap/archive/master.zip
```

##### Data
Our data is publicly available at https://zenodo.org/record/2558433. 
The dataset consists of the data released by Twitter on October 2018 for Russian and Iranian state-sponsored troll accounts, which is available at https://about.twitter.com/en_us/values/elections-integrity.html#data as well as intermediate data that we generated after processing the raw data.
For instance, we include trained Word2Vec and LDA models, the output of our influence estimation experiments via Hawkes Processes, and a lot of other data necessary to reproduce the results in the paper.
To use the provided data simply download the compressed file from https://zenodo.org/record/2558433 and make sure that the uncompressed `data` folder is in the same directory as the IPython Notebook.


## Reproducing the results
The plots and tables in the paper can be reproduced using the provided IPython Notebook. The notebook contains the code and the resulting Figures and Tables. Also, it refers to some scripts that need to be run outside the notebook (e.g., `location_share/plot_locations.py`).


## Reference
If you use or find this source code or dataset useful please cite the following work:

    @article{zannettou2018let,
      title={{Who Let The Trolls Out? Towards Understanding State-Sponsored Trolls}},
      author={Zannettou, Savvas and Caulfield, Tristan and Setzer, William and Sirivianos, Michael and Stringhini, Gianluca and Blackburn, Jeremy},
      journal={arXiv preprint arXiv:1811.03130},
      year={2018}
    }


## Acknowledgments

* This project has received funding from the European Union’s Horizon 2020 Research and Innovation program under the Marie Skłodowska-Curie ENCASE project (Grant Agreement No. 691025).

