import pytest

from mta.base.application.implementations.web_ui import navigate_to


@pytest.mark.smoke
@pytest.mark.parametrize("mta_app", ["ViaWebUI", "ViaOperatorUI"], indirect=True)
def test_login(application, mta_app):
    """Test login nav destination"""
    view = navigate_to(application.collections.base, "LoggedIn")
    assert view.is_displayed
