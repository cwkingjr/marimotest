import marimo

__generated_with = "0.14.12"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    df = pd.read_csv("fake-data-3000-rows.csv")
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
