
import math
import sys

from rich.layout import Layout
from rich.panel import Panel

from ..baseComponents.alignedPanel import CenterAlignedPanel
from ..option import Option
from .optionGroup import OptionGroup


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
            width=self.questionPanelWidth)
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
    
    # def ask(self):
    #     inputDone = False
    #     while not inputDone:
    #         print(self.getLayout())
    #         sys.stdout.write("\033[1A")
    #         sys.stdout.write("\033[1A")
    #         sys.stdout.write("\033[1A")
    #         sys.stdout.write("\033[K")
    #         res = input("│ │ > ")
    #         inputDone = self.checkInput(res)
    #         self.clear()
    #     print(self.getLayout())
    #     return res
    
    def _adjustUnit(self):
        self.practicalOptPerLine = self.maxOptionPerUnit if self.maxOptionPerUnit < self.optNum else self.optNum
        self.countLine = math.ceil(self.optNum/self.practicalOptPerLine)
        # 计算一行以及多行选项的情况下，问题栏的正确长度
        adaption = (self.singleOptionPanelWidth)*self.practicalOptPerLine
        self.questionPanelWidth = self.questionPanelWidth if self.questionPanelWidth > adaption else adaption

        # 计算一行以及多行选项的情况下，选项框的正确长度
        if self.practicalOptPerLine * self.singleOptionPanelWidth < self.questionPanelWidth:
            self.singleOptionPanelWidth = int(self.questionPanelWidth / self.practicalOptPerLine)
