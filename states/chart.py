from typing import Optional
from pydantic import BaseModel

class VisualisationOutput(BaseModel):
    create_chart: bool
    reason: str
    chart_type: Optional[str] = None
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    title: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None