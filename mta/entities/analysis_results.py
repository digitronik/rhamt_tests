from taretto.navigate import NavigateToAttribute
from taretto.navigate import NavigateToSibling
from wait_for import wait_for
from widgetastic.widget import Text
from widgetastic_patternfly import Button
from widgetastic_patternfly import Input

from mta.base.application.implementations.web_ui import MTANavigateStep
from mta.base.application.implementations.web_ui import NavigatableMixin
from mta.base.application.implementations.web_ui import navigate_to
from mta.base.application.implementations.web_ui import ViaWebUI
from mta.entities import AllProjectView
from mta.entities import BaseLoggedInPage
from mta.entities import ProjectView
from mta.utils.update import Updateable
from mta.widgetastic import AnalysisResults


class AnalysisResultsView(BaseLoggedInPage):

    run_analysis_button = Button("Run Analysis")
    title = Text(locator=".//div/h2[normalize-space(.)='Active Analysis']")
    search = Input("searchValue")
    analysis_results = AnalysisResults()
    # Two locators for searching two different rows
    analysis_number_1 = Text(locator=".//tr[1]//a[@class='pointer link']")
    analysis_number_2 = Text(locator=".//tr[2]//a[@class='pointer link']")

    @property
    def is_displayed(self):
        return self.run_analysis_button.is_displayed and self.title.is_displayed

    def clear_search(self):
        """Clear search"""
        if self.search.value:
            self.search.fill("")


class AnalysisResults(Updateable, NavigatableMixin):
    """Analysis Configuration"""

    def __init__(self, application, project_name):
        self.application = application
        self.project_name = project_name

    def search_analysis(self, row):
        """ Search analysis results with analysis number
        """
        view = navigate_to(self, "AnalysisResultsPage")
        if row == 1:
            analysis_num = view.analysis_number_1.text
        else:
            analysis_num = view.analysis_number_2.text
        only_digits = "".join([c for c in analysis_num if c.isdigit()])
        view.search.fill(only_digits)

    def run_analysis(self):
        """ Run analysis"""
        view = navigate_to(self, "AnalysisResultsPage")
        view.run_analysis_button.click()
        wait_for(lambda: view.analysis_results.in_progress(), delay=0.2, timeout=120)
        wait_for(lambda: view.analysis_results.is_analysis_complete(), delay=0.2, timeout=120)
        assert view.analysis_results.is_analysis_complete()


@ViaWebUI.register_destination_for(AnalysisResults)
class AllProject(MTANavigateStep):
    VIEW = AllProjectView
    prerequisite = NavigateToAttribute("application.collections.base", "LoggedIn")

    def step(self):
        if not self.prerequisite_view.is_empty:
            self.prerequisite_view.home_navigation.select("Projects")


@ViaWebUI.register_destination_for(AnalysisResults)
class SelectProject(MTANavigateStep):
    VIEW = ProjectView
    prerequisite = NavigateToSibling("AllProject")

    def step(self):
        self.prerequisite_view.projects.select_project(self.obj.project_name)


@ViaWebUI.register_destination_for(AnalysisResults)
class AnalysisResultsPage(MTANavigateStep):
    prerequisite = NavigateToSibling("SelectProject")
    VIEW = AnalysisResultsView

    def step(self):
        self.prerequisite_view.navigation.select("Analysis Results")
