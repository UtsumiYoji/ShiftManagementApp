function formatDate(date) {
    var year = date.getFullYear();
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var day = String(date.getDate()).padStart(2, '0');
    var hours = String(date.getHours()).padStart(2, '0');
    var minutes = String(date.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

// Start making a shift
$(document).on('click', '.make-calendar', function() {
    // before adding, store original
    clone = $(this).closest('.shift-calendar').clone();
    
    // make elements
    var title_elm = $(this).closest('.shift-calendar')
    var start_datetime = new Date(title_elm.find('.start_datetime').val());
    var end_datetime = new Date(title_elm.find('.end_datetime').val());

    // if its empty, return
    if (start_datetime == 'Invalid Date' || end_datetime == 'Invalid Date') {
        alert('Please set start and end time.');
        return;
    }

    // Rewrite date
    start_datetime.setMinutes(0);
    end_datetime.setMinutes(0);
    title_elm.find('.start_datetime').val(formatDate(start_datetime)).datetimepicker('update');
    title_elm.find('.end_datetime').val(formatDate(end_datetime)).datetimepicker('update');

    // calculate diff
    diff = (end_datetime - start_datetime) / (1000 * 60);
    if (diff < 60){
        alert('Please set more than 60 minutes. (end time should be after start time)');
        return;
    } else {
        count = diff / 30 + 1;
    }
    
    datetimes = [];
    for (i = 0; i < count/2; i++) {
        datetimes.push(new Date(start_datetime.getTime() + (i * 60 * 60 * 1000)));
    }
    
    // create times
    var element = '<table class="datetimes">\n<tbody>\n<tr>';
    datetimes.forEach(datetime => {
        element += '<td>' + datetime.getHours() + ':00</td>';
    });
    element += '\n</tr">\n</tbody>\n</table>';

    // create calendar
    element += '<table class="shift overflow-x-scroll">\n<tbody>\n<tr>';
    element += '\n<td class="most-left-cell"><select class="user">\n<option></option>';
    users.forEach(user => {
        element += '\n<option value="' + user.id + '">' + user.first_name + '</option>';
    });
    element += '\n<option value="-1" style="color:red;">Delete</option>';
    element += '\n</select></td>';
    element += '\n<td class="total-hour">0:00</td>'

    count -= 1;
    for (var i = 0; i < count; i++) {
        datetime = new Date(start_datetime.getTime() + (i * 60 * 30 * 1000))
        element += '\n<td class="shift_cell" value="'+datetime+'" work_location_id=""></td>';
    }
    element += '\n</tr>\n</tbody>\n</table>';

    // change button to delete, add calendar
    title_elm.find('.start_datetime').prop('disabled', true);
    title_elm.find('.end_datetime').prop('disabled', true);
    $(this).closest('.shift-calendar').find('.make-calendar').toggle();
    $(this).closest('.shift-calendar').find('.delete-calendar').toggle();
    $(this).closest('.shift-calendar').find('.calendar-container').append(element);

    // add new blank shift-calendar
    start_datetime.setDate(start_datetime.getDate() + 1);
    end_datetime.setDate(end_datetime.getDate() + 1);
    clone.find('.datetimepicker').datetimepicker()
    clone.find('.start_datetime').val(formatDate(start_datetime)).datetimepicker('update');
    clone.find('.end_datetime').val(formatDate(end_datetime)).datetimepicker('update');
    $(this).closest('.shift-calendar').after(clone);
});

// delete calendar
$(document).on('click', '.delete-calendar', function() {
    if (confirm('Are you sure to delete?')) {
        $(this).closest('.shift-calendar').remove();
    }
});

// store previous value
$(document).on('focus', '.most-left-cell>select', function() {
    previousValue = $(this).val();
});


// adding a row
$(document).on('change', '.most-left-cell>select' , function() {
    // judge user doesn't exit
    var selected_user_id = $(this).val()
    let count = 0;

    if (selected_user_id == '') {
        return
    }

    $(this).closest('tbody').find('.user').each(function() {
        if ($(this).val() == selected_user_id) {
            count += 1;
        }
    });
    if (count > 1) {
        alert('User already exists.');
        $(this).val('');
        return;
    }

    // judge if it is delete
    if (selected_user_id == -1) {
        // cannot delete last row
        if ($(this).closest('tr').is(':last-child')) {
            $(this).val('');
            return;
        }

        if (!confirm('Are you sure to this row delete?')) {
            $(this).val(previousValue);
        } else {
            $(this).closest('tr').remove();
        }
        return;
    }
    
    // judge if it is the last row
    if (!($(this).closest('tr').is(':last-child'))) {
        return;
    }

    var row = this.closest('tr');
    var clone = row.cloneNode(true);
    row.parentNode.appendChild(clone);

    // clear row
    $(clone).find('td').css('background-color', '');
    $(clone).find('td').attr('work_location_id', '');
    $(clone).find('total-hour').text('0:00');
});

function date_to_string(date) {
    return (date.getHours()+':'+date.getMinutes().toString().padStart(2, '0'))
}

function paint_out_cell(work_location_id=null) {
    // Retain datetimes
    var card = $('.shift_detail').first()
    var start_at = card.find('.start-at').attr('value');
    var finish_at = card.find('.finish-at').attr('value');

    // Retain color
    var color = card.find('option:selected').attr('color');

    // Paint out cells
    var tr = card.closest('tr');
    if (finish_at == "") {
        tr.find('td[value="'+start_at+'"]').css('background-color', color)
        if (work_location_id != null) {
            tr.find('td[value="'+start_at+'"]').attr('work_location_id', work_location_id);
        }
        return
    }

    var start_cell = tr.find('td[value="'+start_at+'"]');
    var finish_cell = tr.find('td[value="'+finish_at+'"]');
    start_cell.css('background-color', color);
    
    // do not paint out break time
    start_cell.nextUntil(finish_cell).filter(
        function() {
            return $(this).css('background-color') != 'rgb(255, 255, 0)';
        }
    ).css('background-color', color);

    // Save work location id
    if (work_location_id != null) {
        start_cell.attr('work_location_id', work_location_id);
        start_cell.nextUntil(finish_cell).attr('work_location_id', work_location_id);
    }
}

function calculate_total_hour(tr_elm) {
    var total_minites = 0;
    tr_elm.find('td').each(function() {
        var bg_color = $(this).css('background-color');
        
        if ((bg_color != 'rgba(0, 0, 0, 0)') && (bg_color != 'rgb(255, 255, 0)')) {
            total_minites += 30;
        }
    });
    tr_elm.find('.total-hour').text(
        Math.floor(total_minites/60) + ':' + (total_minites % 60).toString().padStart(2, '0'));
}

ADDING_BREAK_TEXT = 'Click calendar to add break or here to cancel';
WAITING_BREAK_TEXT = 'Add break time';

// clicking a cell
$(document).on('click', 'td.shift_cell', function() {
    // check if it alreday has a detail card
    if ($('.shift_detail').length == 1) {
        // If clicked row already has work_location_id(color)
        if ($(this).attr('work_location_id')) {
            // declare variables
            var work_location_id = $(this).attr('work_location_id');

            // find start cell
            start_cell = $(this)
            temp = start_cell.prevUntil('.shift_cell[work_location_id!="'+work_location_id+'"]')
            if (!temp.length == 0) {
                if (temp.last().hasClass('most-left-cell')) {
                    start_cell = temp.last().next().next();
                } else {
                    start_cell = temp.last();
                }
            }

            // find finish cell
            finish_cell = $(this)
            temp = finish_cell.nextUntil('.shift_cell[work_location_id!="'+work_location_id+'"]')
            if (!temp.length == 0) {
                finish_cell = temp.last();
            }

            // create time str
            var start_at = new Date(start_cell.attr('value'));
            var finish_at = new Date(finish_cell.attr('value'))
            finish_at.setMinutes(finish_at.getMinutes() + 30);

            // add card
            elm = $(".shift_detail").clone(true).appendTo(this);
            elm.find('.start-at').text(date_to_string(start_at));
            elm.find('.finish-at').text(date_to_string(finish_at));
            elm.find('.start-at').attr('value', start_at);
            elm.find('.finish-at').attr('value', finish_at);
            elm.find('h5').append('form ' + date_to_string(start_at) + ' to ' + date_to_string(finish_at));
            elm.find('select').val(work_location_id);
            elm.find('.work-location-color').css('color', elm.find('option:selected').attr('color'));
        } else {
            // show new detail card
            var datetime = new Date($(this).attr('value'));

            elm = $(".shift_detail").clone(true).appendTo(this);
            $(this).find('.start-at').attr('value', datetime);

            datetime = date_to_string(datetime);
            $(this).find('.start-at').text(datetime);
            elm.find('h5').append(datetime);
            
            work_location_id = elm.find('.work-location').find('option:selected').val();
            paint_out_cell(work_location_id);
            calculate_total_hour($(this).closest('tr'));
            
            // disable select and break button
            elm.find('.break').prop('disabled', true);
            $(".most-left-cell>select").prop('disabled', true);
        }
        // if card located right side of screen, add right:0px
        if (elm.offset().left > $(window).width() / 2) {
            elm.css('right', '0px');
        }

        return;
    }

    // check clicked cell is same row with the detail card
    card = $('.shift_detail').first();
    var clicked_row = $(this).closest('tr');
    var detail_row = card.closest('tr');
    if (!(clicked_row[0] == detail_row[0])) {
        return;
    }

    // If user is making break time
    if (card.find('.break').text() == ADDING_BREAK_TEXT) {
        // Make sure user clicling cell which has work_location_id
        if ($(this).attr('work_location_id')) {
            // If cell is already painted out, it will become normal
            if ($(this).css('background-color') == 'rgb(255, 255, 0)') {
                var color = card.find('option:selected').attr('color');
                $(this).css('background-color', color);
            } else {
                // Paint out a cell
                $(this).css('background-color', 'rgb(255, 255, 0)');
            }
            calculate_total_hour($(this).closest('tr'));
        return;
        }
    }

    // If card alreday has finish time, it cannot be fixed
    if (card.find('.finish-at').attr('value') != "") {
        return;
    }

    // Retain datetimes
    var finish_at = new Date($(this).attr('value'));
    var start_at = new Date(card.closest('td').attr('value'));
    
    // If user clicked cell before start time cell
    if (finish_at < start_at) {
        var tmp = finish_at;
        finish_at = start_at;
        start_at = tmp;
        card.find('.start-at').text(date_to_string(start_at));
        card.find('.start-at').attr('value', start_at);
    }
    finish_at.setMinutes(finish_at.getMinutes() + 30);
    card.find('h5').text("You're selecting from ");
    card.find('h5').append(card.find('.start-at').text() + ' to ' + date_to_string(finish_at));
    card.find('.finish-at').text(date_to_string(finish_at));
    card.find('.finish-at').attr('value', finish_at);
    var work_location_id = card.find('.work-location').find('option:selected').val();
    paint_out_cell(work_location_id);
    calculate_total_hour($(this).closest('tr'));
    elm.find('.break').prop('disabled', false);
});

// clicking a detial card
$(document).on('click', '.shift_detail', function(event) {
    event.stopPropagation();
});

// selecting a work location
$(document).on('change', '.work-location', function() {
    var color = $(this).find('option:selected').attr('color');
    var work_location_id = $(this).find('option:selected').val();
    $(this).closest('.shift_detail').find('.work-location-color').css('color',color);
    paint_out_cell(work_location_id);    
});

// clicking break
$(document).on('click', '.break', function() {
    if ($(this).text() == ADDING_BREAK_TEXT) {
        $(this).text(WAITING_BREAK_TEXT);
    } else {
        $(this).text(ADDING_BREAK_TEXT);
    }
});

// clicking save
$(document).on('click', '.save', function() {
    $(this).closest('.shift_detail').remove();

    // enable select
    $(".most-left-cell>select").prop('disabled', false);
});

// clicking delete
$(document).on('click', '.delete', function() {
    // Retain datetimes
    var card = $('.shift_detail').first()
    var start_at = card.find('.start-at').attr('value');
    var finish_at = card.find('.finish-at').attr('value');

    // Paint off cells
    var tr = card.closest('tr');
    var start_cell = tr.find('td[value="'+start_at+'"]').prev();
    var finish_cell = tr.find('td[value="'+finish_at+'"]');

    // delete color
    start_cell.nextUntil(finish_cell).css('background-color', '');
    start_cell.nextUntil(finish_cell).attr('work_location_id', '');

    // delete card
    calculate_total_hour($(this).closest('tr'));
    $(this).closest('.shift_detail').remove();
    $(".most-left-cell>select").prop('disabled', false);
});

// submit form
$(document).on('click', '.submit', function() {
    var data = [];

    $('.shift tr').each(function() {
        // check if it has user
        if ($(this).find('.user').val() == '') {
            return true;
        }

        // get user id
        var user_id = $(this).find('.user').val();

        // get td elements which has work_location_id
        cells = $(this).find('td[work_location_id!=""]').slice(2);
        work_location_id = cells.eq(0).attr('work_location_id');
        start_at = cells.eq(0).attr('value');
        var breaks = [];

        if (cells.eq(0).css('background-color') == 'rgb(255, 255, 0)') {
            breaks.push(formatDate(new Date(cells.eq(0).attr('value'))));
        }

        for (var i = 1; i < cells.length; i++) {
            cell = cells.eq(i);
            
            // if it is break time
            if (cell.css('background-color') == 'rgb(255, 255, 0)') {
                breaks.push(formatDate(new Date(cell.attr('value'))));
            }

            // it is end of row
            if (i == cells.length - 1) {
                finish_at = new Date(cells.eq(i).attr('value'));
                finish_at.setMinutes(finish_at.getMinutes() + 30);
                data.push({
                    'user_id': user_id,
                    'work_location_id': work_location_id,
                    'start_at': formatDate(new Date(start_at)),
                    'finish_at': formatDate(finish_at),
                    'break_time': breaks
                });
            } else if (cell.attr('work_location_id') != work_location_id) {
                // If work_location_id is changed, push data
                // use current time as a finish time because it has to be added 30 minutes
                finish_at = cell.attr('value')
                data.push({
                    'user_id': user_id,
                    'work_location_id': work_location_id,
                    'start_at': formatDate(new Date(start_at)),
                    'finish_at': formatDate(new Date(finish_at)),
                    'break_time': breaks
                });

                // Go to next work_location_id
                work_location_id = cell.attr('work_location_id');
                start_at = cell.attr('value');
                var breaks = [];
            }
        }
    });

    if (data.length == 0) {
        alert('There is no data to save.');
        return;
    }

    $.ajax({
        url: '/shift/create',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        data: {
            'data': JSON.stringify(data)
        },
        success: function(response) {
            window.location.href = response.url;
        },
        error: function(xhr, status, error) {
            alert('Error');
        }
    });
});
