# coding: utf-8

"""
    Kipartman

    Kipartman api specifications

    OpenAPI spec version: 1.0.0
    Contact: --
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class PartNew(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, comment=None, octopart=None, updated=None, category=None, childs=None, footprint=None, parameters=None, distributors=None, manufacturers=None):
        """
        PartNew - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'comment': 'str',
            'octopart': 'str',
            'updated': 'datetime',
            'category': 'PartCategoryRef',
            'childs': 'list[PartRef]',
            'footprint': 'FootprintRef',
            'parameters': 'list[PartParameter]',
            'distributors': 'list[PartDistributor]',
            'manufacturers': 'list[PartManufacturer]'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'comment': 'comment',
            'octopart': 'octopart',
            'updated': 'updated',
            'category': 'category',
            'childs': 'childs',
            'footprint': 'footprint',
            'parameters': 'parameters',
            'distributors': 'distributors',
            'manufacturers': 'manufacturers'
        }

        self._name = name
        self._description = description
        self._comment = comment
        self._octopart = octopart
        self._updated = updated
        self._category = category
        self._childs = childs
        self._footprint = footprint
        self._parameters = parameters
        self._distributors = distributors
        self._manufacturers = manufacturers

    @property
    def name(self):
        """
        Gets the name of this PartNew.

        :return: The name of this PartNew.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PartNew.

        :param name: The name of this PartNew.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this PartNew.

        :return: The description of this PartNew.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PartNew.

        :param description: The description of this PartNew.
        :type: str
        """

        self._description = description

    @property
    def comment(self):
        """
        Gets the comment of this PartNew.

        :return: The comment of this PartNew.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """
        Sets the comment of this PartNew.

        :param comment: The comment of this PartNew.
        :type: str
        """

        self._comment = comment

    @property
    def octopart(self):
        """
        Gets the octopart of this PartNew.

        :return: The octopart of this PartNew.
        :rtype: str
        """
        return self._octopart

    @octopart.setter
    def octopart(self, octopart):
        """
        Sets the octopart of this PartNew.

        :param octopart: The octopart of this PartNew.
        :type: str
        """

        self._octopart = octopart

    @property
    def updated(self):
        """
        Gets the updated of this PartNew.

        :return: The updated of this PartNew.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """
        Sets the updated of this PartNew.

        :param updated: The updated of this PartNew.
        :type: datetime
        """

        self._updated = updated

    @property
    def category(self):
        """
        Gets the category of this PartNew.

        :return: The category of this PartNew.
        :rtype: PartCategoryRef
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this PartNew.

        :param category: The category of this PartNew.
        :type: PartCategoryRef
        """

        self._category = category

    @property
    def childs(self):
        """
        Gets the childs of this PartNew.

        :return: The childs of this PartNew.
        :rtype: list[PartRef]
        """
        return self._childs

    @childs.setter
    def childs(self, childs):
        """
        Sets the childs of this PartNew.

        :param childs: The childs of this PartNew.
        :type: list[PartRef]
        """

        self._childs = childs

    @property
    def footprint(self):
        """
        Gets the footprint of this PartNew.

        :return: The footprint of this PartNew.
        :rtype: FootprintRef
        """
        return self._footprint

    @footprint.setter
    def footprint(self, footprint):
        """
        Sets the footprint of this PartNew.

        :param footprint: The footprint of this PartNew.
        :type: FootprintRef
        """

        self._footprint = footprint

    @property
    def parameters(self):
        """
        Gets the parameters of this PartNew.

        :return: The parameters of this PartNew.
        :rtype: list[PartParameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this PartNew.

        :param parameters: The parameters of this PartNew.
        :type: list[PartParameter]
        """

        self._parameters = parameters

    @property
    def distributors(self):
        """
        Gets the distributors of this PartNew.

        :return: The distributors of this PartNew.
        :rtype: list[PartDistributor]
        """
        return self._distributors

    @distributors.setter
    def distributors(self, distributors):
        """
        Sets the distributors of this PartNew.

        :param distributors: The distributors of this PartNew.
        :type: list[PartDistributor]
        """

        self._distributors = distributors

    @property
    def manufacturers(self):
        """
        Gets the manufacturers of this PartNew.

        :return: The manufacturers of this PartNew.
        :rtype: list[PartManufacturer]
        """
        return self._manufacturers

    @manufacturers.setter
    def manufacturers(self, manufacturers):
        """
        Sets the manufacturers of this PartNew.

        :param manufacturers: The manufacturers of this PartNew.
        :type: list[PartManufacturer]
        """

        self._manufacturers = manufacturers

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, PartNew):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
