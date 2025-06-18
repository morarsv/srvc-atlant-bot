from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    authorization: Authorization
    start: Start
    atlant: Atlant
    project: Project
    viewers: Viewers
    company: Company
    connect: Connect
    input: Input
    error: Error
    description: Description
    help: Help
    hello: Hello
    successfully: Successfully
    unsuccessfully: Unsuccessfully
    pls: Pls
    update: Update
    unknown: Unknown
    template: Template
    user: User
    ya: Ya
    button: Button
    faq: Faq
    alert: Alert

    @staticmethod
    def info() -> Literal["""Информация о компании Atlant"""]: ...


class Authorization:
    input: AuthorizationInput

    @staticmethod
    def authorized() -> Literal["""Вы уже авторизированы."""]: ...

    @staticmethod
    def unauthorized() -> Literal["""Для авторизации нажмите &lt;b&gt;Войти&lt;/b&gt;."""]: ...

    @staticmethod
    def fail() -> Literal["""Неверный логин или пароль.

Попробуйте войти снова или обратитесь в &lt;b&gt;помощь&lt;/b&gt; /help"""]: ...


class AuthorizationInput:
    @staticmethod
    def password() -> Literal["""Введите пароль:"""]: ...

    @staticmethod
    def login() -> Literal["""Ведите логин:"""]: ...


class Start:
    preview: StartPreview


class StartPreview:
    @staticmethod
    def hello(*, username) -> Literal["""Привет, &lt;b&gt;{ $username }&lt;/b&gt;!"""]: ...

    @staticmethod
    def viewer() -> Literal["""&lt;b&gt;Проекты&lt;/b&gt; - Предоставляет доступ к разделу с проектами. Вы можете просматривать доступные проекты, и отчёты по ним."""]: ...

    @staticmethod
    def admin() -> Literal["""&lt;b&gt;Администрирование&lt;/b&gt; - Предназначен, чтобы создать новый профиль, изменить данные существующего или просмотреть список всех профилей и проектов компании.
Это позволит вам легко управлять персональной информацией и контролировать учетные записи, также позволяет переназначать менеджеров на проект.

&lt;b&gt;Проекты&lt;/b&gt; - Предоставляет доступ к разделу управления проектами.
Вы сможете создать новый проект, настроить параметры существующего проекта, а также просмотреть список всех ваших проектов.

&lt;b&gt;Управление аккаунтами зрителей&lt;/b&gt; - предоставляет инструменты для настройки доступов зрителей к проектам, просмотра их прав и редактирования разрешений."""]: ...

    @staticmethod
    def manager() -> Literal["""&lt;b&gt;Проекты&lt;/b&gt; - Предоставляет доступ к разделу управления проектами.
Вы сможете создать новый проект, настроить параметры существующего проекта, а также просмотреть список всех ваших проектов.

&lt;b&gt;Управление аккаунтами зрителей&lt;/b&gt; - предоставляет инструменты для настройки доступов зрителей к проектам, просмотра их прав и редактирования разрешений."""]: ...


class Atlant:
    admin: AtlantAdmin


class AtlantAdmin:
    list: AtlantAdminList
    add: AtlantAdminAdd
    info: AtlantAdminInfo
    company: AtlantAdminCompany

    @staticmethod
    def preview() -> Literal["""&lt;b&gt;Добавить компанию&lt;/b&gt; - создает компанию и добавляет в базу данных.

&lt;b&gt;Добавить пользователя&lt;/b&gt; - выберите из списка компанию и создайте нового пользователя в роли &lt;b&gt;admin&lt;/b&gt;.

&lt;b&gt;Список компаний&lt;/b&gt; - отображает список зарегистрированных компаний."""]: ...


class AtlantAdminList:
    @staticmethod
    def companies() -> Literal["""Ниже представлен список компаний.
Нажмите на любую, чтобы просмотреть подробную информацию."""]: ...


class AtlantAdminAdd:
    company: AtlantAdminAddCompany

    @staticmethod
    def user() -> Literal["""Выберите компанию, к которой будет привязан новый пользователь."""]: ...


class AtlantAdminInfo:
    edit: AtlantAdminInfoEdit

    @staticmethod
    def company(*, company_id, company_name, count_users, count_projects, created_at) -> Literal["""&lt;b&gt;Полная информация о компании&lt;/b&gt;
&lt;b&gt;ID компания:&lt;/b&gt; { $company_id }
&lt;b&gt;Компания:&lt;/b&gt; { $company_name }
&lt;b&gt;Количество пользователей:&lt;/b&gt; { $count_users }
&lt;b&gt;Количество проектов:&lt;/b&gt; { $count_projects }

&lt;b&gt;Дата создания:&lt;/b&gt; { $created_at }"""]: ...

    @staticmethod
    def user(*, username, company_name, count_projects, role, status, creates_at) -> Literal["""&lt;b&gt;Профиль пользователя&lt;/b&gt;

&lt;b&gt;Пользователь:&lt;/b&gt; { $username }
&lt;b&gt;Компания:&lt;/b&gt; { $company_name }
&lt;b&gt;Проекты:&lt;/b&gt; { $count_projects }
&lt;b&gt;Роль в компания:&lt;/b&gt; { $role }

&lt;b&gt;Статус аккаунта:&lt;/b&gt; { $status }
&lt;b&gt;Дата создания:&lt;/b&gt; { $creates_at }"""]: ...

    @staticmethod
    def counter(*, project_title, attribution, minor_attribution, counter, counter_id, k_goals, m_goals, ecommerce) -> Literal["""&lt;b&gt;Название проекта:&lt;/b&gt; { $project_title }

&lt;b&gt;Атрибуция:&lt;/b&gt; { $attribution }
&lt;b&gt;Дополнительная атрибуция:&lt;/b&gt; { $minor_attribution }

&lt;b&gt;Счётчик:&lt;/b&gt; { $counter }
&lt;b&gt;ID счётчика:&lt;/b&gt; { $counter_id }

&lt;b&gt;Ключевые цели - ID:&lt;/b&gt;
{ $k_goals }

&lt;b&gt;Дополнительные цели - ID:&lt;/b&gt;
{ $m_goals }

&lt;b&gt;Электронная коммерция:&lt;/b&gt; { $ecommerce }"""]: ...

    @staticmethod
    def project(*, project_id, project_title, project_description, ya_logins, ya_counters, company_name, author, created_at, managers) -> Literal["""&lt;b&gt;Полная информация о проекте&lt;/b&gt;

&lt;b&gt;ID проекта:&lt;/b&gt; { $project_id }
&lt;b&gt;Название проекта:&lt;/b&gt; { $project_title }
&lt;b&gt;Описание:&lt;/b&gt; { $project_description }

&lt;b&gt;Яндекс Директ логины:&lt;/b&gt; { $ya_logins }

&lt;b&gt;Яндекс Метрика счётчики:&lt;/b&gt; { $ya_counters }

&lt;b&gt;Компания:&lt;/b&gt; { $company_name }
&lt;b&gt;Автор:&lt;/b&gt; { $author }
&lt;b&gt;Дата создания:&lt;/b&gt; { $created_at }

&lt;b&gt;Менеджеры проекта:&lt;/b&gt; { $managers }"""]: ...


class AtlantAdminInfoEdit:
    @staticmethod
    def user(*, full_name, login, password, company) -> Literal["""&lt;b&gt;Пользователь:&lt;/b&gt; { $full_name }
&lt;b&gt;Логин:&lt;/b&gt; { $login }
&lt;b&gt;Пароль:&lt;/b&gt; { $password }
&lt;b&gt;Компания:&lt;/b&gt; { $company }

&lt;b&gt;Подтвердить&lt;/b&gt; - вносит все изменения в базу данных."""]: ...


class AtlantAdminCompany:
    list: AtlantAdminCompanyList


class AtlantAdminCompanyList:
    @staticmethod
    def users(*, company_name) -> Literal["""Список всех пользователей в &lt;b&gt;{ $company_name }&lt;/b&gt;.
Нажмите на любого пользователя, чтобы просмотреть подробную информацию."""]: ...

    @staticmethod
    def projects(*, company_name) -> Literal["""Список проектов &lt;b&gt;{ $company_name }&lt;/b&gt;.
Нажмите на любой проект, чтобы просмотреть подробную информацию."""]: ...


class AtlantAdminAddCompany:
    @staticmethod
    def preview(*, company) -> Literal["""&lt;b&gt;Компания:&lt;/b&gt; { $company }

&lt;b&gt;Подтвердить&lt;/b&gt; - создает компанию и добавляет в базу данных, без пользователей.

&lt;b&gt;Добавить пользователя&lt;/b&gt; - добавляет пользователя в роли &lt;b&gt;admin&lt;/b&gt; и закрепляет его за данной компанией."""]: ...


class Project:
    preview: ProjectPreview
    list: ProjectList
    info: ProjectInfo
    add: ProjectAdd
    ya: ProjectYa
    direct: ProjectDirect


class ProjectPreview:
    viewer: ProjectPreviewViewer

    @staticmethod
    def manager() -> Literal["""Здесь вы можете создать &lt;b&gt;новый проект&lt;/b&gt; с нуля или выбрать существующий проект из &lt;b&gt;списка&lt;/b&gt; для дальнейшего редактирования и настройки."""]: ...


class ProjectPreviewViewer:
    @staticmethod
    def fill() -> Literal["""Выберите нужный вам проект из &lt;b&gt;списка проектов&lt;/b&gt;."""]: ...

    @staticmethod
    def empty() -> Literal["""Увы, но у вас нет доступных проектов. Обратитесь к своему ведущему менеджеру."""]: ...


class ProjectList:
    @staticmethod
    def metrika() -> Literal["""Выберите счётчик метрики из списка, чтобы просмотреть детали."""]: ...

    @staticmethod
    def projects() -> Literal["""Просмотрите все созданные проекты и выберите &lt;b&gt;нужный&lt;/b&gt;.
Нажмите на проект, чтобы открыть карточку для просмотра."""]: ...


class ProjectInfo:
    about: ProjectInfoAbout
    ya: ProjectInfoYa


class ProjectInfoAbout:
    @staticmethod
    def project(*, title, description) -> Literal["""&lt;b&gt;Название проекта&lt;/b&gt;: { $title }

&lt;b&gt;Описание проекта&lt;/b&gt;: { $description }"""]: ...


class ProjectInfoYa:
    @staticmethod
    def logins(*, logins) -> Literal["""&lt;b&gt;Подключенные логины Яндекс Директа &lt;/b&gt;: { $logins }"""]: ...

    @staticmethod
    def counters(*, counters) -> Literal["""&lt;b&gt;Подключенные счётчики Яндекс Метрики&lt;/b&gt;: { $counters }"""]: ...


class ProjectAdd:
    services: ProjectAddServices


class ProjectAddServices:
    @staticmethod
    def project() -> Literal["""Выберите нужные вам &lt;b&gt;сервисы&lt;/b&gt; для подключения.

Для подключения &lt;b&gt;сервиса&lt;/&gt;, нужно перейти по нему и дать доступ ✅. После передачи доступа &lt;b&gt;обновите статус&lt;/b&gt;."""]: ...


class ProjectYa:
    direct: ProjectYaDirect
    metrika: ProjectYaMetrika

    @staticmethod
    def access() -> Literal["""Вы можете предоставить доступ, выбрав один из следующих способов:

🔹 Через веб-браузер — перейдите по предоставленной ссылке и выполните необходимые действия.

🔹 Через Telegram Web — откройте соответствующее уведомление и следуйте инструкции."""]: ...


class ProjectYaDirect:
    add: ProjectYaDirectAdd
    logins: ProjectYaDirectLogins


class ProjectYaDirectAdd:
    logins: ProjectYaDirectAddLogins
    representative: ProjectYaDirectAddRepresentative
    request: ProjectYaDirectAddRequest

    @staticmethod
    def preview() -> Literal["""Выберите один из предложенных вариантов.

&lt;b&gt;Агентский кабинет&lt;/b&gt; — предоставляет список логинов рекламодателей, если у Вас агентский логин в Яндекс Директе, выберите данный вариант.

&lt;b&gt;Прямой рекламодатель&lt;/b&gt; — если Вы самостоятельно размещаете рекламу в Яндекс Директ, выберите данный вариант.

&lt;b&gt;Представитель&lt;/b&gt; - если Вы действуете от имени другого рекламодателя и имеете доступ к аккаунту рекламодателя с различными уровнями прав, в зависимости от того, какие полномочия им предоставляет владелец рекламного кабинета, то выберите данный вариант."""]: ...


class ProjectYaDirectLogins:
    settings: ProjectYaDirectLoginsSettings


class ProjectYaDirectLoginsSettings:
    @staticmethod
    def preview(*, active, inactive) -> Literal["""Активные логины: { $active }

Неактивные логины: { $inactive }

Здесь вы можете управлять логинами, изменяя их статус на активный или неактивный. Если какие-либо логины были отключены, измените их статус на неактивный."""]: ...

    @staticmethod
    def activate() -> Literal["""Отметьте один или несколько логинов, при &lt;b&gt;подтверждении&lt;/b&gt; отмеченные логины сменят статус на активный."""]: ...

    @staticmethod
    def deactivate() -> Literal["""Отметьте один или несколько логинов, при &lt;b&gt;подтверждении&lt;/b&gt; отмеченные логины сменят статус на неактивный."""]: ...


class ProjectYaDirectAddLogins:
    @staticmethod
    def empty() -> Literal["""Увы, но логинов для подключения нет."""]: ...

    @staticmethod
    def full() -> Literal["""Отметьте ✅ один или несколько &lt;b&gt;логинов&lt;/b&gt; из предложенного списка, используя кнопки."""]: ...


class ProjectYaDirectAddRepresentative:
    description: ProjectYaDirectAddRepresentativeDescription
    accept: ProjectYaDirectAddRepresentativeAccept
    input: ProjectYaDirectAddRepresentativeInput

    @staticmethod
    def logins(*, accept, deny) -> Literal["""Логины прошедшие проверку на наличие доступа.

&lt;b&gt;Есть доступ&lt;/b&gt;: { $accept }

&lt;b&gt;Доступ отсутствует&lt;/b&gt;: { $deny }"""]: ...


class ProjectYaDirectAddRepresentativeDescription:
    @staticmethod
    def select() -> Literal["""&lt;b&gt;Выбрать логины&lt;/b&gt; — предоставляет список логинов, которые вы ранее ввели и к которым имеете доступ. Вы можете выбрать необходимые логины, и после подтверждения они будут добавлены в базу."""]: ...

    @staticmethod
    def add() -> Literal["""&lt;b&gt;Добавить логины&lt;/b&gt; — позволяет ввести новые логины для проверки доступа к аккаунтам рекламодателей. После ввода система проверит, есть ли у вас доступ к указанным логинам."""]: ...


class ProjectYaDirectAddRequest:
    @staticmethod
    def error(*, code, detail) -> Literal["""При запросе возникла ошибка, обратитесь в помощь для её решения проблемы.

Код ошибки: { $code }
Детали: { $detail }"""]: ...


class ProjectYaDirectAddRepresentativeAccept:
    add: ProjectYaDirectAddRepresentativeAcceptAdd


class ProjectYaDirectAddRepresentativeAcceptAdd:
    @staticmethod
    def logins() -> Literal["""Отметьте ✅ один или несколько &lt;b&gt;логинов&lt;/b&gt; из предложенного списка, используя кнопки.

После выбора нажмите &lt;b&gt;Подтвердить&lt;/b&gt; для добавления отмеченных логинов в базу данных."""]: ...


class ProjectYaDirectAddRepresentativeInput:
    @staticmethod
    def logins() -> Literal["""Введите один или несколько логинов через запятую для проверки наличия доступа.
Пример : login1, login2, login3"""]: ...

    @staticmethod
    def error() -> Literal["""Внимание! Логин не может пустым или иметь меньше двух символов."""]: ...


class ProjectYaMetrika:
    counters: ProjectYaMetrikaCounters
    config: ProjectYaMetrikaConfig
    button: ProjectYaMetrikaButton
    key: ProjectYaMetrikaKey
    minor: ProjectYaMetrikaMinor

    @staticmethod
    def ecommerce() -> Literal["""Данный счётчик используется для электронной коммерции?
Выберите ✅ &lt;b&gt;да&lt;/b&gt; или &lt;b&gt;нет&lt;/b&gt;."""]: ...


class ProjectYaMetrikaCounters:
    info: ProjectYaMetrikaCountersInfo
    preview: ProjectYaMetrikaCountersPreview
    selected: ProjectYaMetrikaCountersSelected


class ProjectYaMetrikaCountersInfo:
    @staticmethod
    def counter(*, project_title, attribution, minor_attribution, counter, counter_id, k_goals, m_goals, ecommerce) -> Literal["""&lt;b&gt;Название проекта:&lt;/b&gt; { $project_title }

&lt;b&gt;Атрибуция:&lt;/b&gt; { $attribution }
&lt;b&gt;Дополнительная атрибуция:&lt;/b&gt; { $minor_attribution }

&lt;b&gt;Счётчик:&lt;/b&gt; { $counter }
&lt;b&gt;ID счётчика:&lt;/b&gt; { $counter_id }

&lt;b&gt;Ключевые цели - ID:&lt;/b&gt;
{ $k_goals }

&lt;b&gt;Дополнительные цели - ID:&lt;/b&gt;
{ $m_goals }

&lt;b&gt;Электронная коммерция:&lt;/b&gt; { $ecommerce }"""]: ...


class ProjectYaMetrikaCountersPreview:
    @staticmethod
    def viewer(*, key_attribution, minor_attribution) -> Literal["""Текущая атрибуция.

&lt;b&gt;Основная:&lt;/b&gt; { $key_attribution }
&lt;b&gt;Дополнительная:&lt;/b&gt; { $minor_attribution }"""]: ...

    @staticmethod
    def manager(*, key_attribution, minor_attribution) -> Literal["""Текущая атрибуция.

&lt;b&gt;Основная:&lt;/b&gt; { $key_attribution }
&lt;b&gt;Дополнительная:&lt;/b&gt; { $minor_attribution }

Для изменения атрибуции на всех счётчиках метрики используйте кнопку &lt;b&gt;Изменить атрибуцию&lt;/b&gt;.

Для добавления нового счётчика метрики нажмите кнопку &lt;b&gt;Добавить счётчик метрики&lt;/b&gt;.

Выберите счётчик метрики из списка, чтобы просмотреть детали."""]: ...


class ProjectYaMetrikaCountersSelected:
    @staticmethod
    def attribution(*, key_attribution, minor_attribution) -> Literal["""Выбранная атрибуция.

&lt;b&gt;Основная:&lt;/b&gt; { $key_attribution }
&lt;b&gt;Дополнительная:&lt;/b&gt; { $minor_attribution }

После подтверждения, изменения вступят в силу.
&lt;b&gt;Внимание!&lt;/b&gt; Выбранная атрибуция будет присвоена ко всем текущим и последующим метрикам."""]: ...


class ProjectYaMetrikaConfig:
    counters: ProjectYaMetrikaConfigCounters
    edit: ProjectYaMetrikaConfigEdit
    m: ProjectYaMetrikaConfigM

    @staticmethod
    def attribution() -> Literal["""Выберите✅ одну из предложенных атрибуций."""]: ...


class ProjectYaMetrikaConfigCounters:
    @staticmethod
    def empty() -> Literal["""Увы, но список счётчиков пуст."""]: ...

    @staticmethod
    def full() -> Literal["""Выберите ✅ один счётчик из списка."""]: ...


class ProjectYaMetrikaConfigEdit:
    notice: ProjectYaMetrikaConfigEditNotice


class ProjectYaMetrikaConfigEditNotice:
    @staticmethod
    def counter() -> Literal["""&lt;b&gt;Внимание!&lt;/b&gt; Смена счётчика приведёт к полному сбросу ранее сделанной настройки."""]: ...


class ProjectYaMetrikaConfigM:
    @staticmethod
    def attribution() -> Literal["""Выберите ✅ дополнительную атрибуцию из предложенного списка.

Если отсутствует необходимость выбора, можете пропустить данный шаг нажав на кнопку &lt;b&gt;Продолжить&lt;/b&gt;."""]: ...


class ProjectYaMetrikaButton:
    @staticmethod
    def cancel() -> Literal["""&lt;b&gt;Отменить&lt;/b&gt; - отменяет действия по добавлению счётчика метрики."""]: ...

    @staticmethod
    def back() -> Literal["""◀️ &lt;b&gt;Назад&lt;/b&gt; - возвращает на шаг назад, к ранее сделанной настройки."""]: ...


class ProjectYaMetrikaKey:
    goals: ProjectYaMetrikaKeyGoals


class ProjectYaMetrikaKeyGoals:
    @staticmethod
    def full() -> Literal["""Выберите ✅ от одной до трёх ключевых целей."""]: ...

    @staticmethod
    def empty() -> Literal["""Увы, но список целей пуст.

&lt;&lt;У самурая нет цели, только путь, а путь самурая -
   это смерть.&gt;&gt;, - Ямамото Цунэтомо &#34;Хагакурэ&#34;."""]: ...


class ProjectYaMetrikaMinor:
    goals: ProjectYaMetrikaMinorGoals


class ProjectYaMetrikaMinorGoals:
    @staticmethod
    def full() -> Literal["""Выберите ✅ от одной до трёх дополнительных целей.

Если отсутствует необходимость выбора дополнительных целей, можете пропустить данный шаг нажав на кнопку &lt;b&gt;Продолжить&lt;/b&gt;"""]: ...

    @staticmethod
    def empty() -> Literal["""Список дополнительных целей пуст, можете пропустить данный шаг нажав на кнопку &lt;b&gt;Продолжить&lt;/b&gt;"""]: ...


class Viewers:
    info: ViewersInfo
    preview: ViewersPreview
    description: ViewersDescription
    list: ViewersList
    settings: ViewersSettings
    add: ViewersAdd


class ViewersInfo:
    @staticmethod
    def viewer(*, full_name, login) -> Literal["""Профиль пользователя:

&lt;b&gt;ФИО:&lt;/b&gt; { $full_name }
&lt;b&gt;Уровень доступа:&lt;/b&gt; viewer
&lt;b&gt;Логин:&lt;/b&gt; &lt;span class=&#34;tg-spoiler&#34;&gt; { $login } &lt;/span&gt;"""]: ...


class ViewersPreview:
    @staticmethod
    def viewers() -> Literal["""Здесь вы можете настроить аккаунт для &lt;b&gt;зрителя&lt;/b&gt;.

&lt;b&gt;Зритель&lt;/b&gt; - пользователь, с таким уровнем доступа может просматривать разрешённые ему проекты и отчёты по ним.

&lt;b&gt;Создать профиль&lt;/b&gt; - создаёт пользователя с уровнем доступа &lt;b&gt;зритель&lt;/b&gt;."""]: ...


class ViewersDescription:
    list: ViewersDescriptionList
    connect: ViewersDescriptionConnect
    remove: ViewersDescriptionRemove


class ViewersDescriptionList:
    @staticmethod
    def viewers() -> Literal["""&lt;b&gt;Список зрителей&lt;/b&gt; - отображает созданных вами пользователей, с возможностью настроить доступ Проекты, перейдя в карточку конкретного пользователя."""]: ...


class ViewersDescriptionConnect:
    @staticmethod
    def projects() -> Literal["""&lt;b&gt;Подключить проекты&lt;/b&gt; - отображает список проектов, доступных вам для предоставления разрешения на просмотр данному зрителю."""]: ...


class ViewersDescriptionRemove:
    @staticmethod
    def projects() -> Literal["""&lt;b&gt;Отключить проекты&lt;/b&gt; - отображает список проектов, доступных зрителю, с возможностью отозвать доступ к ним."""]: ...


class ViewersList:
    @staticmethod
    def viewers() -> Literal["""Просмотрите все созданные профили и выберите &lt;b&gt;нужный&lt;/b&gt; для редактирования.

Нажмите на &lt;b&gt;профиль&lt;/b&gt;, чтобы внести изменения."""]: ...


class ViewersSettings:
    @staticmethod
    def projects() -> Literal["""Отметьте один или несколько проектов из данного списка для отзыва доступа на просмотр.
После &lt;b&gt;подтверждения&lt;/b&gt; изменения вступят в силу."""]: ...


class ViewersAdd:
    info: ViewersAddInfo


class ViewersAddInfo:
    @staticmethod
    def viewer(*, full_name, login, password) -> Literal["""Профиль пользователя:

&lt;b&gt;ФИО:&lt;/b&gt; { $full_name }
&lt;b&gt;Уровень доступа:&lt;/b&gt; viewer
&lt;b&gt;Логин:&lt;/b&gt; &lt;span class=&#34;tg-spoiler&#34;&gt; { $login } &lt;/span&gt;
&lt;b&gt;Пароль:&lt;/b&gt; &lt;span class=&#34;tg-spoiler&#34;&gt; { $password } &lt;/span&gt;"""]: ...


class Company:
    admin: CompanyAdmin


class CompanyAdmin:
    description: CompanyAdminDescription
    set: CompanyAdminSet
    remove: CompanyAdminRemove
    list: CompanyAdminList
    info: CompanyAdminInfo
    add: CompanyAdminAdd


class CompanyAdminDescription:
    button: CompanyAdminDescriptionButton


class CompanyAdminDescriptionButton:
    list: CompanyAdminDescriptionButtonList
    add: CompanyAdminDescriptionButtonAdd
    set: CompanyAdminDescriptionButtonSet
    remove: CompanyAdminDescriptionButtonRemove
    logout: CompanyAdminDescriptionButtonLogout


class CompanyAdminDescriptionButtonList:
    @staticmethod
    def users() -> Literal["""&lt;b&gt;Список профилей&lt;/b&gt; -  Открывает список всех созданных профилей.
Вы может выбрать любой профиль из списка, чтобы просмотреть его детали и при необходимости отредактировать информацию."""]: ...

    @staticmethod
    def projects() -> Literal["""&lt;b&gt;Список проектов&lt;/b&gt; - Предоставляет список всех проектов Вашей компании, для дальнейшей настройки по передачи прав на ведение выбранным проектом."""]: ...


class CompanyAdminDescriptionButtonAdd:
    @staticmethod
    def user() -> Literal["""&lt;b&gt;Создать профиль&lt;/b&gt; - Позволяет создать новый профиль, заполнив необходимые данные, такие как фамилию и имя, логин и пароль.
После заполнения данных новый профиль будет добавлен в систему и появится в списке профилей."""]: ...


class CompanyAdminDescriptionButtonSet:
    @staticmethod
    def manager() -> Literal["""&lt;b&gt;Назначить менеджера&lt;/b&gt; — отображает список доступных менеджеров для назначения на проект. Проект будет виден и доступен только выбранному менеджеру."""]: ...


class CompanyAdminDescriptionButtonRemove:
    @staticmethod
    def manager() -> Literal["""&lt;b&gt;Отстранить менеджера&lt;/b&gt; — предоставляет список менеджеров, работающих над данным проектом, для возможного снятия их с руководства проектом."""]: ...


class CompanyAdminDescriptionButtonLogout:
    frm: CompanyAdminDescriptionButtonLogoutFrm


class CompanyAdminDescriptionButtonLogoutFrm:
    @staticmethod
    def sessions() -> Literal["""&lt;b&gt;Выйти из сессий&lt;/b&gt; — Позволяет завершить все активные сессии в веб-системе отчетов.
После выполнения действия пользователи будут автоматически разлогинены и потребуется повторная авторизация."""]: ...


class CompanyAdminSet:
    @staticmethod
    def managers() -> Literal["""Отметьте ✅ одного или нескольких менеджеров для передачи прав на ведение проекта."""]: ...


class CompanyAdminRemove:
    @staticmethod
    def managers() -> Literal["""Отметьте ✅ одного или нескольких менеджеров, чтобы отстранить от проекта.
После подтверждения проекты перестанут отображаться  в списке проектов у отстраненных менеджеров."""]: ...


class CompanyAdminList:
    @staticmethod
    def users() -> Literal["""Просмотрите все созданные профили и выберите &lt;b&gt;нужный&lt;/b&gt; для редактирования.

Нажмите на &lt;b&gt;профиль&lt;/b&gt;, чтобы внести изменения."""]: ...

    @staticmethod
    def projects() -> Literal["""Просмотрите все созданные проекты и выберите &lt;b&gt;нужный&lt;/b&gt;.
Нажмите на проект, чтобы открыть карточку для просмотра."""]: ...


class CompanyAdminInfo:
    ya: CompanyAdminInfoYa

    @staticmethod
    def project(*, title, description, list_managers) -> Literal["""&lt;b&gt;Название проекта&lt;/b&gt;: { $title }

&lt;b&gt;Описание проекта&lt;/b&gt;: { $description }

&lt;b&gt;Проект ведёт&lt;/b&gt;: { $list_managers }"""]: ...


class CompanyAdminInfoYa:
    @staticmethod
    def logins(*, logins) -> Literal["""&lt;b&gt;Подключенные логины Яндекс Директа &lt;/b&gt;: { $logins }"""]: ...

    @staticmethod
    def counters(*, counters) -> Literal["""&lt;b&gt;Подключенные счётчики Яндекс Метрики&lt;/b&gt;: { $counters }"""]: ...


class CompanyAdminAdd:
    edit: CompanyAdminAddEdit


class CompanyAdminAddEdit:
    @staticmethod
    def user(*, full_name, role_name, login, password) -> Literal["""Профиль пользователя:

&lt;b&gt;ФИО:&lt;/b&gt; { $full_name }
&lt;b&gt;Уровень доступа:&lt;/b&gt; { $role_name }
&lt;b&gt;Логин:&lt;/b&gt; &lt;span class=&#34;tg-spoiler&#34;&gt; { $login } &lt;/span&gt;
&lt;b&gt;Пароль:&lt;/b&gt; &lt;span class=&#34;tg-spoiler&#34;&gt; { $password } &lt;/span&gt;
Для изменения профиля воспользуйтесь &lt;b&gt;функциями&lt;/b&gt; ниже.

После &lt;b&gt;подтверждения&lt;/b&gt; изменения вступят в силу и пользователь данного профиля будет автоматически разлогинен."""]: ...


class Connect:
    user: ConnectUser


class ConnectUser:
    send: ConnectUserSend

    @staticmethod
    def preview(*, report) -> Literal["""Здравствуйте!

Благодарим вас за интерес к нашему боту.

Если вы уже являетесь пользователем, пожалуйста, пройдите &lt;b&gt;авторизацию&lt;/b&gt;.

Если вы ещё не зарегистрированы, просим заполнить регистрационную форму: укажите ваше имя, фамилию и название компании. Это позволит нам создать для вас учётную запись в системе.
После регистрации с вами свяжется наш менеджер.

Вы можете ознакомиться с демонстрационным вариантом отчёта по следующей ссылке: { $report }."""]: ...


class ConnectUserSend:
    @staticmethod
    def form() -> Literal["""Спасибо!
Ваша анкета успешно отправлена.

Наш менеджер свяжется с вами в ближайшее время для подтверждения регистрации и предоставления доступа к системе.

Если у вас возникли вопросы — не стесняйтесь обращаться /help. Мы всегда готовы помочь."""]: ...


class Input:
    project: InputProject

    @staticmethod
    def username() -> Literal["""Пожалуйста, введите фамилию и имя в следующем формате:
Пример: Иванов Иван"""]: ...

    @staticmethod
    def company() -> Literal["""Пожалуйста, введите название компании.
Название должно содержать не менее 3 символов."""]: ...

    @staticmethod
    def login() -> Literal["""Логин может содержать только латинские буквы и цифры.
Длина от 4 до 20 символов.
Пример: &#39;user123&#39;, &#39;johndoe&#39;, &#39;admin007&#39;

Введите логин:"""]: ...

    @staticmethod
    def password() -> Literal["""Длина пароля: от 8 до 20 символов.
Пароль должен содержать как минимум одну цифру, одну строчную букву.
Пароль может содержать только латинские буквы и цифры.
Пример: pAssword1, Z9yXwVuT, 1234abcd

Введите пароль:"""]: ...


class InputProject:
    @staticmethod
    def description() -> Literal["""Введите небольшое описание проекта:"""]: ...

    @staticmethod
    def title() -> Literal["""Название проекта не может быть пустым или содержать меньше 3 символов.
Введите название проекта:"""]: ...


class Error:
    format: ErrorFormat
    uniq: ErrorUniq
    airflow: ErrorAirflow


class ErrorFormat:
    @staticmethod
    def login() -> Literal["""Некорректный формат логина.
Логин может содержать только латинские буквы и цифры. Длина от 4 до 20 символов.
Пример: &#39;user123&#39;, &#39;johndoe&#39;, &#39;admin007&#39;.

Введите логин:"""]: ...

    @staticmethod
    def password() -> Literal["""Некорректный формат пароля.
Длина пароля: от 8 до 20 символов.
Пароль должен содержать как минимум одну цифру, одну строчную букву.
Пароль может содержать только латинские буквы и цифры.
Пример: password1, Z9yXwVuT, 1234abcd

Введите пароль:"""]: ...

    @staticmethod
    def project() -> Literal["""Название проекта не может быть пустым или содержать меньше 3 символов.

Введите название проекта:"""]: ...


class ErrorUniq:
    @staticmethod
    def company() -> Literal["""Компания с таким названием уже существует."""]: ...

    @staticmethod
    def login() -> Literal["""Такой логин уже занят."""]: ...

    @staticmethod
    def project() -> Literal["""Проект с таким названием уже существует.
Придумайте другое название.

Введите название проекта:"""]: ...


class Description:
    button: DescriptionButton


class DescriptionButton:
    @staticmethod
    def confirm() -> Literal["""Чтобы изменения вступили в силу нажмите на &lt;b&gt;Подтвердить&lt;/b&gt;."""]: ...


class Help:
    submit: HelpSubmit
    input: HelpInput
    application: HelpApplication

    @staticmethod
    def main() -> Literal["""Если у вас возникли трудности с использованием бота, пожалуйста, &lt;b&gt;оставьте заявку&lt;/b&gt;, и наш менеджер оперативно свяжется с вами в рабочее время, чтобы помочь решить проблему."""]: ...


class HelpSubmit:
    request: HelpSubmitRequest


class HelpSubmitRequest:
    @staticmethod
    def unknown(*, username, datetime) -> Literal["""Поступил запрос на помощь от незарегистрированного пользователя { $username }.
&lt;b&gt;Время заявки:&lt;/b&gt; { $datetime }"""]: ...

    @staticmethod
    def user(*, login, company_name, datetime, text) -> Literal["""&lt;b&gt;Логин пользователя:&lt;/b&gt; { $login }
&lt;b&gt;Компания:&lt;/b&gt; { $company_name }
&lt;b&gt;Время заявки:&lt;/b&gt; { $datetime }

&lt;b&gt;Текст обращения:&lt;/b&gt;
{ $text }"""]: ...


class HelpInput:
    @staticmethod
    def request() -> Literal["""Если у вас возникли трудности с использованием бота, пожалуйста, опишите проблему в сообщении и отправьте боту. Наш менеджер оперативно свяжется с вами в рабочее время."""]: ...


class HelpApplication:
    @staticmethod
    def form(*, username, company_name, datetime) -> Literal["""&lt;b&gt;Пользователя:&lt;/b&gt; { $username }
&lt;b&gt;Компания:&lt;/b&gt; { $company_name }
&lt;b&gt;Время заявки:&lt;/b&gt; { $datetime }
Запрос на создания кабинета."""]: ...


class Hello:
    @staticmethod
    def user(*, username) -> Literal["""Привет, &lt;b&gt;{ $username }&lt;/b&gt;!"""]: ...


class ProjectDirect:
    request: ProjectDirectRequest


class ProjectDirectRequest:
    @staticmethod
    def error(*, code, detail) -> Literal["""При запросе возникла ошибка, обратитесь в помощь для её решения проблемы.

Код ошибки: { $code }
Детали: { $detail }"""]: ...


class Successfully:
    @staticmethod
    def added() -> Literal["""Успешно добавлено!"""]: ...

    @staticmethod
    def created() -> Literal["""Успешно создано!"""]: ...

    @staticmethod
    def updated() -> Literal["""Успешно обновлено!"""]: ...


class Unsuccessfully:
    @staticmethod
    def updated() -> Literal["""Ошибка при обновлении!"""]: ...


class Pls:
    @staticmethod
    def wait() -> Literal["""Пожалуйста, ожидайте. Идёт обработка!"""]: ...


class Update:
    @staticmethod
    def status() -> Literal["""Статус обновлён"""]: ...


class Unknown:
    @staticmethod
    def user() -> Literal["""@tg_username"""]: ...


class Template:
    @staticmethod
    def report() -> Literal["""Шаблон отчёта"""]: ...


class User:
    @staticmethod
    def url() -> Literal["""&lt;b&gt;Пользователь:&lt;/b&gt;"""]: ...


class Ya:
    @staticmethod
    def direct() -> Literal["""Яндекс Директ логины"""]: ...

    @staticmethod
    def metric() -> Literal["""Яндекс Метрика счётчик"""]: ...


class Button:
    add: ButtonAdd
    create: ButtonCreate
    delete: ButtonDelete
    edit: ButtonEdit
    filled: ButtonFilled
    remove: ButtonRemove
    report: ButtonReport
    select: ButtonSelect
    set: ButtonSet
    settings: ButtonSettings
    submit: ButtonSubmit
    list: ButtonList
    ya: ButtonYa
    info: ButtonInfo
    to: ButtonTo
    update: ButtonUpdate
    url: ButtonUrl
    viewer: ButtonViewer
    web: ButtonWeb

    @staticmethod
    def agency() -> Literal["""Агентский кабинет"""]: ...

    @staticmethod
    def advertiser() -> Literal["""Прямой рекламодатель"""]: ...

    @staticmethod
    def authorization() -> Literal["""Авторизация"""]: ...

    @staticmethod
    def back() -> Literal["""◀️ Назад"""]: ...

    @staticmethod
    def cancel() -> Literal["""Отменить"""]: ...

    @staticmethod
    def confirm() -> Literal["""Подтвердить"""]: ...

    @staticmethod
    def login() -> Literal["""Войти"""]: ...

    @staticmethod
    def logout() -> Literal["""Выйти"""]: ...

    @staticmethod
    def start() -> Literal["""На главную"""]: ...

    @staticmethod
    def skip() -> Literal["""Пропустить"""]: ...

    @staticmethod
    def no() -> Literal["""Нет"""]: ...

    @staticmethod
    def next() -> Literal["""Продолжить"""]: ...

    @staticmethod
    def representative() -> Literal["""Представитель"""]: ...

    @staticmethod
    def yes() -> Literal["""Да"""]: ...


class ButtonAdd:
    ya: ButtonAddYa

    @staticmethod
    def project() -> Literal["""Новый проект ✏️"""]: ...

    @staticmethod
    def service() -> Literal["""Добавить сервис"""]: ...

    @staticmethod
    def company() -> Literal["""Добавить компанию"""]: ...

    @staticmethod
    def user() -> Literal["""Добавить пользователя"""]: ...

    @staticmethod
    def login() -> Literal["""Добавить логины"""]: ...


class ButtonAddYa:
    @staticmethod
    def counters() -> Literal["""Добавить счётчик метрики"""]: ...

    @staticmethod
    def logins() -> Literal["""Добавить директ логины"""]: ...


class ButtonCreate:
    @staticmethod
    def profile() -> Literal["""Создать профиль"""]: ...


class ButtonDelete:
    @staticmethod
    def object() -> Literal["""Удалить ❌"""]: ...


class ButtonEdit:
    @staticmethod
    def object() -> Literal["""Редактировать ️ 🛠"""]: ...

    @staticmethod
    def attribution() -> Literal["""Изменить атрибуцию"""]: ...

    @staticmethod
    def company() -> Literal["""Изменить название компании"""]: ...

    @staticmethod
    def description() -> Literal["""Изменить описание"""]: ...

    @staticmethod
    def username() -> Literal["""Изменить ФИО"""]: ...

    @staticmethod
    def password() -> Literal["""Сменить пароль"""]: ...

    @staticmethod
    def counter() -> Literal["""Изменить счётчик"""]: ...

    @staticmethod
    def title() -> Literal["""Изменить название"""]: ...


class ButtonFilled:
    @staticmethod
    def application() -> Literal["""Заполнить заявку"""]: ...


class ButtonRemove:
    @staticmethod
    def manager() -> Literal["""Отстранить менеджера"""]: ...


class ButtonReport:
    @staticmethod
    def company() -> Literal["""Отчёт компании"""]: ...

    @staticmethod
    def project() -> Literal["""Отчёт проекта"""]: ...


class ButtonSelect:
    @staticmethod
    def logins() -> Literal["""Выбрать логины"""]: ...


class ButtonSet:
    @staticmethod
    def manager() -> Literal["""Назначить менеджера"""]: ...


class ButtonSettings:
    @staticmethod
    def logins() -> Literal["""Управление Директ логинами"""]: ...


class ButtonSubmit:
    @staticmethod
    def application() -> Literal["""Оставить заявку"""]: ...


class ButtonList:
    ya: ButtonListYa

    @staticmethod
    def companies() -> Literal["""Список компаний"""]: ...

    @staticmethod
    def profile() -> Literal["""Список профилей 📋"""]: ...

    @staticmethod
    def projects() -> Literal["""Список проектов 📂"""]: ...

    @staticmethod
    def viewers() -> Literal["""Список зрителей 📋"""]: ...

    @staticmethod
    def users() -> Literal["""Список пользователей"""]: ...


class ButtonListYa:
    @staticmethod
    def counters() -> Literal["""Список счётчиков метрики"""]: ...


class ButtonYa:
    logins: ButtonYaLogins
    access: ButtonYaAccess


class ButtonYaLogins:
    @staticmethod
    def activate() -> Literal["""Активировать логины"""]: ...

    @staticmethod
    def deactivate() -> Literal["""Деактивировать логины"""]: ...


class ButtonInfo:
    @staticmethod
    def counter() -> Literal["""Подробнее о счётчике"""]: ...


class ButtonTo:
    atlant: ButtonToAtlant
    card: ButtonToCard

    @staticmethod
    def administrator() -> Literal["""Администрирование"""]: ...

    @staticmethod
    def project() -> Literal["""Проекты"""]: ...

    @staticmethod
    def viewers() -> Literal["""Управление аккаунтами зрителей"""]: ...


class ButtonToAtlant:
    @staticmethod
    def administrator() -> Literal["""Атлант администрирование ботом"""]: ...


class ButtonToCard:
    @staticmethod
    def company() -> Literal["""Назад к компании"""]: ...


class ButtonUpdate:
    @staticmethod
    def status() -> Literal["""Обновить статус"""]: ...

    @staticmethod
    def metrika() -> Literal["""Обновить счётчик метрики"""]: ...


class ButtonUrl:
    @staticmethod
    def report() -> Literal["""Ссылка на отчёт"""]: ...


class ButtonViewer:
    set: ButtonViewerSet
    remove: ButtonViewerRemove


class ButtonViewerSet:
    @staticmethod
    def projects() -> Literal["""Подключить проекты"""]: ...


class ButtonViewerRemove:
    @staticmethod
    def projects() -> Literal["""Отключить проекты"""]: ...


class ButtonWeb:
    logout: ButtonWebLogout


class ButtonWebLogout:
    frm: ButtonWebLogoutFrm


class ButtonWebLogoutFrm:
    @staticmethod
    def sessions() -> Literal["""Выйти из сессий"""]: ...


class ButtonYaAccess:
    open: ButtonYaAccessOpen

    @staticmethod
    def direct() -> Literal["""Доступ Яндекс Директ"""]: ...

    @staticmethod
    def metrika() -> Literal["""Доступ Яндекс Метрика"""]: ...


class ButtonYaAccessOpen:
    tg: ButtonYaAccessOpenTg
    web: ButtonYaAccessOpenWeb


class ButtonYaAccessOpenTg:
    @staticmethod
    def web() -> Literal["""Открыть в телеграме"""]: ...


class ButtonYaAccessOpenWeb:
    @staticmethod
    def browser() -> Literal["""Открыть в браузере"""]: ...


class ErrorAirflow:
    add: ErrorAirflowAdd
    start: ErrorAirflowStart


class ErrorAirflowAdd:
    connection: ErrorAirflowAddConnection


class ErrorAirflowAddConnection:
    @staticmethod
    def direct(*, user, company, project_id, counter_login, time, code, err_text) -> Literal["""Возникла проблема при добавлении connection в Airflow.

Пользователь: { $user }
Компания: { $company }
Проект-ID: { $project_id }
Логин / Счётчик_ID: { $counter_login }
Время: { $time }

Status code: { $code }
Text: { $err_text }"""]: ...


class ErrorAirflowStart:
    @staticmethod
    def dag(*, user, company, project_id, time, code, err_text) -> Literal["""Возникла проблема при старте дага Airflow.

    Пользователь: { $user }
    Компания: { $company }
    Проект-ID: { $project_id }
    Время: { $time }

    Status code: { $code }
Text: { $err_text }"""]: ...


class Faq:
    how: FaqHow
    what: FaqWhat
    where: FaqWhere

    @staticmethod
    def preview() -> Literal["""Часто задаваемые вопросы по взаимодействию с ботом.
Если не нашли нужный ответ на свой вопрос, можете обратиться в /help."""]: ...


class FaqHow:
    add: FaqHowAdd
    create: FaqHowCreate
    connect: FaqHowConnect
    work: FaqHowWork
    give: FaqHowGive


class FaqHowAdd:
    extra: FaqHowAddExtra


class FaqHowAddExtra:
    counter: FaqHowAddExtraCounter


class FaqHowAddExtraCounter:
    @staticmethod
    def title() -> Literal["""Могу я добавить в проект ещё один счётчик?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Могу я добавить в проект ещё один счётчик?&lt;/b&gt;
Да, для этого в проекте перейдите в &#34;Список счётчиков метрик&#34; &gt; &#34;Добавить счётчик метрики&#34;, далее используя подсказки настройте счётчик метрики.
Имейте ввиду, что выбранная вами атрибуция в первом счётчике применяется ко всем следующим. Для изменения атрибуции у всех счётчиков перейдите в &#34;Изменить атрибуцию&#34;."""]: ...


class FaqHowCreate:
    project: FaqHowCreateProject
    manager: FaqHowCreateManager


class FaqHowCreateProject:
    @staticmethod
    def title() -> Literal["""Как создать проект?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Как создать проект?&lt;/b&gt;
  Для создания проекта вам необходимо выполнить несколько шагов:
  · Перейдите в &#34;Проекты&#34; &gt; &#34;Новый проект&#34; &gt; дайте название вашему новому проекту и добавьте небольшое описание &gt; нажмите &#34;Подтвердить&#34;.
Готово! Вы успешно создали проект, и теперь он будет отображаться в &#34;Списке проектов&#34;."""]: ...


class FaqWhat:
    next: FaqWhatNext
    are: FaqWhatAre


class FaqWhatNext:
    after: FaqWhatNextAfter


class FaqWhatNextAfter:
    project: FaqWhatNextAfterProject


class FaqWhatNextAfterProject:
    @staticmethod
    def title() -> Literal["""Что делать дальше после создания проекта?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Что делать дальше после создания проекта?&lt;/b&gt;
  Теперь вам нужно раздать доступ для подключения Яндекс Метрики и Директ логинов.
Что для этого нужно?
Перейдите в &#34;Проекты&#34; &gt; &#34;Список проектов&#34; &gt; выберите нужный проект &gt; &#34;Добавить сервис&#34;. Теперь вы можете раздать доступ к той почте, где у вас привязана Яндекс Метрика или Директ. Во избежание дальнейших ошибок, обязательно, проверьте доступы у почты.
Перейдите по ссылке &#34;Яндекс Метрика&#34; или &#34;Яндекс Директ&#34;, в веб-приложении выберите нужный аккаунт с доступами к данным сервисам. Если возникнет ошибка, обратитесь к менеджеру или повторите попытку. В случае успеха закройте окно и нажмите &#34;Обновить статус&#34;.
После обновления у вас появятся кнопки (в зависимости от переданного доступа):
  · &#34;Добавить Директ логины&#34; – здесь вы можете выбрать один из предложенных вариантов в зависимости от типа вашего кабинета:
     · &#34;Агентский кабинет&#34; и &#34;Прямой рекламодатель&#34; отобразят список доступных логинов. Выбрав их, вы сможете добавить их в свой проект.
     · &#34;Представитель&#34; даёт возможность &#34;Добавить логины&#34;, вводя их вручную через запятую (например, login1, login2, login3). Бот проверит, есть ли у вас доступ к введённым логинам, и отобразит их вам в сообщении. Логины с доступами можно будет выбрать в &#34;Выбрать логины&#34;, отметив их в предоставленном списке и нажав &#34;Подтвердить&#34;, тем самым добавив их в проект.
  · &#34;Добавить счётчик Метрики&#34; – здесь всё проще: следуйте пошаговым инструкциям и ориентируйтесь на подсказки в сообщениях."""]: ...


class FaqHowConnect:
    disconnect: FaqHowConnectDisconnect


class FaqHowConnectDisconnect:
    direct: FaqHowConnectDisconnectDirect


class FaqHowConnectDisconnectDirect:
    logins: FaqHowConnectDisconnectDirectLogins


class FaqHowConnectDisconnectDirectLogins:
    @staticmethod
    def title() -> Literal["""Мне нужно отключить некоторые логины Директа в проекте, как это сделать?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Мне нужно отключить некоторые логины Директа в проекте, как это сделать?&lt;/b&gt;
Для отключения одного или нескольких логинов Директа:
  1. Перейдите в нужный вам проект.
  2. Нажмите &#34;Управление Директ логинами&#34;.
  3. В следующем меню выберите &#34;Деактивировать логины&#34;.
  4. Из представленного списка активных логинов отметьте один или несколько логинов.
  5. Нажмите &#34;Подтвердить&#34;.
Проект будет обновлён. Для возврата ранее деактивированных логинов перейдите в окно со списком логинов и нажмите &#34;Активировать логины&#34;."""]: ...


class FaqWhatAre:
    viewers: FaqWhatAreViewers
    management: FaqWhatAreManagement


class FaqWhatAreViewers:
    @staticmethod
    def title() -> Literal["""Для чего нужны  зрители?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Для чего нужны  зрители?&lt;/b&gt;
Зритель – это аккаунт с разрешением на просмотр проекта, а именно отчёта по нему и текущих настроек, включая подключённые логины и счётчики Метрики. Такой аккаунт полезен, если вы хотите показать клиенту, как ведётся проект."""]: ...


class FaqHowWork:
    viewers: FaqHowWorkViewers


class FaqHowWorkViewers:
    @staticmethod
    def title() -> Literal["""Как работать с аккаунтами зрителей?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Как работать с аккаунтами зрителей?&lt;/b&gt;
Для создания и управления аккаунтами зрителей:
  1. Перейдите в главное меню и нажмите &#34;Управление аккаунтами зрителей&#34;.
  2. В данном меню выберите &#34;Создать профиль&#34; и следуйте пошаговой инструкции в сообщениях Telegram-бота.
  3. После подтверждения можете передать логин и пароль зрителю.
Теперь, после создания профиля, у вас есть возможность предоставить просмотровый доступ выбранному зрителю:
 · Перейдите в &#34;Список зрителей&#34;.
 · Выберите нужный профиль и нажмите &#34;Подключить проекты&#34;.
 · Вам отобразится список ваших текущих проектов.
 · Отметьте один или несколько проектов и нажмите &#34;Подтвердить&#34;.
Для отзыва доступа у зрителя:
 · Нажмите &#34;Отключить проекты&#34;.
 · В появившемся списке проектов отметьте один или несколько проектов.
 · Нажмите &#34;Подтвердить&#34;, чтобы отозвать доступ."""]: ...


class FaqWhatAreManagement:
    profile: FaqWhatAreManagementProfile


class FaqWhatAreManagementProfile:
    @staticmethod
    def title() -> Literal["""Для чего нужно меню &#34;Администрирование&#34;?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Для чего нужно меню &#34;Администрирование&#34;?&lt;/b&gt;
Так как вы являетесь администратором компании, у вас есть возможность:
 · добавлять и удалять менеджеров,
 · просматривать все проекты компании.
Менеджер – это аккаунт, который может:
 · создавать и вести проекты,
 · создавать профили зрителей и настраивать их,
 · использовать функционал &#34;Проекты&#34; и &#34;Управление аккаунтами зрителей&#34;."""]: ...


class FaqHowCreateManager:
    @staticmethod
    def title() -> Literal["""Как создать менеджера?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Как создать менеджера?&lt;/b&gt;
Для создания менеджера:
  1. Перейдите в главное меню и нажмите &#34;Администрирование&#34;.
  2. Выберите &#34;Создать профиль&#34;.
  3. Следуйте пошаговой инструкции в сообщениях.
После создания профиля передайте логин и пароль менеджеру, чтобы он мог взаимодействовать с Telegram-ботом.
Если необходимо сменить пароль или ФИО менеджера:
  1. Перейдите в меню &#34;Администрирование&#34;.
  2. Нажмите &#34;Список профилей&#34;.
  3. В списке выберите нужный профиль."""]: ...


class FaqHowGive:
    withdraw: FaqHowGiveWithdraw


class FaqHowGiveWithdraw:
    permission: FaqHowGiveWithdrawPermission


class FaqHowGiveWithdrawPermission:
    @staticmethod
    def title() -> Literal["""Как дать/забрать разрешение на ведение проекта?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Как дать/забрать разрешение на ведение проекта?&lt;/b&gt;
Чтобы дать или забрать разрешение на ведение определённого проекта:
  1. Перейдите в главное меню и нажмите &#34;Администрирование&#34;.
  2. Выберите &#34;Список проектов&#34;.
  3. Вам отобразится список всех проектов компании.
  4. Выберите нужный проект.
  5. В текущем проекте выберите &#34;Отстранить менеджера&#34; или &#34;Назначить менеджера&#34;.
  6. Вам будет представлен список менеджеров компании.
  7. Отметьте нужного менеджера и подтвердите изменения.
Так же карточка проекта содержит всю актуальную информацию по проекту."""]: ...


class FaqWhere:
    see: FaqWhereSee


class FaqWhereSee:
    project: FaqWhereSeeProject


class FaqWhereSeeProject:
    report: FaqWhereSeeProjectReport


class FaqWhereSeeProjectReport:
    @staticmethod
    def title() -> Literal["""Где мне увидеть проект и отчёт по нему?"""]: ...

    @staticmethod
    def text() -> Literal["""&lt;b&gt;Где мне увидеть проект и отчёт по нему?&lt;/b&gt;
Для просмотра доступных проектов перейдите в &#34;Проекты&#34; &gt; &#34;Список проектов&#34;.
В представленном списке выберите нужный проект, кликнув по нему.
В карточке проекта нажмите на &#34;Отчёт&#34; – после этого в веб-приложении откроется отчёт (при необходимости потребуется авторизация)."""]: ...


class Alert:
    added: AlertAdded
    edited: AlertEdited
    deleted: AlertDeleted


class AlertAdded:
    ya: AlertAddedYa

    @staticmethod
    def project(*, title, company) -> Literal["""Проект создан!
Название проекта: { $title }
Компания: { $company }"""]: ...


class AlertAddedYa:
    direct: AlertAddedYaDirect
    metrika: AlertAddedYaMetrika


class AlertAddedYaDirect:
    @staticmethod
    def login(*, title, company) -> Literal["""Добавлены логины директа!
Название проекта: { $title }
Компания: { $company }"""]: ...


class AlertAddedYaMetrika:
    @staticmethod
    def counters(*, title, company, ya_counter) -> Literal["""Добавлен счётчик метрики!
Название проекта: { $title }
Компания: { $company }
Счётчик метрики: { $ya_counter }"""]: ...


class AlertEdited:
    ya: AlertEditedYa


class AlertEditedYa:
    metrika: AlertEditedYaMetrika
    direct: AlertEditedYaDirect


class AlertEditedYaMetrika:
    counter: AlertEditedYaMetrikaCounter

    @staticmethod
    def counters(*, title, company) -> Literal["""Произошли изменения в проекте, изменение счётчика!
Название проекта: { $title }
Компания: { $company }"""]: ...


class AlertEditedYaMetrikaCounter:
    @staticmethod
    def attr(*, title, company) -> Literal["""Произошли изменения в проекте, смена аттрибуции в счётчиках!
Название проекта: { $title }
Компания: { $company }"""]: ...


class AlertEditedYaDirect:
    logins: AlertEditedYaDirectLogins


class AlertEditedYaDirectLogins:
    @staticmethod
    def activated(*, title, company) -> Literal["""Произошли изменения в проекте, изменение логинов директа!
Изменение статуса некоторых логинов с неактивного на активное.
Название проекта: { $title }
Компания: { $company }"""]: ...

    @staticmethod
    def deactivated(*, title, company) -> Literal["""Произошли изменения в проекте, изменение логинов директа!
Изменение статуса некоторых логинов с активного на неактивное.
Название проекта: { $title }
Компания: { $company }"""]: ...


class AlertDeleted:
    @staticmethod
    def project(*, title, company) -> Literal["""Проект удален!
Название проекта: { $title }
Компания: { $company }"""]: ...

