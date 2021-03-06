# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model as BaseModel
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class StorageData(BaseModel):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, comment=None):
        """
        StorageData - a model defined in Swagger

        :param name: The name of this StorageData.
        :type name: str
        :param description: The description of this StorageData.
        :type description: str
        :param comment: The comment of this StorageData.
        :type comment: str
        """
        self.swagger_types = {
            'name': str,
            'description': str,
            'comment': str
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'comment': 'comment'
        }

        self._name = name
        self._description = description
        self._comment = comment

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The StorageData of this StorageData.
        :rtype: StorageData
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this StorageData.

        :return: The name of this StorageData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this StorageData.

        :param name: The name of this StorageData.
        :type name: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this StorageData.

        :return: The description of this StorageData.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this StorageData.

        :param description: The description of this StorageData.
        :type description: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this StorageData.

        :return: The comment of this StorageData.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this StorageData.

        :param comment: The comment of this StorageData.
        :type comment: str
        """

        self._comment = comment

