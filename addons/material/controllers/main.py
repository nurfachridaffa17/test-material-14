from odoo import http
from odoo.http import request

class AuthController(http.Controller):

    @http.route('/api/authentication', type='json', auth='none', methods=['POST'], csrf=False)
    def auth(self, **post):
        db = post.get('db')
        login = post.get('login')
        password = post.get('password')
        try:
            request.session.authenticate(db, login, password)
            return {'success': True, 'session_id': request.session.sid}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @http.route('/api/logout', type='json', auth='user', methods=['POST'], csrf=False)
    def logout(self, **post):
        request.session.logout()
        return {'success': True}

class MaterialController(http.Controller):

    @http.route('/api/material', type='json', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, **post):
        get_all_materials = request.env['material.material'].sudo().search([])
        materials = [material.read() for material in get_all_materials]
        return {'success': True, 'materials': materials}
    
    @http.route('/api/material/filter', type='json', auth='user', methods=['GET'], csrf=False)
    def filter_materials(self, **post):
        name = post.get('name')
        material_type = post.get('material_type')
        supplier_id = post.get('supplier_id')

        domain = []

        if name:
            domain.append(('name', 'ilike', name))
        if material_type:
            domain.append(('material_type', '=', material_type))
        if supplier_id:
            domain.append(('supplier_id', '=', supplier_id))

        materials = request.env['material.material'].sudo().search(domain)

        material_data = [{
            'id': material.id,
            'name': material.name,
            'default_code': material.default_code,
            'material_type': material.material_type,
            'material_buying_price': material.material_buying_price,
            'supplier_id': material.supplier_id.id
        } for material in materials]
        
        return {'success': True, 'materials': material_data}


    @http.route('/api/material/<int:material_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_material(self, material_id, **post):
        material = request.env['material.material'].sudo().search([('id', '=', material_id)], limit=1)
        material = material.read()
        return {'success': True, 'material': material}
    
    @http.route('/api/material', type='json', auth='user', methods=['POST'], csrf=False)
    def create_material(self, **post):
        name = post.get('name')
        default_code = post.get('default_code')
        material_type = post.get('material_type')
        material_buying_price = post.get('material_buying_price')
        supplier_id = post.get('supplier_id')
        material = request.env['material.material'].sudo().create({
            'name': name,
            'default_code': default_code,
            'material_type': material_type,
            'material_buying_price': material_buying_price,
            'supplier_id': supplier_id,
        })

        if material:
            return {'success': True, 'material': material}
        else:
            return {'success': False, 'message': 'Error create material'}
    
    @http.route('/api/material/<int:material_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **post):
        name = post.get('name')
        default_code = post.get('default_code')
        material_type = post.get('material_type')
        material_buying_price = post.get('material_buying_price')
        supplier_id = post.get('supplier_id')
        material = request.env['material.material'].sudo().search([('id', '=', material_id)], limit=1)
        
        if name:
            material.write({'name': name})
        if default_code:
            material.write({'default_code': default_code})
        if material_type:
            material.write({'material_type': material_type})
        if material_buying_price:
            material.write({'material_buying_price': material_buying_price})
        if supplier_id:
            material.write({'supplier_id': supplier_id})

        if material:
            return {'success': True, 'material': material}
        else:
            return {'success': False, 'message': 'Error update material'}
        
    @http.route('/api/material/<int:material_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def hard_delete_material(self, material_id, **post):
        material = request.env['material.material'].sudo().search([('id', '=', material_id)], limit=1)
        material.unlink()
        return {'success': True}
    
    @http.route('/api/material/<int:material_id>', type='json', auth='user', methods=['PATCH'], csrf=False)
    def soft_delete_material(self, material_id, **post):
        material = request.env['material.material'].sudo().search([('id', '=', material_id)], limit=1)
        material.write({'active': False})
        return {'success': True}


class SupplierController(http.Controller):

    @http.route('/api/supplier', type='json', auth='user', methods=['GET'], csrf=False)
    def get_suppliers(self, **post):
        get_all_suppliers = request.env['res.partner'].sudo().search([('is_supplier', '=', True)])
        suppliers = [supplier.read() for supplier in get_all_suppliers]
        return {'success': True, 'suppliers': suppliers}
    
    @http.route('/api/supplier/country', type='json', auth='user', methods=['GET'], csrf=False)
    def get_countries(self, **post):
        get_all_countries = request.env['res.country'].sudo().search([])
        countries = [country.read() for country in get_all_countries]
        return {'success': True, 'countries': countries}
    
    @http.route('/api/supplier/state', type='json', auth='user', methods=['GET'], csrf=False)
    def get_states(self, **post):
        country_id = post.get('country_id')
        get_all_states = request.env['res.country.state'].sudo().search([('country_id', '=', country_id)])
        states = [state.read() for state in get_all_states]
        return {'success': True, 'states': states}
    
    @http.route('/api/supplier/filter', type='json', auth='user', methods=['GET'], csrf=False)
    def filter_suppliers(self, **post):
        name = post.get('name')
        country_id = post.get('country_id')
        state_id = post.get('state_id')
        city = post.get('city')

        domain = []

        if name:
            domain.append(('name', 'ilike', name))
        if country_id:
            domain.append(('country_id', '=', country_id))
        if state_id:
            domain.append(('state_id', '=', state_id))
        if city:
            domain.append(('city', '=', city))

        if not domain:
            domain = []
        
        domain.append(('is_supplier', '=', True))
        suppliers = request.env['res.partner'].sudo().search(domain)

        supplier_data = [{
            'id': supplier.id,
            'name': supplier.name,
            'street': supplier.street,
            'city': supplier.city,
            'state_id': supplier.state_id.id,
            'zip': supplier.zip,
            'country_id': supplier.country_id.id
        } for supplier in suppliers]
        
        return {'success': True, 'suppliers': supplier_data}
        
    @http.route('/api/supplier/<int:supplier_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_supplier(self, supplier_id, **post):
        supplier = request.env['res.partner'].sudo().search([('id', '=', supplier_id)], limit=1)
        supplier = supplier.read()
        return {'success': True, 'supplier': supplier}
    
    @http.route('/api/supplier', type='json', auth='user', methods=['POST'], csrf=False)
    def create_supplier(self, **post):
        address_type = ''
        name = post.get('name')
        company_type = post.get('company_type')
        if company_type != 'company':
            address_type = post.get('address_type')
        street = post.get('street')
        city = post.get('city')
        state_id = post.get('state_id')
        zip_code = post.get('zip')
        country_id = post.get('country_id')
        supplier = request.env['res.partner'].sudo().create({
            'name': name,
            'company_type': company_type,
            'type': address_type,
            'street': street,
            'city': city,
            'state_id': state_id,
            'zip': zip_code,
            'country_id': country_id,
            'is_supplier': True,
        })

        if supplier:
            return {'success': True, 'supplier': supplier}
        else:
            return {'success': False, 'message': 'Error create supplier'}
    
    @http.route('/api/supplier/<int:supplier_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_supplier(self, supplier_id, **post):
        address_type = ''
        name = post.get('name')
        company_type = post.get('company_type')
        if company_type != 'company':
            address_type = post.get('address_type')
        street = post.get('street')
        city = post.get('city')
        state_id = post.get('state_id')
        zip_code = post.get('zip')
        country_id = post.get('country_id')
        supplier = request.env['res.partner'].sudo().search([('id', '=', supplier_id)], limit=1)
        
        if name:
            supplier.write({'name': name})
        if address_type:
            supplier.write({'address_type': address_type})
        if street:
            supplier.write({'street': street})
        if city:
            supplier.write({'city': city})
        if state_id:
            supplier.write({'state_id': state_id})
        if zip_code:
            supplier.write({'zip': zip_code})
        if country_id:
            supplier.write({'country_id': country_id})

        if supplier:
            return {'success': True, 'supplier': supplier}
        else:
            return {'success': False, 'message': 'Error update supplier'}
        
    
    @http.route('/api/supplier/<int:supplier_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def hard_delete_supplier(self, supplier_id, **post):
        supplier = request.env['res.partner'].sudo().search([('id', '=', supplier_id)], limit=1)
        supplier.unlink()
        return {'success': True}
    
    @http.route('/api/supplier/<int:supplier_id>', type='json', auth='user', methods=['PATCH'], csrf=False)
    def soft_delete_supplier(self, supplier_id, **post):
        supplier = request.env['res.partner'].sudo().search([('id', '=', supplier_id)], limit=1)
        supplier.write({'active': False})
        return {'success': True}