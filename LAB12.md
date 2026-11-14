# Laboratorio 12 Servicios web con React y Django

La sección Exámenes del cliente consume la API de cuestionarios del laboratorio 8. Django espera el origen `http://127.0.0.1:5174` y React apunta a `http://127.0.0.1:8000/api/`.

## Servidor

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/manage.py migrate
python src/manage.py createsuperuser
python src/manage.py drf_create_token USUARIO
python src/manage.py runserver 127.0.0.1:8000
```

Reemplaza `USUARIO` por el usuario que creaste. Copia su token y colócalo en el campo Token de Django en la sección Exámenes. El token se conserva en la sesión de la pestaña.

## Cliente

```sh
cd frontend
npm ci
npm run dev
```

Abre `http://127.0.0.1:5174/#exams`. Si cambias alguna dirección puedes configurar `DAE_REACT_ORIGIN` para Django y `VITE_API_URL` para Vite.

## Comprobaciones

| Acción | Petición | Resultado |
| --- | --- | --- |
| Entrar o actualizar el listado | GET /api/exams/?page=1 | Esqueleto durante la carga y tabla paginada con la respuesta |
| Guardar un título válido | POST /api/exams/ | Alta y retorno al listado |
| Enviar el título vacío | POST /api/exams/ | El mensaje del campo devuelto por Django aparece debajo del título |
| Eliminar un examen | DELETE /api/exams/{id}/ | Tras confirmar, se actualiza el listado |
| Actualizar con Django detenido | GET /api/exams/?page=1 | Mensaje de error y botón Reintentar |
