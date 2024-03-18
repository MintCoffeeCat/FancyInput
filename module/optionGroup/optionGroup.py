import sys
from typing import List

from rich import print
from rich.layout import Layout
from wcwidth import wcswidth

from ..exp.exceptions import InputTypeError

from ..option import Option


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
    
    def checkInput(self,input)->Option:
        if input == "" and self.defaultIndex != -1:
            self.options[self.defaultIndex].assgin()
            return self.options[self.defaultIndex]
        for opt in self.options:
            try:
                if opt.checkInput(input):
                    opt.assgin()
                    return opt
            except InputTypeError as e: 
                continue
        return None
    
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

    def ask(self)->Option:
        selectedOption = None
        while selectedOption is None:
            print(self.getLayout())
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[K")
            res = input("│ │ > ")
            selectedOption = self.checkInput(res)
            self.clear()
        print(self.getLayout())
        return selectedOption
    
    def getLayout(self)->Layout:
        pass
    
    def clear(self):
        pass

    def _adjustUnit(self):
        pass



