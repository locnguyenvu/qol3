
class numbers(object):
    GENERAL_THOUSAND_SEPARATOR = ","
    GENERAL_DECIMAL_POINT = "."

    VN_THOUSAND_SEPARATOR = "."
    VN_DECIMAL_POINT = ","

    @classmethod
    def float_(cls, input: str, precision=2) -> float:
        """
        Convert 76,098.37 => float(76098.37)
        """
        number = input.replace(cls.GENERAL_THOUSAND_SEPARATOR, "")
        return round(float(number), precision)

    @classmethod
    def vncurrencyformat_tofloat(cls, input: str, precision=2) -> float:
        """
        Convert 76.098,37 => float(76098.37)
        """
        # remove thousand separator
        parts = input.split(cls.VN_DECIMAL_POINT)
        number_part = parts[0].replace(cls.VN_THOUSAND_SEPARATOR, "")
        if len(parts) == 2:
            number = f"{number_part}.{parts[1]}"
        else:
            number = number_part
        return round(float(number), precision)

    pass
