# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from src.communication_structs.base_model_ import Model
from src.communication_structs.report import Report  # noqa: F401,E501
from src.routes import util


class InlineResponse200(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, reports: List[Report]=None):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger

        :param reports: The reports of this InlineResponse200.  # noqa: E501
        :type reports: List[Report]
        """
        self.swagger_types = {
            'reports': List[Report]
        }

        self.attribute_map = {
            'reports': 'reports'
        }
        self._reports = reports

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse200':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200 of this InlineResponse200.  # noqa: E501
        :rtype: InlineResponse200
        """
        return util.deserialize_model(dikt, cls)

    @property
    def reports(self) -> List[Report]:
        """Gets the reports of this InlineResponse200.


        :return: The reports of this InlineResponse200.
        :rtype: List[Report]
        """
        return self._reports

    @reports.setter
    def reports(self, reports: List[Report]):
        """Sets the reports of this InlineResponse200.


        :param reports: The reports of this InlineResponse200.
        :type reports: List[Report]
        """

        self._reports = reports
