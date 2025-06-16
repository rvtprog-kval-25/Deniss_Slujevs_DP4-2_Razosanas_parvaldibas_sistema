import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload
import jwt
from sqlalchemy import func
import datetime
from functools import wraps
import bcrypt
import logging
from dotenv import load_dotenv
from dateutil import parser
import io
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from io import BytesIO
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
from sqlalchemy import or_

# Load environment variables from .env file in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

# Configure CORS with strict settings
CORS(app, 
     resources={r"/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True,
         "max_age": 3600
     }},
     supports_credentials=True)

# Add error handling for CORS preflight
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

SECRET_KEY = os.getenv('SECRET_KEY')

logging.basicConfig(level=logging.DEBUG)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    vards = db.Column(db.String(15))
    uzvards = db.Column(db.String(15))
    amats = db.Column(db.String(20))
    kods = db.Column(db.Integer)
    status = db.Column(db.String(10))
    token = db.Column(db.String(512))
    password = db.Column(db.String(200))

    shifts = db.relationship("Shift", backref="employee")
    orders = db.relationship("Order", backref="employee")

    def serialize(self):
        return {
            "id": self.id,
            "vards": self.vards,
            "uzvards": self.uzvards,
            "amats": self.amats,
            "kods": self.kods,
            "status": self.status
        }

class Shift(db.Model):
    __tablename__ = 'shifts'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True)) 

class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    nosaukums = db.Column(db.String(50))
    noliktava = db.Column(db.String(20))
    vieta = db.Column(db.String(20))
    vieniba = db.Column(db.String(20))
    daudzums = db.Column(db.Float)
    reserved_quantity = db.Column(db.Float, default=0)

    order_links = db.relationship(
    "OrderMaterial",
    backref="material",
    cascade="all, delete-orphan",
    passive_deletes=True
)

    def serialize(self):
        return {
            "id": self.id,
            "nosaukums": self.nosaukums,
            "noliktava": self.noliktava,
            "vieta": self.vieta,
            "vieniba": self.vieniba,
            "daudzums": self.daudzums or 0,
            "reserved_quantity": self.reserved_quantity or 0,
            "available_quantity": (self.daudzums or 0) - (self.reserved_quantity or 0)
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    nosaukums = db.Column(db.String(50))
    daudzums = db.Column(db.Float)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    status = db.Column(db.String(20), default="Nav sākts")      
   
    materials = db.relationship("OrderMaterial", backref="order", cascade="all, delete-orphan")

    def to_dict(self):
        employee_data = None
        if self.employee:
            employee_data = self.employee.serialize()
        
        materials_in_order = []
        for om in self.materials:
            logging.debug(f"Processing OrderMaterial: order_id={om.order_id}, material_id={om.material_id}, raw_daudzums={om.daudzums}")
            material = db.session.get(Material, om.material_id)
            if material:
                materials_in_order.append({
                    'material_id': material.id,
                    'nosaukums': material.nosaukums,
                    'vieniba': material.vieniba, 
                    'daudzums': om.daudzums or 0
                })
            else:
                logging.warning(f"Material not found for OrderMaterial with material_id: {om.material_id}")
        
        logging.debug(f"Final materials_in_order for order {self.id}: {materials_in_order}")
        
        return {
            'id': self.id,
            'nosaukums': self.nosaukums,
            'daudzums': self.daudzums or 0, 
            'status': self.status,
            'employee_id': self.employee_id,
            'employee': employee_data,
            'materials': materials_in_order
        }

class OrderMaterial(db.Model):
    __tablename__ = 'order_materials'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id', ondelete='CASCADE'), primary_key=True)
    daudzums = db.Column(db.Float)
    reserved = db.Column(db.Boolean, default=True)

    def serialize(self):
        return {
            "order_id": self.order_id,
            "material_id": self.material_id,
            "daudzums": self.daudzums or 0,
            "reserved": self.reserved
        }

def generate_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {'user_id': user_id, 'exp': expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing or incorrect format!"}), 403

        token = token[7:]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = db.session.get(Employee, decoded['user_id'])
            if not user:
                return jsonify({"error": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403

        return f(user, *args, **kwargs)
    return decorator

@app.route('/api/shifts/stats', methods=['GET'])
@token_required
def get_shifts_stats(current_user):
    try:
        start = request.args.get('start')
        end = request.args.get('end')

        start_date = parser.parse(start) if start else None
        end_date = parser.parse(end) if end else None

        employees = Employee.query.options(joinedload(Employee.shifts)).all()
        stats = []

        for emp in employees:
            for shift in emp.shifts:
                if not shift.start_time or not shift.end_time:
                    continue
                if start_date and shift.start_time < start_date:
                    continue
                if end_date and shift.end_time > end_date:
                    continue

                duration_hours = (shift.end_time - shift.start_time).total_seconds() / 3600
                stats.append({
                    "id": emp.id,
                    "vards": emp.vards,
                    "uzvards": emp.uzvards,
                    "amats": emp.amats,
                    "hours": round(duration_hours, 2),
                    "start_time": shift.start_time.isoformat() if shift.start_time else None,
                    "end_time": shift.end_time.isoformat() if shift.end_time else None
                })

        response = jsonify(stats)
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', 'https://kv-darbs.vercel.app'))
        response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response, 200

    except Exception as e:
        logging.error(f"Stats error: {str(e)}")
        return jsonify({"error": "Stats generation failed"}), 500 

@app.route("/api/stats/materials", methods=["GET"])
@token_required
def get_material_stats(current_user):
    try:
        # Get all materials with their usage in completed orders
        results = db.session.query(
            Material.id,
            Material.nosaukums,
            Material.vieniba,
            db.func.coalesce(db.func.sum(OrderMaterial.daudzums * Order.daudzums), 0).label("total_used")
        ).outerjoin(OrderMaterial, Material.id == OrderMaterial.material_id) \
         .outerjoin(Order, Order.id == OrderMaterial.order_id) \
         .filter(or_(Order.status == "Pabeigts", Order.status == None)) \
         .group_by(Material.id, Material.nosaukums, Material.vieniba) \
         .all()

        data = [
            {
                "id": material_id,
                "nosaukums": nosaukums,
                "vieniba": vieniba,
                "totalUsed": float(total_used) if total_used is not None else 0
            }
            for material_id, nosaukums, vieniba, total_used in results
        ]

        return jsonify(data), 200

    except Exception as e:
        logging.error(f"Material stats error: {str(e)}")
        return jsonify({"error": "Failed to get material statistics"}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("Received data:", data)  
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        kods = data.get("kods")
        if not kods:
            return jsonify({"error": "Kods not provided"}), 400

        
        try:
            if isinstance(kods, str):
                kods = int(kods)
        except ValueError:
            return jsonify({"error": "Nederīgs koda formāts"}), 400

        user = Employee.query.filter_by(kods=kods).first()
        if not user:
            return jsonify({"error": "Nepareizs kods"}), 401

        token = generate_token(user.id)
        user.token = token
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Pieteikšanās veiksmīga",
            "token": token,
            "user": {
                "id": user.id,
                "vards": user.vards,
                "uzvards": user.uzvards,
                "amats": user.amats
            },
            "redirect": "/admin" if user.amats == "Administrators" else "/home"
        }), 200
    except Exception as e:
        print("Error during login:", str(e))
        return jsonify({"error": "Server error"}), 500

@app.route("/login/password", methods=["POST"])
def login_with_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        kods = data.get("kods")
        password = data.get("password")
        
        if not kods or not password:
            return jsonify({"error": "Kods or password not provided"}), 400

        
        try:
            if isinstance(kods, str):
                kods = int(kods)
        except ValueError:
            return jsonify({"error": "Nederīgs koda formāts"}), 400
        
        user = Employee.query.filter_by(kods=kods).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"error": "Incorrect password"}), 401

        token = generate_token(user.id)
        user.token = token
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "vards": user.vards,
                "uzvards": user.uzvards,
                "amats": user.amats
            },
            "redirect": "/admin" if user.amats == "Administrators" else "/home"
        }), 200

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500 

@app.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    current_user.token = None
    db.session.commit()
    return jsonify({"success": True, "message": "Logout successful"}), 200

@app.route("/materials", methods=["GET"])
@token_required
def get_materials(current_user):
    try:
        materials = Material.query.all()
        return jsonify([{
            'id': material.id,
            'nosaukums': material.nosaukums,
            'noliktava': material.noliktava,
            'vieta': material.vieta,
            'vieniba': material.vieniba,
            'daudzums': material.daudzums or 0,
            'reserved_quantity': material.reserved_quantity or 0,
            'available_quantity': (material.daudzums or 0) - (material.reserved_quantity or 0)
        } for material in materials]), 200
    except Exception as e:
        logging.error(f"Error getting materials: {str(e)}")
        return jsonify({"error": "Неизвестная ошибка при получении материалов", "details": str(e)}), 500

@app.route("/materials/<int:material_id>", methods=["GET"])
@token_required
def get_material(current_user, material_id):
    try:
        material = db.session.get(Material, material_id)
        if not material:
            return jsonify({"error": "Materiāls nav atrasts"}), 404
            
        return jsonify({
            'id': material.id,
            'nosaukums': material.nosaukums,
            'noliktava': material.noliktava,
            'vieta': material.vieta,
            'vieniba': material.vieniba,
            'daudzums': material.daudzums or 0,
            'reserved_quantity': material.reserved_quantity or 0,
            'available_quantity': (material.daudzums or 0) - (material.reserved_quantity or 0)
        }), 200
    except Exception as e:
        logging.error(f"Error getting material: {str(e)}")
        return jsonify({"error": "Неизвестная ошибка при получении материала", "details": str(e)}), 500

@app.route("/orders", methods=["GET"])
@token_required
def get_orders(current_user):
    try:
        orders = Order.query.all()
        orders_list = []
        
        for order in orders:
            order_data = order.to_dict()
            logging.debug(f"Order data from to_dict in get_orders: {order_data}")
            orders_list.append(order_data)

        return jsonify(orders_list), 200

    except Exception as e:
        logging.error(f"Error getting orders: {str(e)}")
        return jsonify({"error": "Failed to get orders", "details": str(e)}), 500

@app.route("/orders/<int:order_id>", methods=["GET"])
@token_required
def get_order(current_user, order_id):
    try:
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify({'error': 'Pasūtījums nav atrasts'}), 404

        order_data = order.to_dict()
        logging.debug(f"Order data from to_dict in get_order: {order_data}")

        return jsonify(order_data), 200

    except Exception as e:
        logging.error(f"Error getting order: {str(e)}")
        return jsonify({"error": "Неизвестная ошибка при получении заказа", "details": str(e)}), 500

@app.route("/api/orders/<int:order_id>/accept", methods=["PATCH"])
@token_required
def accept_order(current_user, order_id):
    logging.info(f"Starting accept_order for order_id: {order_id}")
    try:
        order = db.session.get(Order, order_id)
        if not order:
            logging.warning(f"Order with ID {order_id} not found.")
            return jsonify({"error": "Order not found"}), 404

        if order.status != "Nav sākts":
            logging.warning(f"Order {order_id} is not in 'Nav sākts' status. Current status: {order.status}")
            return jsonify({"error": "Can only accept orders with status 'Nav sākts'"}), 400

        # Get order quantity
        order_daudzums = float(order.daudzums) if order.daudzums is not None else 0.0
        logging.info(f"Order daudzums: {order_daudzums}")

        # Deduct materials and remove reservations
        for order_material in order.materials:
            material = db.session.get(Material, order_material.material_id)
            if not material:
                logging.error(f"Material with id {order_material.material_id} not found during order acceptance.")
                return jsonify({"error": f"Material with id {order_material.material_id} not found"}), 404

            try:
                material_per_order_unit_daudzums = float(order_material.daudzums)
            except (TypeError, ValueError):
                logging.error(f"Invalid daudzums format for material {order_material.material_id} in order acceptance: {order_material.daudzums}")
                return jsonify({"error": f"Invalid material quantity format for material {order_material.material_id}"}), 400

            # Calculate total quantity to deduct
            total_material_quantity_for_order = material_per_order_unit_daudzums * order_daudzums
            
            # Deduct from available quantity
            material.daudzums = (material.daudzums or 0) - total_material_quantity_for_order
            
            # Remove reservation
            material.reserved_quantity = (material.reserved_quantity or 0) - total_material_quantity_for_order
            order_material.reserved = False
            
            logging.info(f"Material {material.id}: deducted {total_material_quantity_for_order}, new quantity {material.daudzums}, new reserved {material.reserved_quantity}")

        # Update order status and assign employee
        order.status = "Pieņemts"
        order.employee_id = current_user.id
        db.session.commit()
        logging.info(f"Order {order_id} accepted successfully. Returning: {order.to_dict()}")
        return jsonify(order.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.exception(f"Error accepting order {order_id}")
        return jsonify({"error": str(e)}), 500

@app.route("/orders/<int:order_id>/finish", methods=["PATCH"])
@token_required
def finish_order(current_user, order_id):
    try:
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        # Remove any remaining reservations
        for order_material in order.materials:
            material = db.session.get(Material, order_material.material_id)
            if material:
                # Calculate total quantity that was reserved
                total_reserved = float(order_material.daudzums or 0) * float(order.daudzums or 0)
                # Remove reservation
                material.reserved_quantity = (material.reserved_quantity or 0) - total_reserved
                order_material.reserved = False
        
        order.status = "Pabeigts"
        db.session.commit()
        
        return jsonify(order.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/employees", methods=["GET"])
@token_required
def get_employees(current_user):
    try:
        employees = db.session.query(Employee).all()
        return jsonify([{"id": employee.id,"vards": employee.vards,"uzvards": employee.uzvards,"amats": employee.amats,"kods": employee.kods,"status": employee.status} for employee in employees]), 200
    except Exception as e:
        logging.error(f"Error fetching employees: {str(e)}")
        return jsonify({"error": "Failed to fetch employees", "details": str(e)}), 500

@app.route("/employees", methods=["POST"])
@token_required
def add_employee(current_user):
    try:
        data = request.get_json()

        # Pārbaudam, vai jau eksistē darbinieks ar šādu kodu
        existing_employee = Employee.query.filter_by(kods=data["kods"]).first()
        if existing_employee:
            return jsonify({"error": "Darbinieks ar šādu kodu jau eksistē"}), 400

        password_hash = None
        if data["amats"].lower() == "administrators":
            raw_password = data.get("password")
            if not raw_password:
                return jsonify({"error": "Parole ir obligāta administratoram"}), 400
            password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_employee = Employee(
            vards=data["vards"],
            uzvards=data["uzvards"],
            amats=data["amats"],
            kods=data["kods"],
            status=data["status"],
            password=password_hash
        )

        db.session.add(new_employee)
        db.session.commit()
        return jsonify({"success": True, "message": "Darbinieks pievienots"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/employees/<int:id>", methods=["PUT"])
@token_required
def update_employee(current_user, id):
    try:
        data = request.get_json()
        employee = db.session.get(Employee, id)
        if not employee:
            return jsonify({"error": "Darbinieks nav atrasts"}), 404

        # Check for duplicate kods
        if "kods" in data and data["kods"] != employee.kods:
            existing_employee = Employee.query.filter_by(kods=data["kods"]).first()
            if existing_employee and existing_employee.id != employee.id:
                return jsonify({"error": "Darbinieks ar šādu kodu jau eksistē"}), 400

        # Update employee data
        employee.vards = data.get("vards", employee.vards)
        employee.uzvards = data.get("uzvards", employee.uzvards)
        employee.amats = data.get("amats", employee.amats)
        employee.kods = data.get("kods", employee.kods)
        employee.status = data.get("status", employee.status)
        
        if "password" in data and data["password"]:
            employee.password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        db.session.commit()
        return jsonify({"success": True, "message": "Darbinieks atjaunināts", "employee": employee.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Неизвестная ошибка при обновлении сотрудника", "details": str(e)}), 500

@app.route("/employees/<int:id>", methods=["DELETE"])
@token_required
def delete_employee(current_user, id):
    try:
        employee = db.session.get(Employee, id)
        if not employee:
            return jsonify({"error": "Darbinieks nav atrasts"}), 404

        db.session.delete(employee)
        db.session.commit()
        return jsonify({"success": True, "message": "Darbinieks dzēsts"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Неизвестная ошибка при удалении сотрудника", "details": str(e)}), 500

@app.route("/api/orders/<int:order_id>", methods=["PUT"])
@token_required
def update_order(current_user, order_id):
    logging.info(f"Starting update_order for order_id: {order_id}")
    try:
        order = db.session.get(Order, order_id)
        if not order:
            logging.warning(f"Order with ID {order_id} not found.")
            return jsonify({"error": "Order not found"}), 404

        data = request.get_json()
        logging.debug(f"Received data for update_order: {data}")
        
        # Validate required fields
        if not all(key in data for key in ['nosaukums', 'daudzums', 'materials']):
            logging.error(f"Missing required fields in request data: {data}")
            return jsonify({"error": "Missing required fields"}), 400

        # Ensure order daudzums is a float
        try:
            order_daudzums = float(data['daudzums'])
        except (TypeError, ValueError):
            logging.error(f"Invalid daudzums format for order: {data['daudzums']}")
            return jsonify({"error": "Invalid order quantity format"}), 400
        logging.info(f"Order daudzums after casting: {order_daudzums}")

        # Store old materials for comparison
        old_materials = {om.material_id: om for om in order.materials}
        
        # First, release all old reservations
        for order_material in order.materials:
            material = db.session.get(Material, order_material.material_id)
            if material:
                old_reserved = material.reserved_quantity or 0
                old_total = float(order_material.daudzums or 0) * float(order.daudzums or 0)
                material.reserved_quantity = old_reserved - old_total
                logging.info(f"Released old reservation for material {material.id}: {old_total}")

        # Check if new materials are available
        insufficient_materials = []
        for material_data in data['materials']:
            material = db.session.get(Material, material_data['material_id'])
            if not material:
                logging.error(f"Material with id {material_data['material_id']} not found during availability check.")
                return jsonify({"error": f"Material with id {material_data['material_id']} not found"}), 404
            
            try:
                material_per_order_unit_daudzums = float(material_data['daudzums'])
            except (TypeError, ValueError):
                logging.error(f"Invalid daudzums format for material {material_data['material_id']}: {material_data['daudzums']}")
                return jsonify({"error": f"Invalid material quantity format for material {material_data['material_id']}"}), 400

            # Calculate total required quantity for the entire order
            total_required_quantity = material_per_order_unit_daudzums * order_daudzums
            available_quantity = (material.daudzums or 0) - (material.reserved_quantity or 0)
            
            logging.info(f"Material {material.id}: required {total_required_quantity}, available {available_quantity}")
            if total_required_quantity > available_quantity:
                insufficient_materials.append({
                    "nosaukums": material.nosaukums,
                    "required": total_required_quantity,
                    "available": available_quantity,
                    "unit": material.vieniba
                })

        if insufficient_materials:
            # Restore old reservations
            for order_material in order.materials:
                material = db.session.get(Material, order_material.material_id)
                if material:
                    old_total = float(order_material.daudzums or 0) * float(order.daudzums or 0)
                    material.reserved_quantity = (material.reserved_quantity or 0) + old_total
            db.session.rollback()
            
            error_message = "Nepietiek materiālu:\n"
            for mat in insufficient_materials:
                error_message += f"- {mat['nosaukums']}: Nepieciešams {mat['required']} {mat['unit']}, Pieejams {mat['available']} {mat['unit']}\n"
            return jsonify({"error": error_message}), 400
                
        # Update order
        logging.info(f"Updating order {order_id} details: nosaukums={data['nosaukums']}, daudzums={order_daudzums}")
        order.nosaukums = data['nosaukums']
        order.daudzums = order_daudzums

        # Clear old materials
        logging.info(f"Clearing old order materials for order {order_id}.")
        OrderMaterial.query.filter_by(order_id=order.id).delete()

        # Add new materials and reserve them
        logging.info(f"Adding new materials and reserving them.")
        for material_data in data['materials']:
            material = db.session.get(Material, material_data['material_id'])
            if not material:
                logging.error(f"Material with id {material_data['material_id']} not found during order creation.")
                return jsonify({"error": f"Material with id {material_data['material_id']} not found"}), 404
            
            try:
                material_per_order_unit_daudzums = float(material_data['daudzums'])
            except (TypeError, ValueError):
                logging.error(f"Invalid daudzums format for material {material_data['material_id']} in order creation: {material_data['daudzums']}")
                return jsonify({"error": f"Invalid material quantity format for material {material_data['material_id']}"}), 400

            total_material_quantity_for_order = material_per_order_unit_daudzums * order_daudzums
            
            # Create order-material link
            order_material = OrderMaterial(
                order_id=order.id,
                material_id=material.id,
                daudzums=material_per_order_unit_daudzums,
                reserved=True
            )
            db.session.add(order_material)
            
            # Update material reservation
            material.reserved_quantity = (material.reserved_quantity or 0) + total_material_quantity_for_order
            logging.info(f"Material {material.id}: new reserved {material.reserved_quantity} after adding new order material.")

        db.session.commit()
        logging.info(f"Order {order_id} updated successfully. Returning: {order.to_dict()}")
        return jsonify(order.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        logging.exception(f"Error updating order {order_id}") # Log full traceback
        return jsonify({"error": str(e)}), 500

@app.route("/materials", methods=["POST"])
@token_required
def create_material(current_user):
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['nosaukums', 'noliktava', 'vieta', 'vieniba', 'daudzums']):
            return jsonify({"error": "Missing required fields"}), 400

        # Check for duplicate material with same name and warehouse
        existing_material = Material.query.filter_by(nosaukums=data['nosaukums'], noliktava=data['noliktava']).first()
        if existing_material:
            # If duplicate, update quantity
            existing_material.daudzums = (existing_material.daudzums or 0) + (data['daudzums'] or 0)
            db.session.commit()
            return jsonify(existing_material.serialize()), 200
        
        new_material = Material(
            nosaukums=data['nosaukums'],
            noliktava=data['noliktava'],
            vieta=data['vieta'],
            vieniba=data['vieniba'],
            daudzums=data['daudzums'] or 0
        )
        db.session.add(new_material)
        db.session.commit()
        return jsonify(new_material.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/materials/<int:material_id>", methods=["PUT"])
@token_required
def update_material(current_user, material_id):
    try:
        material = db.session.get(Material, material_id)
        if not material:
            return jsonify({"error": "Materiāls nav atrasts"}), 404

        data = request.get_json()
        
        # If quantity becomes zero or less, delete the material
        if 'daudzums' in data and (data['daudzums'] or 0) <= 0:
            db.session.delete(material)
            db.session.commit()
            return jsonify({"message": "Material deleted due to zero quantity"}), 200

        material.nosaukums = data.get('nosaukums', material.nosaukums)
        material.noliktava = data.get('noliktava', material.noliktava)
        material.vieta = data.get('vieta', material.vieta)
        material.vieniba = data.get('vieniba', material.vieniba)
        material.daudzums = data.get('daudzums', material.daudzums or 0)

        db.session.commit()
        return jsonify(material.serialize()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/materials/<int:material_id>", methods=["DELETE"])
@token_required
def delete_material(current_user, material_id):
    try:
        material = db.session.get(Material, material_id)
        if not material:
            return jsonify({"error": "Materiāls nav atrasts"}), 404

        # Remove any reservations associated with this material from orders
        orders_with_this_material = Order.query.join(OrderMaterial).filter(OrderMaterial.material_id == material_id).all()

        for order in orders_with_this_material:
            for order_material in order.materials:
                if order_material.material_id == material_id and order_material.reserved:
                    material.reserved_quantity = (material.reserved_quantity or 0) - (order_material.daudzums * order.daudzums)
        
        db.session.delete(material)
        db.session.commit()
        return jsonify({"message": "Material deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/orders", methods=["POST"])
@token_required
def create_order(current_user):
    try:
        data = request.get_json()
        logging.debug(f"Received data for create_order: {data}") # Added logging
        
        # Validate required fields
        if not all(key in data for key in ['nosaukums', 'daudzums', 'materials']):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if materials are available
        for material_data in data['materials']:
            material = db.session.get(Material, material_data['material_id'])
            if not material:
                return jsonify({"error": f"Material with id {material_data['material_id']} not found"}), 404
            
            required_quantity = (material_data['daudzums'] or 0) * (data['daudzums'] or 0)
            available_quantity = (material.daudzums or 0) - (material.reserved_quantity or 0);
            
            if required_quantity > available_quantity:
                return jsonify({
                    "error": f"Not enough material {material.nosaukums}. Required: {required_quantity}, Available: {available_quantity}"
                }), 400
            
        # Create order
        try:
            order_daudzums = float(data['daudzums'])
        except (TypeError, ValueError):
            logging.error(f"Invalid daudzums format for order: {data['daudzums']}")
            return jsonify({"error": "Invalid order quantity format"}), 400

        order = Order(
            nosaukums=data['nosaukums'],
            daudzums=order_daudzums,
            status="Nav sākts"
        )
        db.session.add(order)
        db.session.flush()

        # Add materials and reserve them
        for material_data in data['materials']:
            material = db.session.get(Material, material_data['material_id'])
            if not material:
                logging.error(f"Material with id {material_data['material_id']} not found during order creation.")
                return jsonify({"error": f"Material with id {material_data['material_id']} not found"}), 404
            
            try:
                material_per_order_unit_daudzums = float(material_data['daudzums'])
            except (TypeError, ValueError):
                logging.error(f"Invalid daudzums format for material {material_data['material_id']} in order creation: {material_data['daudzums']}")
                return jsonify({"error": f"Invalid material quantity format for material {material_data['material_id']}"}), 400

            total_material_quantity_for_order = material_per_order_unit_daudzums * order_daudzums
            
            # Create order-material link
            order_material = OrderMaterial(
                order_id=order.id,
                material_id=material.id,
                daudzums=material_per_order_unit_daudzums,
                reserved=True
            )
            db.session.add(order_material)
            
            # Update material reservation
            material.reserved_quantity = (material.reserved_quantity or 0) + total_material_quantity_for_order
        
        db.session.commit()
        return jsonify(order.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/orders/<int:order_id>", methods=["DELETE"])
@token_required
def delete_order(current_user, order_id):
    try:
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        # Remove reservations only if the order is not started
        if order.status == "Nav sākts":
            for order_material in order.materials:
                material = db.session.get(Material, order_material.material_id)
                if material:
                    # Calculate total reserved quantity (material quantity * order quantity)
                    total_reserved = float(order_material.daudzums or 0) * float(order.daudzums or 0)
                    # Remove reservation
                    material.reserved_quantity = (material.reserved_quantity or 0) - total_reserved
                    order_material.reserved = False
                    logging.debug(f"Delete Order: Removed reservation for material {material.nosaukums} (ID: {material.id}). Removed quantity: {total_reserved}")
        
        # Delete order (this will also delete order_materials due to cascade)
        db.session.delete(order)
        db.session.commit()

        return jsonify({"message": "Order deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting order {order_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/shifts/start', methods=['POST'])
@token_required
def start_shift(current_user):
    try:
        data = request.get_json()
        if not data or 'employee_id' not in data:
            return jsonify({"error": "Missing employee_id"}), 400

        employee = db.session.get(Employee, data['employee_id'])
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        shift = Shift(employee_id=employee.id, start_time=datetime.datetime.now())
        db.session.add(shift)
        db.session.commit()
        return jsonify({"message": "Shift started", "shift_id": shift.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/shifts/end/<int:shift_id>', methods=['PUT'])
@token_required
def end_shift(current_user, shift_id):
    try:
        shift = db.session.get(Shift, shift_id)
        if not shift:
            return jsonify({"error": "Shift not found"}), 404

        shift.end_time = datetime.datetime.now()
        db.session.commit()
        return jsonify({"message": "Shift ended"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/shifts", methods=["GET"])
@token_required
def get_shifts(current_user):
    try:
        shifts = Shift.query.all()
        shifts_list = []
        for shift in shifts:
            # Calculate status based on start_time and end_time
            status = "Nav sākts"
            if shift.start_time:
                status = "Pabeigts" if shift.end_time else "Aktīva"
            
            shift_data = {
                'id': shift.id,
                'datums': shift.start_time.isoformat() if shift.start_time else None,
                'status': status,
                'start_time': shift.start_time.isoformat() if shift.start_time else None,
                'end_time': shift.end_time.isoformat() if shift.end_time else None
            }
            
            # Get employee data if exists
            if shift.employee_id:
                employee = db.session.get(Employee, shift.employee_id)
                if employee:
                    shift_data['employee'] = {
                        'id': employee.id,
                        'vards': employee.vards,
                        'uzvards': employee.uzvards
                    }
                else:
                    shift_data['employee'] = None
            else:
                shift_data['employee'] = None
                
            shifts_list.append(shift_data)
            
        return jsonify(shifts_list), 200
    except Exception as e:
        logging.error(f"Error getting shifts: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    try:
        # Basic counts
        total_materials = Material.query.count()
        total_workers = Employee.query.count()
        total_orders = Order.query.count()
        total_shifts = Shift.query.count()
        
        # Calculate total materials quantity
        total_materials_quantity = db.session.query(db.func.sum(Material.daudzums)).scalar() or 0

        return jsonify({
            "total_materials": total_materials,
            "total_workers": total_workers,
            "total_orders": total_orders,
            "total_shifts": total_shifts,
            "total_materials_quantity": float(total_materials_quantity)
        }), 200

    except Exception as e:
        logging.error(f"Stats error: {str(e)}")
        return jsonify({"error": "Failed to get statistics"}), 500

@app.route('/materials/transfer', methods=['POST'])
@token_required
def transfer_material(current_user):
    try:
        data = request.get_json()
        print(f"Received transfer data: {data}")  # Debug log
        
        if not data:
            return jsonify({"error": "No data provided"}), 400

        material_id = data.get('material_id')
        to_warehouse = data.get('toNoliktava')  # Changed from to_warehouse to toNoliktava
        quantity = data.get('daudzums')  # Changed from quantity to daudzums

        print(f"Parsed values - material_id: {material_id}, to_warehouse: {to_warehouse}, quantity: {quantity}")  # Debug log

        if not all([material_id, to_warehouse, quantity is not None]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            quantity = float(quantity)
            if quantity <= 0:
                return jsonify({"error": "Quantity must be greater than 0"}), 400
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid quantity value"}), 400

        material = db.session.get(Material, material_id)
        if not material:
            return jsonify({"error": "Material not found"}), 404

        print(f"Source material: {material.nosaukums}, current quantity: {material.daudzums}")  # Debug log

        if (material.daudzums or 0) < quantity:
            return jsonify({"error": "Not enough material in source location"}), 400

        # Deduct from source material
        material.daudzums = (material.daudzums or 0) - quantity

        # Add to target material (find or create)
        target_material = Material.query.filter_by(nosaukums=material.nosaukums, noliktava=to_warehouse).first()
        if target_material:
            target_material.daudzums = (target_material.daudzums or 0) + quantity
            print(f"Updated existing target material: {target_material.nosaukums}, new quantity: {target_material.daudzums}")  # Debug log
        else:
            new_material = Material(
                nosaukums=material.nosaukums,
                noliktava=to_warehouse,
                vieta=material.vieta,
                vieniba=material.vieniba,
                daudzums=quantity
            )
            db.session.add(new_material)
            print(f"Created new target material: {new_material.nosaukums}, quantity: {new_material.daudzums}")  # Debug log

        # If source material quantity becomes zero or less, delete it
        if (material.daudzums or 0) <= 0:
            db.session.delete(material)
            print(f"Deleted source material as quantity reached zero")  # Debug log

        db.session.commit()
        return jsonify({"message": "Material transferred successfully"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in transfer_material: {str(e)}")  # Debug logging
        return jsonify({"error": str(e)}), 500

@app.route("/orders/<int:order_id>/cancel", methods=["PATCH"])
@token_required
def cancel_order(current_user, order_id):
    try:
        order = db.session.get(Order, order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        if order.status == "Pabeigts":
            return jsonify({"error": "Cannot cancel a finished order"}), 400

        # Release reserved materials if order was not started or is in progress
        if order.status == "Nav sākts" or order.status == "Procesā":
            for order_material in order.materials:
                material = db.session.get(Material, order_material.material_id)
                if material:
                    material.reserved_quantity = (material.reserved_quantity or 0) - ((order_material.daudzums or 0) * (order.daudzums or 0))
                    order_material.reserved = False # Mark as not reserved
        
        order.status = "Atcelts"
        db.session.commit()
        
        return jsonify({"message": "Order cancelled successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/materials/<int:material_id>/move", methods=["PATCH"])
@token_required
def move_material(current_user, material_id):
    try:
        data = request.get_json()
        target_location = data.get('to_location')
        quantity_to_move = data.get('quantity') or 0

        if not all([target_location, quantity_to_move is not None]):
            return jsonify({"error": "Missing required fields"}), 400

        source_material = db.session.get(Material, material_id)
        if not source_material:
            return jsonify({"error": "Source material not found"}), 404

        if (source_material.daudzums or 0) < quantity_to_move:
            return jsonify({"error": "Not enough material to move"}), 400

        # Deduct from source
        source_material.daudzums = (source_material.daudzums or 0) - quantity_to_move

        # Find or create in target location
        target_material = Material.query.filter_by(nosaukums=source_material.nosaukums, noliktava=target_location).first()
        if target_material:
            target_material.daudzums = (target_material.daudzums or 0) + quantity_to_move
        else:
            new_material = Material(
                nosaukums=source_material.nosaukums,
                noliktava=target_location,
                vieta=source_material.vieta, 
                vieniba=source_material.vieniba,
                daudzums=quantity_to_move
            )
            db.session.add(new_material)
        
        # If source material quantity becomes zero or less, delete it
        if (source_material.daudzums or 0) <= 0:
            db.session.delete(source_material)

        db.session.commit()
        return jsonify({"message": "Material moved successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/materials/<int:material_id>/quantity", methods=["PATCH"])
@token_required
def update_material_quantity(current_user, material_id):
    try:
        data = request.get_json()
        new_quantity = data.get('quantity')
        
        if new_quantity is None:
            return jsonify({"error": "Quantity not provided"}), 400

        material = db.session.get(Material, material_id)
        if not material:
            return jsonify({"error": "Material not found"}), 404

        # If new quantity is zero or less, delete the material
        if (new_quantity or 0) <= 0:
            db.session.delete(material)
            db.session.commit()
            return jsonify({"message": "Material deleted due to zero quantity"}), 200

        material.daudzums = new_quantity or 0
        db.session.commit()
        return jsonify({"message": "Material quantity updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

