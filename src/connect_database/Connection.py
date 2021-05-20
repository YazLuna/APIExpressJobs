import mysql.connector
from mysql.connector import Error

from src.configuration.config_server import ConfigServer


class Connection:
	static_host = ""
	static_database = ""
	static_user = ""
	static_password = ""

	def __init__(self, host=None, database=None, user=None, password=None):
		if host is not None:
			self.user = user
			self.password = password
			self.database = database
			self.host = host
		elif Connection.static_host != "":
			self.host = Connection.static_host
			self.database = Connection.static_database
			self.user = Connection.static_user
			self.password = Connection.static_password

	@staticmethod
	def build_from_static():
		connection = None
		if Connection.static_host == "":
			config_server = ConfigServer("expressjobs")
			results = config_server.patch(["db_name", "db_host", "db_user", "db_password"]).json()

			Connection.static_host = results["db_host"]
			Connection.static_database = results["db_name"]
			Connection.static_user = results["db_user"]
			Connection.static_password = results["db_password"]

			connection = Connection()
			connection.host = results["db_host"]
			connection.database = results["db_name"]
			connection.user = results["db_user"]
			connection.password = results["db_password"]
		elif Connection.static_host != "":
			connection = Connection()
			connection.host = Connection.static_host
			connection.database = Connection.static_database
			connection.user = Connection.static_user
			connection.password = Connection.static_password
		return connection

	def connect(self, include_params: bool = False):
		self.connection = mysql.connector.connect(
			host=self.host,
			database=self.database,
			user=self.user,
			password=self.password
		)
		return self.connection.cursor(prepared=include_params)

	def close_connection(self):
		if self.connection.is_connected():
			self.connection.close()

	def send_query(self, query, values: list = None):
		executed = False
		if self.host is not None:
			parameters: tuple = ()
			try:
				if values is not None:
					cursor = self.connect(True)
					parameters = tuple(values)
				else:
					cursor = self.connect()
				cursor.execute(query, parameters)
				self.connection.commit()
				executed = True
			except Error as error:
				print(f"Problem connecting to the database: {error}")
			finally:
				self.close_connection()
		return executed

	def select(self, query, values: list = None):
		results = []
		if self.host is not None:
			parameters: tuple = ()
			try:
				if values is not None:
					cursor = self.connect(True)
					parameters = tuple(values)
				else:
					cursor = self.connect(False)
				cursor.execute(query, parameters)
				tmp_results = cursor.fetchall()
				for row in tmp_results:
					results.append(dict(zip(cursor.column_names, row)))
			except Error as error:
				print(f"Problem connecting to the database: {error}")
			finally:
				self.close_connection()
		return results
