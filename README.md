
# API Rest Flask + JWT

## Introducción

Esta API REST, construida con Flask y protegida con JWT (JSON Web Tokens), usa como base de datos a Firebase. Proporciona funcionalidades básicas de registro, inicio de sesión y gestión de usuarios.


## Configuration

### Requerimientos:

* Python (versión recomendada: 3.6+)
* Virtualenv o venv
* Un gestor de paquetes como pip



### Instalación:

1. Clona este repositorio:
```
git clone https://github.com/lKinox/APIRest-Flask-JWT-Firebase.git
```
2. Crea y activa un entorno virtual
```
python -m venv venv

source venv/bin/activate  # Linux/macOS

venv\Scripts\activate  # Windows
```
3. Instala las dependencias:

```
pip install -r requirements.txt
```
## Uso de la API

### Endpoints:

* /register (GET)
  - Respuesta:
    ```json
    {
      "Mensaje": "Inserte parámetros de registro"
    }
    ```
* /register (POST)
  - Cuerpo:
    ```json
    {
      "username": "Example",
      "email": "example@example.com",
      "password": "example123"
    }
    ```
  - Respuesta:
    ```json
    {
      "mensaje": "Usuario registrado exitosamente"
    }
    ```
    En caso de que el username ya exista en la base de datos:
    ```json
    {
      "error": "Username already exists"
    }
    ```
* /login (GET)
  - Respuesta:
    ```json
    {
      "mensaje": "Inserte Usuario y Contraseña"
    }
    ```
* /login (POST)
  - Cuerpo:
    ```json
    {
    "username": "Example",
    "password": "example123"
    }
    ```
  - Respuesta:
    ```json
    {
      "mensaje": "El usuario fue autenticado satisfactoriamente"
    }
    ```
    En caso de que el username o el password sean incorrectos
    ```json
    {
      "error": "Credenciales inválidas"
    }
    ```
* /user (GET)
  - Headers:
    ```
    Authorization <JWT TOKEN>
    ```
  - Respuesta:
    ```json
    {
      "Created At": "Wed, 07 Aug 2024 18:17:59 GMT",
      "Email": "example@example.com",
      "ID": "d4e1c603-6ec3-4020-a626-67c430f49813",
      "Usuario": "Example"
    }
    ```
* /user (PUT)
  - Headers:
    ```
    Authorization <JWT TOKEN>
    ```
  - Cuerpo:
    ```json
    {
      "username": "Example2",
      "email": "example2@example.com"
    }
    ```
  - Respuesta:
    ```json
    {
      "Nuevo Email": "example2@example.com",
      "Nuevo Usuario": "Example2",
      "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQ0ZTFjNjAzLTZlYzMtNDAyMC1hNjI2LTY3YzQzMGY0OTgxMyIsInVzZXJuYW1lIjoiRXhhbXBsZTIiLCJleHAiOjE3MjMyMjM4NzN9.gXT2nk9zjgFEEKZfXt9xGdfBqvoTXu-8YBgc84bBGj8"
    }
    ```
    En caso de que el username o el email sean iguales al que tienen actualmente
    ```json
    {
      "error": "El nuevo nombre de usuario no puede ser el mismo que el actual."
    }
    ```
    ```json
    {
      "error": "El nuevo email no puede ser el mismo que el actual."
    }
    ```
* /user (DELETE)
  - Headers:
    ```
    Authorization <JWT TOKEN>
    ```
  - Respuesta:
    ```json
    {
      "Mensaje": "Usuario eliminado correctamente"
    }
    ```


## Pruebas

Para probar esta API puede usar la siguiente URL:
```
https://lkinox.pythonanywhere.com
```
Además puede utilizar https://reqbin.com/ como herramienta de testing
