import { useState } from "react";

export default function App() {
  const [idea, setIdea] = useState("");
  const [targetMarket, setTargetMarket] = useState("");
  const [location, setLocation] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate inputs
    if (!idea || !targetMarket || !location) {
      setError("Please fill in all fields.");
      setResponse("");
      return;
    }
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:5000/api/validate-idea", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea, targetMarket, location }),
      });
      const data = await res.json();
      if (res.ok) {
        setResponse(data.message);
      } else {
        setError(data.message || "Something went wrong!");
      }
    } catch (err) {
      setError("Error connecting to server.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-500 to-indigo-500 p-4">
      <div className="bg-white rounded-2xl shadow-lg max-w-md w-full p-6">
        <h1 className="text-2xl font-bold text-center text-indigo-600 mb-4">
          Business Idea Validator
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-medium text-gray-700">Business Idea</label>
            <input
              type="text"
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Enter your business idea"
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label className="block font-medium text-gray-700">Target Market</label>
            <input
              type="text"
              value={targetMarket}
              onChange={(e) => setTargetMarket(e.target.value)}
              placeholder="e.g., job seekers, students"
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          <div>
            <label className="block font-medium text-gray-700">Location</label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="City or country"
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
          </div>
          {error && (
            <p className="text-red-500 text-sm text-center">{error}</p>
          )}
          <button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            Validate Idea
          </button>
        </form>
        {response && (
          <div className="mt-4 p-3 bg-green-100 text-green-700 rounded-lg text-center">
            {response}
          </div>
        )}
      </div>
    </div>
  );
}
