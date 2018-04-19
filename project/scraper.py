from lxml import html
import requests, time

def clean_data(raw_list, destination_list):
	for element in raw_list :
		element = element.replace('\n', '')
		element = element.replace('\x95', '')
		element = element.strip()
		destination_list.append(element)

	return destination_list

def time_to_seconds(clocks):
	seconds = []
	for clock in clocks:
		time_s = clock.split('|')
		period = int(time_s[0][0])
		minutes = time_s[1].strip()
		if minutes == '00.0':
			minutes = '0:0'
		elif '.' in minutes:
			minutes = '0:'+minutes.split('.')[0]
		timeremaining = time.strptime(minutes, '%M:%S')
		secondsremaining = ((timeremaining.tm_min + ((4 - period) * 12)) * 60) + timeremaining.tm_sec
		seconds.append(secondsremaining)
	return seconds
		
def scrape(url='https://www.si.com/nba/scoreboard', away=None, home=None):
	tree = html.fromstring(requests.get(url).text)
	# initializing variables
	awayTeamsCityProcessed = []
	awayTeamsRecordProcessed = []

	homeTeamsCityProcessed = []
	homeTeamsRecordProcessed = []

	gameStatus = []
	awayScores = []
	homeScores = []

	# scraping city, team name, and team record data
	awayTeamsCityRaw = tree.xpath('//div[@class="teams"]/div[1]/div[2]/div[1]/a/text()')
	awayTeamsName = tree.xpath('//div[@class="teams"]/div[1]/div[2]/a[2]/span/text()')
	awayTeamsRecordRaw = tree.xpath('//div[@class="teams"]/div[1]/div[2]/span/text()')

	homeTeamsCityRaw = tree.xpath('//div[@class="teams"]/div[3]/div[2]/div[1]/a/text()')
	homeTeamsName = tree.xpath('//div[@class="teams"]/div[3]/div[2]/a[2]/span/text()')
	homeTeamsRecordRaw = tree.xpath('//div[@class="teams"]/div[3]/div[2]/span/text()')

	# cleaning up city and record data
	awayTeamsCityProcessed = clean_data(awayTeamsCityRaw, awayTeamsCityProcessed)
	homeTeamsCityProcessed = clean_data(homeTeamsCityRaw, homeTeamsCityProcessed)
	awayTeamsRecordProcessed = clean_data(awayTeamsRecordRaw, awayTeamsRecordProcessed)
	homeTeamsRecordProcessed = clean_data(homeTeamsRecordRaw, homeTeamsRecordProcessed)


	# games in progress
	if tree.xpath('//span[@class="status-active uppercase"]/text()'):
		
		clocks = tree.xpath('//span[@class="status-active uppercase"]/text()')
		gameStatus = clean_data(clocks, gameStatus)
		
		awayScoresRaw = tree.xpath("//span[@class='status-active uppercase']/../../../div[2]/div/div[1]/div/div[1]/div[3]/div/text()")
		awayScores = clean_data(awayScoresRaw, awayScores)
		homeScoresRaw = tree.xpath("//span[@class='status-active uppercase']/../../../div[2]/div/div[1]/div/div[3]/div[3]/div/text()")
		homeScores = clean_data(homeScoresRaw, homeScores)

	gameStatus = list(filter(None, gameStatus))		# remove empty strings from list
	if home and away:
		if away in awayTeamsCityProcessed:
			i = awayTeamsCityProcessed.index(away)
			return {'clock': gameStatus[i], 'awayTeams': awayTeamsCityProcessed[i], 'awayScores': awayScores[i], 'homeTeams': homeTeamsCityProcessed[i], 'homeScores': homeScores[i]}
		
	return {'clock': gameStatus, 'awayTeams': awayTeamsCityProcessed, 'awayScores': awayScores, 'homeTeams': homeTeamsCityProcessed, 'homeScores': homeScores, 'games':len(gameStatus)}#time_to_seconds(gameStatus)
if __name__ == '__main__':
	scrape()