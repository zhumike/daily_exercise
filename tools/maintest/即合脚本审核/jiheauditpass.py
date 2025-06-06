# coding=utf8

import datetime
import json
import time
import sys
from frame import logger as logging

from star.business.audit.audit_base import create_or_update_resource_audit, check_is_latest_resource
from star.common.session import supplier_db_commit
from star.common.const import AuditType, ResourceType, ResourceAuditSource, AuthorTaskType, AuditStatus, \
    CreativeOrderAuditStatus, VideoAdSupplierOrderStatus
from star.dals.audit import ResourceAuditFetcher
from star.dals.order import StarOrderDAL
from star.dals.resource import StarResourceDAL
from star_async.kafka_processors.base_processor import BaseProcessor
from star_core.common.exception import DataError
from star.dals.creative_order import StarCreativeOrderOutcomeSubmissionDAL as SubmissionDAL, \
    StarCreativeOrderOutcomeSubmissionRelationDAL as SubmissionRelationDAL
from star.common.const_dir.creative_order import OutcomeType, SubmissionStatus, SubmissionRelationType
from star.common.rpc.star.base_rpc import orders_client

class JiheAuditProcessor(BaseProcessor):
    @supplier_db_commit
    def save_audit_data(self, audit_info, resource):
        order = StarOrderDAL.query_by_id(resource.order_or_demand_id)
        if not order:
            logging.error('not found order_id from resource: %s', resource.id)
            raise DataError(u'resource=%s order_id %s is invalid' % (resource.id, resource.order_or_demand_id))
        audit_status = audit_info.get("verify_status", 0)
        audit_time = datetime.datetime.fromtimestamp(audit_info.get("create_time"))
        logging.info('call create_or_update_resource_audit for resource: %s', resource.id)
        create_or_update_resource_audit(resource.id, audit_status, audit_time, ban_reason=0,
                                        ban_reason_detail=audit_info.get("remark", ""),
                                        platform_source=order.platform_source,
                                        audit_type=AuditType.first_audit.value,
                                        resource=resource,
                                        audit_info=json.dumps(audit_info, ensure_ascii=False),
                                        resource_audit_source=ResourceAuditSource.ad_material.value,
                                        )
        logging.info('create_or_update_resource_audit finish')

    @supplier_db_commit
    def update_order_audit_status(self, resource):
        order = StarOrderDAL.query_by_id(resource.order_or_demand_id)
        if not order:
            logging.error('not found order_id from resource: %s', resource.id)
            raise DataError(u'resource=%s order_id %s is invalid' % (resource.id, resource.order_or_demand_id))
        if check_is_latest_resource(resource):
            logging.info('update_order_audit_status for resource: %s', resource.id)
            order_audit_status = ResourceAuditFetcher.get_order_audit_status(resource.id)
            order.update(audit_status=order_audit_status)
            logging.info('finish update_order_audit_status for resource: %s', resource.id)

    @supplier_db_commit
    def update_submission_status(self, resource):
        order = StarOrderDAL.query_by_id(resource.order_or_demand_id)
        if not order:
            logging.error('not found order_id from resource: %s', resource.id)
            raise DataError(u'resource=%s order_id %s is invalid' % (resource.id, resource.order_or_demand_id))

        resource_audit_status = ResourceAuditFetcher.get_resource_audit_status(resource.id)
        resource.update(audit_status=resource_audit_status)
        outcome_type = OutcomeType.script.value if resource.resource_type == ResourceType.script.value else OutcomeType.material.value
        submission = SubmissionDAL.query_one({
            'order_id': order.id,
            'outcome_type': outcome_type,
        }, order_by='-create_time')

        # 如果不存在 或 已经有审核结果了 直接返回
        if not submission or submission.status != SubmissionStatus.auditing.value:
            return

        submission_relations = SubmissionRelationDAL.query({'submission_id': submission.id})
        related_resource_ids = [_.resource_id for _ in submission_relations]
        if resource.id not in related_resource_ids:
            return

        # 更新submission状态
        related_resources = StarResourceDAL.query_by_ids(related_resource_ids)
        resource_audit_status_list = [_.audit_status for _ in related_resources]
        if AuditStatus.unknown.value in resource_audit_status_list:
            submission_status = SubmissionStatus.auditing.value
            order_audit_status = CreativeOrderAuditStatus.script_system_auditing.value if outcome_type == OutcomeType.script.value else CreativeOrderAuditStatus.material_system_auditing.value
        elif AuditStatus.audit_failed.value in resource_audit_status_list:
            submission_status = SubmissionStatus.audit_reject.value
            order_audit_status = CreativeOrderAuditStatus.script_system_reject.value if outcome_type == OutcomeType.script.value else CreativeOrderAuditStatus.material_system_reject.value
        else:
            submission_status = SubmissionStatus.audit_pass.value
            order_audit_status = CreativeOrderAuditStatus.script_demander_auditing.value if outcome_type == OutcomeType.script.value else CreativeOrderAuditStatus.material_demander_auditing.value

        submission.update(status=submission_status, system_audit_time=datetime.datetime.now())
        order.update(audit_status=order_audit_status)

    @supplier_db_commit
    def update_resource_status(self, resource):
        order = StarOrderDAL.query_by_id(resource.order_or_demand_id)
        if not order:
            logging.error('not found order_id from resource: %s', resource.id)
            raise DataError(u'resource=%s order_id %s is invalid' % (resource.id, resource.order_or_demand_id))

        resource_audit_status = ResourceAuditFetcher.get_resource_audit_status(resource.id)
        resource.update(audit_status=resource_audit_status)

        if resource.resource_type != ResourceType.video.value:
            return

        if resource_audit_status != AuditStatus.audit_pass.value:
            return

        submission = SubmissionDAL.query_one({
            'order_id': order.id,
            'outcome_type': OutcomeType.material.value,
            'status': SubmissionStatus.demander_pass.value
        }, order_by='-create_time')
        if not submission:
            return

        SubmissionRelationDAL.new(
            submission_id=submission.id,
            origin=SubmissionRelationType.additional.value,
            resource_id=resource.id
        )


    def RealHandler(self, data):
        """
         data = {
            "resource_id": ,
            "audit_info": {
                "task_id": audit_result.task_id,
                "verify_id": audit_result.verify_id,
                "verifier": audit_result.verifier,
                "verify_status":,
                "remark": audit_result.remark,
                'create_time': int(time.time())
            },
            "demand_name": audit_result.demand_name,
            "demander_telephone": audit_result.demander_telephone,
            "author_telephone": audit_result.author_telephone,
            "event_type": "star_material_task_audit"
        }
        :param data:
        :return:
        """
        try:
            logging.info(u"JiheAuditProcessor receive message: %s", data)
            if data.get("event_type", "") != "star_material_task_audit" or data.get("resource_id") is None:
                logging.info('skip invalid data: %s', data)
                return True
            audit_info = data.get("audit_info", {})
            resource_id = data.get("resource_id")

            resource = StarResourceDAL.query_by_id(resource_id)
            if not resource:
                raise DataError(u'resource_id=%s not exist' % resource_id)
            if resource.resource_type not in [ResourceType.video.value, ResourceType.script.value]:
                raise DataError(u'resource=%s type=%s is not allowed for audit' % (resource_id, resource.resource_type))
            order = StarOrderDAL.query_by_id(resource.order_or_demand_id)
            if not order:
                logging.error('not found order_id from resource: %s', resource.id)
                raise DataError(u'resource=%s order_id %s is invalid' % (resource.id, resource.order_or_demand_id))

            self.save_audit_data(audit_info, resource)
            if order.video_type in [AuthorTaskType.free_market_task.value]:
                orders_client.InnerSaveCreativeAuditResult(resource_id=resource.id,
                                                           audit_status=audit_info.get("verify_status", 0))
            else:
                self.update_order_audit_status(resource)
            logging.info('JiheAuditProcessor process finish')
        except Exception as err:
            logging.exception('JiheAuditProcessor process ad audit error: %s', err)
            return False
        return True


if __name__ == "__main__":
    resource_id = sys.argv[1]
    verify_status = sys.argv[2]
    data = {
        "resource_id": resource_id,
        "audit_info": {
            "task_id": 1223112,
            "verify_id": 332112,
            "verifier": "zhoufengshun",
            "verify_status": verify_status,
            "remark": "good",
            'create_time': int(time.time())
        },
        "event_type": "star_material_task_audit",
    }
    JiheAuditProcessor().RealHandler(data)