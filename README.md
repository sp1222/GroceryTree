# GroceryTree
This is a web crawler Python project designed to build a tree of grocery categories off of a local grocery store's website and allocate grocery items into their respective categories.

This program uses a combination of selenium's webdriver and BeautifulSoup's parser capabilities to gather the html code we need.

Note to self:  need to work on tree node object class (its late and my brain is fried) to start building the category tree and add some data to the node.

Currently, when the program runs, the web crawler will go to our local grocery store and sift through the html for the texts of the categories and subcategories under the "shop" dropdown box and print them out sequentially (is this the correct term to use?).

This method will only work for our local grocery store, but will eventually try to solve how to dynamically work with other grocery store web sites.

Working on the class that will create objects and use them in a multi-linked list fashion to create a tree of categories and sub categories.
