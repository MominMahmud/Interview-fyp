import React, { useState } from "react";
import MicRecorder from "mic-recorder-to-mp3";
import Question from "./Question";
import logo from '../../images/loggg.png'

const Mp3Recorder = new MicRecorder({ bitRate: 128 });
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const mic = new SpeechRecognition();

mic.continuous = true;
mic.interimResults = true;
mic.lang = "en-US";

export default function App() {
  const [isRecording, setRecording] = useState(false);
  const [blobURL, setBlob] = useState("");
  const [isBlocked, setBlocked] = useState(false);
  const [note, setNote] = useState(null);
  const [savedNotes, setSavedNotes] = useState([]);
  var [nextQuestion, setNextQuestion] = useState(0);

  function start() {
    mic.start();
    mic.onend = () => {
      console.log("continue..");
      mic.start();
    };
    mic.onstart = () => {
      console.log("Mics on");
    };
    Mp3Recorder.start()
      .then(() => {
        setRecording(true);
      })
      .catch((e) => console.error(e));
    mic.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0])
        .map((result) => result.transcript)
        .join("");
      console.log(transcript);
      setNote(transcript);
      mic.onerror = (event) => {
        console.log(event.error);
      };
    };
  }

  function stop() {
    setRecording(!isRecording);
    mic.stop();
    mic.onend = () => {
      console.log("Stopped Mic on Click");
    };
    Mp3Recorder.stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const blobURL = URL.createObjectURL(blob);
        setBlob(blobURL);
        setRecording(false);
      })
      .catch((e) => console.log(e));
  }
  const handleSaveNote = () => {
    setSavedNotes([...savedNotes, note]);
    setNote("");
  };

  return (
    <>
      <div id="background"></div>
      <div className="interview-section">
        <div className="section">
            <img src={logo} className="logo"></img>
          <Question index={nextQuestion}></Question>
          
          <button className="btn btn-primary" onClick={start} disabled={isRecording}>
            Record
          </button>
          <button className="btn btn-outline-primary" onClick={stop} disabled={!isRecording}>
            Stop
          </button>
          <button  className="btn btn-outline-success"onClick={handleSaveNote} disabled={!note}>
            Save Answer
          </button>
          <button
            onClick={() =>
              setNextQuestion((nextQuestion) => (nextQuestion += 1))
            }
            className="btn btn-outline-primary"
          >
            Next Question
          </button>
          <div className="box">
            <h2>Answer</h2>
            {savedNotes.map((n) => (
              <p key={n}>{n}</p>
            ))}
          </div>
          <audio src={blobURL} controls="controls" />
          <button className="btn btn-outline-success">Submit</button>
        </div>
      </div>
    </>
  );
}
