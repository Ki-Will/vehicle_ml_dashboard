
import pandas as pd
from pathlib import Path
from django.shortcuts import render

from .dashboard import frequency_table, frequency_table_filtered , manufacturer_transmission_sales, grouped_vehicle_table

BASE_DIR = Path(__file__).resolve().parent.parent


def dashboard_view(request):
    csv_path = BASE_DIR / "dummy_data" / "vehicles_ml_dataset.csv"
    df = pd.read_csv(csv_path)

    return render(request, "vehicles/index.html", {
        "frequency_table": frequency_table(df),
        "frequency_table_filtered": frequency_table_filtered(df),
        "manufacturer_transmission_sales": manufacturer_transmission_sales(df),
        "grouped_vehicle_table": grouped_vehicle_table(df),
    })
