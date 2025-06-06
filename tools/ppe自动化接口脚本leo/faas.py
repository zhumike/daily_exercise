import json
import requests


def handler(event, context):
    try:
        url = "https://bytedpe.bytedance.net/neptune/dag/build"

        body = {
            "dag_id": 352,
            # 触发者名称
            "user_name": "zhuzhenzhong",
            "bytecycle_id": 12263765,
            "dag": {
                "init_leo_auto": {
                    "atomic_class_name": "E2eWeekendDslInitAtomic",
                    "max_retry_count": 0,
                    "atomic_strategy": {
                        "timeout_seconds": 60
                    },
                    "params": {
                        "supportRetry": 1,
                        # DSL的caseId
                        "caseIds": [
                            3745837
                        ],
                        "pipelineType": 18,
                        "taskSuccessRate": 0.95,
                        # 被测服务的环境
                        "leoEnv": "ppe_ad_star",
                        "testType": 1,
                        # weekend_leo代码分支
                        "branch": "zzz_leo",
                        # 展示到weekend测试报告上的任务标题
                        "taskTitle": "星图接口测试"
                    }
                },
                "leo_trigger_auto": {
                    "max_retry_count": 1,
                    "atomic_class_name": "E2eWeekendTriggerAtomic",
                    "atomic_strategy": {
                        "timeout_seconds": 60
                    }
                },
                "leo_report_auto": {
                    "atomic_class_name": "E2eReportGenerateAtomic",
                    "max_retry_count": 0,
                    "atomic_strategy": {
                        "timeout_seconds": 3600
                    }
                }
            },
            "dag_strategy": {
                "max_week_parallel": 10,
                "is_reuse_with_hash_key": True,
                "failed": {
                    "process_nodes": [
                        {
                            "method": "save",
                            "node_name": "*",
                            "params": {
                                "minutes": 30
                            }
                        }
                    ]
                }
            },
            "global_context": {
                "customParams": {
                    "weekend_ppe_env": "ppe_ad_star"
                }
            }
        }

        header = {
            'x-use-ppe': '1'

        }
        resp = requests.post(url=url, headers=header, json=body)
        resp_data = json.loads(resp.content.decode("utf-8"))
        print(url)
        print(json.dumps(body))
        print(json.dumps(resp_data))
    except Exception as e:
        print(str(e))

    result = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'hello faas'
        })
    }
    return result

    # 如果是本地可以加上main函数做触发
if __name__ == "__main__":
        handler(None, None)