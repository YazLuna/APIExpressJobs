# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from src.communication_structs.base_model_ import Model
from src.communication_structs.country import Country  # noqa: F401,E501
from src.routes import util


class State(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, name: str=None, country: Country=None):  # noqa: E501
        """State - a model defined in Swagger

        :param id: The id of this State.  # noqa: E501
        :type id: int
        :param name: The name of this State.  # noqa: E501
        :type name: str
        :param country: The country of this State.  # noqa: E501
        :type country: Country
        """
        self.swagger_types = {
            'id': int,
            'name': str,
            'country': Country
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'country': 'country'
        }
        self._id = id
        self._name = name
        self._country = country

    @classmethod
    def from_dict(cls, dikt) -> 'State':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The State of this State.  # noqa: E501
        :rtype: State
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this State.

        ID of State  # noqa: E501

        :return: The id of this State.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this State.

        ID of State  # noqa: E501

        :param id: The id of this State.
        :type id: int
        """

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this State.

        name of state  # noqa: E501

        :return: The name of this State.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this State.

        name of state  # noqa: E501

        :param name: The name of this State.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def country(self) -> Country:
        """Gets the country of this State.


        :return: The country of this State.
        :rtype: Country
        """
        return self._country

    @country.setter
    def country(self, country: Country):
        """Sets the country of this State.


        :param country: The country of this State.
        :type country: Country
        """

        self._country = country
