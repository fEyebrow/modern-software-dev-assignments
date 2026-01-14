from fastapi import HTTPException
from sqlalchemy import UnaryExpression, asc, desc
from sqlalchemy.orm import DeclarativeBase


def parse_sort_param(
    sort: str,
    model: type[DeclarativeBase],
    allowed_fields: set[str],
) -> UnaryExpression:
    """Parse a sort parameter and return a SQLAlchemy order_by clause.

    Args:
        sort: Sort string, optionally prefixed with '-' for descending order.
        model: SQLAlchemy model class to get the column from.
        allowed_fields: Set of field names that are valid for sorting.

    Returns:
        SQLAlchemy UnaryExpression for use in order_by().

    Raises:
        HTTPException: If the sort field is not in allowed_fields.
    """
    field = sort.lstrip("-")

    if field not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field: {field}. Allowed fields: {', '.join(sorted(allowed_fields))}",
        )

    order_fn = desc if sort.startswith("-") else asc
    return order_fn(getattr(model, field))
