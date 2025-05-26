import React, { useState, useRef } from "react";
import Webcam from "react-webcam";

function VideoUploader() {
  const [videoFile, setVideoFile] = useState(null);
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [isRecording, setIsRecording] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setVideoFile(file);
    }
  };

  const startRecording = () => {
    setRecordedChunks([]);
    setIsRecording(true);

    const stream = webcamRef.current.stream;
    mediaRecorderRef.current = new MediaRecorder(stream, {
      mimeType: "video/webm",
    });

    mediaRecorderRef.current.ondataavailable = (e) => {
      if (e.data.size > 0) {
        setRecordedChunks((prev) => [...prev, e.data]);
      }
    };

    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setIsRecording(false);
  };

  const sendVideoToServer = async () => {
    const videoBlob = videoFile || new Blob(recordedChunks, { type: "video/webm" });

    const formData = new FormData();
    formData.append("video", videoBlob, "video_input.webm");

    try {
      const response = await fetch("http://localhost:8000/predict/by_video", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      alert("Распознанный жест: " + result.result);
    } catch (err) {
      console.error("Ошибка отправки:", err);
    }
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold">Распознавание жестов</h2>

      <div>
        <p>Загрузить видео:</p>
        <input type="file" accept="video/*" onChange={handleFileUpload} />
      </div>

      <div className="mt-4">
        <p>Или записать с камеры:</p>
        <Webcam ref={webcamRef} audio={false} />
        <div className="space-x-2 mt-2">
          {!isRecording ? (
            <button onClick={startRecording} className="px-4 py-2 bg-green-600 text-white rounded">
              Начать запись
            </button>
          ) : (
            <button onClick={stopRecording} className="px-4 py-2 bg-red-600 text-white rounded">
              Остановить запись
            </button>
          )}
        </div>
      </div>

      <button onClick={sendVideoToServer} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">
        Отправить видео на сервер
      </button>
    </div>
  );
}

export default VideoUploader;
