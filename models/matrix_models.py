from odoo import models, fields, api
from odoo.exceptions import ValidationError



class MatrixMotivation(models.Model):
    _name = 'sk.matrix_motivation'
    _description = "Define rate per category versus motivation section"

    motivation_id = fields.Many2one(
        comodel_name='sk.motivation_section',
        required=True
    )

    category_id = fields.Many2one(
        comodel_name='sk.category',
        required=True
    )

    surgery_id = fields.Many2one(
        comodel_name='sk.surgery'
    )

    rate = fields.Integer(
        string='Rate(FCFA)'
    )

    @api.constrains('rate')
    def _check_rate(self):
        if self.rate <= 0:
            raise ValidationError('Every motivation Rate must be a positif integer')
        
class MatrixMaterialsDrugs(models.Model):
    _name = 'sk.matrix_materials_drugs'
    _description = "Define quantity per category versus material or drug item"

    item_id = fields.Many2one(
        comodel_name='sk.materials_n_drugs',
        required=True
    )

    category_id = fields.Many2one(
        comodel_name='sk.category',
        required=True
    )

    surgery_id = fields.Many2one(
        comodel_name='sk.surgery'
    )

    quantity = fields.Integer(
        string='Quantity'
    )

    @api.constrains('quantity')
    def _check_quantity(self):
        if self.quantity <= 0:
            raise ValidationError('Every Item Quantity must be a positif integer')
        
class MatrixSurgeon(models.Model):
    _name = 'sk.matrix_surgeon'
    _description = "Define rate per category versus surgeon"

    surgeon_id = fields.Many2one(
        comodel_name='sk.surgeon',
        required=True
    )

    category_id = fields.Many2one(
        comodel_name='sk.category',
        required=True
    )

    surgery_id = fields.Many2one(
        comodel_name='sk.surgery'
    )

    rate = fields.Integer(
        string='Rate(FCFA)'
    )

    @api.constrains('rate')
    def _check_rate(self):
        if self.rate <= 0:
            raise ValidationError('Every Surgeon Rate must be a positif integer')