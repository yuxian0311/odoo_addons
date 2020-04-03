# -*- coding: utf-8 -*-
{
    'name': "中国省市区数据插件",

    'summary': "中国省市区数据插件",

    'description': """
        中国省市区数据插件
    """,

    'author': "Alex Yu",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_address_city', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/res_country_state_data.xml',
        'data/res_city_data.xml',
        'data/res_district_data.xml',
        'views/address_views.xml',
    ],
}