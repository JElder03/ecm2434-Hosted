"""
Author: Jamie Elder
"""

from django import forms


class CommaSeparatedStrings(forms.CharField):
    """
    An input class for forms consisting of string values separated by commas.
    Provides a method of stripping the commas and returning a list of string.
    """

    def to_python(self, value):
        """
        Strips the commas from the string and returns a list of strings.
        """
        if value in self.empty_values:
            return self.empty_value
        value = str(value).split(",")
        if self.strip:
            value = [s.strip() for s in value]
        return value

    def prepare_value(self, value):
        """
        Converts a list into a comma separated string
        """
        if value is None:
            return None
        return ", ".join([str(s) for s in value])
