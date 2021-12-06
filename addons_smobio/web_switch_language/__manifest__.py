# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Web Switch Language',
    'version': '13.0.1.0.0',
    'summary': 'Lets users quickly change language',
    'description': """This module lets users quickly change language.""",
    'author': 'dong@freshoo.cn',
    'license': 'AGPL-3',
    'website': 'https://www.freshoo.cn',
    'images': ['static/description/banner.png'],
    'category': 'Tools',
    'depends': ['web'],
    'data': [
        'data/res_lang_data.xml',
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
