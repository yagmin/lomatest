from uuid import UUID
from flask import abort, request
import marshmallow
from webargs import fields
from webargs.flaskparser import parser
from sqlalchemy import and_, func
from marketplace.server import app, db
from marketplace.models import CommunityProfile, Item, Listing, ListingItem, ListingLodging, Lodging, SourceItem
import marketplace.api.validate as v
from marketplace.api.utils import json_dict, row_to_dict, row_to_json


def get_listing_item(listing_id: UUID):
    item = (
        db.session.query(
            Item.id,
            Item.item_name,
            Item.condition,
            Item.photos,
            Item.shipping_zipcode,
            Item.item_details,
            SourceItem.source_item_name,
            SourceItem.category_id,
            SourceItem.source_item_details,
        )
        .filter(ListingItem, ListingItem.listing_id == listing_id)
        .join(Item, ListingItem.item_id == Item.id)
        .outerjoin(SourceItem, SourceItem.id == Item.source_item_id)
    ).one_or_none()

    if item is None:
        return None

    return item


def get_listing_lodging(listing_id: UUID):
    lodging = (
        db.session.query(
            Lodging.id,
            Lodging.lodging_name,
            Lodging.address,
            Lodging.start_date,
            Lodging.end_date,
            Lodging.lodging_type,
            Lodging.lodging_url,
            Lodging.lodging_details,
        )
        .filter(ListingLodging, ListingLodging.listing_id == listing_id)
        .join(Lodging, ListingLodging.lodging_id == Lodging.id)
    ).one_or_none()

    if lodging is None:
        return None

    return lodging


@app.route("/marketplace/api/listing/<uuid:id>", methods=["GET"])
def get_listing(listing_id: UUID):
    listing = (
        db.session.query(
            Listing.id,
            Listing.listed_by_id,
            Listing.listed_on,
            Listing.status,
            Listing.listing_type,
            Listing.sale_type,
            Listing.listing_price_cents,
            Listing.listing_title,
            Listing.listing_desc,
            Listing.available_count,
            CommunityProfile.alias.label("listed_by_alias"),
        )
        .join(CommunityProfile, and_(
                CommunityProfile.community_id == Listing.community_id,
                CommunityProfile.user_id == Listing.listed_by_id,
            )
        )
    ).one_or_none()

    if listing is None:
        abort(404, description="listing does not exist")

    response = {
        "listing": row_to_dict(listing),
    }

    """
    General idea: each broad type of listing will have its own table and related metadata.
    This provides some structure to the listing types and can be extended easily for new types.
    The "details" JSON field in each type's table also allows a lot of extensibility and optional fields.
    Once a "sub-type" becomes popular or complex enough it can be spun off into a new listing type.
    """
    item = get_listing_item(listing_id) if listing.get("listing_type") == "item" else None
    if item is not None:
        response["item"] = row_to_dict(item)

    lodging = get_listing_lodging(listing_id) if listing.get("listing_type") == "lodging" else None
    if lodging is not None:
        response["lodging"] = row_to_dict(lodging)

    return json_dict(response)


create_listing_args = {
    "community_id": fields.UUID(required=True),
    "listed_by_id": fields.UUID(required=True),
    "status": fields.Str(required=True, validate=v.validate_listing_status),
    "listing_type": fields.Str(required=True, validate=v.validate_listing_type),
    "sale_type": fields.Str(required=True, validate=v.validate_sale_type),
    "listing_price_cents": fields.Int(required=True),
    "listing_title": fields.Str(required=True),
    "listing_desc": fields.Str(),
    "available_count": fields.Int(required=True),
}

create_item_args = {
    "source_item_id": fields.UUID(),
    "item_name": fields.Str(required=True),
    "condition": fields.Str(required=True, validate=v.validate_condition),
    "photos": fields.List(fields.Raw()),
    "shipping_zipcode": fields.Str(required=True),
    "item_details": fields.Raw(),
}

create_lodging_args = {
    "lodging_name": fields.Str(required=True),
    "address": fields.Str(required=True),
    "start_date": fields.Date(required=True),
    "end_date": fields.Date(required=True),
    "lodging_type": fields.Str(required=True, validate=v.validate_lodging_type),
    "lodging_url": fields.Str(),
    "lodging_details": fields.Raw(),
}


def create_item(item_dict):
    item = Item(
        source_item_id=item_dict.get("source_item_id"),
        item_name=item_dict.get("item_name"),
        condition=item_dict.get("condition"),
        photos=item_dict.get("photos"),
        shipping_zipcode=item_dict.get("shipping_zipcode"),
        item_details=item_dict.get("item_details"),
    )
    db.session.add(item)
    return item


def create_lodging(lodging_dict):
    lodging = Lodging(
        lodging_name=lodging_dict.get("lodging_name"),
        address=lodging_dict.get("address"),
        start_date=lodging_dict.get("start_date"),
        end_date=lodging_dict.get("end_date"),
        lodging_type=lodging_dict.get("lodging_type"),
        lodging_url=lodging_dict.get("lodging_url"),
        lodging_details=lodging_dict.get("lodging_details"),
    )
    db.session.add(lodging)
    return lodging


@app.route("/marketplace/api/listing/create", methods=["POST"])
def create_listing() -> str:
    listing_dict = parser.parse(create_listing_args, request, unknown=marshmallow.EXCLUDE)

    v.validate_create_listing(listing_dict)

    listed_on = func.now() if listing_dict.get("status") == "active" else None

    listing = Listing(
        community_id=listing_dict.get("community_id"),
        listed_by_id=listing_dict.get("listed_by_id"),
        listed_on=listed_on,
        status=listing_dict.get("status"),
        listing_type=listing_dict.get("listing_type"),
        sale_type=listing_dict.get("sale_type"),
        listing_price_cents=listing_dict.get("listing_price_cents", 0),
        listing_title=listing_dict.get("listing_title"),
        listing_desc=listing_dict.get("listing_desc"),
        available_count=listing_dict.get("available_count"),
    )
    db.session.add(listing)

    if listing_dict.get("listing_type") == "item":
        item_dict = parser.parse(create_item_args, request, unknown=marshmallow.EXCLUDE)
        item = create_item(item_dict)
        db.session.flush()

        listing_item = ListingItem(
            listing_id=listing.id,
            item_id=item.id,
        )
        db.session.add(listing_item)

    if listing_dict.get("listing_type") == "lodging":
        lodging_dict = parser.parse(create_lodging_args, request, unknown=marshmallow.EXCLUDE)
        lodging = create_lodging(lodging_dict)
        db.session.flush()

        listing_lodging = ListingLodging(
            listing_id=listing.id,
            lodging_id=lodging.id,
        )
        db.session.add(listing_lodging)

    db.session.commit()
    db.session.refresh(listing)

    response = {}
    response["listing"] = row_to_dict(listing)
    if listing_dict.get("listing_type") == "item":
        db.session.refresh(item)
        response["item"] = row_to_dict(item)
    if listing_dict.get("listing_type") == "lodging":
        db.session.refresh(lodging)
        response["lodging"] = row_to_dict(lodging)

    return json_dict(response)
