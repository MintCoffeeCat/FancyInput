import sys,math
from typing import List,TypedDict,Callable
from enum import Enum

from rich import print
from rich.layout import Layout
from rich.panel import Panel
from wcwidth import wcswidth

from ..baseComponents.alignedPanel import CenterAlignedPanel
from ..exp.exceptions import InputTypeError
from .option import Option

class GroupLayout(Enum):
        Horizontal = 0
        Vertical = 1
        
class ConstructorDict(TypedDict):
    GroupLayout.Horizontal:Callable # type: ignore
    GroupLayout.Vertical:Callable   # type: ignore
    
    
class OptionGroup():
    def __init__(self, question:str, *options:Option) -> None:
        self.options:List[Option] = []
        self.question = question
        self.lenQuestion = wcswidth(question)
        self.defaultIndex = -1
        self.maxOptionPerUnit = 3
        self.maxCharacterPerLineOfQuestion = self.lenQuestion
        self.singleOptionPanelWidth = 0
        # 一些常量设置
        for idx,opt in enumerate(options):
            if opt.opt is None:
                opt.opt = str(idx)
            self.options.append(opt)
            self.singleOptionPanelWidth = opt.getPanelWidth() if opt.getPanelWidth() > self.singleOptionPanelWidth else self.singleOptionPanelWidth
        self.optNum = len(self.options)
        self.singleOptionPanelHeight = 3
        self.questionPanelWidth = self.lenQuestion + CenterAlignedPanel.MIN_PADDING[0]*2 + 2
        self.inputPanelHeight = 3
    
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



class VerticalOptionGroup(OptionGroup):
    def __init__(self, question:str, *options:Option) -> None:
        super().__init__(question, *options)
        self._adjustUnit()

    def clear(self):
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[1B")
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[1A")
        for i in range(self.optNum*3 + 3):
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[K")
        
    def getCols(self, list_A):
        list_C = []
        for i in range(0, len(list_A), self.maxOptionPerUnit):
            end = i+self.maxOptionPerUnit
            if end > len(list_A):
                end = len(list_A)
            sublist_B = list_A[i:end]
            list_C.append(sublist_B)
        return list_C
    
    def getColsLayout(self,nCol):
        return [Layout(name=f"Col-{i}") for i in range(nCol)]
    
    def setMaxLengthOfQuestion(self, maxnum:int):
        self.maxCharacterPerLineOfQuestion = maxnum
        self.questionPanelWidth = self.maxCharacterPerLineOfQuestion + 2
        
    def getLayout(self)->Panel:
        # 设置选项的ui
        p_options = [pn for pn in self.getOptionsPanel()]
        p_options = self.getCols(p_options)
        cols = self.getColsLayout(len(p_options))
        for idx,lyot in enumerate(cols):
            lyot.split_column(
                *p_options[idx]
            )
        l_options = Layout(name="Options",size=self.singleOptionPanelWidth*len(cols))
        l_options.split_row(
            *cols
        )
        # 设置问题的ui
        p_question = CenterAlignedPanel(
            self.question,title="Question",
            height=self.questionPanelHeight, 
            width=self.questionPanelWidth,
            expand=True,
            completeCenter=False
        )
        
        # 设置问题和选项的组合ui
        l_QnO = Layout(name="Quest&Opt")
        l_QnO.split_row(
            p_question,
            l_options
        )
        
        # 设置输入框的ui
        inputBox = Layout(Panel("",title="Input"),size=self.inputPanelHeight)
        
        # 设置输入框和问题选项的组合ui
        ly = Layout(name="Outer")
        ly.split_column(
            l_QnO,
            inputBox
        )
        
        # 设置最外层宽高约束
        pn = Panel(ly,
                   width=self.questionPanelWidth+self.countCol*self.singleOptionPanelWidth+4, 
                   height=self.questionPanelHeight+self.inputPanelHeight+2)

        return pn

    def _adjustUnit(self):
        self.practicalOptPerCol = self.maxOptionPerUnit if self.maxOptionPerUnit < self.optNum else self.optNum
        self.countCol = math.ceil(self.optNum/self.practicalOptPerCol)
        # 计算一列以及多列选项的情况下，问题栏的正确高度
        adaption = (self.singleOptionPanelHeight)*self.countCol
        self.questionPanelHeight = adaption 


class HorizontalOptionGroup(OptionGroup):
    def __init__(self, question:str, *options:Option) -> None:
        super().__init__(question, *options)
        # 控制每行的选项数量、间距、长度
        self._adjustUnit()
    
    def getLines(self, list_A):
        list_C = []
        for i in range(0, len(list_A), self.maxOptionPerUnit):
            end = i+self.maxOptionPerUnit
            if end > len(list_A):
                end = len(list_A)
            sublist_B = list_A[i:end]
            list_C.append(sublist_B)
        return list_C
    
    def getLinesLayout(self,nLine):
        return [Layout(name=f"Line-{i}") for i in range(nLine)]
    
    def getLayout(self)->Panel:
        # 设置选项的ui
        p_options = [pn for pn in self.getOptionsPanel()]
        p_options = self.getLines(p_options)
        lines = self.getLinesLayout(len(p_options))
        for idx,lyot in enumerate(lines):
            lyot.split_row(
                *p_options[idx]
            )
        l_options = Layout(name="Options",size=self.inputPanelHeight*len(lines))

        l_options.split_column(
            *lines
        )
        # 设置问题的ui
        p_question = CenterAlignedPanel(
            self.question,title="Question",
            height=self.inputPanelHeight, 
            width=self.questionPanelWidth,
            expand=True)
        # 设置问题和选项的组合ui
        l_QnO = Layout(name="Quest&Opt",size=self.inputPanelHeight + self.inputPanelHeight*len(lines))
        l_QnO.split_column(
            p_question,
            l_options
        )
        # 设置输入框的ui
        inputBox = Panel("",title="Input", width=self.questionPanelWidth, height=self.inputPanelHeight)
        
        # 设置输入框和问题选项的组合ui
        ly = Layout(name="Outer", size=self.inputPanelHeight*2 + self.inputPanelHeight * len(lines))
        ly.split_column(
            l_QnO,
            inputBox
        )
        
        # 设置最外层宽高约束
        pn = Panel(
            ly,
            width=self.questionPanelWidth + 4, 
            height=self.inputPanelHeight*2 + self.inputPanelHeight* len(lines) + 2)
        # print(ly.tree)
        return pn

    def clear(self):
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[1B")
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[1A")
        for i in range(self.countLine*3 + self.inputPanelHeight + 3):
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[K")
    
    def _adjustUnit(self):
        self.practicalOptPerLine = self.maxOptionPerUnit if self.maxOptionPerUnit < self.optNum else self.optNum
        self.countLine = math.ceil(self.optNum/self.practicalOptPerLine)
        # 计算一行以及多行选项的情况下，问题栏的正确长度
        adaption = (self.singleOptionPanelWidth)*self.practicalOptPerLine
        self.questionPanelWidth = self.questionPanelWidth if self.questionPanelWidth > adaption else adaption

        # 计算一行以及多行选项的情况下，选项框的正确长度
        if self.practicalOptPerLine * self.singleOptionPanelWidth < self.questionPanelWidth:
            self.singleOptionPanelWidth = int(self.questionPanelWidth / self.practicalOptPerLine)


ConstructorFactory: ConstructorDict = {
    GroupLayout.Horizontal:HorizontalOptionGroup,
    GroupLayout.Vertical:VerticalOptionGroup
} 