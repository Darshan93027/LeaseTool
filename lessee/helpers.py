from datetime import timedelta
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from datetime import timedelta
from datetime import datetime, time

def calculate_price(tool, start_date, end_date, is_overdue=False):
    """
    Helper to calculate tool usage price based on daily/hourly rate.
    Night hours (12AM–6AM) are excluded in hourly mode.
    """
    base_price = 0
    hours = 0
    days = 0

    # Ensure start_date and end_date are date objects
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime):
        end_date = end_date.date()

    if tool.price_type == 'daily':
        # Calculate the number of days between start_date and end_date
        days = (end_date - start_date).days or 1  # Ensure there's at least 1 day
        base_price = tool.price * days

    elif tool.price_type == 'hourly':
        current = start_date
        while current < end_date:
            if 6 <= current.hour < 18:  # only count daytime hours
                hours += 1
            current += timedelta(hours=1)
        base_price = tool.price * hours

    # Extra charge if overdue
    extra_charge = base_price * 0.05 if is_overdue else 0
    total_price = base_price + extra_charge

    return {
        "base_price": round(base_price, 2),
        "extra_charge": round(extra_charge, 2),
        "total_price": round(total_price, 2),
        "days": days,
        "hours": hours
    }

def update_lessee_overdue_and_price(lessee):
    """
    Updates lessee with overdue info and recalculated pricing.
    """
    now = timezone.now()
    today = now.date()

    tool = lessee.tool if hasattr(lessee, 'tool') else None
    if not tool:
        try:
            from tool.models import Tool
            tool = Tool.objects.get(tool_code=lessee.tool_code)
        except Exception:
            return {}

    # Ensure return_date is a datetime or fallback to now
    end_date = lessee.return_date or now
    end_date = end_date if isinstance(end_date, datetime) else datetime.combine(end_date, time.min)

    is_overdue = end_date.date() < today

    # Set overdue fields
    if is_overdue:
        lessee.tool_status = 'Overdue'
        lessee.is_overdue = True
        lessee.overdue_date = now
        lessee.overdue_days = (today - end_date.date()).days
    else:
        lessee.is_overdue = False
        lessee.overdue_days = 0

    # Calculate and update price info
    price_data = calculate_price(tool, lessee.start_date, end_date, is_overdue=is_overdue)

    lessee.price = price_data['base_price']
    lessee.extra_charge = price_data['extra_charge']
    lessee.total_price = price_data['total_price']

    lessee.save(update_fields=[
        'tool_status', 'is_overdue', 'overdue_date', 'overdue_days',
        'price', 'extra_charge', 'total_price'
    ])

    return price_data
