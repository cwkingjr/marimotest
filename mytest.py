import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full", app_title="SIM Ticket Explorer")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    df = pd.read_csv("fake-data-3000-rows.csv")
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
    df["Created"] = pd.to_datetime(df.Created, format="%m/%d/%y %H:%M")
    df["LastUpdated"] = pd.to_datetime(df.LastUpdated, format="%m/%d/%y %H:%M")
    df
    return


if __name__ == "__main__":
    app.run()
