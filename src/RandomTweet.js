import { useState, useEffect } from "react";
import tweetData from "./data/tweetBody.json";
import RefreshLogo from "./imgs/refresh.svg";

function RandomTweet(props) {
  const [currentTweet, randomizeTweet] = useState({
    user: "",
    bio: "",
    followers_count: "",
    verb: "",
    body: "",
    body_tokenized: [],
    mentions: [],
  });

  const [bioIsHidden, updateBioIsHidden] = useState(true);

  const getRandomIndex = (array) => {
    return Math.floor(Math.random() * array.length);
  };

  const generateTweet = () => {
    const tweetsFromThisTimeInterval = tweetData[`${props.count}-tweets`];
    const randomTweetIndex = getRandomIndex(tweetsFromThisTimeInterval);
    randomizeTweet(tweetsFromThisTimeInterval[randomTweetIndex]);
    updateBioIsHidden(true);
    return tweetsFromThisTimeInterval[randomTweetIndex];
  };

  const hideShowBio = () => {
    updateBioIsHidden(!bioIsHidden);
  };

  useEffect(() => generateTweet(), [props.count]);

  return (
    <div className="tweet">
      <div
        className="randomizeTweetButton"
        onClick={() => {
          generateTweet();
        }}
      >
        Randomize Tweet
        <img
          src={RefreshLogo}
          style={{ height: 16, width: 16, margin: "0px 0px 0px 10px" }}
        />
      </div>
      <div className="randomTweetUser">
        <div className="userName">
          @{currentTweet.user + "         "}
          <button
            className="hideShowBio"
            onClick={() => {
              hideShowBio();
            }}
          >
            {bioIsHidden ? "Show bio" : "Hide bio"}
          </button>{" "}
        </div>
        <div className="randomTweetBio">
          {" "}
          {bioIsHidden
            ? ""
            : currentTweet.bio === "null"
            ? ""
            : currentTweet.bio.toString()}
        </div>
        <div className="mentions">
          mentioned @
          {currentTweet.mentions.length > 4
            ? currentTweet.mentions.slice(0, 4).join(", @") + " and others"
            : currentTweet.mentions.join(", @")}
        </div>
      </div>
      <div className="randomTweetBody">
        {" "}
        {currentTweet.verb === "share"
          ? currentTweet.body.toString()
          : currentTweet.body
              .split(" ")
              .slice(currentTweet.mentions.length, currentTweet.body.length)
              .join(" ")}
      </div>
    </div>
  );
}

export default RandomTweet;
