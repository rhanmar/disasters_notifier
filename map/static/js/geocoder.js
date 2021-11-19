// Функция ymaps.ready() будет вызвана, когда
// загрузятся все компоненты API, а также когда будет готово DOM-дерево.
ymaps.ready(init);
function init() {
    // Создание карты.
    var myMap = new ymaps.Map("map", {
        // Координаты центра карты.
        // Порядок по умолчанию: «широта, долгота».
        // Чтобы не определять координаты центра карты вручную,
        // воспользуйтесь инструментом Определение координат.
        center: [55.76, 37.64],
        // Уровень масштабирования. Допустимые значения:
        // от 0 (весь мир) до 19.
        zoom: 7
    });

    var myGeoObject = new ymaps.GeoObject({ // REMOVE LATER TODO
        // Описание геометрии.
        geometry: {
            type: "Point",
            coordinates: [55.8, 37.8]
        },
        // Свойства.
        properties: {
            // Контент метки.
            iconContent: 'Я тащусь',
            hintContent: 'Ну давай уже тащи'
        }
    }, {
        // Опции.
        // Иконка метки будет растягиваться под размер ее содержимого.
        preset: 'islands#blackStretchyIcon',
        // Метку можно перемещать.
        draggable: true
    })

    myMap.geoObjects
        .add(myGeoObject)
        .add(new ymaps.Placemark([55.684758, 37.738521], { // REMOVE LATER TODO
            balloonContent: 'цвет <strong>воды пляжа бонди</strong>'
        }, {
            preset: 'islands#icon',
            iconColor: '#0095b6'
        }))
        .add(new ymaps.Placemark([55.833436, 37.715175], { // REMOVE LATER
            balloonContent: '<strong>серобуромалиновый</strong> цвет'
        }, {
            preset: 'islands#dotIcon',
            iconColor: '#735184'
        }))


    $('#create_point_form').submit(function (event) {
        event.preventDefault();
        console.log('submitted');
        $.ajax({
            // data: $(this).serialize(), TODO
            data: $(this).serializeArray(),
            type: "POST",
            url: pointList,
            success: function (response) {
                // console.log($('#create_point_form'))
                $('#create_point_form')[0].reset()
                $('#modal_point_create').modal("hide");
                getPoints()  // renew map
            },
            error: function (response) {
                // TODO handler
                alert("error! can't do it")
                // alert(response.responseJSON.errors)

            }
        })
    });

    const clearMap = function () {
      myMap.geoObjects.removeAll()
    };

    const createPoint = function (e) {
        let coords = e.get('coords')
        $('#modal_point_create').modal("show");
        $("#location_field").val(coords);
    };

    const getPoints = function () {
      $.ajax({
          type: "GET",
          url: pointList,
          success: function (response) {
              showPoints(response);
          },
          error: function (response) {
            showFail();
          },
      })
    };


    counter = 0

    // Создание макета содержимого балуна.
    // Макет создается с помощью фабрики макетов с помощью текстового шаблона.
    BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
        '<div style="margin: 10px;">' +
            '<b>{{ properties.id }}</b><br>' +
            '<b>{{ properties.name }}</b><br>' +
            // '<i id="count"></i> ' +
            '<button id="counter-button"> Delete </button>' +
        '</div>', {

        // Переопределяем функцию build, чтобы при создании макета начинать
        // слушать событие click на кнопке-счетчике.
        build: function () {
            // Сначала вызываем метод build родительского класса.
            BalloonContentLayout.superclass.build.call(this);
            // А затем выполняем дополнительные действия.
            $('#counter-button').bind('click', this.onCounterClick);
            $('#count').html(counter);
        },

        // Аналогично переопределяем функцию clear, чтобы снять
        // прослушивание клика при удалении макета с карты.
        clear: function () {
            // Выполняем действия в обратном порядке - сначала снимаем слушателя,
            // а потом вызываем метод clear родительского класса.
            $('#counter-button').unbind('click', this.onCounterClick);
            BalloonContentLayout.superclass.clear.call(this);
        },

        onCounterClick: function () {
            alert('ajax delete')
            showPointDetail()
        }
    });




    const showPoints = function (response) {
        clearMap()
        console.log(response)
        response.forEach(
            point => {
                myMap.geoObjects.add(
                    new ymaps.Placemark(
                        point['coordinates'].split(','),
                        {
                            id:point["id"],
                            name:point["name"]
                            // balloonContent: point['name'], // TODO remove

                        },
                        {
                            balloonContentLayout: BalloonContentLayout,
                            balloonPanelMaxMapArea: 0,
                            preset: point['verified'] ? 'islands#greenDotIconWithCaption' : 'islands:icon',
                            // islands#greenDotIconWithCaption
                            // iconColor: '#0095b6'
                        }
                        )
                )
            }
        )
    };

    const showFail = function () {
      alert("Not OK")
    };

    $('#modal_point_detail_delete_button').click(function (e) {
        let pointId = $("#modal_point_detail_id").text()
        let url = pointList + pointId
        console.log(e)
        let csrfToken = e.target.ownerDocument.cookie.split("=")[1]
        console.log(url)
        $.ajax({
            url: url,
            type: "DELETE",
            headers: {
                "X-CSRFTOKEN": csrfToken,
            },
            success: function (response) {
                // alert("success");
                $('#modal_point_detail').modal("hide");
                getPoints()  // renew map
            },
            error: function (response) {
                // TODO handler
                alert("error!")
                alert(response)
                console.log(response)
            }
        })
    })

    const showPointDetail = function (e) {
        // console.log(e)
        let target = e.get("target")
        // console.log("!!showPointDetail")
        // console.log(target.properties.get("id"))
        // console.log(target.properties.get("balloonContent"))
        $('#modal_point_detail_id').text(target.properties.get("id"))
        // $('#modal_point_detail_id').val(target.properties.get("id"))
        // $('#modal_point_detail_name').text(target.properties.get("balloonContent"))
        $('#modal_point_detail').modal("show");
    };

    myMap.events.add('click', createPoint);
    // myMap.events.add('balloonopen', showPointDetail);  // TODO balloon or Modal Form
    getPoints()
}
