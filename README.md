Note‼️:

1. **The app works only if the main directory contains twitter credentials.**
2. **The environment variable for google cloud credentials should also be set before executing for language translation.**

## Setup

Download `nn_model.h5` from releases on github and place it in the project root.

We recommend that you install dependencies in a seperate environment. Here's how -

#### Create a conda Environment

- Install anaconda and run the following commands

```sh
conda create -n sih python=3.5
conda activate sih
```

- Make sure that you are in the **sih** conda environment throughout the setup process.
- You can validate this by looking at the environment name prefixed to your command prompt **(sih)**.

#### Install the deps

```sh
pip install -r requirements.txt
```

#### Run the app

- In the project root folder, run the following command -

```sh
python index.py
```

#### Getting out of the created conda environment

```sh
conda deactivate
```
