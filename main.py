from fancyInput.optionGroup.horizontalOptionGroup import HorizontalOptionGroup
from fancyInput.optionGroup.verticalOptionGroup import VerticalOptionGroup
from fancyInput.option import NumberOption,AsciiOption

if __name__ == "__main__":
    gr = HorizontalOptionGroup(
            "What receipe do you want for today's dinner?",
            NumberOption("roasted beef"),
            NumberOption("porridge"),
            NumberOption("barbecue"),
            NumberOption("fruit salad"),
        )
    gr.setDefaultOption(0)
    gr.setMaxOptionPerUnit(4)
    gr.ask()




