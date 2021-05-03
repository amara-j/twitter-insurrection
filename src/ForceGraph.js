import { useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";

const Graph = (props) => {
  const getNodeColor = (text) => {
    let color;
    text === "Yes"
      ? (color = "rgba(239,71,111,0.85)")
      : (color = "rgb(255,205,0,0.85)");
    return color;
  };

  const getNodeSize = (text) => {
    let size;
    text === "Yes" ? (size = 5) : (size = 1);
    return size;
  };

  const getLinkColor = () => {
    return "rgb(0,0,0, 0.2)";
  };

  const getNodeLabel = (username) => {
    return `@${username}`;
  };

  const fgRef = useRef();

  return (
    <div className="graph">
      <ForceGraph2D
        ref={fgRef}
        width={650}
        height={650}
        graphData={props.displayData}
        nodeLabel={(node) => getNodeLabel(node.id)}
        nodeColor={(node) => getNodeColor(node.isTopAccount)}
        nodeVal={(node) => getNodeSize(node.isTopAccount)}
        linkOpacity={1}
        linkColor={() => getLinkColor()}
        onEngineTick={() => fgRef.current.zoomToFit(100)}
        dagMode="radialin"
        dagLevelDistance={75}
      />
    </div>
  );
};

export default Graph;
