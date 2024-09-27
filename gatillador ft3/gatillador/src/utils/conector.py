import oracledb

from utils.constants import CREDENTIAL_ALIAS, ORA_CONFIG_DIRECTORY

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.connection = self._connect_to_database()

    def _connect_to_database(self):
        oracledb.init_oracle_client(config_dir=ORA_CONFIG_DIRECTORY)
        return oracledb.connect(externalauth=True, dsn=CREDENTIAL_ALIAS)

    def get_connection(self):
        return self.connection