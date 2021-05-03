import { useState, useEffect } from "react";
import forceData from "./data/forceData.json";
import RandomTweet from "./RandomTweet";
import DisplayTrends from "./DisplayTrends.js";
import ProgressBar from "./ProgressBar.js";
import DateTimeDisplay from "./DateTimeDisplay";
import ForceGraph from "./ForceGraph.js";
import BackArrow from "./imgs/BackArrow.svg";
import ForwardArrow from "./imgs/ForwardArrow.svg";
import BackArrowGray from "./imgs/BackArrowGray.svg";
import ForwardArrowGray from "./imgs/ForwardArrowGray.svg";

const TimeTravel = () => {
  const [count, updateCount] = useState(28);
  const [displayData, updateData] = useState(forceData[`${count}-force`]);

  const handleDataChange = (newData) => {
    updateData(forceData[newData]);
  };

  useEffect(() => {
    handleDataChange(`${count}-force`);
  }, [count]);

  const stepForward = () => {
    if (count < 52) {
      updateCount(count + 1);
    }
  };

  const stepBack = () => {
    if (count > 28) {
      updateCount(count - 1);
    }
  };

  const handleKeyDown = (e) => {
    if (e.code === "ArrowLeft") {
      stepBack();
    }
    if (e.code === "ArrowRight") {
      stepForward();
    }
  };

  useEffect(() => {
    document.title = "Jan. 6, 2021";
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  return (
    <div className="TimeTravel">
      <ProgressBar count={count} />
      <div className="dateTimeButtonContainer">
        <button
          className={"backButton"}
          onClick={() => {
            stepBack();
          }}
        >
          <img
            alt=""
            src={count > 28 ? BackArrow : BackArrowGray}
            style={{ height: 50, width: 50 }}
          ></img>
        </button>
        <DateTimeDisplay count={count} />
        <button
          className={"forwardButton"}
          onClick={() => {
            stepForward();
          }}
        >
          <img
            alt=""
            src={count < 52 ? ForwardArrow : ForwardArrowGray}
            style={{ height: 50, width: 50 }}
          ></img>
        </button>
      </div>
      <ForceGraph displayData={displayData}></ForceGraph>
      <div className="randomTweetContainer">
        {" "}
        <RandomTweet count={count} />
        <RandomTweet count={count} />
        <RandomTweet count={count} />
      </div>
      <div className="trendContainer">
        <DisplayTrends count={count} wordsOrAccounts="Words" />
        <DisplayTrends count={count} wordsOrAccounts="Accounts" />
      </div>
    </div>
  );
};

export default TimeTravel;
