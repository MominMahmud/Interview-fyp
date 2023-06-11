import React, { useEffect, useState,useRef } from "react";
import Question from "./Question";
import axios from "axios";
import { useParams } from "react-router-dom";
import { ReactMediaRecorder } from 'react-media-recorder';
import VideoPreview from "./VideoPreview";
export default function Answers() {

  var [nextQuestion, setNextQuestion] = useState(0);
  const [enable, setEnable] = useState(true);
  const { id } = useParams()

  const handleUpload = async (mediaBlobUrl) => {
    

    let blob = await fetch(mediaBlobUrl['mediaBlobUrl']).then(r => r.blob());
    let data =  new FormData()
    data.append('file',blob,id)
    try {
        await axios.post('http://localhost:90/setEmotions',data).then((res)=>{
        console.log(res)
        // Perform further operations with the Blob object
      })
      
      
 
      
      console.log('Upload successful');

    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  
  return (
    <div>
            <div id="background"></div>
      
      <div className="interview-section">
        <div className="section"></div>
        <Question index={nextQuestion} id = {id}></Question>
        <button className="btn btn-primary"onClick={()=>{
        setNextQuestion(nextQuestion+1)
        }}>Next Question</button>
        {/* <button className="btn btn-danger" onClick={startRecording}>Start Recording</button>
        <button onClick={stopRecording} className="btn btn-primary">Stop Recording</button> */}
      <div>
        <ReactMediaRecorder
          // video
          // render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
          //   <div>
          //     <p>{status}</p>
          //     <button onClick={startRecording}>Start Recording</button>
          //     <button onClick={stopRecording}>Stop Recording</button>
          //     <video src={mediaBlobUrl} controls autoPlay loop />
          //   </div>
          // )}
          // audio
          video
          blobPropertyBag={{
            type: 'video/webm',
          }}
          // askPermissionOnMount={true}
          render={({
            previewStream,
            status,
            startRecording,
            stopRecording,
            mediaBlobUrl,
          }) => {
            console.log(previewStream);
            
            return (
              <div>
                <p>{status}</p>
                <button onClick={startRecording}>Start Recording</button>
                <button onClick={()=>{
                  stopRecording()
                }}>Stop Recording</button>
                <button onClick={()=>{

                  handleUpload({mediaBlobUrl})
                }}>
                  Save

                </button>
                <button
                  onClick={() => {
                    startRecording();
                    setTimeout(stopRecording, 2000);
                    setEnable(false);
                  }}
                >
                  togglestreaming
                </button>
                {/* <audio src={mediaBlobUrl} controls autoPlay loop /> */}
                {enable && <VideoPreview stream={previewStream} />}
              </div>
            );
          }}
        />
      </div>

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
