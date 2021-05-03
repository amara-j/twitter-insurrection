import { useState, useEffect } from "react";
import topWordData from "./data/topWords.json";
import topAccountData from "./data/topAccounts.json";

function DisplayTrends(props) {
  const [currentTrending, updateTrending] = useState([]);

  let trendData = [];
  let maybePrependAtSymbol = "";

  if (props.wordsOrAccounts === "Words") {
    trendData = topWordData;
  } else if (props.wordsOrAccounts === "Accounts") {
    trendData = topAccountData;
    maybePrependAtSymbol = "@";
  }

  const getTrending = () => {
    const trendingArray = trendData[
      `${props.count}-top${props.wordsOrAccounts}`
    ].slice(0, 5);
    updateTrending(trendingArray);
    return trendingArray;
  };

  useEffect(() => getTrending(), [props.count]);

  return (
    <div className="trend">
      <div className="trendTitle">{`Top ${props.wordsOrAccounts}`}</div>
      <ul className="trendList">
        {currentTrending.map((value, index) => {
          return <li key={index}>{maybePrependAtSymbol + value}</li>;
        })}
      </ul>
    </div>
  );
}

export default DisplayTrends;
