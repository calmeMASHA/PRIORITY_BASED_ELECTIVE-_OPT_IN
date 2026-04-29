$(document).ready(function() {
    $('.elective-select').change(function() {
        var electiveId = $(this).val();
        var selectId = $(this).attr('id');
        var counterId = '#seats-' + selectId;
        
        if (electiveId) {
            $.ajax({
                url: '/electives/api/seats/' + electiveId + '/',
                type: 'GET',
                success: function(response) {
                    var seats = response.available_seats;
                    $(counterId).text('Seats: ' + seats);
                    
                    if (seats === 0) {
                        $(counterId).removeClass('bg-success bg-warning').addClass('bg-danger');
                    } else if (seats < 10) {
                        $(counterId).removeClass('bg-success bg-danger text-white').addClass('bg-warning text-dark');
                    } else {
                        $(counterId).removeClass('bg-danger bg-warning text-dark').addClass('bg-success text-white');
                    }
                },
                error: function() {
                    $(counterId).text('Seats: Error');
                }
            });
        } else {
            $(counterId).text('Seats: -');
            $(counterId).removeClass('bg-danger bg-warning text-dark').addClass('bg-success text-white');
        }
    });

    // Trigger change on load for any pre-selected values
    $('.elective-select').trigger('change');
});
