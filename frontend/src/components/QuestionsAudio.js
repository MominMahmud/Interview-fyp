import { useSpeechSynthesis } from 'react-speech-kit';
import React, { useState, useEffect } from 'react'

function QuestionsAudio(props) {

    const questions=["What is your name?","Where do you live"];
    const [text,setText] = useState('');
    const {speak} = useSpeechSynthesis();
    console.log(props)
    const handleOnClick = () => {
        console.log(props.index)
      speak({text:questions[props.index]})
    }
  
    return (
            <>
            <h1>Text to Speech Converter in React</h1>
            <h5>{questions}</h5>
            <button className="buttonStyle" onClick={()=>{handleOnClick()}}>Listen</button>
            </>

      );
}
export default QuestionsAudio




