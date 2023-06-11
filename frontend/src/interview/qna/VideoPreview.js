import {React, useEffect, useRef} from 'react'
function VideoPreview  ({ stream }) {
    const videoRef = useRef(null);

    useEffect(() => {
      if (videoRef.current && stream) {
        videoRef.current.srcObject = stream;
      }
    }, [stream]);
    if (!stream) {
      return null;
    }
    return <video ref={videoRef} width={300} height={300} autoPlay controls />;

}
export default VideoPreview