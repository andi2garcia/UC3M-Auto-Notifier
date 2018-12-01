Auto notificador de tareas UC3M
----

NOTE: These docs are written in Spanish just because it's made for my university colleages and me. Please do not hesitate to contact me if you need info in English.

Este programa se encarga de notificar acciones pendientes en la plataforma aulaglobal de la UC3M,
aunque vale para cualquier plataforma de Moodle (por ende, para cualquier universidad que lo use).
Si eres de otra universidad o requieres del programa y tienes conocimientos nulos de programación en Pyton,
contáctame e intentamos arreglarlo.


**Acciones notificadas:**

- Calificaciones nuevas o actualizadas.
- Encuestas nuevas o actualizadas.
- Cuestionarios nuevos o actualizados.
- Recursos nuevos o actualizados.
- Tareas nuevas o actualizadas.

Posee dos modos de notificación, por la propia consola al ejecutarlo, email o Telegram bot.

La utilidad principal de este programa es dejarlo corriendo en un servidor o en el propio PC en segundo plano, de modo que
cuando surja una actualización te notifique al instante. Si lo cierras, no notifica.
Lo óptimo sería un cron ejecutado cada x tiempo.

**¿Cómo usarlo?**

0. Tener instalado Python.
1. Editar el fichero Config.py. Introducir entre las comillas correspondientes el usuario y contraseña de la UC3M.
2. Correr el archivo ejecutándolo con Python.

TODO (Tareas pendientes): 
- Notificación por EMAIL
- Notificación por Telegram
- Si hay mucha demanda, un manejo más fácil de este (cloud-oriented for dummies)
