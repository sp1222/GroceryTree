from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import GroceryCategoryTreeClass
import re
import time


# funtion where selenium gathers html from each web page
def seleniumGetsHTML(site):


    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(site)
    time.sleep(6)  ### Timer to allow time for the compiler to grab html

    html = BeautifulSoup(driver.page_source, 'html.parser')

    driver.close()
    driver.quit()

    return html

## returns the text of the starting node.
# add the first node to the tree here...
def buildTree(html, site):
    
    ### FIRST we try to find the first node of our tree, generally 'Shop' or 'Menu', or etc..
    # and we sent this first node back to main with Name of Node and href.

    startingKeyword = ['SHOP']#, 'SHOP BY DEPARTMENT', 'MENU']  # MAYBE ADD DEPARTMENT, MENU, SHOP BY DEPARTMENT, ETC..
    tagSearch = html.findAll('a')  # this will work for heb.com, will need to adjust for other websites..   
    rootNodeOfTree = GroceryCategoryTreeClass.GroceryCategoryTree()
    
    # Finds the startingKeyword as apart of startingKeywordTag,  <a> tag in this case   
    for search in tagSearch:
        for keyword in startingKeyword:
            if search.get_text().upper() == keyword:
                #here we append the first node in the category tree
                htmlNode = search  # first node's name in the tree.
                
    rootNodeOfTree.setCategoryName(htmlNode.get_text())
    rootNodeOfTree.setCategory_href(htmlNode['href'])
    rootNodeOfTree.setCategoryParent(None)

    # root node is in the tree, we will now add categories to the tree.
    driver = webdriver.Chrome(ChromeDriverManager().install()) 
    driver.get(site)

    addSubCategoryToCurrentCategory(rootNodeOfTree, driver, site)
    
    driver.close()
    driver.quit()

    return rootNodeOfTree

# this recursive function works with heb.com
def addSubCategoryToCurrentCategory(currentCategory, dr, site):
    
    # FIRST: go to current node's website
    # SECOND: Determine if there are sub categories
    # THIRD: if there are sub categories, add them to the list of sub categories at current node.

    currentSite = site + currentCategory.getCategory_href()
    time.sleep(5)
    dr.execute_script("window.open(''); ")
    dr.switch_to.window(dr.window_handles[1])
    dr.get(currentSite)
    time.sleep(3)
    
    html = BeautifulSoup(dr.page_source, 'html.parser')

    subCategoryExists = False
    subCatHTML = ''
    subCategoryExists, subCatHTML = doesCurrentCategoryHaveSubCategories(html)
    currentCategory.setSubCategoriesExist(subCategoryExists)
    
    if currentCategory.doSubCategoriesExist() == True:
    
        # for the root node on HEB.com, subCatHTML.parent will allow us to access the next layer of categories.
        subCatHTML = subCatHTML.parent
        # then the next layer categories are in an <ul> of <li>s and is the second <a> in each <li>
        ulTags = subCatHTML.findAll('ul')
        for ul in ulTags:
            liTags = ul.findAll('li')
            for li in liTags:
                aTags = li.findAll('a')
                tempSubCategory = GroceryCategoryTreeClass.GroceryCategoryTree()
                name = aTags[1].get_text()
                name = re.sub('[0-9()]', '', name)  # to remove any unwanted characters in the name of the category.
                tempSubCategory.setCategoryName(name)
                tempSubCategory.setCategory_href(aTags[1]['href'])
#                tempSubCategory.setCategoryParent(currentcategory.getCategoryName())
#                print('Adding: ' + name + ' to ' + currentCategory.getCategoryName())
                
                # and while we are here, we will see if there are more child categories in currentcategory.
                currentCategory.addSubCategory(tempSubCategory)

                # close the tab somewhere before recursively calling buildTree and go back to first tab
                dr.close()
                dr.switch_to.window(dr.window_handles[0])

                addSubCategoryToCurrentCategory(tempSubCategory, dr, site)       

    # if not true, add items to list here or do it later on?

## here we look for the 'shop by type' keyword to determine if we have leaf nodes to add or not..
def doesCurrentCategoryHaveSubCategories(html):

    startingKeyword = ['SHOP BY TYPE', 'SHOP BY DEPARTMENT']  # MAYBE ADD DEPARTMENT, MENU, SHOP BY DEPARTMENT, ETC..
    hTagKeys = ['h1', 'h2', 'h3', 'h4']

    ### FIRST see if we can find our next nodes based on a combination of startingKeywords and tagKeys.
    divSearch = html.findAll('div')  # this will work for heb.com

    ### If not, then we look for a <button> with aria-expanded="false"?
    
    exists = False
    subHTML = None
    # Finds the startingKeyword as apart of startingKeywordTag, <a> tag in this case
    for search in divSearch:
        # since the keyword is in an <h2>, we need to sift through each h tag in each nested <div>
        for tag in hTagKeys:
            hCurTag = search.findAll(tag)
            if hCurTag != None:    # if an h tag from the list exists, look for keyword
                for h in hCurTag:
                    for keyword in startingKeyword:
                        if h != None and h.get_text().upper() == keyword:
                            exists = True
                            subHTML = search

                            # note, we have to loop this because the keywords and tagkeys are in nested <div> tags
                            # so we have to go all the way through to the last <div> tag to get the info we want
                        
    return exists, subHTML
    
#*******************************************************************************************************
# Sending tree information to an excel sheet.


def createWorkbook(tree, grocery):
    wb = Workbook()
    treeLine = tree.getCategoryName()    
    addToNewWorkbook(wb, tree, treeLine, index = 0)    
    wb.save('D:\\Python Projects\\HEB.xlsx')

def addToNewWorkbook(wb, currentCategory, line, index):

    wb.create_sheet(index = index, title = currentCategory.getCategoryName())
    wb.active = index
    sheet = wb.active
    catName = sheet.cell(row = 1, column = 1)
    catName.value = 'Category Name:'
    catName = sheet.cell(row = 1, column = 2)    
    catName.value = currentCategory.getCategoryName()

    catLine = sheet.cell(row = 2, column = 1)
    catLine.value = 'Category Tree Line:'
    catLine = sheet.cell(row = 2, column = 2)    
    catLine.value = line
    
    
    catName = sheet.cell(row = 3, column = 1)
    catName.value = 'Category href:'
    catName = sheet.cell(row = 3, column = 2)
    catName.value = currentCategory.getCategory_href()
    
    catName = sheet.cell(row = 4, column = 1)
    catName.value = 'Sub Categories:'

    columnCount = 2
    for each in currentCategory.getSubCategory():
        catName = sheet.cell(row = 4, column = columnCount)
        catName.value = each.getCategoryName()
        columnCount += 1
    
    catProd = sheet.cell(row = 6, column = 1)
    catProd.value = 'Products'

    # this is where we loop each product item from currentCategory
    # and their respective product information.
    
# send subcategory to add to the workbook through.
    index += 1
    if  currentCategory.doSubCategoriesExist() == True:
        for subCategory in currentCategory.getSubCategory():
            temp = line
            line += ' / ' + subCategory.getCategoryName()
            addToNewWorkbook(wb, subCategory, line, index = index)
            line = temp


    
#******************************************************************************************************************************
# Outputting tree to screen
# prints a visual representation of the categories and sub categories tree.
def printCategoryTree(currentCategory, level):

    if currentCategory.doSubCategoriesExist() == True:
        for sub in currentCategory.getSubCategory():
            print((' |    ')*level)
            print((' |    ')*level)
            print((' |    ')*(level-1) + ' |--' + sub.getCategoryName())
            printCategoryTree(sub, (level+1))
        level -= 1

#*******************************************************************************************************
# Get information from excel for updating purposes.

def openWorkbook(tree, grocery):
    
    openName = 'D:\\Python Projects\\' + grocery + '.xlsx'
    wb = load_workbook(openName)

    getFromExistingWorkbook(wb, tree, 0)

    wb.close()

def getFromExistingWorkbook(wb, currentCategory, index):

    
    wb.active = index
    sheet = wb.active
    sheetName = sheet.title
    categoryName = sheet.cell(row = 1, column = 2)
    if sheetName == categoryName:
        currentCategory.setCategoryName(sheet.title)
    else:
        print('names do not match!')
        currentCategory.setCategoryName(categoryName)

    catHREF = sheet.cell(row = 2, column = 2)
    currentCategory.setCategory_href(catHREF)
    
    catHREF = sheet.cell(row = 2, column = 2)
    currentCategory.setCategory_href(catHREF)

    columnCount = 2
    while sheet.cell(row = 3, column = columnCount) != None:
        subCategory = sheet.cell(row = 3, column = columnCount)
        currentCategory.addSubCategory(subCategory)
        columnCount += 1
    

    
#    catProd = wb.active.cell(row = 5, column = 1)
#    catProd.value = 'Products'

    # this is where we loop each product item from currentCategory
    # and their respective product information.
    
    
# send subcategory to add to the workbook through.
#    if  currentCategory.doSubCategoriesExist() == True:
#        for subCategory in currentCategory.getSubCategory():
#            index += 1
#            addToNewWorkbook(wb, subCategory, index = index)

#***********************************************************************************************************************************
# menu options.


def treeMenuOptions():
    
    choice = -1
    while choice < 0 or choice > 2:
        print('HEB is the only grocery option we have right now..')
        print('What operation are we running?')
        print('0. QUIT')
        print('1. Build Category Tree: scrape grocery website for its CATEGORIES to build a tree')
        # NOTE: only if a categories tree already exists in the program!
        print('2. Print Tree: print the tree to screen')
#        print('3. Print Tree: Print an existing tree to the screen')
        # NOTE: requires loading cateogires and items tree from excel
#        print('4. Look for missing CATEGORIES in Excel file')
#        print('5. Look for missing ITEMS in Excel file')    
#        print('6. Look for missing CATEGORIES in Excel file')
#        print('7. Load and print CATEGORIES tree')
        choice = int(input())

        
    return choice

# option 1
# function that builds a category tree
def buildCategoryTree(gURL, gName):
    print('Building category tree..\n')
    print(currentCategory.getCategoryName())
    printCategoryTree(currentCategory, 1)
    print('\nTree has been built!')
    # our tree object where we append the nodes and their respective data values.
    tree = GroceryCategoryTreeClass.GroceryCategoryTree()
    # gets the html via selenium and beautifulsoup combination
    soupSource = seleniumGetsHTML(gURL)
    # get the tree's starting node.
    tree = buildTree(soupSource, gURL)
    return tree

# option 2
# function that saves created tree to a workbook
def buildCategoryTree(tree, gName):
    print('Saving category tree to Workbook..\n')
    print(currentCategory.getCategoryName())
    printCategoryTree(currentCategory, 1)
    print('\nTree has been Saved!')
    # output tree data to excel.
    createWorkbook(tree, gName)
    return tree



# option 3
# prints a visual representation of the categories and sub categories tree.

def printTree(currentCategory):
    print('Printing category tree to screen..\n')
    print(currentCategory.getCategoryName())
    printCategoryTree(currentCategory, 1)
    print('\nTree has been printed!')


                        
#*******************************************************************************************************
# main function    
def main():

    # our tree object where we append the nodes and their respective data values.
    groceryCategoryTreeObject = GroceryCategoryTreeClass.GroceryCategoryTree()

#    groceryChoice
#    while groceryChoice != 1:
#        print('Grocery Web Scraping App')
#        print('Select the grocery you want to run the app on')
#        print('1. HEB')
#        choice = input()

    # THIS ONLY WORKS FOR HEB.COM At the moment
    # page we will be visiting to build our tree
    groceryURL = 'https://www.heb.com'
    # Grocery Name
    groceryName = 'HEB'
    operationChoice = treeMenuOptions()

    while(operationChoice != 0):
        if(operationChoice == 1):
            groceryCategoryTreeObject = buildCategoryTree(groceryURL, groceryName)
            operationChoice = treeMenuOptions()            
            
        elif(operationChoice == 2):
            # output tree data to excel.
            saveToWorkbook(groceryCategoryTreeObject, groceryName)
            operationChoice = treeMenuOptions()            
            
            
        elif(operationChoice == 3):
            printTree(groceryCategoryTreeObject)
            operationChoice = treeMenuOptions()
            
    #    elif(operationChoice == 4):
            
    #    elif(operationChoice == 5):
            
    #    elif(operationChoice == 6):
            
    #    elif(operationChoice == 7):

    exit()
        
        
main()
