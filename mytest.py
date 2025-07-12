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
            "LastUpdatedDate":"Updated"
        },
        inplace=True,
    )

    # change the date columns from strings to datetimes so we can use the datetime methods on them
    df["Created"] = pd.to_datetime(df.Created, format="%m/%d/%y %H:%M")
    df["Updated"] = pd.to_datetime(df.Updated, format="%m/%d/%y %H:%M")
    return


@app.cell
def _(df, mo):
    # create some sidebar selection ui controls

    # create a dropdown of assignees included in the infile to allow the dataframe
    # to be filtered by any one of the assignees.
    assignee_select = mo.ui.dropdown.from_series(
        df["Assignee"], label="Filter By Assignee"
    )

    # create radio group of viewer options
    radiogroup = mo.ui.radio(
        options=["Table", "Transformer", "Explorer"], value="Table", label="Choose Data Viewer"
    )
    return assignee_select, radiogroup


@app.cell
def _(assignee_select, infile, mo, radiogroup):
    # create the sidebar view to show info that can be collapsed
    # out of the way to make more screen real estate for the tables
    mo.sidebar(
        [
            mo.vstack(
            [
                mo.md("##Explorer Info"),
                mo.md("~~~~~"),
                mo.md(f"infile {infile}"),
                mo.md("~~~~~"),
                assignee_select,
                mo.md("~~~~~"),
                radiogroup,
            ])
        ]
    )
    return


@app.cell
def _(assignee_select, df):
    # If assignee filter in sidebar has assignee selected, filter table
    # data by that assignee, otherwise show all records (--).
    if assignee_select.value is None:
        filtered_df = df
    else:
        filtered_df = df[df["Assignee"] == assignee_select.value]
    return (filtered_df,)


@app.cell
def _(filtered_df, mo, radiogroup):
    # Determine how to show the data based upon the built-in marimo views available.
    if radiogroup.value == "Table":
        showme = mo.ui.table(filtered_df)
    elif radiogroup.value == "Transformer":
        showme = mo.ui.dataframe(filtered_df)
    elif radiogroup.value == "Explorer":
        showme = mo.ui.data_explorer(filtered_df)
    else:
        print("Unknown viewer selection error")
    return (showme,)


@app.cell
def _(showme):
    showme
    return


if __name__ == "__main__":
    app.run()
