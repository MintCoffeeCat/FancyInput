from rich.style import Style

from .exp.exceptions import InputTypeError
from .baseComponents.alignedPanel import CenterAlignedPanel


class Option():
    def __init__(self, opt:str, name) -> None:
        self.opt = opt 
        self.name = name
        self.assigned = False
        self.gapSpace = ""

    def getPanel(self):
        return CenterAlignedPanel(
            self.name,
            title=self.opt,
            style=Style(
                color= "green" if self.assigned else None
            )
        )
    
    def assgin(self):
        self.assigned = True
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
    def __init__(self, name:str) -> None:
        super().__init__(None, name)
    
    def transitionInput(self, input:str):
        if not input.isdigit():
            raise InputTypeError(expected_type="整数",current_value=input)
        return input
        
class AsciiOption(Option):
    def __init__(self, opt:str, name) -> None:
        if not opt.isascii():
            raise Exception(f"字母选项的选择头只能是字母！当前为{opt}")
        super().__init__(opt, name)
    
    def transitionInput(self, input:str):
        if not input.isascii():
            raise InputTypeError(expected_type="字母",current_value=input)
        
        return input