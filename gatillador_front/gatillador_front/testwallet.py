import oracledb

ORA_CONFIG=r'C:\Users\Pancho\Documents\Programacion\Axway\gatillador_front\ORA_CONFIG'
CREDENTIAL_ALIAS='Desarrollo'

oracledb.init_oracle_client(config_dir=ORA_CONFIG)
with oracledb.connect(externalauth=True, dsn=CREDENTIAL_ALIAS) as connection:
    with connection.cursor() as cursor:
        cursor = connection.cursor()
        cursor_data = connection.cursor()
        cursor.callproc("PROC_OBTENER_USUARIOS_VENCIMIENTO_PASSWORD", [cursor_data])
        cursor_data = cursor.fetchone()[0]
        print(cursor_data)





    

