"""
Pytest configuration for custom command line options
"""


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--model",
        action="store",
        default="llama3.2:1b",
        help="Model to test (default: llama3.2:1b)",
    )


def pytest_generate_tests(metafunc):
    """Use custom model option in tests"""
    if "model_name" in metafunc.fixturenames:
        model = metafunc.config.getoption("model")
        metafunc.parametrize("model_name", [model])
