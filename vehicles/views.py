import pandas as pd
from pathlib import Path
from django.shortcuts import render
from .dashboard import frequency_table

BASE_DIR = Path(__file__).resolve().parent.parent


def dashboard_view(request):
    queryset = pd.read_csv(BASE_DIR / "dummy_data" / "vehicles_ml_dataset.csv")
    df = pd.DataFrame(queryset)
    return render(request, "vehicles/index.html", {
        "frequency_table": frequency_table(df)
    })
