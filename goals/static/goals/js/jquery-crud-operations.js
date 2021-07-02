
(function ($) {

    // when the user click on detail, create, update or delete buttons 
    // fetch (detail, create, update or delete) template and put it in the bootstrap modal
    $("#list-temp-place").on("click", "#fetch-detail-temp", fetchTemp);
    $("#list-temp-place").on("click", "#fetch-create-temp", fetchTemp);
    $("#list-temp-place").on("click", "#fetch-update-temp", fetchTemp);
    $("#list-temp-place").on("click", "#fetch-delete-temp", fetchTemp);
    $("#list-temp-place").on("click", "#change-task-status", changeTaskStatus);

    // when the user submit create, update or delete templates
    // submit (create, update or delete) template 
    $(".modal").on("submit", "#submit-create-temp", submitTemp);
    $(".modal").on("submit", "#submit-update-temp", submitTemp);
    $(".modal").on("submit", "#submit-delete-temp", submitTemp);
    

    //********************** handler functions ********************** 
    

    // fetch (detail, create, update or delete) template and put it in the bootstrap modal
    function fetchTemp(e) {
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $(".modal").modal("show"); 
            },
            success: function (data) {
                // put the (detail, create, update or delete) templates in our bootstrap modal
                $(".modal-content").html(data['modal_temp']); 
            },
            error: function() {
                alert('Could Not Fetch Template')
            }
        });
    }
    
    // submit (create, update or delete) template 
    function submitTemp(e) {
        e.preventDefault();
        var form = $(this);
        var fd = new FormData(form[0]);
        $.ajax({
            url: form.attr('action'),
            data: fd, // <-- add this when using FromData
            processData: false, // <-- add this when using FromData
            contentType: false, // <-- add this when using FromData
            type: form.attr("method"),
            dataType: 'json',
            success: function(data) {
                // the server should return 'form_is_valid'=True or 'form_is_valid'=False
                if (data.form_is_valid) { 
                    // we render list template
                    $(".modal").modal("hide"); 
                    $("#list-temp-place").html(data['list_temp']); 
                }
                else { 
                    // we rerender template with error messages to correct
                    $(".modal-content").html(data['modal_temp']); 
                }
            },
            error: function() {
                alert('Could Not Submit Template')
            }
        });
        return false;
    }

    // change task status
    function changeTaskStatus(e) {
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#list-temp-place").html(data['list_temp']); 
            },
            error: function() {
                alert('Could Not Perform This Operation')
            }
        });
    }
    

})(jQuery);

