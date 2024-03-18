import math
from typing import Optional,  Union

from rich import print
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from wcwidth import wcswidth

StyleType = Union[str, "Style"]

class CenterAlignedPanel(Panel):
    def __init__(self, 
                 renderable: str, 
                 title: str = "",
                 style: StyleType = "none", 
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
        ) -> None:
        super().__init__(
            renderable, 
            title=title, 
            title_align="center",  
            style=style, 
            width=width, 
            height=height
        )
        self.renderableLength = wcswidth(renderable)
        if self.width is None:
            self.width = self.renderableLength + 2
        if self.height is None:
            self.height = 1 + 2
        self.resize()

    def resize(self, width:int = None, height:int = None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
            
        paddingLeft = int((self.width - self.renderableLength - 2 )/2)
        if paddingLeft < 0:
            paddingLeft = 0
        line = math.ceil(self.renderableLength / (self.width -2))
        paddingTop = int((self.height - 2 - line)/2)
        if paddingTop < 0: 
            paddingTop = 0
        self.padding = (paddingTop,0,0,paddingLeft)
    

if __name__ == "__main__":
    a = CenterAlignedPanel("aa",width=10,height=5)
    print(a)