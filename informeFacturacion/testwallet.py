import oracledb

ORA_CONFIG = r'C:\Users\Pancho\Documents\Programacion\Axway\gatillador_front\ORA_CONFIG'
CREDENTIAL_ALIAS = 'Desarrollo'

oracledb.init_oracle_client(config_dir=ORA_CONFIG)
with oracledb.connect(externalauth=True, dsn=CREDENTIAL_ALIAS) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT SYSDATE FROM dual")
        sysdate = cursor.fetchone()[0]
        print("La fecha y hora actual de la base de datos es:", sysdate)




    

