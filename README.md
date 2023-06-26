# Image-Recommendation

This is AI application for image recommendation based on [EfficientNet-B7](https://arxiv.org/abs/1905.11946) / [Vision Transformer](https://arxiv.org/abs/2010.11929).

## How to use
1. Prepare train/test datasets for image recommendation as required below.
2. Create AI model for the recommendation.
    1. Run all notebooks in src directory.
3. Start streamlit application.

## Required datasets
- images : {id}.png or {id}.jpg

- label_tran.csv : label for images
    | id | like | update |
    |---|---|---|
    | 0000 | 1 | 20220909...|
    | 0010 | 0 | 20220909...|
    | 0204 | 0 | 20220909...|
    | ... | ... | ...|

- exclude.csv : exclude label
    | id |
    |---|
    | 9587 |
    | 1452 |
    | 7628 |
    | ... |

- redundant.csv : label for not training
    | id |
    |---|
    | 2754 |
    | 1752 |
    | 8635 |
    | ... |
