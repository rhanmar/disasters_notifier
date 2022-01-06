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
        console.log('submitted create'); // TODO REMOVE
        console.log($(this).serializeArray())
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
        let coords = e.get('coords');
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

    const getCSRFTokenFromCookie = function(cookies) {
        let csrfToken = null
        let data = cookies.split(';');
        data.forEach(element => {
            if (element.replace(/\s/g, "").startsWith('csrftoken')) {
                csrfToken = element.replace(/\s/g, "").split('=')[1]
            }
        })
        return csrfToken
    }



    // // Создание макета содержимого балуна.
    // // Макет создается с помощью фабрики макетов с помощью текстового шаблона.
    // BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
    //     '<div style="margin: 10px;">' +
    //         // '<b>{{ properties.id }}</b><br>' +
    //         '<h4>name: {{ properties.name }}<br></h4>' +
    //
    //         '<p>disaster type: {{ properties.disasterType }}<br>' +
    //         'disaster level: {{ properties.disasterLevel }}/5<br></p>' +
    //         '<button id="edit-point-button" class="btn btn-info btn-sm"> Edit </button>\t\t\t' +
    //         '<button id="delete-point-button" class="btn btn-danger btn-sm"> Delete </button><br>' +
    //         '<p>created at: {{ properties.createdAt }}<br>' +
    //         'last modified at: {{ properties.lastModifiedAt }}<br></p>' +
    //     '</div>', {
    //
    //     // Переопределяем функцию build, чтобы при создании макета начинать
    //     // слушать событие click на кнопке-счетчике.
    //     build: function () {
    //         // Сначала вызываем метод build родительского класса.
    //         BalloonContentLayout.superclass.build.call(this);
    //         // А затем выполняем дополнительные действия.
    //         $('#delete-point-button').bind('click', this.onDeleteClick);
    //         $('#edit-point-button').bind('click', this.onEditClick);
    //
    //     },
    //
    //     // Аналогично переопределяем функцию clear, чтобы снять
    //     // прослушивание клика при удалении макета с карты.
    //     clear: function () {
    //         // Выполняем действия в обратном порядке - сначала снимаем слушателя,
    //         // а потом вызываем метод clear родительского класса.
    //         $('#delete-point-button').unbind('click', this.onDeleteClick);
    //         $('#edit-point-button').unbind('click', this.onEditClick);
    //         BalloonContentLayout.superclass.clear.call(this);
    //     },
    //
    //     onDeleteClick: function () {
    //         alert('ajax delete')
    //         showPointDetail()
    //     },
    //
    //     onEditClick: function () {
    //         alert('ajax edit')
    //         // $('#modal_point_detail').modal("show");
    //         showPointDetail()
    //     },
    // });

    const definePointDisplay = function (point) {
        //
        // console.log(point)
        // console.log(point["verified"])
        // console.log('!!!!!')
        // return "islands:icon"
        if (point["verified"]) {
            if (point["disaster_type"] == "fire") {
                return "islands#redDotIcon"
            }
            if (point["disaster_type"] == "water") {
                return "islands#darkBlueDotIcon"
            }
            if (point["disaster_type"] == "geo") {
                return "islands#brownDotIcon"
            }
            if (point["disaster_type"] == "meteo") {
                return "islands#grayDotIcon"
            }
        }
        else {
            return "islands:icon"
            // return "islands#blueCircleDotIcon"
        }
    }


    const showPoints = function (response) {
        clearMap()
        console.log(response)
        response.forEach(
            point => {
                myMap.geoObjects.add(
                    new ymaps.Placemark(
                        point['coordinates'].split(','),
                        {
                            id: point["id"],
                            name: point["name"],
                            createdAt: point["created_at"],
                            modifiedAt: point["modified_at"],
                            disasterType: point["disaster_type"],
                            disasterLevel: point["disaster_level"],
                            verified: point["verified"],
                            createdBy: point["created_by"],
                            createdByID: point["created_by.id"],
                            balloonContent: "Point info is opened", // TODO remove

                        },
                        {
                            // balloonContentLayout: BalloonContentLayout,
                            // balloonPanelMaxMapArea: 0,

                            // preset: point['verified'] ? 'islands#greenDotIconWithCaption' : 'islands:icon',
                            preset: definePointDisplay(point)
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
        let csrfToken = getCSRFTokenFromCookie(e.target.ownerDocument.cookie)
        // console.log(csrfToken2)
        // console.log(e.target.ownerDocument.cookie)
        // console.log(csrfToken)
        // console.log(url)
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
                // console.log(response)
            }
        })
    });

    $('#edit_point_form').submit(function (event) {
        event.preventDefault();
        let pointId = $("#modal_point_detail_id").text()
        let url = pointList + pointId + '/'
        // let csrfToken = event.target.ownerDocument.cookie.split("=")[1]
        let csrfToken = getCSRFTokenFromCookie(event.target.ownerDocument.cookie)
        // alert(csrfToken)


        console.log("submitted edit") // TODO REMOVE
        // console.log(pointId)
        console.log('!!')
        // console.log(url)
        console.log($(this).serializeArray())
        console.log($(this))
        console.log($(this).serialize())

        // let data = $(this).serializeArray()
        // let newData = ""
        // if (!("name" in data)) {
        //     alert('not')
        //     // data["name"] = 'off';
        //     newData = $(this).serialize()
        //     newData += "&verified=off"
        // }
        // else {
        //     alert("IN")
        //
        // }
        let data = $(this).serialize()
        if (!data.includes("verified")) {
            data += "&verified=off";
        }
        // if ($("edit_point_form input#id_verified").checked) {
        //     alert("IS")
        // }
        // else {
        //     alert("NOT")
        // }
        console.log('!!')
        console.log(csrfToken)
        console.log(data)
        // console.log(newData)
        $.ajax({
            // data: $(this).serializeArray(),
            data: data,
            type: "PATCH",
            url: url,
            headers: {
                "X-CSRFTOKEN": csrfToken,
            },
            success: function (response) {
                // alert("success edit");
                getPoints();
                $('#modal_point_edit').modal("hide");
            },
            error: function (response, errors) {
                alert("error edit")
                alert(response.error)
                // console.log('error edit')
                // console.log(response)
                // console.log(response.error)
                // console.log(errors)
            }
        })
    });


    $('#modal_point_detail_edit_button').click(function (e) {
        let pointId = $("#modal_point_detail_id").text()
        let url = pointList + pointId
        console.log(url)
        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                // alert("success");
                // console.log(response)
                $("#edit_point_form input#id_name").val(response['name'])
                $("#edit_point_form select#id_disaster_level").val(response['disaster_level'])
                // $("#edit_point_form input#id_verified").val(response['verified'])
                $("#edit_point_form input#id_verified").prop("checked", response['verified'])
                // console.log($("#edit_point_form ul#id_disaster_type").children())
                // console.log($("#edit_point_form input[name='disaster_type']"))

                $("#edit_point_form input[name='disaster_type']").each(function() {
                    if ($(this).val() == response["disaster_type"]) {
                        console.log($(this).val())
                        $(this).prop("checked", "checked")
                    }

                })

            },
            error: function (response) {
                // TODO handler
                alert("error!")
                alert(response)
                console.log(response)
            }

        })
        alert("edit");
        $('#modal_point_detail').modal("hide");
        $('#modal_point_edit').modal("show");
    });

    const showPointDetail = function (e) {
        // console.log(e)
        let target = e.get("target")
        console.log("!!showPointDetail")
        console.log(e)
        // console.log(target.properties.get("id"))
        // console.log(target.properties.get("balloonContent"))
        $('#modal_point_detail_id').text(target.properties.get("id"))
        $('#modal_point_detail_name').text(target.properties.get("name"))
        $('#modal_point_detail_disaster_level').text(target.properties.get("disasterLevel"))
        $('#modal_point_detail_disaster_type').text(target.properties.get("disasterType"))
        $('#modal_point_detail_verified').text(target.properties.get("verified"))
        $('#modal_point_detail_created_at').text(target.properties.get("createdAt")) // TODO to footer
        $('#modal_point_detail_created_by').text(target.properties.get("createdBy")) // TODO to footer
        $('#modal_point_detail_created_by_id').text(target.properties.get("createdByID"))

        console.log(currentUserID === target.properties.get("createdBy"))
        console.log(isCurrentUserSuperUser)
        if (!(currentUserID === target.properties.get("createdBy")) && (!isCurrentUserSuperUser)) {
            $('#modal_point_detail_delete_button').hide()
            $('#modal_point_detail_edit_button').hide()
        }
        else {
            $('#modal_point_detail_delete_button').show()
            $('#modal_point_detail_edit_button').show()
        }


        // $('#modal_point_detail_id').val(target.properties.get("id"))
        // $('#modal_point_detail_name').text(target.properties.get("balloonContent"))
        $('#modal_point_detail').modal("show");
        target.balloon.close()
    };

    myMap.events.add('click', createPoint);
    myMap.events.add('balloonopen', showPointDetail);  // TODO balloon or Modal Form
    getPoints()
}
