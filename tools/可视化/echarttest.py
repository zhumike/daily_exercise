# -*- coding: utf-8 -*-
# @Time : 2022/11/2 9:21 下午
# @Author : zhuzhenzhong
# 柱状图
import random
import pyecharts.options as opts
from pyecharts.charts import Bar,Line
x_vals = ['7-03','7-10','7-24','8-07','8-21','9-04','9-18']
#x_vals2 = ['3-06','3-20','4-03','4-17']

# bar = (
#     Bar()
#     .add_xaxis(x_vals)
#     .add_yaxis('接口实现数量', [1476,1489])
#     .add_yaxis('接口总数', [1979,1992])
#     .set_series_opts(label_opts=opts.LabelOpts(is_show=True, font_size=14,margin=5),
#                           # markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=30, name="达标线")])
#                      )
#     .set_global_opts(title_opts=opts.TitleOpts(title='接口统计', subtitle='数量'),
#                      xaxis_opts=opts.AxisOpts(name='月份'),
#                      yaxis_opts=opts.AxisOpts(name='单位:个'))
# )
#
# bar.render('柱状图.html')

bar2 = (
    Line()
    .add_xaxis(x_vals)
    .add_yaxis('接口实现数量', [293,510,531,560,560,614,615])
    .add_yaxis('接口总数', [349,677,671,684,678,694,702])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, font_size=14,margin=5),
                          # markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=30, name="达标线")])
                     )
    .set_global_opts(title_opts=opts.TitleOpts(title='接口统计', subtitle='数量'),
                     xaxis_opts=opts.AxisOpts(name='日期'),
                     yaxis_opts=opts.AxisOpts(name='单位:个'))
)

bar2.render('接口折线图.html')
#
#
bar3 = (
    Line()
    .add_xaxis(x_vals)
    .add_yaxis('P0接口覆盖率', [90.48,75.33,79.14,81.87,82.60,88.47,87.61])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, font_size=14,margin=5),
                          # markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=30, name="达标线")])
                     )
    .set_global_opts(title_opts=opts.TitleOpts(title='接口统计', subtitle='百分比'),
                     xaxis_opts=opts.AxisOpts(name='日期'),
                     yaxis_opts=opts.AxisOpts(name='单位:%'))
)

bar3.render('P0接口覆盖率折线图.html')


bar4 = (
    Line()
    .add_xaxis(x_vals)
    .add_yaxis('行覆盖率', [31.46,33.31,33.70,34.60,36.72,37.96,38.11])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True, font_size=14,margin=5,color="black"),
                          markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(y=50, name="期望目标线"),opts.MarkLineItem(y=30, name="最低目标线")])
                     )
    .set_global_opts(title_opts=opts.TitleOpts(title='行覆盖率统计', subtitle='百分比'),
                     xaxis_opts=opts.AxisOpts(name='日期'),
                     yaxis_opts=opts.AxisOpts(name='单位:%'))
)

bar4.render('go代码覆盖率折线图.html')