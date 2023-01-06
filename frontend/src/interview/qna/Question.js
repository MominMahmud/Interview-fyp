import { useSpeechSynthesis } from "react-speech-kit";
import React, { useState, useEffect } from "react";
import axios from "axios";
function Question(props) {
  //var [questions, setQuestions] = useState("");
  const [text, setText] = useState("");
  const { speak } = useSpeechSynthesis();
/*   useEffect(() => {
    axios.get("http://127.0.0.1:5000/questions").then((res) => {
      setQuestions(res.data);
      console.log(res.data);
    });
  });*/

  console.log(props);
  const handleOnClick = () => {
    var questions = ["What is your name?","Where do you live?"]
    console.log(props.index);
    speak({ text: questions[props.index] });
  };

  return (
    <>
      <div className="listen-margin">
        <button className="btn btn-primary"
          
          onClick={() => {
            handleOnClick();
          }}
        >
          Listen
        </button>
      </div>
    </>
  );
}
export default Question;
