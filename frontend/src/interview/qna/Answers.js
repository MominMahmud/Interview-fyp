import React, { useState } from "react";
import MicRecorder from "mic-recorder-to-mp3";

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
    <div>
      <button onClick={start} disabled={isRecording}>
        Record
      </button>
      <button onClick={stop} disabled={!isRecording}>
        Stop
      </button>
      <button onClick={handleSaveNote} disabled={!note}>
        Save Answer
      </button>
      <div className="box">
        <h2>Answer</h2>
        {savedNotes.map((n) => (
          <p key={n}>{n}</p>
        ))}
      </div>
      <audio src={blobURL} controls="controls" />
    </div>
  );
}
