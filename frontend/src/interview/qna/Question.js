import { useSpeechSynthesis } from 'react-speech-kit';
import React, { useState, useEffect } from 'react'
import axios from 'axios';
import requests from '../../config'

function Question(props) {
  var [questions, setQuestions] = useState([]);
  const [text, setText] = useState("");
  const { speak } = useSpeechSynthesis();
   useEffect(() => {
    setQuestions([])
    axios.get(requests.getJobById+'/'+props.id).then((res)=>{

      console.log(res)
    }).then(()=>{
      axios.get(requests.getQuestions).then((res) => {

        //setQuestions(res.data);
        console.log(res.data);
  
        for(let i =0;i<res.data.length;i++){
          questions = [...questions, res.data[i].text]
        }
        setQuestions(questions);
        console.log(questions)
      });
    })

  },[]);



  console.log(props);
  const handleOnClick = () => {
    
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
export default Question




