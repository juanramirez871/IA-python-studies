# Instalación

* Ejecutar ```pip install```

* Ejecutar ```docker-compose up -d```

## Funcionalidad

* Primero debes crear un usuario, existes dos tipos de roles el *admin* y el *user*.
Endpoint = ```/users```

```JSON
{
    "name": "user",
    "email": "user@gmail.com",
    "password": "123",
    "role": "admin"
}
```

Generara un token y sera el que debes enviar en cada header para tener acceso a la api

* Tambien puedes iniciar session si se te ha perdido el token.
Endpoindt = ```/users/login```

```JSON
{
    "email": "juandiegoramirez071@gmail.com",
    "password": "123"
}
```

* Si se te olvida la contraseña la api envia un correo con el codigo verificador para poder cambiar la contraseña

Endpoindt = ```/users/send-email```

```JSON
{
    "email": "juandiegoramirez071@gmail.com"
}
```

* En este endpoindt tendras que enviar el codigo dado en el correo

Endpoindt = ```/users/forgot-password```

```JSON
{
    "email": "juandiegoramirez071@gmail.com",
    "code": 71602,
    "password": "new password"
}
```

* Ya podras crear un equipo pero solo si eres un administrador
Endpoindt = ```/teams```

```JSON
{
    "name": "team",
    "description": "the best team" 
}
```

* Podes agregar miembros al equipo
Endpoindt = ```team/{team_id}/user/{user_id}```

* Podes Listar todos los usuarios que pertenece a un equipo
Endpoindt = ```teams/{team_id}```

* Ahora podes crear una tarea a un equipo
Endpoindt = ```teams/1/tasks```

```JSON
{
    "name": "Easy task",
    "description": "Create facebook" 
}
```

* Ahora podes ver las tareas de un equipo
Endpoindt = ```teams/1/tasks```
