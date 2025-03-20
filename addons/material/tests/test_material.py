from odoo.tests.common import TransactionCase, HttpCase
from odoo.exceptions import ValidationError


class TestMaterial(TransactionCase):
    
    # Setup data untuk test
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.Material = self.env['material.material']
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_supplier': True,
        })
        # Data valid untuk membuat material
        self.valid_material_data = {
            'name': 'Test Material',
            'default_code': 'MAT001',
            'material_type': 'fabric',
            'material_buying_price': 150.0,
            'supplier_id': self.supplier.id,
        }
    
    # Test pembuatan material dengan data valid
    def test_create_material_valid(self):
        material = self.Material.create(self.valid_material_data)
        self.assertEqual(material.name, 'Test Material')
        self.assertEqual(material.default_code, 'MAT001')
        self.assertEqual(material.material_buying_price, 150.0)

    # Test pembuatan material dengan default_code yang sudah ada
    def test_create_material_duplicate_default_code(self):
        self.Material.create(self.valid_material_data)
        with self.assertRaises(ValidationError):
            self.Material.create({
                'name': 'Test Material 2',
                'default_code': 'MAT001',
                'material_type': 'jeans',
                'material_buying_price': 200.0,
                'supplier_id': self.supplier.id,
            })
    
    # Test pembuatan material dengan material_buying_price yang kurang dari 100
    def test_create_material_invalid_buying_price(self):
        with self.assertRaises(ValidationError):
            self.Material.create({
                'name': 'Test Material',
                'default_code': 'MAT003',
                'material_type': 'fabric',
                'material_buying_price': 50.0,
                'supplier_id': self.supplier.id,
            })
    
    # Test update material dengan data valid
    def test_update_material_valid(self):
        material = self.Material.create(self.valid_material_data)
        material.write({
            'name': 'Updated Material',
            'default_code': 'MAT005',
            'material_type': 'fabric',
            'material_buying_price': 200.0,
            'supplier_id': self.supplier.id,
        })
        self.assertEqual(material.name, 'Updated Material')
        self.assertEqual(material.default_code, 'MAT005')
        self.assertEqual(material.material_buying_price, 200.0)
        self.assertEqual(material.supplier_id, self.supplier)
    
    # Test update material dengan default_code yang sudah ada
    def test_update_material_duplicate_default_code(self):
        self.Material.create(self.valid_material_data)
        material = self.Material.create({
            'name': 'Test Material 2',
            'default_code': 'MAT001',
            'material_type': 'fabric',
            'material_buying_price': 150.0,
            'supplier_id': self.supplier.id,
        })
        with self.assertRaises(ValidationError):
            material.write({
                'name': 'Updated Material',
                'default_code': 'MAT001',
                'material_type': 'fabric',
                'material_buying_price': 200.0,
                'supplier_id': self.supplier.id,
            })
    
    # Test update material dengan material_buying_price yang kurang dari 100
    def test_update_material_invalid_buying_price(self):
        material = self.Material.create(self.valid_material_data)
        with self.assertRaises(ValidationError):
            material.write({
                'name': 'Updated Material',
                'default_code': 'MAT006',
                'material_type': 'fabric',
                'material_buying_price': 50.0,
                'supplier_id': self.supplier.id,
            })
        
        with self.assertRaises(ValidationError):
            material.write({
                'name': 'Updated Material',
                'default_code': 'MAT007',
                'material_type': 'fabric',
                'material_buying_price': 0.0,
                'supplier_id': self.supplier.id,
            })
        

class TestMaterialController(HttpCase):
    def test_get_materials(self):
        self.url = '/api/material'
        response = self.url_open(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_get_material(self):
        self.url = '/api/material/1'
        response = self.url_open(self.url)
        self.assertEqual(response.status_code, 200)