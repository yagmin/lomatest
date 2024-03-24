import pytest
from marketplace.server import app, db
from marketplace.models import Community, User, Listing, SourceItem, ListingItem, Item, ListingLodging, Lodging


@pytest.fixture
def client():
    client = app.test_client()

    yield client


@pytest.fixture
def test_context():
    app_context = app.app_context()

    yield app_context


def pytest_runtest_teardown():
    with app.app_context():
        model_class_list = [ListingItem, Item, ListingLodging, Lodging, SourceItem, Listing, User, Community]

        for model in model_class_list:
            db.session.query(model).delete()
            db.session.commit()
