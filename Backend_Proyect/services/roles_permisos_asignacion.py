from model.roles import Rol
from model.permisos import Permisos
from model.roles_permisos import Rol_permiso


rol_super_admin = Rol(nombre_rol="super_admin", descripcion="Para la creacion de empresas")
rol_admin = Rol(nombre_rol="admin", descripcion="Para la creacion de usuarios")
rol_user = Rol(nombre_rol="user", descripcion="Para la creacion de alertas")
rol_entertainer = Rol(nombre_rol="entertainer", descripcion="Para la creacion de eventos")
rol_segurity = Rol(nombre_rol="segurity", descripcion="Para la creacion de alertas")

permiso_crear_empresa = Permisos(nombre_permiso="crear_empresa", descripcion="Permite la creacion de empresas")
permiso_crear_usuario = Permisos(nombre_permiso="crear_usuario", descripcion="Permite la creacion de usuarios")
permiso_editar_usuario = Permisos(nombre_permiso="editar_usuario", descripcion="Permite la edicion de usuarios")
permiso_lee_usuario = Permisos(nombre_permiso="lee_usuario", descripcion="Permite la lectura de usuarios")
permiso_eliminar_usuario = Permisos(nombre_permiso="eliminar_usuario", descripcion="Permite la eliminacion de usuarios")


