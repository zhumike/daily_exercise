
# -*- coding: utf-8 -*-
# @Time    : 2023/7/2 1:50 PM
# @Author  : zhangsijian
import json
import os
import sys

import click
import pytest

from weekend_leo.core.base.case_meta import CaseBase
from weekend_leo.core.base.case_selector import case_map
from weekend_leo.core.storm.testbase.conf import settings
from weekend_leo.core.util.tos_util import TosClient


@click.group()
def leo():
    # 命令分组
    pass


@leo.command()
def version():
    return "0.0.1"


@leo.command()
def upload_dsl():
    tos_client = TosClient()
    tos_client.upload_file('../data/tmp_dsl.json', 'weekend_leo/tmp_dsl.json')


@leo.command()
@click.option('--leo-dsls', type=str, default='file://./data/tmp_dsl.json',
              help='DSL逗号分隔，支持file://./tmp_dsl.json')
@click.option('--leo-task-id', type=int, default=1, help='Leo Task ID 主ID')
@click.option('--leo-step-list', type=str,
              default="""[{"stepIx":0,"subTaskId":123,"taskId":1,"caseId":1,"stepId":1},
                          {"stepIx":1,"subTaskId":123,"taskId":1,"caseId":1,"stepId":2}]""",
              help='Leo Step的Json定义')
@click.option('--leo-sub-task-ids', type=str, default='123', help='Leo子任务ID列表')
def execute(leo_dsls: str, leo_task_id: int, leo_step_list: str, leo_sub_task_ids: str):
    # environ 上下文中有 LEO_TASK_ID，LEO_SUB_TASK_ID_LIST，LEO_CASE_DSL_LIST，LEO_CASE_DSL_STEP_LIST
    # 其中 DSL 是 TOS的链接，可以用 TosClient 获取
    CaseBase.set_leo_task_id(int(os.environ.get('LEO_TASK_ID', leo_task_id)))
    leo_case_dsl_step_list = os.environ.get('LEO_CASE_DSL_STEP_LIST', leo_step_list)
    step_list = {}
    for step in json.loads(leo_case_dsl_step_list):
        sub_task_id = step.get("subTaskId", -1)
        if sub_task_id not in step_list:
            step_list[sub_task_id] = {}
        step_list[sub_task_id][step.get("stepIx", 0)] = step
    CaseBase.set_leo_case(step_list)

    leo_sub_task_id_list = os.environ.get('LEO_SUB_TASK_ID_LIST', leo_sub_task_ids).split(',')
    leo_dsl_list = os.environ.get('LEO_CASE_DSL_LIST', leo_dsls).split(',')
    for sub_task_id, dsl in zip(leo_sub_task_id_list, leo_dsl_list):
        print(f'execute: {sub_task_id}, {dsl}, {step_list[int(sub_task_id)]}')
        CaseBase.set_leo_sub_task_id(int(sub_task_id))
        dsl_data = parse_dsl(dsl)
        CaseBase.set_dsl(json.loads(dsl_data))
        res = CaseBase.get_dsl()

        # 配置环境变量
        settings.STORM_SERVER_ENV = CaseBase.get_env()

        case_steps = [i.get('case_step', '') for i in res.get('case_info', {}).get('case_step_list', [])]
        case_items = [case_map[i] for i in case_steps if i in case_map]
        print(f"pytest {' '.join(case_items)}")
        exit_code = pytest.main(case_items)
        sys.exit(exit_code)


def parse_dsl(dsl):
    if dsl and dsl.startswith('file://'):
        from pathlib import Path
        return Path(dsl[len('file://'):]).read_text(encoding='utf8')
    tos_client = TosClient()
    dsl_data = tos_client.download(dsl)
    return dsl_data


if __name__ == "__main__":
    leo()
