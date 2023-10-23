from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SurgeryEntry(models.Model):
    _name = 'sk.surgery_entry'
    _description = "Record every entry"

    def validate(self):
        for entry in self:
            matrix_surgeon_lines = self.env['sk.matrix_surgeon'].search([
                ('category_id', '=', entry.category_id.id),
                ('surgery_id', '=', entry.surgery_id.id)]).filtered(
                    lambda x: x.surgeon_id in entry.surgeon_ids)
            
            matrix_motivation_lines = self.env['sk.matrix_motivation'].search([
                ('category_id', '=', entry.category_id.id), ('surgery_id', '=', entry.surgery_id.id)
            ])

            for line in matrix_surgeon_lines:
                if line.surgeon_id in entry.surgeon_ids:
                    total_surgeon = entry.cases * line.rate
                    self.env['sk.surgeon_allocation_line'].create({
                        'surgeon_id': line.surgeon_id.id,
                        'surgery_entry_id': entry.id,
                        'percentage': total_surgeon * (20/100),
                        'payable': total_surgeon * (80/100)
                        })
            
            if matrix_motivation_lines:
                for line in matrix_motivation_lines:
                    total_motivation = entry.cases * line.rate
                    self.env['sk.motivation_allocation_line'].create({
                        'motivation_section_id': line.motivation_id.id,
                        'surgery_entry_id': entry.id,
                        'percentage': total_motivation * (20/100),
                        'payable': total_motivation * (80/100)
                    })

            entry.write({'validated': True})                       
        return True


    validated = fields.Boolean(
        string='Already validated',
        default=False

    )
   
    name = fields.Char(
        string='Code',
        required=True,
        readonly=True,
        default='New'
    )

    surgery_id = fields.Many2one(
        comodel_name='sk.surgery', 
        string='Surgery',
        required=True)
    
    surgeon_ids = fields.Many2many(
        comodel_name='sk.surgeon', 
        string='Surgeons',
        required=True)
    
    category_id = fields.Many2one(
        comodel_name='sk.category',
        required=True, 
        string='Category')
    
    cases = fields.Integer(
        string='Nbr of cases',
        default=1,
        required=True
    )
    entry_date = fields.Date(
        string='Date',
        required=True
    )

    total_amount = fields.Integer(
        string='Total Amount',
        compute='compute_amount',
        store=True
    )

    @api.depends('cases', 'surgeon_ids', 'category_id', 'surgery_id')
    def compute_amount(self):
        for record in self:
            if record.cases > 0 and record.surgeon_ids and record.category_id and record.surgery_id:
                drugs_amount = 0
                drugs_matrix = self.env['sk.matrix_materials_drugs'].search([('surgery_id', '=', record.surgery_id.id), ('category_id', '=', record.category_id.id)])
                if drugs_matrix:
                    for line in drugs_matrix:
                        drugs_amount += self.env['sk.materials_n_drugs'].search([(
                            'id', '=', line.item_id.id
                        )]).price * line.quantity
                
                surgeon_cost = 0
                for surgeon in record.surgeon_ids:
                    surgeon_cost += self.env['sk.matrix_surgeon'].search([
                            ('surgery_id', '=', record.surgery_id.id),
                            ('surgeon_id', '=', surgeon.id),
                            ('category_id', '=', record.category_id.id)
                        ]).rate
            
                team_motivation_cost = sum(self.env['sk.matrix_motivation'].search([('surgery_id', '=', record.surgery_id.id), ('category_id', '=', record.category_id.id)]).mapped('rate'))

                record.total_amount = (drugs_amount + surgeon_cost + team_motivation_cost) * record.cases


    @api.constrains('cases')
    def _check_cases(self):
        if self.cases <= 0:
            raise ValidationError('Number of cases must be a positif integer')

    @api.model
    def create(self, vals):
        res = super(SurgeryEntry, self).create(vals)
        res['name'] = self.env['ir.sequence'].next_by_code('surgery_entry.code')        
        return res

    @api.onchange('surgeon_ids')
    def _onchange_surgeon(self):
        for rec in self:
            if rec.surgeon_ids:
                for surgeon in rec.surgeon_ids:
                    if not self.env['sk.matrix_surgeon'].search([
                        ('surgery_id', '=', rec.surgery_id.id),
                        ('surgeon_id', '=', surgeon.id),
                        ('category_id', '=', rec.category_id.id)
                    ]):
                        import pdb
                        raise ValidationError(
                            'There is no Matrix (%s, %s) for the surgeon: %s' %
                             (rec.surgery_id.name, rec.category_id.name, surgeon.name)
                        )