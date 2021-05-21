# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from src.communication_structs.base_model_ import Model
from src.routes import util


class InlineResponse2001(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, rating: int=None):  # noqa: E501
        """InlineResponse2001 - a model defined in Swagger

        :param rating: The rating of this InlineResponse2001.  # noqa: E501
        :type rating: int
        """
        self.swagger_types = {
            'rating': int
        }

        self.attribute_map = {
            'rating': 'rating'
        }
        self._rating = rating

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse2001':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200_1 of this InlineResponse2001.  # noqa: E501
        :rtype: InlineResponse2001
        """
        return util.deserialize_model(dikt, cls)

    @property
    def rating(self) -> int:
        """Gets the rating of this InlineResponse2001.

        rating  # noqa: E501

        :return: The rating of this InlineResponse2001.
        :rtype: int
        """
        return self._rating

    @rating.setter
    def rating(self, rating: int):
        """Sets the rating of this InlineResponse2001.

        rating  # noqa: E501

        :param rating: The rating of this InlineResponse2001.
        :type rating: int
        """

        self._rating = rating