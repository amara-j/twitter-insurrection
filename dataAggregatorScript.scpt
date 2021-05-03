set thePath to "[your path to compressed data archive]"

repeat with theDay from 5 to 7
	repeat with theHour from 0 to 23
		
		if theHour < 10 then
			set theHour to ("0" & theHour) as text
		else
			set theHour to theHour as text
		end if
		
		
		repeat with theMin from 0 to 11
			
			if theMin < 10 then
				set theMin to "0" & (theMin as text)
			else
				set theMin to theMin as text
			end if
			
			set theFile to thePath & ("2021-01-0" & theDay & "/" & theHour & "/" & theMin & ".json.gz")
			
			
			set saveAs to thePath & ("/" & "01-0" & theDay & "-" & theHour)
			
			
			do shell script "zcat < " & theFile & " | /usr/local/bin/jq 'select(.actor.followers_count >1000)| .actor.username, .actor.bio, .actor.followers_count, .verb, .body, .body_tokenized, .mentions' >>" & saveAs & ".txt"
			
		end repeat
	end repeat
end repeat
