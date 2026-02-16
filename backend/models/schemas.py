from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SectionOutput(BaseModel):
    """Schema for a single research section."""
    content: str = Field(description="The executive research text for this section.")
    citations: List[dict] = Field(default_factory=list, description="List of normalized source dictionaries.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0.")

class ResearchState(BaseModel):
    """The global state of the research workflow."""
    target_company: str
    annual_report: Optional[str] = ""
    # Store all sections in a single dictionary for easy iteration
    sections: Dict[str, SectionOutput] = {}
    final_output: str = ""
