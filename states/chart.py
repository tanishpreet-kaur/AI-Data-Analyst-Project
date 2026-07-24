from typing import Literal, Optional
from pydantic import BaseModel
 
class VisualisationOutput(BaseModel):
    create_chart: bool
    reason: str
    chart_type: Optional[Literal["bar", "horizontal_bar", "line", "pie", "scatter", "histogram"]] = None
    x_column: str = ""
    y_column: str = ""
    title: str = ""
    x_label: str = ""
    y_label: str = ""
