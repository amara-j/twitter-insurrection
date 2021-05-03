const ProgressBar = (props) => {
  const containerStyles = {
    height: 5,
    width: "97%",
    backgroundColor: "lightgray",
    borderRadius: 50,
    margin: 20,
  };

  const filledStyles = {
    height: "100%",
    width: `${(100 * (props.count - 28)) / 24}%`,
    backgroundColor: "#BFD200",
    borderRadius: "inherit",
    textAlign: "right",
    transition: "width 1s ease-in-out",
  };
  return (
    <div className="progressBar" style={containerStyles}>
      <div className="progressBarFilled" style={filledStyles}></div>
    </div>
  );
};

export default ProgressBar;
