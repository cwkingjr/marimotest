import marimo

__generated_with = "0.14.13"
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

    if infile.endswith(".xlsx"):
        df = pd.read_excel(infile)
    elif infile.endswith(".csv"):
        df = pd.read_csv(infile)
    else:
        raise ValueError(f"Input processing for file type of {infile} is not implimented yet.")
    return df, infile


@app.cell
def _():
    # Instead of trying to restrict the input file to a particular schema, which is a problem because
    # folks can select what fields they want when they generate the input file in another system,
    # here we will just list the fields that are required for processing later in this notebook.
    # So, if you modify this notebook to add functionality, it's on you to ensure your field
    # requirements are included here.

    # Fields/columns used for processing in subsequent cells
    REQUIRED_FIELDS=[
        "AssigneeIdentity",
        "CreateDate",
        "LastUpdatedDate",
        "ResolvedByIdentity",
        "Status",
    ]
    return (REQUIRED_FIELDS,)


@app.cell
def _(REQUIRED_FIELDS, df):
    # make sure we have all required fields before proceeding
    missing_fields = set()

    for required_field in REQUIRED_FIELDS:
        if not required_field in df.columns:
            missing_fields.add(required_field)

    if len(missing_fields):    
        raise ValueError("missing_fields:" + ",".join(missing_fields))
    return


@app.cell
def _(df, pd):
    # clean up the data before we use it

    def rename_df_col_in_place(dataframe, from_name, to_name):
        dataframe.rename(
            columns={
                from_name: to_name.strip(),
            },
            inplace=True,
        )

    all_columns = df.columns

    for one_col in all_columns:
        if "(string)" in one_col:
            no_string = one_col.replace("(string)", "")
            rename_df_col_in_place(df, one_col, no_string)

    # Date column processing
    INPUT_DATE_FORMAT_SEEN_SHORT = "%m/%d/%y %H:%M"  # "12/29/24 14:58"
    INPUT_DATE_FORMAT_SEEN_LONG = "%Y-%m-%dT%H:%M:%S.%fZ"  # "2025-07-18T14:42:21.193Z"

    # if the dataframe doesn't pick up the date columns we need as datatimes, try to 
    # change the date columns from strings to datetimes so we can use the datetime methods on them
    if not str(df.dtypes["CreateDate"]).startswith("datetime"):
        try:
            df["CreateDate"] = pd.to_datetime(df.CreateDate, format=INPUT_DATE_FORMAT_SEEN_LONG)
            df["LastUpdatedDate"] = pd.to_datetime(df.LastUpdatedDate, format=INPUT_DATE_FORMAT_SEEN_LONG)
        except ValueError:
            try:
                df["CreateDate"] = pd.to_datetime(df.CreateDate, format=INPUT_DATE_FORMAT_SEEN_SHORT)
                df["LastUpdatedDate"] = pd.to_datetime(df.LastUpdatedDate, format=INPUT_DATE_FORMAT_SEEN_SHORT)
            except ValueError as e:
                print("ERROR: Could not convert date columns to datetime using configured date formats. Please copy error text and provide to developer.")

    # add derived columns
    df["CreateUpdateDelta"] = df["LastUpdatedDate"] - df["CreateDate"]
    return


@app.cell
def _(date, df, mo, relativedelta):
    # create some ui elements for use in other cells. You can't use these from the same cell you create them in.

    dropdown_assignee_select = mo.ui.dropdown.from_series(
        df["AssigneeIdentity"], label="Filter By AssigneeIdentity"
    )

    dropdown_resolvedby_select = mo.ui.dropdown.from_series(
        df["ResolvedByIdentity"], label="Filter By ResolvedByIdentity"
    )

    radio_data_viewer_choice = mo.ui.radio(
        options=["Table", "Transformer", "Explorer"],
        value="Table",
        label="Choose Data Viewer",
    )

    checkbox_filter_by_created = mo.ui.checkbox(label="Filter By CreateDate")
    checkbox_filter_by_updated = mo.ui.checkbox(label="Filter By LastUpdatedDate")

    # grab current dates to use as default value for start and end date values
    pydate_tomorrow = date.today() + relativedelta(days=1)
    pydate_month_ago = pydate_tomorrow + relativedelta(months=-1)

    date_created_start = mo.ui.date(label="Start CreateDate", value=pydate_month_ago)
    date_created_end = mo.ui.date(label="End CreateDate", value=pydate_tomorrow)

    date_updated_start = mo.ui.date(
        label="Start LastUpdatedDate", value=pydate_month_ago
    )
    date_updated_end = mo.ui.date(label="End LastUpdatedDate", value=pydate_tomorrow)
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
    min_created = min(df["CreateDate"])
    max_created = max(df["CreateDate"])

    min_updated = min(df["LastUpdatedDate"])
    max_updated = max(df["LastUpdatedDate"])
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
                            mo.md(f"Min CreateDate: {min_created}"),
                            mo.md(f"Max CreateDate: {max_created}"),
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
                    df["CreateDate"]
                    >= datetime.combine(date_created_start.value, time.min)
                )
                & (
                    df["CreateDate"]
                    <= datetime.combine(date_created_end.value, time.max)
                )
            ]
        else:
            filtered_df = df
    else:
        if checkbox_filter_by_created.value:
            filtered_df = df[
                (df["AssigneeIdentity"] == dropdown_assignee_select.value)
                & (
                    df["CreateDate"]
                    >= datetime.combine(date_created_start.value, time.min)
                )
                & (
                    df["CreateDate"]
                    <= datetime.combine(date_created_end.value, time.max)
                )
            ]
        else:
            filtered_df = df[df["AssigneeIdentity"] == dropdown_assignee_select.value]
    return (filtered_df,)


@app.cell
def _(filtered_df, mo, radio_data_viewer_choice):
    # Determine how to show the data based upon the built-in marimo views available.
    if radio_data_viewer_choice.value == "Table":
        viewer = mo.ui.table(data=filtered_df, label="Tickets", max_columns=None)
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
            label="AssigneeIdentity Filter",
            value=get_assignee_filter_card_display(),
            bordered=True,
        ),
        mo.stat(
            label="CreateDate Filter",
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
            (df["CreateDate"] >= datetime.combine(date_created_start.value, time.min))
            & (df["CreateDate"] <= datetime.combine(date_created_end.value, time.max))
        ]
        monthly_created_plot_header = mo.md(
            f"###Monthly CreateDate Ticket Count - {date_created_start.value} - {date_created_end.value}"
        )
    else:
        created_df = df
        monthly_created_plot_header = mo.md(f"###Monthly CreateDate Ticket Count - All")
    return created_df, monthly_created_plot_header


@app.cell
def _(created_df, mo, monthly_created_plot_header):
    monthly_created = created_df.groupby(
        created_df["CreateDate"].dt.to_period("M")
    ).size()
    mo.stop(monthly_created.empty)

    monthly_created_plot = monthly_created.plot(
        title="Tickets Created Per Month",
        kind="bar",
        grid=True,
        xlabel="Year-Month",
        ylabel="Count",
    )
    mo.vstack(
        [
            mo.md("~~~~~~~~~~"),
            monthly_created_plot_header,
            mo.hstack([monthly_created_plot, monthly_created], justify="start"),
        ]
    )
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
    mo.vstack(
        [
            mo.md("~~~~~~~~~~"),
            mo.hstack(
                [
                    mo.md("### Monthly Resolved Ticket Count"),
                    mo.md(
                        f"Earliest Available LastUpdatedDate: {min_updated}, Latest Available LastUpdatedDate: {max_updated}"
                    ),
                ]
            ),
            mo.hstack(
                [
                    dropdown_resolvedby_select,
                    checkbox_filter_by_updated,
                    date_updated_start,
                    date_updated_end,
                ]
            ),
        ]
    )
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
                    df["LastUpdatedDate"]
                    >= datetime.combine(date_updated_start.value, time.min)
                )
                & (
                    df["LastUpdatedDate"]
                    <= datetime.combine(date_updated_end.value, time.max)
                )
            ]
        else:
            resolved_df = df
    else:
        if checkbox_filter_by_updated.value:
            resolved_df = df[
                (df["ResolvedByIdentity"] == dropdown_resolvedby_select.value)
                & (
                    df["LastUpdatedDate"]
                    >= datetime.combine(date_updated_start.value, time.min)
                )
                & (
                    df["LastUpdatedDate"]
                    <= datetime.combine(date_updated_end.value, time.max)
                )
            ]
        else:
            resolved_df = df[
                df["ResolvedByIdentity"] == dropdown_resolvedby_select.value
            ]
    return (resolved_df,)


@app.cell
def _(dropdown_resolvedby_select, mo, resolved_df):
    monthly_resolved = resolved_df.groupby(
        resolved_df["LastUpdatedDate"].dt.to_period("M")
    ).size()
    mo.stop(monthly_resolved.empty)
    monthly_resolved
    if dropdown_resolvedby_select.value is None:
        monthly_resolved_plot_title = "Tickets Resolved Per Month (By All)"
    else:
        monthly_resolved_plot_title = (
            f"Tickets Resolved Per Month (By {dropdown_resolvedby_select.value})"
        )
    monthly_resolved_plot = monthly_resolved.plot(
        title=monthly_resolved_plot_title,
        kind="bar",
        grid=True,
        xlabel="Year-Month",
        ylabel="Count",
    )

    mo.hstack([monthly_resolved_plot, monthly_resolved], justify="start")
    return


@app.cell
def _(duckdb, filtered_df, mo):
    # let's try a pivot
    # using this approach so that we can register the update dependency outside
    # of the sql statement so that the ui updates when the dependency changes.
    pivot_query = "pivot tickets on AssigneeIdentity using count(*) group by Status;"
    with duckdb.connect() as conn:
        data = filtered_df
        conn.register("tickets", data)
        result_df = conn.execute(pivot_query).fetch_df()
        pivot_df = result_df.copy()
    mo.vstack(
        [
            mo.md(
                "### Status Counts by AssigneeIdentity Using Filter Options Selections"
            ),
            mo.ui.table(pivot_df),
        ]
    )

    return


if __name__ == "__main__":
    app.run()
