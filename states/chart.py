from typing import Literal, Optional
from pydantic import BaseModel

class ChartSpec(BaseModel):
    create_chart: bool
    chart_type: Optional[Literal["bar", "line", "pie", "scatter"]] = None
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    title: Optional[str] = None
    reason: Optional[str] = None