import fauxfactory

from mta.entities.analysis_results import AnalysisResults
from mta.entities.analysis_results import AnalysisResultsView


def test_analysis_results_search_sort_delete(request, application):
    """ Validates Web console Test 03
    1) Upload more than one application into a project to analyse
    2) Search analysis
    3) Delete analysis
    """
    project_name = fauxfactory.gen_alphanumeric(12, start="project_")
    project_collection = application.collections.projects
    project = project_collection.create(
        name=project_name,
        description=fauxfactory.gen_alphanumeric(),
        app_list=[
            "acmeair-webapp-1.0-SNAPSHOT.war",
            "arit-ear-0.8.1-SNAPSHOT.ear",
            "cadmium-war-0.1.0.war",
        ],
        transformation_path="Containerization",
    )
    assert project.exists
    request.addfinalizer(project.delete_if_exists)
    analysis_results = AnalysisResults(application, project_name)
    analysis_results.run_analysis()
    view = analysis_results.create_view(AnalysisResultsView)
    view.wait_displayed("30s")
    # search row 1 in list
    analysis_results.search_analysis(row=1)
    assert view.analysis_row(row=1).analysis_number.is_displayed
    view.clear_search()
    view.wait_displayed("30s")
    # search row 2 in list
    analysis_results.search_analysis(row=2)
    view.clear_search()
    view.wait_displayed("30s")
    # Sort Analysis
    analysis_results.sort_analysis()
    assert analysis_results.get_analysis_number(view, row=1) < analysis_results.get_analysis_number(
        view, row=2
    )
    view.wait_displayed("30s")
    # delete analysis of row 1
    analysis_results.delete_analysis(row=1)
    # Cancel delete operation of remaining analysis row
    view.wait_displayed("30s")
    analysis_results.delete_analysis(row=1, cancel=True)
