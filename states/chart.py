from typing import Optional
from pydantic import BaseModel

class VisualisationOutput(BaseModel):
    create_chart: bool
    reason: str
    chart_type: str = ""
    x_column: str = ""
    y_column: str = ""
    title: str = ""
    x_label: str = ""
    y_label: str = ""