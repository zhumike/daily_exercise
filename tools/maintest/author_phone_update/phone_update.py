# -*- coding: utf-8 -*-
# @Time : 2021/9/29 3:00 下午
# @Author : zhuzhenzhong
# coding: utf-8
from star_common.dals.author import StarAuthorInfoDAL
from star_common.models.author import StarAuthorInfo
from star_common.storage.db_session import supplier_db_commit


class ScriptDAL(StarAuthorInfoDAL):
    __model_cls__ = StarAuthorInfo
    __str_attributes__ = ('id',)

    @classmethod
    @supplier_db_commit
    def update_phone_by_id(cls, star_id, phone):
        session = cls._session()
        session.query(StarAuthorInfo) \
            .filter(StarAuthorInfo.id == star_id, StarAuthorInfo.deleted == 0) \
            .update({"phone": phone})
        session.flush()


def update_phone():
    # ScriptDAL.update_phone_by_id(6641178755068854276, "17521615317")
    ScriptDAL.update_phone_by_id(6901861229250215944, "")


if __name__ == '__main__':
    update_phone()