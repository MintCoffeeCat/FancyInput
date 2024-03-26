import math,warnings
from typing import Optional,  Union

from rich import print
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from wcwidth import wcswidth


"""A Brief Panel that the string content in it is always centered

A Panel for displaying a signle line text on your terminal. The text will always
centerd in the panel.

Attributes:
    renderableLength:   The width of actuall text
    width:              The width of whole Panel. Can be modified by spand behavior
    height:             The height of whole Panel
    minimumPadding:     The minimum padding of Panel. The detail form of this attribute are listed as:
                        (HorizonPadding, VerticalPadding)
    expand:             Configure if the panel width should fit the text length + padding. If this attribute are set to False,
                        The Panel width may be smaller than text width.
    completeCenter      Configure if panel width should added by 1 when the padding space can not divided into two equal parts.

"""
class CenterAlignedPanel(Panel):
    MIN_PADDING = (2,0)
    
    
    def __init__(self, 
                 renderable: str, 
                 title: str = "",
                 style: Union[str, "Style"] = "none", 
                 width: Optional[int] = None, 
                 height: Optional[int] = None, 
                 expand: bool = True,
                 completeCenter: bool = True
        ) -> None:
        super().__init__(
            renderable, 
            title=title, 
            title_align="center",  
            style=style, 
            width=width, 
            height=height
        )
        self.expand = expand
        self.completeCenter = completeCenter
        self.renderableLength = wcswidth(renderable)
        self._init_size(width, height)


    def _init_size(self,width,height):
        if width is None:
            width = self.minimumWidth
        if height is None:
            height = self.minimumHeight
            
        self.resize(width, height)
        
    def resize(self, width:int = None, height:int = None):
        if width is not None:
            if not self.expand and width < self.minimumWidth:
                warnings.warn(f"The panel width you set is not enough contain text and padding. The text may displayed incomplete and padding incorrect.")
                self.width = width
            else: 
                if width < self.minimumWidth:
                    width = self.minimumWidth
                elif self.completeCenter: 
                    # complete center
                    space = width - self.renderableLength - 2
                    width += space % 2
            self.width = width                
        if height is not None:
            if not self.expand and width < self.minimumHeight:
                warnings.warn(f"The panel height you set is not enough contain text and padding. The text may displayed incomplete and padding incorrect.")
                self.height = height
            else:
                if height < self.minimumHeight:
                    height = self.minimumHeight
                elif self.completeCenter: 
                    # complete center
                    space = height - 3
                    height += space % 2
            self.height = height
        self._calculatePadding()
    
    @property
    def minimumWidth(self)->int:
        l = self.renderableLength + CenterAlignedPanel.MIN_PADDING[0]*2 + 2
        return l
    
    @property
    def minimumHeight(self)->int:
        h = 1 + CenterAlignedPanel.MIN_PADDING[1]*2 + 2
        return h
    
    
    def _calculatePadding(self):
        paddingLeft = int((self.width - self.renderableLength - 2 )/2)
        if paddingLeft < 0:
            paddingLeft = 0
        line = math.ceil(self.renderableLength/self.width)
        paddingTop = int((self.height - 2 - line)/2)
        if paddingTop < 0: 
            paddingTop = 0
        self._setPadding(paddingLeft,paddingTop)
    
    def _setPadding(self, padding:tuple):
        self.padding = (padding[1],padding[0],padding[1],padding[0])
        
    def _setPadding(self, horizon:int = None, vertical:int = None):
        self.padding = (vertical,horizon,vertical,horizon)

if __name__ == "__main__":
    a = CenterAlignedPanel("aa",width=10,height=5)
    print(a)