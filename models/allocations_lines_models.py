from odoo import models, fields, api
from odoo.exceptions import ValidationError


        
class SurgeonAllocationLine(models.Model):
    _name = 'sk.surgeon_allocation_line'
    
    surgeon_id = fields.Many2one(
        comodel_name='sk.surgeon'

    )

    percentage = fields.Integer(
        string='20% retained(FCFA)'
    )

    payable = fields.Integer(
        string='Payable(FCFA)'
    )
    
    date_entry = fields.Date(
        string='Date Entry',
        compute='_compute_date',
        store=True
    )

    surgery_entry_id = fields.Many2one(
        comodel_name='sk.surgery_entry', 
        string='Code Entry',
        ondelete="cascade")
    
    @api.one
    @api.depends('surgery_entry_id')
    def _compute_date(self):
        if self.surgery_entry_id:
            self.date_entry = self.surgery_entry_id.entry_date  

class MotivationAllocationLine(models.Model):
    _name = 'sk.motivation_allocation_line'
    
    motivation_section_id = fields.Many2one(
        comodel_name='sk.motivation_section'
    )

    percentage = fields.Integer(
        string='20% retained(FCFA)'
    )
    payable = fields.Integer(
        string='Payable(FCFA)'
    )
    date_entry = fields.Date(
        string='Date Entry',
        compute='_compute_date',
        store=True
    )

    surgery_entry_id = fields.Many2one(
        comodel_name='sk.surgery_entry', 
        string='Code Entry',
        ondelete='cascade')
    
    @api.one
    @api.depends('surgery_entry_id')
    def _compute_date(self):
        if self.surgery_entry_id:
            self.date_entry = self.surgery_entry_id.entry_date