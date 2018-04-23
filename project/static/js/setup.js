Array.prototype.peek = function () {
	return this[this.length-1];
}

function construct_games(i) {
	return $("<div>", {class: "game"}).append(
				$("<table>").append(
					$("<tr>").append(
						$("<th>").text("Away"),
						$("<th>").text("Home")
					),
					$("<tr>").append(
						$("<td>", {class: "team name"}).text(games[i]["awayTeam"]),
						$("<td>", {class: "team name"}).text(games[i]["homeTeam"])
					),
					$("<tr>").append(
						$("<td>", {class: "team score"}).text(games[i]["awayScore"].peek()),
						$("<td>", {class: "team score"}).text(games[i]["homeScore"].peek())
					)
				)
			);
}

function append_game_history(response) {
	
	for (var i = 0; i < response["games"]; i++) {
		
		for (var k = 0; k < games.length; k++) {
			if (response["homeTeams"][i] == games[k]["homeTeam"]) {
				games[k]["clock"].push(response["clock"][i]);
				games[k]["awayScore"].push(response["awayScores"][i]);
				games[k]["homeScore"].push(response["homeScores"][i]);
				games[k]["homeWinprob"].push(response["probs"][i]);
			}
		}
	}
}

$(document).ready( function() {
	
	if (numcurrentgames == 0) {
		$("#current-games").append($("<p>").text("There are no games going on right now"));
	} else {
		var i;
		for (i = 0; i < numcurrentgames; i++) {
			$("#current-games").append(
				construct_games(i)
			);
		}
	}
	
	setInterval(function() {
		$.ajax({url:"/games", success: function(response) {
			append_game_history(response);
			$("#current-games").empty();
			for (i = 0; i < games.length; i++) {
				$("#current-games").append(
					construct_games(i)
				);
			}
		}});
	}, 15000);
});