import uuid
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import PrimaryKeyConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from marketplace.server import db


class Community(db.Model):
    """
    Each community is a different Loma instance.
    """
    __tablename__ = "communities"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    name = db.Column(db.String(128))
    uri = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=func.now())


class User(db.Model):
    """stores user data"""
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password_hash = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class CommunityProfile(db.Model):
    """community-specific details for a user"""
    community_id = db.Column(UUID(as_uuid=True), db.ForeignKey('communities.id'), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    alias = db.Column(db.String)
    active_since = db.Column(db.Date, default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('community_id', 'user_id'),
    )


class Listing(db.Model):
    """
    Listing is a marketplace record posted by a user within a community.
    Generally used for selling individual, physical items, but can be used to represent any transactional
    listing.
    """
    __tablename__ = "listings"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    community_id = db.Column(UUID(as_uuid=True), db.ForeignKey('communities.id'))
    listed_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=func.now())
    listed_on = db.Column(db.DateTime)
    closed_on = db.Column(db.DateTime)
    # status is basically an enum, but keeping as a string for simplicity as enums
    # are hard to revise in production and not worth the minor indexing boost unless at scale.
    # possible statuses: draft/active/suspended/sold/closed/rejected/spam
    status = db.Column(db.String(20), nullable=False, default="draft")
    # another enum, each entry mapped to a different table that stores more precise details of the listing
    # listing types: item, lodging, digital_item, multiple_item, shared_item, etc.
    listing_type = db.Column(db.String(20), nullable=False)
    # sale types: sell, rent, trade, free
    sale_type = db.Column(db.String(20), nullable=False)
    listing_price_cents = db.Column(db.Integer)
    listing_title = db.Column(db.String(100), nullable=False)
    listing_desc = db.Column(db.Text)
    available_count = db.Column(db.Integer, nullable=False, default=1)


class Category(db.Model):
    """
    Nested category structure. This allows assign the most specific category to an item.
    i.e. "Retro 4" and we can walk up the parent categories to see: Sneaker brands > Nike > Air Jordan > Retro 4
    """
    __tablename__ = "categories"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    name = db.Column(db.String(100))
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'))


class SourceItem(db.Model):
    """
    The common details of an item, distinct from a particular instance of it.
    """
    __tablename__ = "source_items"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    source_item_name = db.Column(db.String)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'))
    # leaving this wide open as a JSON blob, as this may hold all the metadata of an item
    # or simply be an API link to an outside source that holds the data.
    source_item_details = db.Column(db.JSON)


class Item(db.Model):
    """
    Single, physical items in marketplace.
    This implies condition, shipping upon sale, and details of the make/model, photos.
    """
    __tablename__ = "items"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    source_item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('source_items.id'))
    item_name = db.Column(db.String)
    condition = db.Column(db.String(20), nullable=False, default="n/a")
    # both photos and shipping location should be in separate tables, but simplifying for time here
    # photos stores image metadata and file locations
    photos = db.Column(db.JSON)
    # needed to calculate shipping
    shipping_zipcode = db.Column(db.String)
    # if the table columns are known data about all items, this JSON allows flexible data to be stored
    # for unexpected item details. My general plan would be to harden certain fields here into new tables/columns
    # based on usage. The near term cost is minor performance and data obscurity, but it provides a flexible
    # structure to handle entirely new item categories without causing backend changes.
    item_details = db.Column(db.JSON)
    

class ListingItem(db.Model):
    """
    Maps listings and items.
    """
    __tablename__ = "listing_items"
    listing_id = db.Column(UUID(as_uuid=True), db.ForeignKey('listings.id'), primary_key=True)
    item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.id'), primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('listing_id', 'item_id'),
    )


class Lodging(db.Model):
    """
    Lodging in marketplace.
    This implies lodging address, start/end dates, lodging type, an external URL.
    """
    __tablename__ = "lodgings"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    # ideally, addresses would be stored in a location table for easier mapping
    lodging_name= db.Column(db.String)
    address = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    lodging_type = db.Column(db.String)
    lodging_url = db.Column(db.String)
    lodging_details = db.Column(db.JSON)


class ListingLodging(db.Model):
    """
    Maps listings and lodgings
    """
    __tablename__ = "listing_lodgings"
    listing_id = db.Column(UUID(as_uuid=True), db.ForeignKey('listings.id'), primary_key=True)
    lodging_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lodgings.id'), primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('listing_id', 'lodging_id'),
    )
