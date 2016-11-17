var numMessages;
var messageJSON;

$(document).ready(
    function() {
        sse = new EventSource('/live_tweets');
        sse.onmessage = function(message) {
                if (numMessages > 10) {
                    document.getElementById("output").deleteRow(-1);
                }
                messageJSON = JSON.parse(message.data)
                $('#output').prepend('<tr id="tweet-row"> ' +
                '<td id="tweet-cell" class="col-md-10">&nbsp<div class="verticalLine">'+ urlify(messageJSON.tweet) + '</div></td>' +
                '<td id="sentiment-cell" class="col-md-2">' + polarityToLabel(messageJSON.polarity) + '</td> </tr>');
        }
    }
);

function polarityToLabel(p) {
    if (p >= 0.9) {
        return "<div style=\"color:green\"> pos </div> "
    } else if (p <= 0.1) {
        return "<div style=\"color:red\"> neg </div> "
    }
    return "neu"
}

function urlify(text) {
    // source: http://stackoverflow.com/questions/1500260/detect-urls-in-text-with-javascript
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    })
}

