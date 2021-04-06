import subprocess

import pytest


@pytest.mark.ci
def test_mta_command():
    """
    Polarion:
        assignee: ghubale
        initialEstimate: 1/30h
        caseimportance: low
        testSteps:
            1. Run `mta` command
        expectedResults:
            1. It should execute properly
    """
    result = subprocess.run("mta", stdout=subprocess.PIPE)
    assert result.returncode == 0
    assert "CLI Tool for MTA" in result.stdout.decode()
