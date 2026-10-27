from html import escape

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


def grouped_vehicle_table(df):
    """
    Aggregate selling prices by manufacturer, transmission, body type,
    and fuel type. Repeated hierarchy labels are merged with HTML rowspan.
    """
    grouping_columns = [
        "manufacturer",
        "transmission",
        "body_type",
        "fuel_type",
    ]

    grouped_df = df.copy()
    grouped_df["selling_price"] = pd.to_numeric(
        grouped_df["selling_price"], errors="coerce"
    )

    grouped_df = (
        grouped_df.groupby(
            grouping_columns,
            as_index=False,
            dropna=False
        )["selling_price"]
        .sum()
        .sort_values(grouping_columns, kind="stable", na_position="last")
        .reset_index(drop=True)
    )

    display_names = {
        "manufacturer": "Manufacturer",
        "transmission": "Transmission",
        "body_type": "Body Type",
        "fuel_type": "Fuel Type",
        "selling_price": "Total Selling Price",
    }

    table_html = """
    <table class="table table-bordered table-striped table-sm">
      <thead>
        <tr>
          <th>Manufacturer</th>
          <th>Transmission</th>
          <th>Body Type</th>
          <th>Fuel Type</th>
          <th>Total Selling Price</th>
        </tr>
      </thead>
      <tbody>
    """

    def display_value(value):
        return "Unknown" if pd.isna(value) else escape(str(value))

    # Merge repeated values at each hierarchy level using rowspan.
    for row_index, row in grouped_df.iterrows():
        table_html += "<tr>"

        for level, column in enumerate(grouping_columns):
            current_value = row[column]
            prefix = grouping_columns[: level + 1]

            previous_prefix_matches = (
                row_index > 0
                and all(
                    (
                        pd.isna(grouped_df.iloc[row_index - 1][key])
                        and pd.isna(row[key])
                    )
                    or grouped_df.iloc[row_index - 1][key] == row[key]
                    for key in prefix
                )
            )

            if previous_prefix_matches:
                continue

            same_prefix = grouped_df[prefix].apply(
                lambda candidate: all(
                    (
                        pd.isna(candidate[key])
                        and pd.isna(row[key])
                    )
                    or candidate[key] == row[key]
                    for key in prefix
                ),
                axis=1,
            )
            rowspan = int(same_prefix.sum())

            table_html += (
                f'<td rowspan="{rowspan}">'
                f'{display_value(current_value)}</td>'
            )

        total = row["selling_price"]
        formatted_total = "" if pd.isna(total) else f"{total:,.2f}"
        table_html += f"<td>{formatted_total}</td></tr>"

    table_html += """
      </tbody>
    </table>
    """
    return table_html
