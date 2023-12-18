# OptiGuide Streamlit App
This is a demo app for running [OptiGuide](https://github.com/microsoft/OptiGuide) with [Streamlit](https://docs.streamlit.io/). 

## Accessing the Demo
The demo app is currently hosted at https://optiguide-chatbot.streamlit.app/.

## Running Locally
OptiGuide has a requires a number of modules to function, most notably Gurobi, OpenAI and the OptiGuide package. The exact requirements can be found in `requirements.txt`.

To run the app locally, run the following commands:
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Chatbot.py
```

## Repository Structure
This respository is structured as follows:
- `data` contains data required for each model
- `models` contains the source code for each model, to be fed into OptiGuide
- `models/icl_examples` contains in-context training examples for each model
- `pages` contains the streamlit page for each model (naming the folder `pages` is a streamlit requirement for multipage apps)

```
.
├───data
├───models
│   ├───icl_examples
└───pages
```

## Resources
- OptiGuide Paper: https://arxiv.org/abs/2307.03875
- OptiGuide Repository: https://github.com/microsoft/OptiGuide
- Streamlit Documentation: https://docs.streamlit.io/