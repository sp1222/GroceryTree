from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
#import GroceryCategoryTreeClass  work in progress
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
#def buildCategoryTree(html, treeObj):

def buildCategoryTree(html):

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
    
    categoryDictionary = {}
    subCatCounterIndex = 0
    index = 0
    
    for eachUmbrella in umbrellaCategoryList:

#        print ('\n')
#        print(eachUmbrella.get_text())
        tempList = []
        count = 0

        while count < subCatCounter[subCatCounterIndex]:

            tempList.append(subLists[index].get_text())
#            print(subLists[index].get_text())

            count += 1
            index += 1

        
        categoryDictionary.update({eachUmbrella.get_text(): tempList[:]})
        subCatCounterIndex += 1

#    print('\n')
#    print (categoryDictionary)


    
# main function    
def main():
    
    # our tree object where we append the nodes and their respective data values.
#    groceryCategoryTreeObject = [0]   Work in Progress
    
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

    # this function will take the components of each sub category tags and add them to
    # a list of instances of the GroceryCategoryTree object
#    groceryCategoryTreeObject = buildCategoryDictionary(allCategoryNodes, groceryCategoryTreeObject)   Work In Progress
    buildCategoryTree(allCategoryNodes)
       
        
main()
