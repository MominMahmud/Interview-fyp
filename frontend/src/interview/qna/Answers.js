import React, { useEffect, useState,useRef } from "react";
import Question from "./Question";
import axios from "axios";
import { useParams } from "react-router-dom";


export default function Answers() {

  var [nextQuestion, setNextQuestion] = useState(0);
  const videoRef = useRef(null);
  const [mediaStream, setMediaStream] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [recordedChunks, setRecordedChunks] = useState([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });
      setMediaStream(stream);
      videoRef.current.srcObject = stream;
      const options = { audioBitsPerSecond: 128000 }; // Adjust the bit rate as needed

      const mediaRecorder = new MediaRecorder(stream, options);
      setRecorder(mediaRecorder);

      mediaRecorder.addEventListener('dataavailable', handleDataAvailable);
      mediaRecorder.start();
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (recorder && recorder.state === 'recording') {
      recorder.stop();
      mediaStream.getTracks().forEach((track) => track.stop());
    }
  };

  const handleDataAvailable = (event) => {
    if (event.data.size > 0) {
      setRecordedChunks((prevChunks) => [...prevChunks, event.data]);
    }
  };

  const handleUpload = async () => {
    try {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);

      // Send the blob URL to the server using axios or fetch
      // ...
      await axios.post('http://localhost:5000/api/convert', { blobUrl: url }).then((res)=>{

      console.log(res)
      });
      console.log('Upload successful');

      // Cleanup the recorded chunks and URL

      setRecordedChunks([]);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  
  return (
    <div>
            <div id="background"></div>
      
      <div className="interview-section">
        <div className="section"></div>
        <Question index={nextQuestion}></Question>
        <button className="btn btn-primary"onClick={()=>{
        setNextQuestion(nextQuestion+1)
        }}>Next Question</button>
        {/* <button className="btn btn-danger" onClick={startRecording}>Start Recording</button>
        <button onClick={stopRecording} className="btn btn-primary">Stop Recording</button> */}
        <div>
          <video ref={videoRef} controls />
          <button onClick={startRecording}>Start Recording</button>
          <button onClick={stopRecording}>Stop Recording</button>
          <button onClick={handleUpload}>Upload Video</button>
        </div>

        {/* <a className="btn btn-success"ref={downloadRef} onClick={onSubmit}>Save</a>
      
        <video ref={videoRef} width="340" height="280" />  */}

      

      
      </div>
    </div>
  )
};



//   return (
//     <>

            
//       {/* <Question index={nextQuestion}></Question> */}

//       <div>
//         {startVideo ? (
//           <video src="" id="gum" playsInline autoPlay muted></video>
//         ) : (
//           <h4 className="my-5">Press Start to Initiate Interview</h4>
//         )}
//       </div>

//       <button id="start" className="btn btn-outline-primary" onClick={start}>
//         Start{" "}
//       </button>
//       <button id="record" className="btn btn-danger" onClick={record}>
//         Record
//       </button>

//       <button id="play" className="btn btn-outline-primary" onClick={stop}>
//         Stop
//       </button>
//       <button
//         id="download"
//         className="btn btn-outline-success"
//         onClick={download}
//       >
//         Save
//       </button>
//       <button
//         onClick={() => setNextQuestion((nextQuestion) => (nextQuestion += 1))}
//         className="btn btn-outline-primary"
//       >
//         Next Question
//       </button>
//       {/* </div>
//           <button className="btn btn-danger" onClick={start} disabled={isRecording}>
//             Record
//           </button>
//           <button className="btn btn-outline-primary" onClick={stop} disabled={!isRecording}>
//             Stop
//           </button>
//           <button  className="btn btn-outline-success"onClick={handleSaveNote} disabled={!note}>
//             Save Answer
//           </button>
//           <button
//             onClick={() =>
//               setNextQuestion((nextQuestion) => (nextQuestion += 1))
//             }
//             className="btn btn-outline-primary"
//           >
//             Next Question
//           </button>
//           <div className="box">
//             <h2>Answer</h2>
//             {savedNotes.map((n) => (
//               <p key={n}>{n}</p>
//             ))}
//           </div>
//             <audio src={blobURL} controls="controls" title="1" download />*/}
//       <div>
//         <button className="btn btn-outline-success submit" onClick={onSubmit}>
//           Submit
//         </button>
//       </div>
//     </div>
//     </div>
//     </>
//   );
// }
