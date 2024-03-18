
import math
import sys

from rich.layout import Layout
from rich.panel import Panel

from ..baseComponents.alignedPanel import CenterAlignedPanel
from ..option import Option
from .optionGroup import OptionGroup


class VerticalOptionGroup(OptionGroup):
    def __init__(self, question:str, *options:Option) -> None:
        super().__init__(question, *options)
        self.questionPanelHeight = self.optNum*self.singleOptionPanelHeight
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
            width=self.questionPanelWidth
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
        adaption = (self.singleOptionPanelHeight)*self.practicalOptPerCol
        self.questionPanelHeight = adaption 
