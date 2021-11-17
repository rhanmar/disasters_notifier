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

    const showPoints = function (response) {
        clearMap()
        response.forEach(
            point => {
                myMap.geoObjects.add(
                    new ymaps.Placemark(
                        point['coordinates'].split(','),
                        {
                            id:point['id'],
                            balloonContent: point['name'] // TODO remove
                        },
                        {
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
        // console.log('123123')
        let id = $("#modal_point_detail_id").text()
        // console.log(id)
        // alert('delete')
        let url = pointList + id
        console.log(url)
        $.ajax({
            url: url,
            type: "DELETE",
            success: function (response) {
                // alert("success");
                $('#modal_point_detail').modal("hide");
                getPoints()  // renew map
            },
            error: function (response) {
                // TODO handler
                alert("error!")
            }
        })
    })

    const showPointDetail = function (e) {
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
    myMap.events.add('balloonopen', showPointDetail);
    getPoints()
}
