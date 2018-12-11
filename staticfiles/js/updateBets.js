$(function () {
    setInterval(function () {
        $.ajax({
            type: "POST",
            url: "/game/",
            data: {
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken" ]').val(),
            },
            success: function (response) {
                $("#userBalance").html(response['userBalance']);

                var betsList = response['betsList'];
                var betListHTML = "";
                $.each(betsList, function (index, value) {
                    betListHTML +=
                        "<div class=\"col-sm-12\">\n" +
                        "<div class=\"container\">\n" +
                        "<div class=\"row\">" +
                        "<div class=\"col-sm-1\"> " + value[0] + " </div>\n" +
                        "<div class=\"col-sm-5\">" + value[1] + "</div>\n" +
                        "<div class=\"col-sm-6\"> " +
                        "<div class=\"container\">\n" +
                        "<div class=\"row\">\n" +
                        "<div class=\"col-sm-4\"> <a href=\"\" onclick=\"return makeBet(" + value[0] + ", 1)\">" + value[2] + " <a/></div>\n" +
                        "<div class=\"col-sm-4\"> <a href=\"\" onclick=\"return makeBet(" + value[0] + ", 0)\">" + value[3] + " <a/></div>\n" +
                        "<div class=\"col-sm-4\"> <a href=\"\" onclick=\"return makeBet(" + value[0] + ", 2)\">" + value[4] + " <a/></div>\n" +
                        "</div>\n" +
                        "</div>" + "</div>\n" +
                        "</div>" + "</div>\n" +
                        "</div>"
                });
                $("#betsList ").html(betListHTML);

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert('Try to refresh the page');
            }
        });
    }, 5000);
});
