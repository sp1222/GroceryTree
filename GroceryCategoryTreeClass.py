import GroceryItemsInformationClass

class GroceryCategoryTree:

    
    def __init__(self):
        # this node's data:
        self.__categoryName = ''
        self.__category_href = ''
        self.__cateogyItems = [0]   # a list of GroceryItemsInformation objects

        # this node's references to the next nodes, or sub nodes
        self.__subCategories = [0] # list of nodes that are next in line from self node.

# this node's data setters and adders:

    def setCategoryName(self, name):
        self.__categoryName = name

    def setCategory_href(self, href):
        self.__category_href = href
        
    def setCategoryItems(self, catItems):
        self.__categoryItems = catItems
        
    def addCategoryItems(self, catItems):
        self.__categoryItems.append(catItems)


# this node's setters and adders for references to the next nodes, or sub nodes.

    def setSubCategory(self, subCat):
        self.__subCategories = subCat # appends a child node to the list
        
    def addSubCategory(self, subCat):
        self.__subCategories.append(subCat) # appends a child node to the list

    def removeSubCategory(self, index):
        self.__subCategories.pop(index)


# this node's data getters:

    def getCategoryName(self):
        return self.__categoryName

    def getCategory_href(self):
        return self.__category_href
        
    def getCategoryItems(self):
        return self.__categoryItems
        
    def getSubCategory(self):
        return self.__subCategories
