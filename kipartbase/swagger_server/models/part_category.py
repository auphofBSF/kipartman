# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.part_category_data import PartCategoryData
from swagger_server.models.part_category_ref import PartCategoryRef
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class PartCategory(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, id=None, parent=None, childs=None):
        """
        PartCategory - a model defined in Swagger

        :param name: The name of this PartCategory.
        :type name: str
        :param id: The id of this PartCategory.
        :type id: int
        :param parent: The parent of this PartCategory.
        :type parent: PartCategoryRef
        :param childs: The childs of this PartCategory.
        :type childs: List[PartCategory]
        """
        self.swagger_types = {
            'name': str,
            'id': int,
            'parent': PartCategoryRef,
            'childs': List[PartCategory]
        }

        self.attribute_map = {
            'name': 'name',
            'id': 'id',
            'parent': 'parent',
            'childs': 'childs'
        }

        self._name = name
        self._id = id
        self._parent = parent
        self._childs = childs

    @classmethod
    def from_dict(cls, dikt):
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PartCategory of this PartCategory.
        :rtype: PartCategory
        """
        return deserialize_model(dikt, cls)

    @property
    def name(self):
        """
        Gets the name of this PartCategory.

        :return: The name of this PartCategory.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PartCategory.

        :param name: The name of this PartCategory.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def id(self):
        """
        Gets the id of this PartCategory.

        :return: The id of this PartCategory.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PartCategory.

        :param id: The id of this PartCategory.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def parent(self):
        """
        Gets the parent of this PartCategory.

        :return: The parent of this PartCategory.
        :rtype: PartCategoryRef
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Sets the parent of this PartCategory.

        :param parent: The parent of this PartCategory.
        :type parent: PartCategoryRef
        """

        self._parent = parent

    @property
    def childs(self):
        """
        Gets the childs of this PartCategory.

        :return: The childs of this PartCategory.
        :rtype: List[PartCategory]
        """
        return self._childs

    @childs.setter
    def childs(self, childs):
        """
        Sets the childs of this PartCategory.

        :param childs: The childs of this PartCategory.
        :type childs: List[PartCategory]
        """

        self._childs = childs

