from pydantic import BaseModel
from typing import Any, List, Optional

class PredictionResults(BaseModel):
    image_url: str