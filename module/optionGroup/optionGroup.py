from rich.layout import Layout

from typing import List
from wcwidth import wcswidth
from ..option import Option
from exp.exceptions import InputTypeError

class OptionGroup():
    def __init__(self, question:str, *options:Option) -> None:
        self.options:List[Option] = []
        self.question = question
        self.lenQuestion = wcswidth(question)
        self.defaultIndex = -1
        self.maxOptionPerUnit = 3
        self.maxCharacterPerLineOfQuestion = self.lenQuestion
        self.maxLenOpt = 0
        for idx,opt in enumerate(options):
            if opt.opt is None:
                opt.opt = str(idx)
            self.options.append(opt)
            self.maxLenOpt = wcswidth(opt.name) if wcswidth(opt.name) > self.maxLenOpt else self.maxLenOpt
        self.optNum = len(self.options)

        # 一些常量设置
        self.singleOptionPanelWidth = self.maxLenOpt + 2
        self.singleOptionPanelHeight = 3
        self.questionPanelWidth = self.lenQuestion + 2
        self.inputPanelHeight = 3
        self.questionPaddingTop = 0
    
    # @group()
    def getOptionsPanel(self):
        for opt in self.options:
            p = opt.getPanel()
            p.resize(width=self.singleOptionPanelWidth, height=self.singleOptionPanelHeight)
            yield p
    
    def getLayout(self)->Layout:
        pass
    
    def checkInput(self,input)->bool:
        if input == "" and self.defaultIndex != -1:
            self.options[self.defaultIndex].assgin()
            return True
        for opt in self.options:
            try:
                if opt.checkInput(input):
                    opt.assgin()
                    return True
            except InputTypeError as e: 
                continue

        return False
    
    def setDefaultOption(self, option:Option):
        for idx, opt in enumerate(self.options):
            if opt == option:
                self.defaultIndex = idx
    
    def setDefaultOption(self, idx:int):
        if idx < 0 or idx > self.optNum:
            raise Exception("The Option index is invalid!")
        
        self.defaultIndex = idx
    
    def setMaxOptionPerUnit(self, maxnum:int):
        if maxnum < 1:
            raise Exception("The number of option per unit cannot be negative or zero!")
        self.maxOptionPerUnit = maxnum
        self._adjustUnit()

    
    def clear(self):
        pass

    def _adjustUnit(self):
        pass

    def ask(self):
        pass   


