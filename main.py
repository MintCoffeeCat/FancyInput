from module.optionGroup.horizontalOptionGroup import HorizontalOptionGroup
from module.optionGroup.verticalOptionGroup import VerticalOptionGroup
from module.option import NumberOption

if __name__ == "__main__":
    gr = HorizontalOptionGroup(
            "What receipe do you want for today's dinner?",
            NumberOption("roasted beef"),
            NumberOption("porridge"),
            NumberOption("barbecue"),
            NumberOption("fruit salad"),
        )
    gr.setDefaultOption(0)
    gr.setMaxOptionPerUnit(3)
    gr.ask()




