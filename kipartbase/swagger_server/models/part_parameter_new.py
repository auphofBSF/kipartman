# coding: utf-8

from __future__ import absolute_import
from swagger_server.models.part_parameter_data import PartParameterData
from swagger_server.models.unit import Unit
from swagger_server.models.unit_prefix import UnitPrefix
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class PartParameterNew(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, unit=None, numeric=None, text_value=None, min_prefix=None, nom_prefix=None, max_prefix=None):
        """
        PartParameterNew - a model defined in Swagger

        :param name: The name of this PartParameterNew.
        :type name: str
        :param description: The description of this PartParameterNew.
        :type description: str
        :param unit: The unit of this PartParameterNew.
        :type unit: Unit
        :param numeric: The numeric of this PartParameterNew.
        :type numeric: bool
        :param text_value: The text_value of this PartParameterNew.
        :type text_value: str
        :param min_prefix: The min_prefix of this PartParameterNew.
        :type min_prefix: UnitPrefix
        :param nom_prefix: The nom_prefix of this PartParameterNew.
        :type nom_prefix: UnitPrefix
        :param max_prefix: The max_prefix of this PartParameterNew.
        :type max_prefix: UnitPrefix
        """
        self.swagger_types = {
            'name': str,
            'description': str,
            'unit': Unit,
            'numeric': bool,
            'text_value': str,
            'min_prefix': UnitPrefix,
            'nom_prefix': UnitPrefix,
            'max_prefix': UnitPrefix
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'unit': 'unit',
            'numeric': 'numeric',
            'text_value': 'text_value',
            'min_prefix': 'min_prefix',
            'nom_prefix': 'nom_prefix',
            'max_prefix': 'max_prefix'
        }

        self._name = name
        self._description = description
        self._unit = unit
        self._numeric = numeric
        self._text_value = text_value
        self._min_prefix = min_prefix
        self._nom_prefix = nom_prefix
        self._max_prefix = max_prefix

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PartParameterNew of this PartParameterNew.
        :rtype: PartParameterNew
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this PartParameterNew.

        :return: The name of this PartParameterNew.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PartParameterNew.

        :param name: The name of this PartParameterNew.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this PartParameterNew.

        :return: The description of this PartParameterNew.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PartParameterNew.

        :param description: The description of this PartParameterNew.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")

        self._description = description

    @property
    def unit(self):
        """
        Gets the unit of this PartParameterNew.

        :return: The unit of this PartParameterNew.
        :rtype: Unit
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """
        Sets the unit of this PartParameterNew.

        :param unit: The unit of this PartParameterNew.
        :type unit: Unit
        """

        self._unit = unit

    @property
    def numeric(self):
        """
        Gets the numeric of this PartParameterNew.

        :return: The numeric of this PartParameterNew.
        :rtype: bool
        """
        return self._numeric

    @numeric.setter
    def numeric(self, numeric):
        """
        Sets the numeric of this PartParameterNew.

        :param numeric: The numeric of this PartParameterNew.
        :type numeric: bool
        """
        if numeric is None:
            raise ValueError("Invalid value for `numeric`, must not be `None`")

        self._numeric = numeric

    @property
    def text_value(self):
        """
        Gets the text_value of this PartParameterNew.

        :return: The text_value of this PartParameterNew.
        :rtype: str
        """
        return self._text_value

    @text_value.setter
    def text_value(self, text_value):
        """
        Sets the text_value of this PartParameterNew.

        :param text_value: The text_value of this PartParameterNew.
        :type text_value: str
        """

        self._text_value = text_value

    @property
    def min_prefix(self):
        """
        Gets the min_prefix of this PartParameterNew.

        :return: The min_prefix of this PartParameterNew.
        :rtype: UnitPrefix
        """
        return self._min_prefix

    @min_prefix.setter
    def min_prefix(self, min_prefix):
        """
        Sets the min_prefix of this PartParameterNew.

        :param min_prefix: The min_prefix of this PartParameterNew.
        :type min_prefix: UnitPrefix
        """

        self._min_prefix = min_prefix

    @property
    def nom_prefix(self):
        """
        Gets the nom_prefix of this PartParameterNew.

        :return: The nom_prefix of this PartParameterNew.
        :rtype: UnitPrefix
        """
        return self._nom_prefix

    @nom_prefix.setter
    def nom_prefix(self, nom_prefix):
        """
        Sets the nom_prefix of this PartParameterNew.

        :param nom_prefix: The nom_prefix of this PartParameterNew.
        :type nom_prefix: UnitPrefix
        """

        self._nom_prefix = nom_prefix

    @property
    def max_prefix(self):
        """
        Gets the max_prefix of this PartParameterNew.

        :return: The max_prefix of this PartParameterNew.
        :rtype: UnitPrefix
        """
        return self._max_prefix

    @max_prefix.setter
    def max_prefix(self, max_prefix):
        """
        Sets the max_prefix of this PartParameterNew.

        :param max_prefix: The max_prefix of this PartParameterNew.
        :type max_prefix: UnitPrefix
        """

        self._max_prefix = max_prefix
