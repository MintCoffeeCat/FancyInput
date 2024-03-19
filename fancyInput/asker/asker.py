from typing import List
from ..groups.option import Option, NumberOption
from ..groups import GroupLayout,OptionGroup,ConstructorFactory
class OnlyQuestionState():
    def __init__(self, question:str, prev:"CompleteQuestionState" = None, asker:"Asker" = None) -> None:
        self.asker = asker
        self.question = question
        self.prev = prev
        self.currentAddOptionIndex = -1
        self.defaultOptionIndex = -1
        
    def opt(self, option:Option)->"QuestionStateWithOneOption":
        return QuestionStateWithOneOption(question = self.question, opt=option, prev=self.prev, asker=self.asker, defaultOptionIndex=self.defaultOptionIndex)
    
    def setDefaultOption(self)->"QuestionStateWithOneOption":
        self.defaultOptionIndex = self.currentAddOptionIndex
        return self

class QuestionStateWithOneOption():
    def __init__(self,question:str, opt:Option, prev:"CompleteQuestionState" = None, asker:"Asker" = None, defaultOptionIndex = -1) -> None:
        self.asker = asker
        self.question = question
        self.option = opt 
        self.prev = prev
        self.currentAddOptionIndex = 0
        self.defaultOptionIndex = defaultOptionIndex
        
    def opt(self, option:Option)->"CompleteQuestionState":
        return CompleteQuestionState(self.question,self.option,option, prev=self.prev, asker=self.asker, defaultOptionIndex=self.defaultOptionIndex)

    def setDefaultOption(self)->"CompleteQuestionState":
        self.defaultOptionIndex = self.currentAddOptionIndex
        return self

class CompleteQuestionState():
    def __init__(self, question:str, opt1:Option,opt2:Option,prev:"CompleteQuestionState" = None, asker:"Asker" = None, defaultOptionIndex = -1) -> None:
        self.nextOne:CompleteQuestionState = None
        self.prevOne = prev
        if prev is not None:
            prev.nextOne = self
        self.question = question
        self.asker = asker
        self.options = [opt1,opt2]
        self.currentAddOptionIndex = 1
        self.defaultOptionIndex = defaultOptionIndex
        self.optionGroupConstructor = ConstructorFactory[GroupLayout.Horizontal]
        self.layout: OptionGroup = None
        if not self.asker.checkQuestionContain(self):
            self.asker.appendQuestion(self)
    
    def __str__(self) -> str:
        res = self.question + "\n"
        for o in self.options:
            res += "\t"+o.name+"\n"
        return res
    
    def opt(self, option:Option)->"CompleteQuestionState":
        if not self.asker.checkQuestionContain(self):
            self.asker.appendQuestion(self)
        self.options.append(option)
        self.currentAddOptionIndex = len(self.options)-1
        return self
    
    def next(self, question:str)->OnlyQuestionState:
        if not self.asker.checkQuestionContain(self):
            self.asker.appendQuestion(self)
        return OnlyQuestionState(question=question,prev=self, asker=self.asker)
    
    def setLayout(self,layout:GroupLayout)->"CompleteQuestionState":
        self.optionGroupConstructor = ConstructorFactory[layout]
        return self
    
    def setDefaultOption(self)->"CompleteQuestionState":
        self.defaultOptionIndex = self.currentAddOptionIndex
        return self
    
    
    def ask(self)->Option:
        if self.layout is None:
            self.layout = self.optionGroupConstructor(self.question, *self.options)
        if self.defaultOptionIndex >= 0:
            self.layout.setDefaultOption(self.defaultOptionIndex)
        opt = self.layout.ask()
        return opt


# TODO: 1. 展示用户已选选项的UI
# TODO: 2. 控制是否在用户选择时始终显示已选选项UI
# TODO: 3. 回调函数执行顺序控制
#           3.1 全部选择完毕后，按顺序执行选项的回调函数
#           3.2 单个选项选择完毕后，立即执行选项的回调函数
class Asker():
    def __init__(self) -> None:
        self.questions:List[CompleteQuestionState] = []
        self.selections = []
    def checkQuestionContain(self,state:CompleteQuestionState)->bool:
        return state in self.questions
    
    def startBuild(self, question:str)->OnlyQuestionState:
        return OnlyQuestionState(question=question, asker=self)
    
    def appendQuestion(self,c:CompleteQuestionState):
        if c is None:
            return
        self.questions.append(c)
    
    def ask(self):
        for (idx,state) in enumerate(self.questions):
            opt = state.ask()
            self.selections.append(opt)
    
    def __str__(self) -> str:
        res = ""
        for q in self.questions:
            res += q.__str__()
        return res


if __name__ == "__main__":
    asker = Asker()
    (asker.startBuild("Question 1")
            .opt(NumberOption("opt1-1"))
            .opt(NumberOption("opt1-2"))
        .next("Question 2")
            .opt(NumberOption("opt2-1"))
            .opt(NumberOption("opt2-2"))
            .opt(NumberOption("opt2-3"))
        .next("Question 3")
            .opt(NumberOption("opt3-1"))
            .opt(NumberOption("opt3-2")))
    print(asker)
    



        