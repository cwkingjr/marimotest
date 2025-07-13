import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full", app_title="SIM Ticket Explorer")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from datetime import datetime,date,time
    from dateutil.relativedelta import relativedelta
    return date, datetime, mo, pd, relativedelta, time


@app.cell
def _(mo, pd):
    # load the data file
    params = mo.cli_args()
    infile = params["infile"]
    df = pd.read_csv(infile)

    # TODO confirm that the infile has the correct schema or notify user of what is expected and quit processing
    # https://pandera.readthedocs.io/en/stable/dataframe_schemas.html

    # TODO determine if we will accept either csv or xlsx and if they will have the same schemas
    # assuming it would be fine to allow either so alternate fieldset can be consumed

    return df, infile


@app.cell
def _():
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

    # add derived columns
    df["CreatedUpdatedDelta"] = df["Updated"] - df["Created"]
    return


@app.cell
def _(date, df, mo, relativedelta):
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

    # create checkbox to determine if created dates will be filtered
    filter_by_created = mo.ui.checkbox(label="Filter By Created Date")

    # determine start and end selections
    tomorrow = date.today() + relativedelta(days=1)
    month_ago = tomorrow + relativedelta(months=-1)

    # create date vars
    filter_create_start_date = mo.ui.date(label="Start Created",value=month_ago)
    filter_create_end_date = mo.ui.date(label="End Created", value=tomorrow)
    return (
        assignee_select,
        filter_by_created,
        filter_create_end_date,
        filter_create_start_date,
        radiogroup,
    )


@app.cell
def _(df):
    # gather some status info
    min_created = min(df["Created"])
    max_created = max(df["Created"])
    return max_created, min_created


@app.cell
def _(
    assignee_select,
    filter_by_created,
    filter_create_end_date,
    filter_create_start_date,
    infile,
    max_created,
    min_created,
    mo,
    radiogroup,
):
    # create the sidebar view to show info that can be collapsed
    # out of the way to make more screen real estate for the tables
    mo.sidebar(
        [
            mo.vstack(
            [
                mo.vstack(
                    [mo.md("#Analysis Info")],
                ),
                mo.vstack([    
                    mo.md("##Infile Info"),
                    mo.md(f"{infile=}"),
                    mo.md(f"Min Created: {min_created}"),
                    mo.md(f"Max Created: {max_created}"),
                ]),
                mo.vstack([
                    mo.md("##Filter Options"),
                    filter_by_created,
                    filter_create_start_date,
                    filter_create_end_date,
                    assignee_select,
                ]),
                mo.vstack([
                    mo.md("##Data View Options"),
                    radiogroup,
                ])
            ])
        ]
    )
    return


@app.cell
def _(
    assignee_select,
    datetime,
    df,
    filter_by_created,
    filter_create_end_date,
    filter_create_start_date,
    time,
):
    # If assignee filter in sidebar has assignee selected, filter table
    # data by that assignee, otherwise show all records (--).
    if assignee_select.value is None:
        if filter_by_created.value:
            filtered_df = df[
                (df["Created"] >= datetime.combine(filter_create_start_date.value,time.min))
                & (df["Created"] <= datetime.combine(filter_create_end_date.value,time.max))
                ]
        else:
            filtered_df = df
    else:
        if filter_by_created.value:
            filtered_df = df[
                (df["Assignee"] == assignee_select.value)
                & (df["Created"] >= datetime.combine(filter_create_start_date.value,time.min))
                & (df["Created"] <= datetime.combine(filter_create_end_date.value,time.max))
                ]
        else:
            filtered_df = df[df["Assignee"] == assignee_select.value]

    return (filtered_df,)


@app.cell
def _(filtered_df, mo, radiogroup):
    # Determine how to show the data based upon the built-in marimo views available.
    if radiogroup.value == "Table":
        showme = filtered_df
    elif radiogroup.value == "Transformer":
        showme = mo.ui.dataframe(filtered_df)
    elif radiogroup.value == "Explorer":
        showme = mo.ui.data_explorer(filtered_df)
    else:
        print("Unknown viewer selection error")
    return (showme,)


@app.cell
def _(
    assignee_select,
    filter_by_created,
    filter_create_end_date,
    filter_create_start_date,
    pd,
    showme,
):
    # gather up some data status to show in cards

    # the transformer and explorer raise errors so restricting to dataframe for now
    if type(showme) is pd.DataFrame:
        num_rows = len(showme)
        num_cols = len(showme.columns)
        show_cards = True
    else:
        show_cards = False

    def get_created_filter_card_display():
        if filter_by_created.value:
            return f"{filter_create_start_date.value} - {filter_create_end_date.value}"
        else:
            return "Not Filtering"

    def get_assignee_filter_card_display():
        if assignee_select.value is None:
            return "--"
        else:
            return assignee_select.value
    return (
        get_assignee_filter_card_display,
        get_created_filter_card_display,
        num_cols,
        num_rows,
        show_cards,
    )


@app.cell
def _(
    get_assignee_filter_card_display,
    get_created_filter_card_display,
    mo,
    num_cols,
    num_rows,
    show_cards,
):
    mo.stop(show_cards == False)

    _cards = [
        mo.stat(
            label="Rows",
            value=num_rows,
            bordered=True,
        ),
        mo.stat(
            label="Cols",
            value=num_cols,
            bordered=True,
        ),
        mo.stat(
            label="Assignee Filter",
            value=get_assignee_filter_card_display(),
            bordered=True,
        ),
        mo.stat(
            label="Created Filter",
            value=get_created_filter_card_display(),
            bordered=True,
        ),
    ]

    _title = f"### Quick Info Cards"

    mo.vstack(
        [
            mo.md(_title),
            mo.hstack(_cards, widths="equal", align="center"),
        ]
    )
    return


@app.cell
def _(showme):
    showme
    return


if __name__ == "__main__":
    app.run()
