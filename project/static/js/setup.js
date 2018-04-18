$(document).ready( function() {
	var numcurrentgames = clocks.length;
	console.log(numcurrentgames);
	if (numcurrentgames == 0) {
		$("#current-games").append($("<p>").text("There are no games going on right now"));
	} else {
		var i;
		for (i = 0; i < numcurrentgames; i++) {
			$("#current-games").append(
				$("<div>", {class: "game"}).append(
					$("<table>").append(
						$("<tr>").append(
							$("<th>").text("Away"),
							$("<th>").text("Home")
						),
						$("<tr>").append(
							$("<td>", {class: "team name"}).text(awayTeams[i]),
							$("<td>", {class: "team name"}).text(homeTeams[i])
						),
						$("<tr>").append(
							$("<td>", {class: "team score"}).text(awayScores[i]),
							$("<td>", {class: "team score"}).text(homeScores[i])
						)
					)
				)
			);
		}
	}
});