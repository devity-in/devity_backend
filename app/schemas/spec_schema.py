from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
import uuid # Import uuid

# --- Base Models ---

class StyleModel(BaseModel):
    backgroundColor: Optional[str] = None # Hex format e.g., #RRGGBB, #AARRGGBB
    textColor: Optional[str] = None # Hex format
    # Pydantic doesn't have a direct union for Object | num, handle parsing elsewhere or simplify
    # For now, expect the object format based on schema update
    padding: Optional[Dict[str, float]] = None # { "top": 8, "bottom": 8, "left": 16, "right": 16 } or {"all": 10}

class ComponentModel(BaseModel):
    id: Optional[str] = None
    type: Literal["Renderer", "Widget"]
    style: Optional[StyleModel] = None

class WidgetModel(ComponentModel):
    type: Literal["Widget"] = "Widget"
    widgetType: str
    attributes: Dict[str, Any] = {}
    onClickActionIds: Optional[List[str]] = None
    onValueChangedActionIds: Optional[List[str]] = None

class RendererModel(ComponentModel):
    type: Literal["Renderer"] = "Renderer"
    rendererType: str
    attributes: Dict[str, Any] = {}
    children: List['AnyComponent'] = []

# --- Widget Models ---

class TextWidgetAttributes(BaseModel):
    text: str
    fontSize: Optional[float] = None
    fontWeight: Optional[str] = None # e.g., "bold", "normal"
    color: Optional[str] = None # Hex format, overrides style.textColor if present
    textAlign: Optional[str] = None
    maxLines: Optional[int] = None

class TextWidget(WidgetModel):
    type: Literal["Widget"] = "Widget"
    widgetType: Literal["Text"] = "Text"
    attributes: TextWidgetAttributes

class ButtonWidgetAttributes(BaseModel):
    text: str
    enabled: bool = True

class ButtonWidget(WidgetModel):
    type: Literal["Widget"] = "Widget"
    widgetType: Literal["Button"] = "Button"
    attributes: ButtonWidgetAttributes
    onClickActionIds: Optional[List[str]] = None

# Define other widget types (TextField, Image) similarly...

AnyWidget = Union[TextWidget, ButtonWidget] # Add other widgets here

# --- Renderer Models ---

class ColumnRendererAttributes(BaseModel):
    # Add alignment, spacing etc. later
    pass

class ColumnRenderer(RendererModel):
    type: Literal["Renderer"] = "Renderer"
    rendererType: Literal["Column"] = "Column"
    attributes: ColumnRendererAttributes = Field(default_factory=ColumnRendererAttributes)
    children: List['AnyComponent'] = []

class RowRendererAttributes(BaseModel):
    # Add alignment, spacing etc. later
    pass

class RowRenderer(RendererModel):
    type: Literal["Renderer"] = "Renderer"
    rendererType: Literal["Row"] = "Row"
    attributes: RowRendererAttributes = Field(default_factory=RowRendererAttributes)
    children: List['AnyComponent'] = []

class PaddingRendererAttributes(BaseModel):
    padding: Dict[str, float] # { "top": 8, ... } or { "all": 10 }

class PaddingRenderer(RendererModel):
    type: Literal["Renderer"] = "Renderer"
    rendererType: Literal["Padding"] = "Padding"
    attributes: PaddingRendererAttributes
    children: List['AnyComponent'] # Spec says exactly one, validation needed

class ScrollableRendererAttributes(BaseModel):
    scrollDirection: Literal["vertical", "horizontal"] = "vertical"

class ScrollableRenderer(RendererModel):
    type: Literal["Renderer"] = "Renderer"
    rendererType: Literal["Scrollable"] = "Scrollable"
    attributes: ScrollableRendererAttributes = Field(default_factory=ScrollableRendererAttributes)
    children: List['AnyComponent'] # Spec says exactly one, validation needed

# Define Stack etc. similarly...

AnyRenderer = Union[ColumnRenderer, RowRenderer, PaddingRenderer, ScrollableRenderer] # Add other renderers
AnyComponent = Union[AnyRenderer, AnyWidget]

# Update forward references
ColumnRenderer.model_rebuild()
RowRenderer.model_rebuild()
PaddingRenderer.model_rebuild()
ScrollableRenderer.model_rebuild()

# --- Screen Model ---

class ScreenModel(BaseModel):
    id: str
    type: Literal["Screen"] = "Screen"
    backgroundColor: Optional[str] = None # Hex format
    # appBar: Optional[AnyComponent] = None # Allow Widget or Renderer?
    body: AnyComponent # Root component for the screen body
    # bottomNavBar: Optional[AnyComponent] = None
    onLoadActions: Optional[List[str]] = None
    persistentData: Optional[Dict[str, Any]] = None

# --- Action Model (Basic Stub) ---

class ActionModel(BaseModel):
    id: str
    type: Literal["Action"] = "Action"
    actionType: str # e.g., "Navigate", "ApiCall"
    attributes: Dict[str, Any] = {}

# --- Rule Model (Basic Stub) ---

class RuleModel(BaseModel):
    id: str
    type: Literal["Rule"] = "Rule"
    # Define trigger, condition, actionIds later
    trigger: Dict[str, Any] = {}
    condition: Dict[str, Any] = {}
    actionIds: List[str] = []

# --- Top-Level Spec Model ---

class Spec(BaseModel):
    project_id: uuid.UUID # Added project ID
    specVersion: str = "1.0.0"
    specId: str
    version: int
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    entryPoint: str
    globalData: Optional[Dict[str, Any]] = None
    screens: Dict[str, ScreenModel]
    actions: Optional[Dict[str, ActionModel]] = None
    rules: Optional[Dict[str, RuleModel]] = None
