import json
import pytest
from marketplace.server import db
from flask.ctx import AppContext
from marketplace.models import Community, SourceItem, User


@pytest.fixture
def seed_community(test_context: AppContext):
    with test_context:
        community = Community(name="Sneaker Gang", uri="sneakergang")
        db.session.add(community)
        db.session.commit()
        db.session.refresh(community)

        yield community


@pytest.fixture
def seed_user(test_context: AppContext):
    with test_context:
        user = User(email="a@a.com", first_name="Bob", last_name="Brown")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        yield user


@pytest.fixture
def seed_source_item(test_context: AppContext):
    with test_context:
        source_item = SourceItem(source_item_name="Keds", source_item_details='{"color": "red"}')
        db.session.add(source_item)
        db.session.commit()
        db.session.refresh(source_item)

        yield source_item


def test_create_listing_with_validation_error(test_context, client):
    with test_context:
        create_response = client.post("/marketplace/api/listing/create", json={})

        assert create_response.status_code == 422
        assert create_response.json == {'errors': {'json': {
            'available_count': ['Missing data for required field.'],
            'community_id': ['Missing data for required field.'],
            'listed_by_id': ['Missing data for required field.'],
            'listing_price_cents': ['Missing data for required field.'],
            'listing_title': ['Missing data for required field.'],
            'listing_type': ['Missing data for required field.'],
            'sale_type': ['Missing data for required field.'],
            'status': ['Missing data for required field.']}
        }}


def test_create_empty_listing(test_context, client, seed_community: Community, seed_user: User):
    json_args = {
        "community_id": seed_community.id,
        "listed_by_id": seed_user.id,
        "status": "active",
        "listing_type": "empty",
        "sale_type": "sell",
        "listing_price_cents": 199,
        "listing_title": "Test List",
        "listing_desc": "",
        "available_count": 1,
    }
    with test_context:
        create_response = client.post("/marketplace/api/listing/create", json=json_args)

        assert create_response.status_code == 200
        listing = create_response.json.get("listing")
        assert listing.get("listing_type") == "empty"
        assert listing.get("listing_title") == "Test List"


def test_create_item_listing(test_context, client, seed_community: Community, seed_user: User, seed_source_item: SourceItem):
    json_args = {
        "community_id": seed_community.id,
        "listed_by_id": seed_user.id,
        "status": "active",
        "listing_type": "item",
        "sale_type": "sell",
        "listing_price_cents": 10099,
        "listing_title": "Sneaker",
        "listing_desc": "",
        "available_count": 1,
        "source_item_id": seed_source_item.id,
        "item_name": "My broken sneakers",
        "condition": "acceptable",
        "photos": [],
        "shipping_zipcode": "94115",
        "item_details": '{"size": 14}',
    }
    with test_context:
        create_response = client.post("/marketplace/api/listing/create", json=json_args)
        assert create_response.status_code == 200
        listing = create_response.json.get("listing")
        assert listing.get("listing_type") == "item"
        assert listing.get("listing_title") == "Sneaker"
        item = create_response.json.get("item")
        assert item.get("item_name") == "My broken sneakers"
        assert item.get("source_item_id") == seed_source_item.id.hex
        item_details = json.loads(item.get("item_details"))
        assert item_details.get("size") == 14


def test_create_lodging_listing(test_context, client, seed_community: Community, seed_user: User):
    json_args = {
        "community_id": seed_community.id,
        "listed_by_id": seed_user.id,
        "status": "active",
        "listing_type": "lodging",
        "sale_type": "book",
        "listing_price_cents": 20099,
        "listing_title": "Hotel Room",
        "listing_desc": "",
        "available_count": 1,
        "lodging_name": "Hilton",
        "address": "1 Main St",
        "start_date": "2024-01-01",
        "end_date": "2024-02-01",
        "lodging_type": "hotel",
        "lodging_url": "http://hilton.com/",
        "lodging_details": '{"parking": "no"}',
    }
    with test_context:
        create_response = client.post("/marketplace/api/listing/create", json=json_args)

        assert create_response.status_code == 200
        listing = create_response.json.get("listing")
        assert listing.get("listing_type") == "lodging"
        assert listing.get("listing_title") == "Hotel Room"
        lodging = create_response.json.get("lodging")
        assert lodging.get("lodging_name") == "Hilton"
        lodging_details = json.loads(lodging.get("lodging_details"))
        assert lodging_details.get("parking") == "no"
