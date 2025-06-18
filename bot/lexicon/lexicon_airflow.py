from environs import Env

env = Env()
env.read_env()

LEXICON_CONNECTION_TYPE: dict[str, str] = {
    'AMAZON_ATHENA': 'athena',
    'AMAZON_CHIME_WEBHOOK': 'chime',
    'AMAZON_ELASTIC_MAPREDUCE': 'emr',
    'AMAZON_REDSHIFT': 'redshift',
    'AMAZON_WEB_SERVICES': 'aws',
    'AZURE': 'azure',
    'AZURE_BATCH_SERVICE': 'azure_batch',
    'Azure Blob Storage': 'wasb',
    'AZURE_CONTAINER_INSTANCE': 'azure_container_instance',
    'AZURE_CONTAINER_REGISTRY': 'azure_container_registry',
    'AZURE_CONTAINER_VOLUME': 'azure_container_volume',
    'AZURE_COSMOS_DB': 'azure_cosmos',
    'AZURE_DATA_EXPLORER': 'azure_data_explorer',
    'AZURE_DATA_FACTORY': 'azure_data_factory',
    'AZURE_DATA_LAKE': 'azure_data_lake',
    'AZURE_DATE_LAKE_STORAGE_V2': 'adls',
    'AZURE_FILESHARE': 'azure_fileshare',
    'AZURE_SERVICE_BUS': 'azure_service_bus',
    'AZURE_SYNAPSE': 'azure_synapse',
    'DOCKER': 'docker',
    'Elasticsearch': 'elasticsearch',
    'EMAIL': 'email',
    'FTP': 'ftp',
    'FILE_(PATH)': 'fs',
    'GRPC_CONNECTION': 'grpc',
    'GENERIC': 'generic',
    'GOOGLE_BIGQUERY': 'gcpbigquery',
    'GOOGLE_CLOUD': 'google_cloud_platform',
    'GOOGLE_CLOUD_SQL': 'gcpcloudsql',
    'GOOGLE_CLOUD_SQL_DATABASE': 'gcpcloudsqldb',
    'GOOGLE_CLOUD_SSH': 'gcpssh',
    'GOOGLE_DATAPREP': 'dataprep',
    'HTTP': 'http',
    'HASHICORP_VAULT': 'vault',
    'IMAP': 'imap',
    'KUBERNETES_CLUSTER_CONNECTION': 'kubernetes',
    'MYSQL': 'mysql',
    'ODBC': 'odbc',
    'PACKAGE_INDEX_(PYTHON)': 'package_index',
    'POSTGRES': 'postgres',
    'POWER_BI': 'powerbi',
    'REDIS': 'redis',
    'SFTP': 'sftp',
    'SMTP': 'smtp',
    'SSH': 'ssh',
    'SLACK_API': 'slack',
    'SLACK_INCOMING_WEBHOOK': 'slackwebhook',
    'SNOWFLAKE': 'snowflake',
    'SQLITE': 'sqlite'
}


LEXICON_URL: dict[str, str] = {
    'AIRFLOW_URL': env.str('AIRFLOW_URL'),
    'API_CREATE_CONNECTION': env.str('API_CREATE_CONNECTION'),
    'API_UPDATE_CONNECTION': env.str('API_UPDATE_CONNECTION'),
    'API_INFO_AND_START_DAG': env.str('API_INFO_AND_START_DAG'),
    'API_RUN_DAG': env.str('API_RUN_DAG')
}

LEXICON_DATA: dict[str, str] = {
    'USER': env.str('USER'),
    'PASSWORD': env.str('PASSWORD')
}