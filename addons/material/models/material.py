from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class Material(models.Model):
    _name = 'material.material'
    _description = 'Material'

    name = fields.Char(string='Material Name', required=True)
    default_code = fields.Char(string='Material Code', required=True)
    material_type = fields.Selection([('fabric', 'Fabric'), ('jeans', 'Jeans'), ('contton', 'Cotton')], default='fabric', required=True)
    material_buying_price = fields.Float(string='Material Buying Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True, domain=[('is_supplier', '=', True)])
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        if vals.get('default_code'):
            default_code = self.env['material.material'].search([('default_code', '=', vals['default_code'])])
            if default_code:
                raise UserError('Material code already exists')
        if vals.get('material_buying_price'):
            if vals['material_buying_price'] < 100:
                raise UserError('Material buying price must be greater than 100')
        return super(Material, self).create(vals)
    

    @api.model
    def write(self, vals):
        if vals.get('default_code'):
            default_code = self.env['material.material'].search([('default_code', '=', vals['default_code'])])
            if default_code:
                raise UserError('Material code already exists')
        if vals.get('material_buying_price'):
            if vals['material_buying_price'] < 100:
                raise UserError('Material buying price must be greater than 100')
        return super(Material, self).write(vals)
    
