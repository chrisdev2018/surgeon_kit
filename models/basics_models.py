
from odoo import models, fields, api

class Surgeon(models.Model):
    _name = 'sk.surgeon'
    _description = "Possibility to record a Surgeon"

    name = fields.Char(
        string='Surname & Name',
        required=True
    )

class Category(models.Model):
    _name = 'sk.category'
    _description = "Possibility to record a Case's category"

    name = fields.Char(
        string='Category',
        required=True
    )

    sequence = fields.Integer(
        string='sequence')
    
class MotivationSection(models.Model):
    _name = 'sk.motivation_section'
    _description = "Possibility to record a Motivation's type"

    name = fields.Char(
        string='Motivation Section',
        required=True
    )

    sequence = fields.Integer(
        string='sequence')

class MaterialsDrugs(models.Model):
    _name = 'sk.materials_n_drugs'
    _description = "Define for materials and drugs"

    name = fields.Char(
        string = 'Item',
        required=True)
    
    sequence = fields.Integer('Sequence')
    type = fields.Selection(
        string='Type',
        selection=[
            ('ms', 'MATERIALS and SUPPLIES'),
            ('ad', 'ANESTHESIA DRUGS')
        ],
        required=True)
    
    price = fields.Integer(
        string='Price(FCFA)',
        required=True
    )


class SurgeryType(models.Model):
    _name = 'sk.surgery'
    _description = "Define Different types of surgery with its configurations"

    name = fields.Char(
        string='Surgery',
        required=True
    )

    matrix_motivation_ids = fields.One2many(
        string='Matrix Lines',
        comodel_name = 'sk.matrix_motivation',
        inverse_name = 'surgery_id'
    )
    matrix_surgeon_ids = fields.One2many(
        string='Matrix Lines',
        comodel_name = 'sk.matrix_surgeon',
        inverse_name = 'surgery_id'
    )
    matrix_materials_n_drugs_ids = fields.One2many(
        string='Matrix Lines',
        comodel_name = 'sk.matrix_materials_drugs',
        inverse_name = 'surgery_id'
    )
