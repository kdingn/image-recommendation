# image-recommendation
## requirements
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
