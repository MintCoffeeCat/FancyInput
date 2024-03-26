from typing import Any
from rich.style import Style

from ..exp.exceptions import InputTypeError
from ..baseComponents.alignedPanel import CenterAlignedPanel


class Option():
    def __init__(self, opt:str, name:str, func) -> None:
        self.opt = opt 
        self.name = name
        self.assigned = False
        self.gapSpace = ""
        self.func = func
        self.panel = None
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.func is not None:
            self.func(*args, **kwds)
        else:
            raise Exception("No callback function was set.")
        
    def getPanel(self, expand=True, completeCenter = False):
        if self.panel is not None:
            return self.panel
        
        self.panel = CenterAlignedPanel(
            self.name,
            title=self.opt,
            expand=expand,
            completeCenter=completeCenter,
            style=Style(
                color= "green" if self.assigned else None
            )
        )
        return self.panel
    
    def getPanelWidth(self):
        panel = self.getPanel()
        return panel.width
    
    def setCallback(self,func)->"Option":
        self.func = func
        return self
    
    def assgin(self):
        self.assigned = True
        if self.panel is not None:
            self.panel.style = Style(
                color= "green" if self.assigned else None
            )
            
    def deAssign(self):
        self.assigned = False
    
    def checkInput(self, input) -> bool:
        if input == "":
            return False
        input = self.transitionInput(input)
        return input == self.opt

    def transitionInput(self, input):
        pass
    
    def getOpt(self):
        return self.opt
    
class NumberOption(Option):
    def __init__(self, name:str, func = None) -> None:
        super().__init__(None, name, func)
    
    def transitionInput(self, input:str):
        if not input.isdigit():
            raise InputTypeError(expected_type="整数",current_value=input)
        return input
        
class AsciiOption(Option):
    def __init__(self, opt:str, name, func = None) -> None:
        if not opt.isascii():
            raise Exception(f"字母选项的选择头只能是字母！当前为{opt}")
        super().__init__(opt, name, func)
    
    def transitionInput(self, input:str):
        if not input.isascii():
            raise InputTypeError(expected_type="字母",current_value=input)
        
        return input