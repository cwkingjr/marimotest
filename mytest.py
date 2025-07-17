import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full", app_title="SIM Ticket Explorer")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from datetime import datetime, date, time
    from dateutil.relativedelta import relativedelta
    import altair as alt
    import duckdb
    return date, datetime, duckdb, mo, pd, relativedelta, time


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
            "AssignedFolderLabel": "AssignFoldLab",
            "CreateDate": "Created",
            "LastUpdatedDate": "Updated",
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
    # create some ui elements for use in other cells. You can't use these from the same cell you create them in.

    dropdown_assignee_select = mo.ui.dropdown.from_series(
        df["Assignee"], label="Filter By Assignee"
    )

    dropdown_resolvedby_select = mo.ui.dropdown.from_series(
        df["ResolvedBy"], label="Filter By ResolvedBy"
    )

    radio_data_viewer_choice = mo.ui.radio(
        options=["Table", "Transformer", "Explorer"],
        value="Table",
        label="Choose Data Viewer",
    )

    checkbox_filter_by_created = mo.ui.checkbox(label="Filter By Created Date")
    checkbox_filter_by_updated = mo.ui.checkbox(label="Filter By Updated Date")

    # grab current dates to use as default value for start and end date values
    pydate_tomorrow = date.today() + relativedelta(days=1)
    pydate_month_ago = pydate_tomorrow + relativedelta(months=-1)

    date_created_start = mo.ui.date(label="Start Created", value=pydate_month_ago)
    date_created_end = mo.ui.date(label="End Created", value=pydate_tomorrow)

    date_updated_start = mo.ui.date(label="Start Updated", value=pydate_month_ago)
    date_updated_end = mo.ui.date(label="End Updated", value=pydate_tomorrow)
    return (
        checkbox_filter_by_created,
        checkbox_filter_by_updated,
        date_created_end,
        date_created_start,
        date_updated_end,
        date_updated_start,
        dropdown_assignee_select,
        dropdown_resolvedby_select,
        radio_data_viewer_choice,
    )


@app.cell
def _(df):
    # gather some status info
    min_created = min(df["Created"])
    max_created = max(df["Created"])

    min_updated = min(df["Updated"])
    max_updated = max(df["Updated"])
    return max_created, max_updated, min_created, min_updated


@app.cell
def _(
    checkbox_filter_by_created,
    date_created_end,
    date_created_start,
    dropdown_assignee_select,
    infile,
    max_created,
    min_created,
    mo,
    radio_data_viewer_choice,
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
                    mo.vstack(
                        [
                            mo.md("##Infile Info"),
                            mo.md(f"{infile=}"),
                            mo.md(f"Min Created: {min_created}"),
                            mo.md(f"Max Created: {max_created}"),
                        ]
                    ),
                    mo.vstack(
                        [
                            mo.md("##Filter Options"),
                            checkbox_filter_by_created,
                            date_created_start,
                            date_created_end,
                            dropdown_assignee_select,
                        ]
                    ),
                    mo.vstack(
                        [
                            mo.md("##Data View Options"),
                            radio_data_viewer_choice,
                        ]
                    ),
                ]
            )
        ]
    )
    return


@app.cell
def _(
    checkbox_filter_by_created,
    date_created_end,
    date_created_start,
    datetime,
    df,
    dropdown_assignee_select,
    time,
):
    # If assignee filter in sidebar has assignee selected, filter table
    # data by that assignee, otherwise show all records (--).
    if dropdown_assignee_select.value is None:
        if checkbox_filter_by_created.value:
            filtered_df = df[
                (
                    df["Created"]
                    >= datetime.combine(date_created_start.value, time.min)
                )
                & (
                    df["Created"]
                    <= datetime.combine(date_created_end.value, time.max)
                )
            ]
        else:
            filtered_df = df
    else:
        if checkbox_filter_by_created.value:
            filtered_df = df[
                (df["Assignee"] == dropdown_assignee_select.value)
                & (
                    df["Created"]
                    >= datetime.combine(date_created_start.value, time.min)
                )
                & (
                    df["Created"]
                    <= datetime.combine(date_created_end.value, time.max)
                )
            ]
        else:
            filtered_df = df[df["Assignee"] == dropdown_assignee_select.value]
    return (filtered_df,)


@app.cell
def _(filtered_df, mo, radio_data_viewer_choice):
    # Determine how to show the data based upon the built-in marimo views available.
    if radio_data_viewer_choice.value == "Table":
        viewer = mo.ui.table(filtered_df)
    elif radio_data_viewer_choice.value == "Transformer":
        viewer = mo.ui.dataframe(filtered_df)
    elif radio_data_viewer_choice.value == "Explorer":
        viewer = mo.ui.data_explorer(filtered_df)
    return (viewer,)


@app.cell
def _(
    checkbox_filter_by_created,
    date_created_end,
    date_created_start,
    dropdown_assignee_select,
    filtered_df,
):
    # gather up some data status to show in cards

    num_rows = len(filtered_df)
    num_cols = len(filtered_df.columns)

    def get_created_filter_card_display():
        if checkbox_filter_by_created.value:
            return f"{date_created_start.value} - {date_created_end.value}"
        return "Not Filtering"

    def get_assignee_filter_card_display():
        if dropdown_assignee_select.value is None:
            return "--"
        return dropdown_assignee_select.value
    return (
        get_assignee_filter_card_display,
        get_created_filter_card_display,
        num_cols,
        num_rows,
    )


@app.cell
def _(
    get_assignee_filter_card_display,
    get_created_filter_card_display,
    mo,
    num_cols,
    num_rows,
):
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

    _title = "### Quick Info Cards for Table Viewer"

    mo.vstack(
        [
            mo.md(_title),
            mo.hstack(_cards, widths="equal", align="center"),
        ]
    )
    return


@app.cell
def _(viewer):
    viewer
    return


@app.cell
def _(
    checkbox_filter_by_created,
    date_created_end,
    date_created_start,
    datetime,
    df,
    mo,
    time,
):
    # Not using filtered_df here because it is also filtered by assignee selection
    if checkbox_filter_by_created.value:
        created_df = df[
                (df["Created"] >= datetime.combine(date_created_start.value, time.min))
                & (df["Created"] <= datetime.combine(date_created_end.value, time.max))
            ]
        monthly_created_plot_header = mo.md(f"###Monthly Created Ticket Count - {date_created_start.value} - {date_created_end.value}")
    else:
        created_df = df
        monthly_created_plot_header = mo.md(f"###Monthly Created Ticket Count - All")
    return created_df, monthly_created_plot_header


@app.cell
def _(created_df, mo, monthly_created_plot_header):
    monthly_created = created_df.groupby(created_df["Created"].dt.to_period('M')).size()
    mo.stop(monthly_created.empty)

    monthly_created_plot = monthly_created.plot(title="Tickets Created Per Month", kind="bar", grid=True, xlabel="Year-Month", ylabel="Count")
    mo.vstack(
        [
        mo.md("~~~~~~~~~~"),
        monthly_created_plot_header,
        mo.hstack([monthly_created_plot,monthly_created],justify="start")
        ])
    return


@app.cell
def _(
    checkbox_filter_by_updated,
    date_updated_end,
    date_updated_start,
    dropdown_resolvedby_select,
    max_updated,
    min_updated,
    mo,
):

    mo.vstack([
        mo.md("~~~~~~~~~~"),
        mo.hstack([
            mo.md("### Monthly Resolved Ticket Count"),
            mo.md(f"Earliest Available Updated: {min_updated}, Latest Available Updated: {max_updated}"),
        ]),
        mo.hstack([
            dropdown_resolvedby_select,
            checkbox_filter_by_updated,
            date_updated_start,
            date_updated_end,
        ]),
    ])
    return


@app.cell
def _(
    checkbox_filter_by_updated,
    date_updated_end,
    date_updated_start,
    datetime,
    df,
    dropdown_resolvedby_select,
    time,
):
    # Monthly resolved

    if dropdown_resolvedby_select.value is None:
        if checkbox_filter_by_updated.value:
            resolved_df = df[
                (
                    df["Updated"]
                    >= datetime.combine(date_updated_start.value, time.min)
                )
                & (
                    df["Updated"]
                    <= datetime.combine(date_updated_end.value, time.max)
                )
            ]
        else:
            resolved_df = df
    else:
        if checkbox_filter_by_updated.value:
            resolved_df = df[
                (df["ResolvedBy"] == dropdown_resolvedby_select.value)
                & (
                    df["Updated"]
                    >= datetime.combine(date_updated_start.value, time.min)
                )
                & (
                    df["Updated"]
                    <= datetime.combine(date_updated_end.value, time.max)
                )
            ]
        else:
            resolved_df = df[df["ResolvedBy"] == dropdown_resolvedby_select.value]
    return (resolved_df,)


@app.cell
def _(dropdown_resolvedby_select, mo, resolved_df):
    monthly_resolved = resolved_df.groupby(resolved_df["Updated"].dt.to_period('M')).size()
    mo.stop(monthly_resolved.empty)
    monthly_resolved
    if dropdown_resolvedby_select.value is None:
        monthly_resolved_plot_title = "Tickets Resolved Per Month (All)"
    else:
        monthly_resolved_plot_title = f"Tickets Resolved Per Month ({dropdown_resolvedby_select.value})"
    monthly_resolved_plot = monthly_resolved.plot(title=monthly_resolved_plot_title, kind="bar", grid=True, xlabel="Year-Month", ylabel="Count")

    mo.hstack([monthly_resolved_plot,monthly_resolved],justify="start")
    return


@app.cell
def _(duckdb, filtered_df, mo):
    # let's try a pivot
    # using this approach so that we can register the update dependency outside
    # of the sql statement so that the ui updates when the dependency changes.
    pivot_query = "pivot tickets on split_part(Assignee, '@', 1) using count(*) group by Status;"
    with duckdb.connect() as conn:
        data = filtered_df
        conn.register("tickets", data)
        result_df = conn.execute(pivot_query).fetch_df()
        pivot_df = result_df.copy()
    mo.vstack([
        mo.md("### Status Counts by Assignee Using Filter Options Selections"),
        mo.ui.table(pivot_df)
    ])

    return


if __name__ == "__main__":
    app.run()
