$(document).ready(function() {
    var offset = 10;
    var limit = 5;
    var loading = false;

    function loadMore() {
        if (loading) {
            return;
        }

        loading = true;

        $.ajax({
            url: '/load-more-siswa/',
            type: 'GET',
            data: {
                offset: offset
            },
            success: function(response) {
                $('#notif-siswa').append(response);
                offset += limit;
                loading = false;
            },
            error: function(xhr, status, error) {
                console.error(error);
                loading = false;
            }
        });
    }

    $(window).scroll(function() {
        var scrollPosition = $(window).scrollTop() + $(window).height();
        var documentHeight = $(document).height();
        var threshold = 200;

        if (scrollPosition >= documentHeight - threshold) {
            loadMore();
        }
    });
});