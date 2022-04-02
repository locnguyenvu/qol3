import re
from datetime import datetime
from calendar import monthrange

class dt(object):

    TODAY = "today"
    CURRENT_MONTH = "current_month"

    @classmethod
    def time_range_from_text(cls, description) -> tuple:
        if description == cls.TODAY:
            carrytime = datetime.today()
            return (
                datetime(carrytime.year, carrytime.month, carrytime.day, 0, 0, 0),
                datetime(carrytime.year, carrytime.month, carrytime.day, 23, 59, 59)
            )
        if description == cls.CURRENT_MONTH:
            carrytime = datetime.today()
            month_range = monthrange(carrytime.year, carrytime.month)
            return (
                datetime(carrytime.year, carrytime.month, 1, 0, 0, 0),
                datetime(carrytime.year, carrytime.month, month_range[1], 23, 59, 59)
            )
        if re.match(r"^\d{4}\-\d{1,2}$", description) is not None:
            year, month = map(lambda e: int(e), description.split("-"))
            month_range = monthrange(year, month)
            return (
                datetime(year, month, 1, 0, 0, 0),
                datetime(year, month, month_range[1], 23, 59, 59)
            )

        return tuple()


class numbers(object):

    @classmethod
    def sipostfix_toint(cls, input:str) -> int:
        """
        Convert 
            1k => 1_000
            1M => 1_000_000
            1G => 1_000_000_000
        """
        carry = 0
        for i in range(len(input)):
            if input[i].isnumeric():
                carry = carry * 10
                carry = carry + int(input[i])

        # multiply with decimal prefix
        if input[-1].isalpha():
            decimal_prefix = input[-1]
            if decimal_prefix == "k":
                carry = carry * 1000
            elif decimal_prefix == "M":
                carry = carry * 1000_000
            elif decimal_prefix == "G":
                carry = carry * 1000_000_000
        return carry
    pass
