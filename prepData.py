#first, run dataAggregatorScript.scpt (AppleScript for mac OS)– this script will aggregate the 5-min level data up to the 1hr level.
#to make the dataset more manageable, the jq selection in the script only pulls out tweets from accounts with 1K+ followers.
#Naming convention: the first hour of January 6th is saved as 01-06-00.txt 
#UTC time conversion: to get the 24 hours of January 6th, we want files saved as 06-04 to 07-04.
#this python program processes the data saved out by the script and converts it to the formats that various visualizations need to run.

import random
import collections
import nltk
from nltk.corpus import stopwords

#CONSTANTS
findThisManyTopWords = 10
findThisManyTopAccounts = 5

for theDay in range(6,8):
    for theHour in range(0,24):
        if theDay == 7 and theHour > 4: 
            break
        print("January ", theDay, " | hour " , theHour)
        if theHour<10:
            theHourPrependZero = "0" + str(theHour)
        else:
            theHourPrependZero = theHour
        #read in the filename that was saved out by the aggregator script
        f = open(f"./sampled/01-0{theDay}-{theHourPrependZero}.txt", "r")

        array = []

        #remove whitespace
        for item in f:
            array.append(item.replace("\n", "").replace('"', "").replace("''", "").replace(",", ""))
            
        f.close()

        #the unprocessed array breaks up mentions and other array fields across multiple entries– this step combines them into a single subarray
        formatted = []
        i = 0

        while i < len(array):
            if array[i] == "[":
                formatted.append([])
                i+=1
                while array[i]!= "]":
                    formatted[-1].append(array[i])
                    i+=1
            elif array[i]!="]":
                formatted.append(array[i])
                i+=1
            else:
                i+=1     

        #each tweet object is now a subarray of length 7.
        #this step creates an array and adds each tweet to it as an object with named fields
        splitLength = 7
        i = 0
        processed = []
        while i+6 < len(formatted):
            processed.append({})
            processed[-1]['user'] = formatted[i]
            processed[-1]['bio'] = formatted[i+1]
            processed[-1]['followers_count'] = formatted[i+2]
            processed[-1]['verb'] = formatted[i+3]
            processed[-1]['body'] = formatted[i+4]
            processed[-1]['body_tokenized'] = formatted[i+5]
            processed[-1]['mentions'] = formatted[i+6]
            i+=7
            
        #remove whitespace from mentions and tokenized body
        for i in range(0, len(processed)):
            if processed[i]['mentions'] != "[]":
                for j in range(0,len(processed[i]['mentions'])):
                    processed[i]['mentions'][j] = processed[i]['mentions'][j].replace(" ", "")
            for k in range(0,len(processed[i]['body_tokenized'])):
                processed[i]['body_tokenized'][k] = processed[i]['body_tokenized'][k].replace(" ", "")
                

        #compute links for network stucture.
        #two nodes (accounts) are linked if one has retweeted or mentioned the other.
        #we only need to look at mentions because a RT adds the source account to the mention array.
        links = []
        for tweet in processed:
            if tweet['mentions']!= '[]':
                for mention in tweet['mentions']:
                    links.append({})
                    links[-1]['source'] = mention
                    links[-1]['target'] = tweet["user"]

        #this step calculates the most common accounts– they could have frequently posted, been mentioned or retweeted in the sample dataset
        temp = []
        for item in links:
            #we restructure at this stage to get an array of the type that can be fed into the Counter object to find frequency
            temp.append(item['target'])
            temp.append(item['source'])
            
        includeTheseAccounts = []
        for i in range(0, findThisManyTopAccounts):
            includeTheseAccounts.append(collections.Counter(temp).most_common(findThisManyTopAccounts)[i][0])
        #includeTheseAccounts is now an array of the N=5 top accounts
            
        #this step strips links to just the ones whose source or target nodes are in the N=5 top accounts
        prunedLinks = []
        for tweet in processed:
            for mention in tweet['mentions']:
                if (tweet['user'] in includeTheseAccounts) or (mention in includeTheseAccounts):
                    prunedLinks.append({})
                    prunedLinks[-1]['source'] = tweet['user']
                    prunedLinks[-1]['target'] = mention

        #pull out tweet bodies involving the top accounts
        tweetbodies = []
        tokenizedTweets = []

        for tweet in processed:
            for mention in tweet['mentions']:
                if (tweet['user'] in includeTheseAccounts) or (mention in includeTheseAccounts):
                    for word in tweet['body_tokenized']:
                        if word.isalpha() and len(word) > 0 and word[0]!= '@' and word != 'rt':
                            tokenizedTweets.append(word)
                    if (len(tweetbodies) == 0)or (random.random() < 0.1): 
                        #only append with 10% chance to keep file size manageable, but include at least 1 tweet
                        tweetbodies.append(tweet)

        #this step removes words that are high in frequency/low in meaning for top word analysis
        stopWords = set(stopwords.words('english'))
        filteredTokenizedTweets = [w for w in tokenizedTweets if not w in stopWords] 

        #use another Counter to find the top words
        topWords = []
        for i in range(0, findThisManyTopWords):
            topWords.append(collections.Counter(filteredTokenizedTweets).most_common(findThisManyTopWords)[i][0])
        
        #pull nodes out of links to make completely sure there are no disconnected nodes
        tempNodeArray = []

        for item in prunedLinks:
            tempNodeArray.append(item['source'])
            tempNodeArray.append(item['target'])

        #remove any duplicate nodes
        nodeset = set(tempNodeArray)
        tempNodeArray = []
        for id in nodeset:
            tempNodeArray.append(id)


        #build the very specific node data structure that the ForceGraph object wants to receive
        nodes = []
        for i in range(0, len(tempNodeArray)):
            nodes.append({})
            nodes[-1]['id'] = tempNodeArray[i]
            if nodes[-1]['id'] in includeTheseAccounts:
                nodes[-1]['isTopAccount'] = 'Yes'
            else:
                nodes[-1]['isTopAccount'] = 'No'


        #dataset starts from hour 0 on 1/5/2021, so to start on 1/6/2021 we want 24 hours later, plus UTC time zone conversion = hour 28
        #We want hours 28-52 to keep just Jan 6th data
        saveForceData = open("./src/data/forceData.json","a") 
        saveAsHourNumber = (24*(theDay-5))+theHour
        print(f"saving as {saveAsHourNumber}-force")
        #save node/link data structure as .json in my React app directory for later use in force graph network visualization
        saveForceData.write(f",'{saveAsHourNumber}-force':")
        saveForceData.write("{'nodes': [")
        for k in range(0, len(nodes)):
                if k == 0:
                    saveForceData.write(f"{nodes[k]}")
                else:
                    saveForceData.write(f",{nodes[k]}")
        saveForceData.write("], 'links': [")
        for i in range(0, len(prunedLinks)):
            if i == 0:
                    saveForceData.write(f"{prunedLinks[i]}")
            else:
                saveForceData.write(f",{prunedLinks[i]}")
        saveForceData.write("]}")

        #save out the subset of tweets for use in the randomized tweet website feature
        saveTweetData = open("./src/data/tweetBody.json","a")
        print(f"saving as {saveAsHourNumber}-tweets")
        saveTweetData.write(f",'{saveAsHourNumber}-tweets': [")
        for j in range(0, len(tweetbodies)):
            if j == 0:
                saveTweetData.write(f"{tweetbodies[j]}")
            else:
                saveTweetData.write(f",{tweetbodies[j]}")
        saveTweetData.write("]")

        #save out top accounts data for use in top account hour-by-hour analysis
        saveTopAccountsData= open("./src/data/topAccounts.json","a")
        print(f"saving as {saveAsHourNumber}-topAccounts")
        saveTopAccountsData.write(f",'{saveAsHourNumber}-topAccounts': [")
        for j in range(0, len(includeTheseAccounts)):
            if j == 0:
                saveTopAccountsData.write(f"'{includeTheseAccounts[j]}'")
            else:
                saveTopAccountsData.write(f",'{includeTheseAccounts[j]}'")
        saveTopAccountsData.write("]")

        #save out top words for use in top word hour-by-hour analysis
        saveTopWordsData= open("./src/data/topWords.json","a")
        print(f"saving as {saveAsHourNumber}-topWords")
        print("=====================================")
        saveTopWordsData.write(f",'{saveAsHourNumber}-topWords': [")
        for j in range(0, len(topWords)):
            if j == 0:
                saveTopWordsData.write(f"'{topWords[j]}'")
            else:
                saveTopWordsData.write(f",'{topWords[j]}'")
        saveTopWordsData.write("]")


saveTopWordsData.write("}")  
saveTopAccountsData.write("}")  
saveTweetData.write("}")  
saveForceData.write("}")

#all data is now cleaned/processed/saved in the src/data directory of my React app, ready to use!:)