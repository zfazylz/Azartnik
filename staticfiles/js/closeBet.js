function closeBet(betID, res) {
    $.ajax({
        type: "POST",
        url: "/closeBet/",
        data: {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken" ]').val(),
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
