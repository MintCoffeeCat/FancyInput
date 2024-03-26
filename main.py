from fancyInput.baseComponents.alignedPanel import CenterAlignedPanel
from fancyInput.groups import HorizontalOptionGroup
from fancyInput import NumberOption,AsciiOption
from fancyInput.asker import Asker

from rich import print

if __name__ == "__main__":
    gr = HorizontalOptionGroup(
            "What receipe do you want for today's dinner?",
            NumberOption("roasted beef").setCallback(lambda:print("roasted beef is selected!!")),
            NumberOption("porridge"),
            NumberOption("barbecue"),
            NumberOption("fruit salad"),
        )
    gr.setDefaultOption(0)
    gr.setMaxOptionPerUnit(4)
    selected = gr.ask()
    selected()
    
    # asker = Asker()
    # (asker.startBuild("Question 1")
    #         .opt(NumberOption("opt1-1"))
    #         .opt(NumberOption("opt1-2")).setDefaultOption()
    #     .next("Question 2")
    #         .opt(NumberOption("opt2-1")).setDefaultOption()
    #         .opt(NumberOption("opt2-2"))
    #         .opt(NumberOption("opt2-3"))
    #     .next("Question 3")
    #         .opt(NumberOption("opt3-1"))
    #         .opt(NumberOption("opt3-2"))
    #         .opt(NumberOption("opt3-3")).setDefaultOption()
    #         .opt(NumberOption("opt3-4")))
    # asker.ask()
    # p_question = CenterAlignedPanel(
    #         "CenterAlignedPanel",title="Question",
    #         height=1, 
    #         width=1,
    #         expand=True)
    # print(p_question)



