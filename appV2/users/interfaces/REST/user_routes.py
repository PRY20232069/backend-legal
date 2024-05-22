from appV2.users.interfaces.REST.controllers.users_controller import router
from appV2.users.interfaces.REST.controllers.register_user_controller import register_user
from appV2.users.interfaces.REST.controllers.login_user_controller import login_user
from appV2.users.interfaces.REST.controllers.recover_user_controller import recover_user
from appV2.users.interfaces.REST.controllers.get_user_controller import get_user
from appV2.users.interfaces.REST.controllers.get_all_users_controller import get_all_users

user_router = router