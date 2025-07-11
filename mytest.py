import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full", app_title="SIM Ticket Explorer")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(mo, pd):
    # load the data file
    params = mo.cli_args()
    infile = params["infile"]
    df = pd.read_csv(infile)
    return df, infile


@app.cell
def _():
    # TODO confirm that the infile has the correct schema or notify user of what is expected and quit processing

    # TODO determine if we will accept either csv or xlsx and if they will have the same schemas
    return


@app.cell
def _(df, pd):
    # clean up the data before we use it

    # rename the columns to make them easier to see in tables and graphs
    df.rename(
        columns={
            "tpa_from (string)": "tpa_from",
            "AssigneeIdentity": "Assignee",
            "RequesterIdentity": "Requester",
            "SubmitterIdentity": "Submitter",
            "ResolvedByIdentity": "ResolvedBy",
            "AssignedFolderLabel":"AssignFoldLab",
            "CreateDate":"Created",
            "LastUpdatedDate":"LastUpdated"
        },
        inplace=True,
    )

    # change the date columns from strings to datetimes so we can use the datetime methods on them
    df["Created"] = pd.to_datetime(df.Created, format="%m/%d/%y %H:%M")
    df["LastUpdated"] = pd.to_datetime(df.LastUpdated, format="%m/%d/%y %H:%M")
    return


@app.cell
def _(infile, mo):
    mo.sidebar(
        [
            mo.md("##Explorer Info"),
            mo.md(f"infile:{infile}")
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""#Dataframe View of Cleaned Up Data""")
    return


@app.cell
def _(df):
    # show the dataframe in a rich table
    df
    return


@app.cell
def _(mo):
    mo.md(r"""#Data By Assignee""")
    return


@app.cell
def _(df, mo):
    assignee_select = mo.ui.dropdown.from_series(
        df["Assignee"], label="Assignee"
    )
    mo.hstack([mo.md("Filter Dataframe By:"),assignee_select,mo.md("Note: You can actually filter any/all columns in the dataframe view above by clicking on the column header and choosing filter. This is just here to make it quicker.")],justify="start")
    return (assignee_select,)


@app.cell
def _(assignee_select, df, mo):
    filtered_df = df[df["Assignee"] == assignee_select.value]
    mo.ui.table(filtered_df)
    return


@app.cell
def _(mo):
    mo.md(r"""#Transform View of Datafame""")
    return


@app.cell
def _(df, mo):
    transformed_df = mo.ui.dataframe(df)
    transformed_df
    return


@app.cell
def _(mo):
    mo.md(r"""#Explorer View of Datafame""")
    return


@app.cell
def _(df, mo):
    explored_df = mo.ui.data_explorer(df)
    explored_df
    return


if __name__ == "__main__":
    app.run()
