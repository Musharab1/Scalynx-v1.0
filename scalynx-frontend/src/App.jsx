import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/test")
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => {
        console.error("Error fetching API:", error);
        setMessage("Failed to connect to backend");
      });
  }, []);

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <h1 className="text-3xl font-bold text-gray-800">
        {message}
      </h1>
    </div>
  );
}

export default App;
