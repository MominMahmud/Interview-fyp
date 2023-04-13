import { useSpeechSynthesis } from 'react-speech-kit';
import React, { useState, useEffect } from 'react'
import axios from 'axios';
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

  const [limit, setLimit] = useState(false)

  console.log(props);
  const handleOnClick = () => {

    if (props.index >= 4) {

      setLimit(true)
    }
    else {
      var questions = ["What is your name?", "Why do you want to work here?", "What about this position made you want to apply?", "How familiar are you with our company and what we do?"]
      console.log(props.index);
      speak({ text: questions[props.index] });
    }
  };

  return (
    <>
      <div className="listen-margin">

        <div>
          {limit?
            <h4>Thank you for your time</h4>
            : <button className="btn btn-primary"

              onClick={() => {
                handleOnClick();
              }}
            >
              Listen
            </button>}
        </div>
      </div>

    </>
  );
}
export default Question




