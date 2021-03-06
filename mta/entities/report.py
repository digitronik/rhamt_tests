from widgetastic.utils import WaitFillViewStrategy
from widgetastic.widget import View
from widgetastic_patternfly import Text
from widgetastic_patternfly4 import Button

from mta.entities import BaseLoggedInPage
from mta.widgetastic import ApplicationList
from mta.widgetastic import DropdownMenu
from mta.widgetastic import FilterInput
from mta.widgetastic import MTATab


class Issues(View):
    """View to represent issues in analysis report"""

    title = Text('.//h1/div[@class="main"]')
    # TODO(ghubale): Add table widget to read all table on page

    @property
    def is_displayed(self):
        return self.title.text == "Issues"


class HardCodedIP(View):
    """View to represent Hard Coded IP addresses report in analysis report"""

    title = Text('.//h1/div[@class="main"]')
    # TODO(ghubale): Add table widget

    @property
    def is_displayed(self):
        return self.title.text == "Hard-coded IP Addresses"


class AllApplicationsView(BaseLoggedInPage):
    """Class for All applications view"""

    filter_application = FilterInput(id="filter")
    title = Text(locator=".//div[text()[normalize-space(.)='Application List']]")
    send_feedback = Text(locator=".//a[contains(text(), 'Send Feedback')]")

    clear = Text('.//a[@id="clear-filters"]')

    filter_selector = DropdownMenu(locator='.//span[@class="filter-by"]/parent::button/parent::div')
    application_table = ApplicationList()

    sort_selector = DropdownMenu(locator='.//span[@id="sort-by"]/parent::button/parent::div')
    alpha_sort = Button(locator=".//button[@id='sort-order']")

    def clear_filters(self):
        if self.clear.is_displayed:
            self.clear.click()

    def search(self, search_value, filter_type="Name", clear_filters=False):
        """Fill input box with 'search_value', use 'filter_type' to choose filter selector.
        If no filter_type is entered then the default for page is used.
        """
        if clear_filters:
            self.clear_filters()
        if filter_type:
            self.filter_selector.item_select(filter_type)
        self.filter_application.fill(search_value)

    def sort_by(self, sort_criteria):
        """
        Select the sort criteria among Name and Story Points to sort applications list
        """
        if self.sort_selector.items is not None:
            self.sort_selector.item_select(sort_criteria)

    @property
    def is_displayed(self):
        return self.filter_application.is_displayed and self.title.is_displayed

    @View.nested
    class tabs(View):  # noqa
        """The tabs on the page"""

        @View.nested
        class issues(MTATab):  # noqa
            fill_strategy = WaitFillViewStrategy("15s")
            TAB_NAME = "Issues"
            including_view = View.include(Issues, use_parent=True)

        @View.nested
        class technologies(MTATab):  # noqa
            fill_strategy = WaitFillViewStrategy("20s")
            TAB_NAME = "Technologies"
            title = Text('.//div[contains(@class, "page-header")]/h1/div')

            @property
            def is_displayed(self):
                return self.title.text == "Technologies"

        @View.nested
        class hard_coded_ip(MTATab):  # noqa
            fill_strategy = WaitFillViewStrategy("20s")
            TAB_NAME = "Hard-coded IP Addresses"
            including_view = View.include(HardCodedIP, use_parent=True)
