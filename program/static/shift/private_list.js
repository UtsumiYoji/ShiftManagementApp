const monthNames = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
];

function formatDate(date) {
    const month = monthNames[date.getMonth()];
    const day = date.getDate();
    return `${month} ${day}`;
}

function time_to_string(date) {
    return (date.getHours()+':'+date.getMinutes().toString().padStart(2, '0'))
}

// Get the URL search parameters
var url = new URL(window.location.href);
var params = url.searchParams;

$(document).on('click', '.today', function() {
    params.delete('start_at__gte');
    window.location.href = url.toString();
});

$(document).on('click', '.previous-week', function() {
    var start_at__gte = new Date(params.get('start_at__gte')+'T00:00:00');
    start_at__gte.setDate(start_at__gte.getDate() - 7);
    var formattedDate = start_at__gte.toISOString().split('T')[0];
    params.set('start_at__gte', formattedDate);
    window.location.href = url.toString();
});

$(document).on('click', '.next-week', function() {
    var start_at__gte = new Date(params.get('start_at__gte')+'T00:00:00');
    start_at__gte.setDate(start_at__gte.getDate() + 7);
    var formattedDate = start_at__gte.toISOString().split('T')[0];
    params.set('start_at__gte', formattedDate);
    window.location.href = url.toString();
});

$(document).ready(function() {
    window.scrollTo(0, 500);

    // Check there is any parameter
    if (!params.has('start_at__gte')) {
        // Get this Sunday
        var day = new Date();
        var dayOfWeek = day.getDay();
        var diffToSunday = dayOfWeek;
        day.setDate(day.getDate() - diffToSunday);
        day.setHours(0, 0, 0, 0);

        var formattedDate = day.toISOString().split('T')[0];
        url.searchParams.set('start_at__gte', formattedDate);
        window.location.href = url.toString();
        return;
    }

    // Create calendar header
    var start_at__gte = new Date(params.get('start_at__gte')+'T00:00:00');
    for (var i = 0; i < 7; i++) {
        var day = new Date(start_at__gte);
        day.setDate(start_at__gte.getDate() + i);

        $('.day'+(i+1)+'>p').text(formatDate(day));

        // judge it is today
        if (formatDate(new Date()) === formatDate(day)) {
            $('.day'+(i+1)).addClass('today');
        }
    }
    // store day as a final day
    var final_day = new Date(day);

    // if there is no shift, return
    if (shifts.length === 0) {
        return;
    }

    shifts.forEach(shift => {
        console.log(shift)
        start_at = new Date(shift.start_at);
        finish_at = new Date(shift.finish_at);

        // find day
        for (var column = 1; column <= 7; column++) {
            if ($('.day'+column+'>p').text() == formatDate(start_at)) {
                break
            }
        }

        // find time
        for (var time = 1; time <= 24; time++) {
            if (start_at.getHours() == time){
                time += 1;
                break;
            }
        }

        // add start work class
        if (start_at.getMinutes() == 30) {
            $('.day'+column+'-'+time).append('<div class="half"></div>')
            $('.day'+column+'-'+time).append('<div class="work half"></div>')
        } else {
            $('.day'+column+'-'+time).append('<div class="work"></div>')
        }
        $('.day'+column+'-'+time+'>.work').css('background-color', shift.color)

        // if 30min work do not add work time
        if (!(finish_at.getHours() == start_at.getHours())) {
            $('.day'+column+'-'+time+'>.work').append(
                '<p>'+shift.work_location_object+'</p>' +
                time_to_string(start_at) + ' - ' + time_to_string(finish_at)
            )
        }

        // adding work class until find finish time
        console.log(time)
        while (true) {
            if (finish_at.getHours() == time) {
                if (finish_at.getMinutes() == 30) {
                    time += 1;
                    $('.day'+column+'-'+time).append('<div class="work half"></div>')
                    $('.day'+column+'-'+time+'>.work').css('background-color', shift.color)
                }
                break;
            } 

            time += 1;
            if (time > 24) {
                time = 1;
                column += 1;
                if (column > 7) {
                    break;
                }
            }

            $('.day'+column+'-'+time).append('<div class="work"></div>')
            $('.day'+column+'-'+time+'>.work').css('background-color', shift.color) 
        }

        // add break time
        shift.breaks.forEach(break_time => {
            break_time = new Date(break_time.start_at);
            
            // if break time is not in this week
            if (break_time > final_day) {
                return;
            }

            td_path = '.day'+(break_time.getDay()+1)+'-'+(break_time.getHours()+1+'>.work')
            if (break_time.getMinutes() == 30) {
                $(td_path).append('<div class="half"></div>')
            }
            $(td_path).append('<div class="break"></div>')
        });
    });
});
