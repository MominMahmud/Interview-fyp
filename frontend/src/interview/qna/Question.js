import { useSpeechSynthesis } from 'react-speech-kit';
import React, { useState, useEffect } from 'react'
import axios from 'axios';
function Question(props) {

    const [questions,setQuestions]=useState();
    const [text,setText] = useState('');
    const {speak} = useSpeechSynthesis();
    useEffect(()=>{
      axios.get('http://127.0.0.1:5000/questions').then(res=>{
          setQuestions(res.data)
          console.log(res.data)
      })
    })

    console.log(props)
    const handleOnClick = () => {
        console.log(props.index)
      speak({text:questions[props.index].question})
    }
  
    return (
            <>
            <h1>FASTHire</h1>
            <h2>Questions</h2>
            
            <button className="buttonStyle" onClick={()=>{handleOnClick()}}>Listen</button>
            </>

      );
}
export default Question




