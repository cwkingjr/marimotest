import marimo

__generated_with = "0.14.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    params = mo.cli_args()
    infile = params["infile"]

    if infile.endswith(".xlsx"):
        df = pd.read_excel(infile)
    elif infile.endswith(".csv"):
        df = pd.read_csv(infile)
    else:
        raise ValueError(
            f"Input processing for file type of {infile} is not implimented yet."
        )

    return df, mo


@app.cell
def _(df):
    df.describe
    return


@app.cell
def _(df):
    print(df.columns)
    return


@app.cell
def _(df, mo):
    mo.ui.table(data=df, max_columns=None)
    return


if __name__ == "__main__":
    app.run()
