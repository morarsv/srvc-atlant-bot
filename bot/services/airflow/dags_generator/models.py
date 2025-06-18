from pydantic import BaseModel, RootModel
from typing import List, Optional, Dict


class DefaultArgs(BaseModel):
    owner: Optional[str] = None
    start_date: Optional[str] = None
    on_failure_callback: Optional[str] = None
    retries: Optional[str | int] = None
    retry_delay: Optional[str] = None


class TaskYaMetrika(BaseModel):
    operator: Optional[str] = None
    bash_command: Optional[str] = None
    python_callable_name: Optional[str] = None
    python_callable_module: Optional[str] = None
    doc: Optional[str] = None

    project: Optional[str] = None
    table_id: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    retries: Optional[int] = None
    ch_conn: Optional[str] = None
    dimensions: Optional[List[str]] = None
    metrics: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None
    yandex_metrica_conn_id: Optional[str] = None
    proxy: Optional[str] = None
    trigger_rule: Optional[str] = None


class TaskYaDirect(BaseModel):
    operator: Optional[str] = None
    bash_command: Optional[str] = None
    python_callable_name: Optional[str] = None
    python_callable_module: Optional[str] = None
    doc: Optional[str] = None

    project: Optional[str] = None
    table_id: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    clickhouse_con: Optional[str] = None
    yandex_direct_conn_id: Optional[str] = None
    field_names: Optional[List[str]] = None
    proxy: Optional[str] = None


class BaseBashTask(BaseModel):
    operator: Optional[str] = None
    bash_command: Optional[str] = None


class DAG(BaseModel):
    dag_id: str
    default_args: DefaultArgs
    schedule_interval: str
    tasks: Dict[str, TaskYaDirect | TaskYaMetrika | BaseBashTask]
    catchup: Optional[bool] = None
    concurrency: Optional[int] = None
    start_date: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class DAGConfig(RootModel):
    root: Dict[str, DAG]
