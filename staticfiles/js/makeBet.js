function makeBet(betID, res) {
    $.ajax({
        type: "POST",
        url: "/makeBet/",
        data: {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken" ]').val(),
            betValue: $("#betValue").val(),
            betID: String(betID),
            res: String(res),
        },
        success: function (response) {
            alert('Done!')
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert('Try to refresh the page');
        }
    })
};