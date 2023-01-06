import React from "react";
import { useParams } from "react-router-dom";

export default function Header(props) {

  let {params}=useParams()
  console.log(params)
  return (
    <div className="header">
      <div className="headerText"> {props.head}</div>
    </div>
  );
}
