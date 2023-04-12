import React, { useCallback, useState } from "react";
import MicRecorder from "mic-recorder-to-mp3";
import Question from "./Question";
import logo from '../../images/loggg.png'
import axios from 'axios'
import { useParams } from "react-router-dom";



const Mp3Recorder = new MicRecorder({ bitRate: 128 });
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const mic = new SpeechRecognition();

mic.continuous = true;
mic.interimResults = true;
mic.lang = "en-US";

export default function App() {
  const [stopRec, setStopRec] = useState(false)
  const [downloadRec, setDownloadRec] = useState(false)
  const [isRecording, setRecording] = useState(false);
  const [blobURL, setBlob] = useState("");
  const [isBlocked, setBlocked] = useState(false);
  const [note, setNote] = useState("");
  const [savedNotes, setSavedNotes] = useState([]);
  var [nextQuestion, setNextQuestion] = useState(0);

  const { id } = useParams();
  console.log(id);
  // function start() {
    // mic.start();
    // mic.onend = () => {
    //   console.log("continue..");
    //   mic.start();
    // };
    // mic.onstart = () => {
    //   console.log("Mics on");
    // };

    // mic.onresult = (event) => {
    //   const transcript = Array.from(event.results)
    //     .map((result) => result[0])
    //     .map((result) => result.transcript)
    //     .join("");
    //   console.log(transcript);
    //   setNote(transcript);
    //   mic.onerror = (event) => {
    //     console.log(event.error);
    //   };
    // };
  //}

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
        console.log(blobURL)
        setRecording(false);
      })
      .catch((e) => console.log(e));
  }
  const handleSaveNote = () => {
    setSavedNotes([...savedNotes, note]);
    ;
  };

  function onSubmit() {

    axios.patch("http://localhost:90/candidatesRes/" + id, {
      res: note

    })
    setNote("")

  }

  let mediaRecorder
  let recordedBlobs



  async function start() {

    


    const constaints = {

      audio: {



      },
      video: {

        width: 1280, height: 720
      }
    }
    await init(constaints)
  }

  async function init(constaints) {

    try {

      const stream = await navigator.mediaDevices.getUserMedia(constaints)
      handleSuccess(stream)
    }
    catch (e) {

      console.log(e)
    }
  }

  function handleSuccess(stream) {

    window.stream = stream

    const gumVideo = document.querySelector('video#gum')
    gumVideo.srcObject = stream
  }


  function record() {

    startRecording()
  }

  function stopRecording() {

    mediaRecorder.stop()
  }
  function startRecording() {

    recordedBlobs = []
    let options = {

      mimiType: 'video/webm;codecs=vp9,opus'
    }

    try {

      console.log('kk')
      mediaRecorder = new MediaRecorder(window.stream, options)

    }
    catch (e) {

      console.log(e)
    }

    console.log(mediaRecorder)
    //recordButton.textContent = "Stop Recording"


    mediaRecorder.start()
    // mediaRecorder.stop = (e)=>{

    //   console.log("Recording is stopped")
    // }

    mediaRecorder.ondataavailable = handleDataAvailable


  }

  function handleDataAvailable(event) {
    console.log(event)
    if (event.data && event.data.size > 0) {

      recordedBlobs.push(event.data)

    }


  }

  let recorded = false


  async function download() {




    console.log(recordedBlobs)
    const blob = new Blob(recordedBlobs, { type: 'video/mp4' })
    console.log(blob)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.style.display = 'none'
    a.style.display = 'none'
    a.href = url
    a.download = id + '.mp4'

    document.body.appendChild(a)
    a.click()

    setTimeout(() => {

      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    }, 100)
  }

  function stop() {

    
    mediaRecorder.stop()

  }
  return (
    <>

      {/* <div id="background"></div>
      <div className="interview-section">
        <div className="section">
            <img src={logo} className="logo"></img> */}
      {/* <Question index={nextQuestion}></Question> */}

      <div >
        <video src='' id='gum' playsInline autoPlay muted ></video>
      </div>

      <button id='start' onClick={start}>Start </button>
      <button id='record' onClick={record}>Record</button>

      <button id='play' onClick={stop}>Stop</button>
      <button id='download' onClick={download}>Save</button>
      {/* </div>
          <button className="btn btn-danger" onClick={start} disabled={isRecording}>
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
          <audio src={blobURL} controls="controls" title="1" download />
          <button className="btn btn-outline-success submit" onClick={onSubmit}>Submit</button>
        </div> */}

    </>
  );
}
