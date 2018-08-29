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

            // Sample date: [2018-08-28 04:29:10 +0200]
            if (split[0].length == 27) {
                var isodate = split[0].substring(1, 11) + 'T';
                isodate += split[0].substring(12, 20);
                isodate += split[0].substring(21, 24);
                isodate += ':' + split[0].substring(24, 26);
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

    socket.on('initial-data', (data) => {
        let lines = data.data.split('\n');
        for (var i = 0; i < lines.length; i++) {
            append_line(lines[i]);
        }
    });

    socket.on('new-log-line', (data) => {
        append_line(data.data);
    });

    socket.emit('request-initial-data');
});
