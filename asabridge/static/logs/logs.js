'use strict';

function append_line(line) {
    let new_log = line + '\n';
    let log = document.getElementById('log-text');
    var full_log = log.textContent;
    for (var i = 0; i < log.childNodes; ++i) {
        full_log += log.childNodes[i].textContent;
    }
    if (full_log.indexOf(new_log) === -1) {
        // Is a new line.

        let bracket_regex = /\s*(\[[a-zA-Z0-9]*\])\s*/g;
        var split = new_log.split(bracket_regex).filter(Boolean);

        if (split.length >= 4) {
            // might be gunicorn logger message.

            // Sample date: [2018-08-30T03:14:42.395+02:00]
            if (split[0].length == 31) {
                var isodate = split[0].substring(1, 30);
                var timestamp = Date.parse(isodate);
                if (isNaN(timestamp) === false) {
                    var timestamp_span = document.createElement('span');
                    timestamp_span.textContent = split[0] + ' ';
                    timestamp_span.style.color = '#8e908c';
                    var pid_span = document.createElement('span');
                    pid_span.textContent = split[1] + ' ';
                    pid_span.style.color = '#8e908c';
                    var log_level_span = document.createElement('span');
                    log_level_span.textContent = split[2] + ' ';
                    if (split[2] === '[DEBUG]') {
                        log_level_span.style.color = '#4271ae';
                    }
                    else if (split[2] === '[INFO]') {
                        log_level_span.style.color = '#718c00';
                    }
                    else if (split[2] === '[WARNING]') {
                        log_level_span.style.color = '#eab700';
                    }
                    else if (split[2] === '[ERROR]') {
                        log_level_span.style.color = '#c82829';
                    }
                    else if (split[2] === '[CRITICAL]') {
                        log_level_span.style.color = '#c82829';
                    }
                    let drop_length = (timestamp_span.textContent + pid_span.textContent + log_level_span.textContent).length;
                    var msg_span = document.createElement('span');
                    msg_span.textContent = new_log.substring(drop_length);
                    log.appendChild(timestamp_span);
                    log.appendChild(pid_span);
                    log.appendChild(log_level_span);
                    log.appendChild(msg_span);
                } else {
                    var msg_span = document.createElement('span');
                    msg_span.textContent = new_log;
                    log.appendChild(msg_span);
                }
            } else {
                var msg_span = document.createElement('span');
                msg_span.textContent = new_log;
                log.appendChild(msg_span);
            }
        } else {
            var msg_span = document.createElement('span');
            msg_span.textContent = new_log;
            log.appendChild(msg_span);
        }
    }
    $('html, body').scrollTop($(document).height());
};

$(document).ready(function() {
    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + "/logstream");
    var has_initial = false;
    var lines_cache_parsed = false;
    var received_before_initial = []

    socket.on('initial-data', (data) => {
        has_initial = true;
        let lines = data.data.split('\n');
        for (var i = 0; i < lines.length; i++) {
            append_line(lines[i]);
        }
        for (var i = 0; i < received_before_initial.length; i++) {
            append_line(received_before_initial[i]);
        }
    });

    socket.on('new-log-line', (data) => {
        if (!lines_cache_parsed) {
            if (!has_initial) {
                for (var i = 0; i < data.data.length; i++) {
                    received_before_initial.push(data.data[i]);
                }
            } else {
                for (var i = 0; i < data.data.length; i++) {
                    append_line(data.data[i]);
                }
            }
            lines_cache_parsed = true;
        } else {
            if (!has_initial) {
                received_before_initial.push(data.data[data.data.length - 1]);
            } else {
                append_line(data.data[data.data.length - 1]);
            }
        }
    });

    socket.emit('request-initial-data');
});
