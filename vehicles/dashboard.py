
import pandas as pd


def frequency_table(df):
    # First table: all vehicles
    manufacturer_counts = df["manufacturer"].value_counts().reset_index()
    manufacturer_counts.columns = ["Manufacturer", "Count"]

    return manufacturer_counts.to_html(
        index=False,
        classes="table table-bordered table-striped table-sm",
        justify="center"
    )

def frequency_table_filtered(df):
    # Display actual vehicle records priced above 5000
    filtered_df = df[
        pd.to_numeric(df["selling_price"], errors="coerce") > 5000
    ]

    return filtered_df.to_html(
        index=False,
        classes="table table-bordered table-striped table-sm",
        justify="center",
        max_rows=None
    )



def manufacturer_transmission_sales(df):
    df = df.copy()

    df["selling_price"] = pd.to_numeric(
        df["selling_price"], errors="coerce"
    )

    # Group by manufacturer and transmission
    grouped_df = (
        df.groupby(
            ["manufacturer", "transmission"],
            as_index=False,
            dropna=False
        )["selling_price"]
        .sum()
        .sort_values(
            ["manufacturer", "transmission"],
            kind="stable"
        )
    )

    grouped_df.columns = [
        "Manufacturer",
        "Transmission",
        "Total Selling Price"
    ]

    table_html = """
    <table class="table table-bordered table-striped table-sm">
        <thead>
            <tr>
                <th>Manufacturer</th>
                <th>Transmission</th>
                <th>Total Selling Price</th>
            </tr>
        </thead>
        <tbody>
    """

    # Merge manufacturer cells across their transmission rows
    for manufacturer, group in grouped_df.groupby(
        "Manufacturer", sort=False, dropna=False
    ):
        for index, (_, row) in enumerate(group.iterrows()):
            table_html += "<tr>"

            if index == 0:
                name = escape(str(manufacturer))
                table_html += (
                    f'<td rowspan="{len(group)}">{name}</td>'
                )

            transmission = escape(str(row["Transmission"]))
            total = f'{row["Total Selling Price"]:,.2f}'

            table_html += f"<td>{transmission}</td>"
            table_html += f"<td>{total}</td>"
            table_html += "</tr>"

    table_html += "</tbody></table>"

    return table_html



