from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Literal


class DoorWindow(BaseModel):
    wall: Literal["north", "south", "east", "west"]
    position: float = Field(..., description="Distance in ft from the wall's starting corner")
    width: float = Field(default=3.0, description="Width of the opening in ft")


class RoomInput(BaseModel):
    # Raw user input, as described in Section 1: INPUT CAPTURE
    length: float = Field(..., gt=0, description="Room length in ft")
    width: float = Field(..., gt=0, description="Room width in ft")
    doors: List[DoorWindow] = Field(default_factory=list)
    windows: List[DoorWindow] = Field(default_factory=list)
    style: Literal["luxury", "standard", "budget"] = "standard"
    budget: int = Field(..., ge=0, description="Budget in NPR")
    required_furniture: List[str] = Field(
        default_factory=list,
        description="e.g. ['single_bed', 'wardrobe', 'medium_table','plastic_chair']",
    )

    @model_validator(mode="after")
    def _width_not_greater_than_length(self):
        if self.width > self.length:
            raise ValueError(
                f"Room width ({self.width:g}ft) cannot be greater than room length "
                f"({self.length:g}ft). Width may equal length."
            )
        return self


class FurniturePlacement(BaseModel):
    name: str
    x: float
    y: float
    w: float
    h: float
    rotation: float = 0.0  # degrees


class LayoutResult(BaseModel):
    layout_id: int
    name: str
    style: str
    furniture: List[FurniturePlacement]
    wall_color: str
    accent_color: str
    match_score: float
    warnings: List[str] = Field(default_factory=list)
    estimated_cost: Optional[int] = None


class ModifyRequest(BaseModel):
    style: Optional[str] = None
    budget: Optional[int] = None
    required_furniture: Optional[List[str]] = None
    notes: Optional[str] = None


class SessionState(BaseModel):
    session_id: str
    stage: str  
    room_input: RoomInput
    current_layout: Optional[LayoutResult] = None
    floorplan_path: Optional[str] = None
    render_prompt: Optional[str] = None
    render_path: Optional[str] = None

