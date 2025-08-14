from enum import Enum


class WordConst(Enum):

    missing = 'Отсутствуют'
    activated = 'Активный'
    deactivated = 'Деактивированный'
    yes = 'да'
    no = 'нет'
    manager = 'manager'
    metrika = 'metrika'
    direct = 'direct'
    goals = 'goals'


class PoolingConstant(Enum):

    text = 'text'
    online_users = '_online_users'
    session = 'session'
    i18n = 'i18n'
    dialog_manager = 'dialog_manager'
    event_from_user = 'event_from_user'


class UserDataConstant(Enum):
    role_id = 'role_id'
    username = 'username'
    login = 'login'


class WidgetDataConstant(Enum):
    companies = 'companies'
    users = 'users'
    projects = 'projects'
    projects_id = 'projects_id'

    list_attributions = 'list_attributions'
    list_m_attributions = 'list_m_attributions'
    list_k_goals = 'list_k_goals'
    list_m_goals = 'list_m_goals'
    list_viewers = 'list_viewers'
    list_projects = 'list_projects'

    company_name = 'company_name'
    company_id = 'company_id'
    company_created = 'company_created'

    err_uniq_company = 'error_uniq_company'
    err_uniq_username = 'error_input_username'
    err_uniq_login = 'error_input_login'
    err_input_title = 'error_input_title'
    err_input_login = 'error_input_login'
    err_input_text = 'error_input_text'
    err_input_date = 'error_input_date'

    username = 'username'
    user_login = 'user_login'
    user_password = 'user_password'
    user_edit = 'user_edit'
    user_uuid = 'user_uuid'
    user_role_id = 'user_role_id'
    user_role_name = 'user_role_name'

    manager_projects = 'manager_projects'
    manager_uuid = 'manager_uuid'

    mode_edit = 'mode_edit'

    counter_name = 'counter_name'
    counter_id = 'counter_id'
    counter_attribution = 'counter_attribution'
    counter_minor_attribution = 'counter_minor_attribution'
    counter_k_goals = 'counter_k_goals'
    counter_m_goals = 'counter_m_goals'
    counter_ecommerce = 'counter_ecommerce'
    counter_created_at = 'counter_created_at'

    selected_counter_name = 'selected_counter_name'
    selected_counter_id = 'selected_counter_id'
    selected_attribution = 'selected_attribution'
    selected_minor_attribution = 'selected_minor_attribution'
    selected_counter_k_goals_id = 'selected_counter_k_goals_id'
    selected_counter_m_goals_id = 'selected_counter_m_goals_id'
    selected_counter_k_goals_names = 'selected_counter_k_goals_names'
    selected_counter_m_goals_names = 'selected_counter_m_goals_names'
    selected_counter_ecommerce = 'selected_counter_ecommerce'

    selected_manager_set_to_project = 'selected_manager_set_to_prjct'
    selected_manager_remove_from_project = 'selected_manager_remove_from_prjct'

    viewer_uuid = 'viewer_uuid'
    viewer_username = 'viewer_username'
    viewer_login = 'viewer_login'
    viewer_password = 'viewer_password'
    viewer_available_list_projects = 'viewer_available_list_prjcts'
    viewer_connected_list_projects = 'viewer_connected_list_prjcts'

    project_id = 'project_id'
    project_title = 'project_title'
    project_description = 'project_description'
    project_connected_counters = 'project_connected_counters'
    project_connected_logins = 'project_connected_logins'
    project_author = 'project_author'
    project_list_counters = 'project_list_counters'
    project_list_logins = 'project_list_logins'
    project_report = 'project_report'
    project_ya_list_active_logins = 'project_ya_list_active_logins'
    project_ya_list_inactive_logins = 'project_ya_list_inactive_logins'
    project_ya_deactivated_logins = 'project_ya_deactivated_logins'
    project_ya_activated_logins = 'project_ya_activated_logins'
    project_ya_direct_access_token = 'project_ya_direct_access_token'
    project_created_at = 'project_created_at'

    comment_id = 'comment_id'
    comment_text = 'comment_text'
    comment_date = 'comment_date'

    ya_direct_activated_logins = 'ya_direct_activated_logins'
    ya_direct_deactivated_logins = 'ya_direct_deactivated_logins'
    ya_direct_representative_accept_logins = 'ya_direct_representative_accept_logins'
    ya_direct_representative_deny_logins = 'ya_direct_representative_deny_logins'

    faq = 'faq'
    item = 'item'

    ya_access_direct = 'ya_access_direct'
    ya_access_metrika = 'ya_access_metrika'
    selected_metrika = 'selected_metrika'
    selected_direct = 'selected_direct'

    status_confirm = 'status_confirm'
    status_edit_project = 'status_edit_project'
    status_edit_counter = 'status_edit_counter'
    status_set_project = 'status_set_project'
    status_remove_project = 'status_remove_project'
    status_old_obj = 'status_old_obj'


class StartDataConstant(Enum):

    authorized = 'authorized'
    unauthorized = 'unauthorized'

    status = 'status'
    status_old_obj = 'status_old_obj'
    status_edit = 'status_edit'
    status_first = 'status_first'

    manager_uuid = 'manager_uuid'
    available_managers = 'available_managers'
    connected_managers = 'connected_managers'

    username = 'username'
    user_uuid = 'user_uuid'
    user_login = 'user_login'
    user_role = 'user_role'
    user_password = 'user_password'
    user_status = 'user_status'
    user_created = 'user_created'
    user_projects = 'user_projects'
    user_role_id = 'user_role_id'
    user_edit = 'user_edit'

    project_id = 'prjct_id'
    project_title = 'prjct_title'
    project_description = 'prjct_d'
    project_ya_direct_logins = 'prjct_y_d_l'
    project_ya_metrika_counters = 'prjct_y_c'
    project_ya_counters_list = 'prjct_y_c_l'
    project_author = 'prjct_a'
    project_created = 'prjct_created'
    project_managers = 'prjct_managers'
    project_counter_id = 'prjct_counter_id'
    project_created_at = 'project_created_at'
    project_comments = 'project_comments'

    project_ya_list_active_logins = 'project_ya_list_active_logins'
    project_ya_list_inactive_logins = 'project_ya_list_inactive_logins'

    company_name = 'company_name'
    company_id = 'company_id'
    old_company = 'old_company'
    new_company = 'new_company'

    ya_direct_activated_logins = 'ya_direct_activated_logins'
    ya_direct_deactivated_logins = 'ya_direct_deactivated_logins'
    ya_metrika_counters = 'ya_metrika_counters'
    ya_access_direct = 'ya_access_direct'
    ya_access_metrika = 'ya_access_metrika'

    faq = 'faq'

    counter_name = 'counter_name'
    counter_id = 'counter_id'
    counter_attribution = 'counter_attribution'
    counter_minor_attribution = 'counter_minor_attribution'
    counter_k_goals = 'counter_k_goals'
    counter_m_goals = 'counter_m_goals'
    counter_ecommerce = 'counter_ecommerce'
    counter_created_at = 'counter_created_at'

    list_counters = 'list_counters'
    list_viewers = 'list_viewers'
    list_users = 'list_users'
    list_projects = 'list_prjcts'
    list_ya_direct_logins = 'list_y_d_l'


class DialogDataConstant(Enum):
    finished_key = 'finished'

    telegram_id = 'telegram_id'
    category_id = 'category_id'

    fail = 'fail'
    form = 'form'

    telegram_username = 'telegram_username'

    user_uuid = 'user_uuid'
    username = 'username'
    user_login = 'user_login'
    company_name = 'company_name'

    input_login = 'input_login'
    input_password = 'input_password'
    input_shop = 'input_shop'
    input_phone = 'input_phone'
    input_model = 'input_model'
    input_username = 'input_username'

    profile = 'profile'
    product = 'product'
    category = 'category'

    promo_products = 'promo_products'

    list_users = 'list_users'


class ConstantID(Enum):
    tg_help_chat_id = 'tg_help_chat_id'
