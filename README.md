# Prerequisites

## Manual installations

#### Python

[https://www.python.org/downloads/]()

#### Conda

[https://www.anaconda.com/distribution/]()

## External libraries

External libraries in this project are managed with conda.

Run

```bash
conda env create -f environment.yml
```

Refer to the documentation if needed:

[https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file]()

You might have to set your IDE project settings to the new conda environment.

# Setup

Run

```bash
jupyter notebook
```
and open (and/or run) the notebook 'setup.ipynb'.

# Using the service

The service uses FastAPI to provide an API.

Run

```bash
uvicorn main:app --reload
```

Afterwards, you can make an API call on localhost, i.e. using Postman:

[https://www.postman.com/downloads/]()


GET  /categorization ["Text1", "Text2", "Text3"] returns a list of keyword lists for each text.

Beware that the very first API call may take a little longer to process due to some initializations happening in the background. Calls made after the initial call should be considerably faster.
