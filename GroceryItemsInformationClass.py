
### this is item specifics, node object
class GroceryItemsInformation:

    def __init__(self):
        self.__itemName = ''
        self.__itemSize = ''
        self.__itemDescription = ''
        self.__itemOnlinePrice = 0.00
        self.__itemPreparationInstructions = ''
        self.__itemIngredients = ''
        self.__itemSafetyWarning = ''
        self.__itemNutritionComponents = ''
        self.__itemNutritionComponentQuantities = 0
        self.__itemNutritionComponentUOM = ''
        self.__itemNutritionComponentDailyPercentage = ''
        

# Setters

    def setItemName(self, name):
        self.__itemName = name

    def setItemSize(self, size):
        self.__itemSize = size
        
    def setItemDescription(self, descript):
        self.__itemDescription = descript

    def setItemOnlinePrice(self, price):
        self.__itemOnlinePrice = price
        
    def setItemPreparationInstructions(self, instructions):
        self.__itemPreparationInstructions = instructions

    def setItemIngredients(self, ingredients):
        self.__itemIngredients = ingredients
        
    def setItemSafetyWarning(self, warning):
        self.__itemSafetyWarning = warning

    def setItemNutritionComponents(self, nutComp):
        self.__itemNutritionComponents = nutComp
        
    def setItemNutritionComponentQuantities(self, nutCompQuant):
        self.__itemNutritionComponentQuantities = nutCompQuant

    def setItemNutritionComponentUOM(self, UOM):
        self.__itemNutritionComponentUOM = UOM
        
    def setItemNutritionComponentDailyPercentage(self, dailyPercentage):
        self.__itemNutritionComponentDailyPercentage = dailyPercentage

# Getters
