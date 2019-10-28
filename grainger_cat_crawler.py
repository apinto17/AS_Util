

import generalized_cat_crawler as gcc


class grainger_cat_crawler(gcc.Site):

    def get_cat_name(self, cat):
        return cat.find_element_by_css_selector("span.category-text").text

    def get_cats(self, browser):
        return browser.find_elements_by_css_selector("ul.categories__list > li.list-item")

    def get_prods(self, browser):
        return browser.find_elements_by_css_selector("ul.search-list-view__products div.search-list-view__product")
