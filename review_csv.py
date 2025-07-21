import marimo

__generated_with = "0.14.12"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    params = mo.cli_args()
    infile = params["infile"]
    df = pd.read_csv(infile)
    return (df,)


@app.cell
def _(df):
    df.describe
    return


@app.cell
def _(df):
    print(df.columns)
    return


@app.cell
def _(df):
    df
    return


if __name__ == "__main__":
    app.run()
