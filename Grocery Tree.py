from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import GroceryCategoryTreeClass # work in progress
import time


# using Selenium to open given websites to extract html code.

def seleniumGetsHTML(site):


    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(site)
    time.sleep(6)  ### Timer to allow time for the compiler to grab html

    html = BeautifulSoup(driver.page_source, 'html.parser')

    driver.close()
    driver.quit()

    return html


## returns the text of the starting node.

def getStartingNode(html):

    startingKeyword = ['SHOP']  # MAYBE ADD DEPARTMENT, MENU, SHOP BY DEPARTMENT, ETC..

    # will need to determine the method to find the correct tag for the starting node.

    ### FIRST see if we can find our lists based on startingKeyword
    tagSearch = html.findAll('a')  # this will work for heb.com

    ### If not, then we look for a <button> with aria-expanded="false"

    
    # Finds the startingKeyword as apart of startingKeywordTag,  <a> tag in this case   
    for search in tagSearch:
        for keyword in startingKeyword:
            if search.get_text().upper() == keyword:
                #here we append the first node in the category tree
                htmlNode = search  # first node's name in the tree.
            
    return htmlNode


# gets the next tag that ends up being all of the categories
def getSiblingCategoryTags(html):

    # may need to come up with a more dynamic method?
    tags = html.find_next_sibling()

    return tags


# gets the tags of the category nodes based off of the siblings
# this will end up being the function where we build our tree and add some data.

# note, this only works for heb.com for the time being, as it is tailored to the html tag's layout specifically from heb.com.


def buildCategoryList(html):

    # because all of the categories are in <a> tags under <li> tags
    allLists = html.findAll('li')

    # general categories, 'Fruits and Vegetables', 'Meats and Seafood', etc..
    umbrellaCategoryList = []

    # First we get the umbrella categories,
    # the categories in the li, right below the first node "Shop"
    # the text for these umbrella categories are in the h4 tags
    for lists in allLists:
        
        h4 = lists.findAll('h4')
        for ea in h4:
            if ea is not None:
                umbrellaCategoryList.append(ea)


                # maybe here we get the parent li?

    # we then figure out how many umbrella categories there are
    # and make an array that will tally up how many categories
    # are under each umbrella category
    # ie Fruit and Vegetables is an umbrella category with two categories
    # Fruits, and Vegetables
    subCatCounter = [0] * len(umbrellaCategoryList)
    subCatCounterIndex = 0
    subLists = []
    
    for lists in allLists:

        # li tags that contain the li tags of both umbrella categories and categories

        count = 0
        for subList in lists:
            subLi = subList.findAll('li') # because categories are li tags nested within umbrella categories li tags.
        
            for each in subLi:  
                
                if each is not None:  # to skip the empty subLi's
                    count += 1
                    subLists.append(each)    # append the category information.
                    
        if count is not 0:  # to skip the empty subLi's
            subCatCounter[subCatCounterIndex] = count
            subCatCounterIndex += 1

        
    # we now put all of the umbrella category and sub category tags and add them to a dictionary
    # the key will be the umbrella category tags, the value is a list of sub categories respective to their umbrella category
    
    categoryList = []
    subCatCounterIndex = 0
    index = 0
    
    for eachUmbrella in umbrellaCategoryList:

        tempList = []
        count = 0

        while count < subCatCounter[subCatCounterIndex]:

            tempList.append(subLists[index])

            count += 1
            index += 1

        
        categoryList.append([eachUmbrella, tempList[:]])
        subCatCounterIndex += 1

    return categoryList


# here we build a tree of categories and collect individual pieces of information regarding each tree
# such as hrefs that will be used to collect data on items of each category and subcategory
def buildCategoryTree(catLists):

    # the tree we will be returning
    tree = GroceryCategoryTreeClass.GroceryCategoryTree()

    tempUmbCat = [] # instead of appending umbrella categories, we fill an empty list
                    # doing so gets rid of the leading 0 object in the list.
    
    for umb in catLists:

        # here we get the umbrella categories, Fruit & Vegetables, Meat & Seafood
        # you will notice that there are no hrefs or items being added
        # we only get the name of the umbrella category and build the list of sub categories

        # create an empty GroceryCategoryTree object.
        umbrellaCategory = GroceryCategoryTreeClass.GroceryCategoryTree()

        umbrellaCategory.setCategoryName(umb[0].get_text())

        tempSubCat = [] # instead of appending umbrella categories, we fill an empty list
                        # doing so gets rid of the leading 0 object in the list.
       
        for sub in umb[1]:

            # here we get the umbrella's subcategories, Fruit, Vegetables, Meat, Seafood
            # you will notice that there are no subcategories
            # items will be added later on
            # we only get the name and href of each sub category
            # then append to a temp list of sub categories
            
            # create an empty GroceryCategoryTree object.
            subCategory = GroceryCategoryTreeClass.GroceryCategoryTree()
            
            subCategory.setCategoryName(sub.get_text())
            subCategory.setCategory_href(sub.find()['href'])

            # here we append the subcategory to a temp list of subcategories
            tempSubCat.append(subCategory)  # list of sub categories within umbrella category

        # here we set the list of subcategories to the umbrellaCategory Object
        umbrellaCategory.setSubCategory(tempSubCat)

        # here we append a list of umbrella categories to a temporary list of umbrella categories
        tempUmbCat.append(umbrellaCategory)
        


    # here we set the umbrella categories of the first node of the tree, named 'Shop'
    # note we do not add href or category items to this node
    # we only set the name and the list of umbrella categories
    
    tree.setCategoryName('Shop')
    tree.setSubCategory(tempUmbCat)
    
    return tree


# prints a visual representation of the categories and sub categories tree.
def printCategoryTree(tree):

    print(tree.getCategoryName())

    umbrellaCategories = tree.getSubCategory()


    for eachUmbrella in tree.getSubCategory():

        print('  |')
        print('  |')
        print('  |--' + eachUmbrella.getCategoryName())

        for eachSub in eachUmbrella.getSubCategory():
            print('  |    |')
            print('  |    |--' + eachSub.getCategoryName())
    

    
# main function    
def main():
    
    
    # THIS ONLY WORKS FOR HEB.COM
    # page we will be visiting to build our tree
    groceryURL = 'https://www.heb.com'

    # gets the html via selenium and beautifulsoup combination
    soupSource = seleniumGetsHTML(groceryURL)

    # gets html to the starting node based on a keyword (in this case 'SHOP')
    # which is a sibling branch of the <li> in the html on heb.com
    # that the rest of the <li> tags with the categories are and subcategories
    # are located on
    startingNode = getStartingNode(soupSource)

    # this function gets the sibling tag (in this case <div>) on heb.com
    # this tag contains children tags that contain the categories and subcategories
    allCategoryNodes = getSiblingCategoryTags(startingNode)

    # build a dictionary of categories and sub categories
    # return a dictionary that will easily be dissectable
    categoryLists = buildCategoryList(allCategoryNodes)

    # this function will take the components of each sub category tags and add them to
    # a list of instances of the GroceryCategoryTree object

    # our tree object where we append the nodes and their respective data values.
    groceryCategoryTreeObject = GroceryCategoryTreeClass.GroceryCategoryTree()

    # build the HEB shopping tree
    groceryCategoryTreeObject = buildCategoryTree(categoryLists)

    printCategoryTree(groceryCategoryTreeObject)
       
        
main()
