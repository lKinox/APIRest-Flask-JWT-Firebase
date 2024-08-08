import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import uuid

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class User:
    def __init__(self, id, username, email, password_hash, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def create_user(username, email, password_hash, created_at):
        id = str(uuid.uuid4())
        doc_ref = db.collection("users").document(username)
        doc = doc_ref.get()

        if doc.exists:
            raise ValueError("Usario ya existente. Intente con uno diferente")
        
        data = {
            "id": id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": created_at
        }
        db.collection("users").document(username).set(data)

        return User(id, username, email, password_hash, created_at)

class Authenticate:
    def __init__(self, id, username, email, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash


    def verify_user(username, password):
        # Obtener el documento de usuario de Firestore
        doc_ref = db.collection("users").document(username)
        doc = doc_ref.get()

        # Verificar si el documento existe
        if doc.exists:
            data = doc.to_dict()
            password_hash_bd = data["password_hash"]

            # Verificar la contraseña
            if verify_hash_password(password, password_hash_bd):
                return User(data["id"], username, data["email"], password_hash_bd, data["created_at"])
            else:
                return None
        else:
            return None
    
    def get_user(username):
        doc_ref = db.collection("users").document(username)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            return (username, data["email"], data["id"], data["created_at"])
        else:
            return None

class Update:
    @staticmethod
    def update_user(username, new_username, email):
        doc_ref = db.collection("users").document(username)
        doc = doc_ref.get()

        if username == new_username:
            return {"error": "El nuevo nombre de usuario no puede ser el mismo que el actual."}

        if doc.exists:

            original_data_db = doc.to_dict()

            if original_data_db.get("email") == email:
                return {"error": "El nuevo email no puede ser el mismo que el actual."}
            
            # Crea un nuevo documento con el nuevo nombre de usuario
            new_data_db = db.collection("users").document(new_username)
            new_data_db.set(original_data_db)  # Copia los datos originales
            
            # Actualiza el nuevo documento con el nuevo nombre de usuario y el correo
            data = {
                "username": new_username,
                "email": email
            }
            new_data_db.update(data)

            # Elimina el documento original
            doc_ref.delete()
            
            # Devuelve una nueva instancia de User
            return User(
                id=original_data_db.get("id"),  # Asegúrate de obtener el ID del nuevo documento
                username=new_username,
                email=email,
                password_hash=original_data_db.get("password_hash"),  # Mantén la contraseña
                created_at=original_data_db.get("created_at")  # Mantén la fecha de creación
            )
        else:
            return None
        
class Delete:
    def delete_user(username):
        doc_ref = db.collection("users").document(username)
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.delete()
            return None
        else:
            return {"error": "Hubo un error al eliminar la cuenta."}


def verify_hash_password(password, password_hash):
    if isinstance(password, list):
        password = str(password[0]) 
    return hashlib.sha256(password.encode('utf-8')).hexdigest() == password_hash