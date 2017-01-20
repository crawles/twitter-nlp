/**
 * Created by crawles on 9/25/16.
 */
synTweets = {"tweets": ["\ub2f9\uc5f0\ud788 \uce89\ud14c\uc9c0 \u314b\u314b\u314b https://t.co/bMGPA5hC5J", "Chapman double gives Chelsea victory: Chelsea Ladies beat Notts County Ladies to move within seven points of ... https://t.co/drMbICCi2O", "Squawka: Confirmed: Chelsea announce squad number for Spaniard https://t.co/cVQV4pjqbF #cfc", "Chelsea Houska may have just leaked the gender of her and Cole DeBoer's unborn child https://t.co/WZVwCgkrpx", "RT @DumbPeopleAsf: You a real fan of the Olympics? Then who is this? https://t.co/HilR5YZexc", "RT @Metro_Sport: N\u2019Golo Kante reveals he rejected Manchester United for Chelsea after talks with Jose Mourinho https://t.co/YFLv5b0sNB", "RT @BuzzFeed: This runner stopped in her Olympics semi-final to help her injured competitor finish https://t.co/LEXpWaECDj https://t.co/DTb\u2026", "RT @AngryGoTFan: \"IF TRUMP IS LOSING, THEY'RE GOING TO NEED TO START BUILDING NEW STADIUMS FOR WHEN HE'S WINNING\" - MIKE PENCE https://t.co\u2026", "RT @OSCARanking: Morata back at Real Madrid\nPogba back at Man United\nLuiz back at Chelsea\nGotze back at Dortmund\nHummels back at Bayern\n\nWh\u2026", "RT ChrisMannixYS: .ClaressaShields cruises to an easy win, and USABoxing is now guaranteed three Olympic medals. Been a solid Olympics for \u2026"]}['tweets']

function duplicateTweets(n) {
    // n = 9 : 100 tweets
    // n = 99: 1000 tweets
    var synTweetsN = synTweets;
    for (i = 0; i < n; i++) {
        synTweetsN = synTweetsN.concat(synTweets);
    }
    return synTweetsN;
}

tenTweets = synTweets;
oneHundredTweets  = duplicateTweets(9);
oneThousandTweets = duplicateTweets(99);

function sendTweets(tweets) {
    $.ajax({
        url: sentimentComputeURL + '/polarity_compute',
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({"data":tweets}),
        processData: false,
        success: function( data, textStatus, jQxhr ){
            $('#response pre').html( JSON.stringify( data ) );
        },
        error: function( jqXhr, textStatus, errorThrown ){
            console.log( errorThrown );
        }
    });
};

function sendTen() {
    sendTweets(tenTweets)
    return 1;
};

function sendOneHundred() {
    sendTweets(oneHundredTweets)
    return 1;
};

function sendOneThousand() {
    sendTweets(oneThousandTweets)
    return 1;
};