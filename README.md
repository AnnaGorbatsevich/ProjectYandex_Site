# ProjectYandex_Site
Проект по Яндекс.Лицею Анна Горбацевич и Алексей Люлько.

Проект – это интернет магазин с опциями:
1.	Регистрация и вход на сайт. Пользователь может зарегистрироваться на сайте путём заполнения соответствующей формы. После окончания процедуры и нажатия кнопки “submit”, пользователь добавляется в базу данных сайта, и с данного момента, может полноценно им пользоваться.

2.	Добавление своего товара на сайт. В левой верхней части интерфейса есть кнопка “добавить продукт”, при нажатии на которую пользователь попадает на страницу редактирования информации для своего товара. На ней он должен указать обязательные параметры: “названия, страна отправки, описание и цена” (Если какое-либо из обязательных полей будет пустым, то товар не будет принят на подтверждение на сайт), а также дополнительные, которые добавляются при помощи специальной кнопки “+”. В них он самолично вписывается необходимые ему названия и вариации параметров. (Если какое-либо из доп. полей будет по подтверждению товара пустым, то в дальнейшем оно не будет отображаться на сайте, так как является невалидным).

3.	Заказ товаров. Под кратким описанием товара на главной странице, при нажатии на кнопку заказа, пользователя переадресует на страницу заказа продукта. На ней пользователь обязан выбрать все подходящие для него параметры товара: (страна отправки, доп. параметры (если есть) и т.п.). При подтверждении покупки товара, продукт добавляется в базу данных, а также в корзину (иконка справа сверху в меню). При этом пользователя перекинет на основную страницу магазина, где он может продолжить заказывать или перейти в корзину для подтверждения.


4.	Редактирование всего заказа и подсчёт результата. В индивидуальной корзине пользователя отображаются все покупки конкретного юзера. В специальных полях “Количество”, пользователь может изменить кол-во заказываемого товара. По дефолту в нём стоит единица, юзер может изменить кол-во на нужное ему и по нажатию на кнопку “пересчитать”, текущая цена заказа пересчитается на корректную-новую. Если в поле указать ноль, то по нажатии кнопки “пересчитать”, товар удалится из заказа и никак не будет включён в текущую стоимость всего заказа. 


Всё реализовано на локальной базе данных, в которую записывается и информация о пользователях и их заказах, так и информация о самих доступных товарах. (sqlite)
Большинство форм работают на flask-forms и wtforms.
Страницы сайта верстались на html+css (и немного js).
Серверная часть полностью написана на python (вычисление, изменение, редактирование информации). За отображение информации на самом сайте отвечал html/css/js.  
