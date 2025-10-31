from playwright.sync_api import Page, Locator


class BasePage:

    def __init__(self, page: Page, urls):
        self.current_page = page
      

    def screen_title(self) -> Locator:
        title_selector = self.current_page.locator(Selectors.CurrentScreenTitle)
        return title_selector


class Selectors:
    CurrentScreenTitle = ".title"
