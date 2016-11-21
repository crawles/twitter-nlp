/**
 * Created by crawles on 9/23/16.
 */

var d = new Date();
var startTime = d.getTime();

var curData;
var tweetRate = 0;
var msg = {tweetRate:0, avgPolarity: 0};
sse1 = new EventSource('/tweet_rate');
sse1.onmessage = function(message) {
    msg = JSON.parse(message.data)
};

function draw(divId,dataMetric,margin,width,height) {
    var nterpType = d3.curveBasis;
    var yLabel = "average sentiment";
    var lineName = "sentiment-line";
    var yLabelPos = -11;
    var idName = "id1";
    if (dataMetric == "tweetRate") {
        interpType = d3.curveMonotoneX;
        yLabel = "tweets/second";
        lineName = "tweet-rate-line";
        yLabelPos = -80;
        idName = "id"
    }
    var n = 40,
        data = Array.apply(null, Array(n)).map(Number.prototype.valueOf, 0);
    var svg = d3.select(divId)
            .append("svg")
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0 " + width + " " + height),
        // margin = margin,
        width = width - margin.left - margin.right,
        height = height - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    g.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "end")
        .attr("x", (width) / 2)
        .attr("y", height + 30)
        .text("time");

    g.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "end")
        .attr("x", yLabelPos)
        .attr("y", -40)
        .attr("transform", "rotate(-90)")
        .text(yLabel);

    var x = d3.scaleLinear()
        .domain([1, n - 2])
        .range([0, width]);
    var y = d3.scaleLinear()
        .domain([0, Math.max(1, d3.max(data))])
        .range([height, 0]);

    var line = d3.line()
        .curve(interpType)
        .x(function (d, i) {
            return x(i);
        })
        .y(function (d, i) {
            return y(d);
        });

    g.append("defs").append("clipPath")
        .attr(idName, "clip")
        .append("rect")
        .attr("width", width)
        .attr("height", height);
    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + y(0) + ")")
        .call(d3.axisBottom(x));
    g.append("g")
        .attr("class", "yaxis")
        .call(d3.axisLeft(y));

    g.append("g")
        .attr("clip-path", "url(#clip)")
        .append("path")
        .datum(data)
        .attr("class", lineName)
        .transition()
        .duration(1000)
        .ease(d3.easeLinear)
        .on("start", tick);

    var d;

    function tick() {
        // Push a new data point onto the back.
        data.push(parseFloat(msg[dataMetric]));
        y.domain([0, Math.max(1, d3.max(data))]).range([height, 0]);
        g.select(".yaxis").call(d3.axisLeft(y));

        // Redraw the line.
        d3.select(this)
            .attr("d", line)
            .attr("transform", null);

        if (dataMetric == "tweetRate") {
            curData = data
        }
        // Slide it to the left.
        d3.active(this)
            .attr("transform", "translate(" + x(0) + ",0)")
            .transition()
            .on("start", tick);
        // Pop the old data point off the front.
        data.shift();
    }
};


draw("div#container","tweetRate",{top: 15, right: 20, bottom: 30, left: 50},800,260);
draw("div#container1","avgPolarity",{top: 10, right: 20, bottom: 35, left: 50},800,155);

function numberWithCommas(x) {
    //http://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function updateStats() {
    // tweets per minute
    var numTweets = curData.reduce(function(a, b) { return a + b; }, 0);
    var d = new Date();
    var timeElapsed = (d.getTime() - startTime)/1000;
    var interval = Math.min(40, timeElapsed)
    var tweetsPerMin = Math.ceil(60*(numTweets/interval));
    $("#tweetsPerMinute").text(numberWithCommas(tweetsPerMin));

    // total tweets
    $.get( "http://compute-tweet-stats.cfapps.pez.pivotal.io/num_tweets", function( data ) {
         $("#totalTweets").text(numberWithCommas(data));
    });
}

setInterval(updateStats, 1000);