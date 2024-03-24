from webargs import ValidationError

LISTING_TYPES = ["item", "lodging", "empty"]
LISTING_STATUSES = ["draft", "active", "suspended", "sold", "closed", "rejected", "spam"]
SALE_TYPES = ["sell", "rent", "book", "trade", "free"]
CONDITIONS = ["n/a", "new", "excellent", "very good", "good", "acceptable", "damaged"]
LODGING_TYPES = ["hotel", "airbnb", "cruise"]


def validate_listing_status(val: str):
    if val not in LISTING_STATUSES:
        raise ValidationError("Listing status doesn't exist")


def validate_listing_type(val: str):
    if val not in LISTING_TYPES:
        raise ValidationError("Listing type doesn't exist")


def validate_sale_type(val: str):
    if val not in SALE_TYPES:
        raise ValidationError("Sale type doesn't exist")


def validate_condition(val: str):
    if val not in CONDITIONS:
        raise ValidationError("Condition doesn't exist")


def validate_lodging_type(val: str):
    if val not in LODGING_TYPES:
        raise ValidationError("Lodging type doesn't exist")


def validate_create_listing(listing_dict: dict):
    """TODO:
        * confirm listed_by_id is the current user in session
        * confirm the user is a valid within the listing's community
        * confirm the user has marketplace listing priviledges within the community
    """
    pass
    # raise ValidationError("User does not have permission to create this listing.")
