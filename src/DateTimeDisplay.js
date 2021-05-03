const DateTimeDisplay = (props) => {
  const dateOptions = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
  };

  const date = new Date(2021, 0, 4, 20);
  const timeStepHrs = 1;
  date.setHours(date.getHours() + timeStepHrs * props.count);

  return (
    <div className="dateDiv">
      {date.toLocaleDateString("en-US", dateOptions)}
    </div>
  );
};

export default DateTimeDisplay;
