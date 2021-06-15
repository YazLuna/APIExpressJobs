"""This module manages the countries."""
from src.connect_database.connection_database import Connection
from src.routes.responses_rest import ResponsesREST


class Country:
    """This class manages the countries."""

    def __init__(self):
        self.id_country = ""
        self.name = ""
        self.connect = Connection.build_from_static()

    def get_country(self):
        """This function sets a country according to your ID."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCountry, name FROM Country WHERE idCountry = %s;"
        param = [self.id_country]
        countries = self.connect.select(query, param)
        if countries:
            country = Country()
            country_found = countries[0]
            country.name = country_found["name"]
            country.id_country = country_found["idCountry"]
            results = country
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def find_countries(self):
        """This function finds all countries."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCountry, name FROM Country;"
        list_countries = self.connect.select(query)
        if list_countries:
            countries_list = []
            for countries in list_countries:
                country = Country()
                country.id_country = countries["idCountry"]
                country.name = countries["name"]
                countries_list.append(country)
            results = countries_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_country(self):
        """This function returns the country data in JSON serializable format."""
        return {"idCountry": self.id_country, "name": self.name}
