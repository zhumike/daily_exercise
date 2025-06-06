# -*- coding: utf-8 -*-

import sys
import time

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star')

from star_search.scripts.iterate_helper import query_objs
from star.dals.user import StarAuthorInfoDAL
from star.common.const import PlatformSource
from star_search.search_business.author import StartAuthorIndexHandler


def sync_author(author_ids):
    filter_dict = {'id': author_ids}
    for (dal, platform_source) in [
        (StarAuthorInfoDAL, PlatformSource.douyin.value),
    ]:
        tmp_dict = filter_dict.copy()
        tmp_dict.update({'core_user_id__gt': 0})
        for objs in query_objs(dal, filters=tmp_dict, limit=500):
            print [_.id for _ in objs]
            StartAuthorIndexHandler().index_authors(objs, platform_source)
        print dal, 'deal at', time.time()


def sync_tags(author_ids):
    # mock 数据
    class AuthorTags(object):
        def __init__(self, author_id, package_ids, package_type):
            self.author_id = author_id
            self.package_ids = package_ids
            self.package_type = package_type

    package_ids = [6992888132098064397]
    platform_source = 1
    pick_author_tags = [AuthorTags(author_id=_, package_ids=package_ids, package_type=1) for _ in author_ids]
    obj_dicts = []
    for pick_author_tag in pick_author_tags:
        tags = [{'package_id': _, "package_type": pick_author_tag.package_type} for _ in pick_author_tag.package_ids]
        obj_dict = {
            'id': pick_author_tag.author_id,
            'pick_author_tag': tags
        }
        obj_dicts.append(obj_dict)
    print StartAuthorIndexHandler().index_authors_part(obj_dicts, platform_source)


if __name__ == '__main__':
    author_ids = [6641178755068854276, 6901239213522419726, 6901866618809221133, 6964278232644321288]
    sync_author(author_ids)
    sync_tags(author_ids)