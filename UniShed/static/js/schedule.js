//Getting csrf token
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Submit post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check

    //Send data to server for getting back sorted
    $.ajax({
        url: '/schedule/sort_group/',
        async: true,
        type: 'post',
        data: { //data sent with the post request
            group_field_value: $("#select_group").children("#group-option:selected").val(),
            lector_field_value: $("#select_lector").children("#lector-option:selected").attr("name"),
            room_field_value: $("#select_room").children("#room-option:selected").val(),
            time_field_value: $("#select_time").children("#time-option:selected").val(),
        },
        dataType: 'json',
        success: function (data) {
        $("#change_by_select").html(data.html_form);

        }
    });
});


//Conflicts show
$(".conflicts_btn").click(function () {

    $.ajax({
        url: '/schedule/conflicts/',
        async: true,
        type: 'post',
        data: { //data sent with the post request

        },
        dataType: 'json',
        success: function (data) {
        $("#change_by_select").html(data.html_form);

        }
    });
})


