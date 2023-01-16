from django.utils.formats import number_format


def intspace(value, use_l10n=True):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    value_str = number_format(value, use_l10n=True, force_grouping=True)
    if len(value_str.split(',')) == 2:
        v, _v = value_str.split(',')
        return ','.join([v, _v[:1]])
    return value_str
