# Copyright 2023 Mepat
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': "Surgeon Kit",
    'version': "11.0.1.0.1",
    'author': "Christian FOMEKONG",
    'license': "AGPL-3",
    'category': "Tools",
    'depends': [
        'base',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/datas.xml',
        'data/sequence.xml',
        'views/config_views.xml',
        'views/surgery_entry_views.xml',
        'views/allocations_views.xml',
    ],
    'application': True,
    'installable': True,
}
