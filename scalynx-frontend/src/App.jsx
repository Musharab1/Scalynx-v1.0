import { useState } from "react";

const App = () => {
  const [idea, setIdea] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/api/validate-idea", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ idea }),
      });

      if (!res.ok) throw new Error("Server error");
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("❌ Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="bg-white p-6 rounded-2xl shadow-lg w-full max-w-xl">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          💡 Scalynx Idea Validator
        </h1>
        <form onSubmit={handleSubmit}>
          <textarea
            className="w-full p-4 border border-gray-300 rounded-xl mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows="5"
            placeholder="Enter your startup idea..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            required
          ></textarea>
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-xl transition duration-200"
            disabled={loading}
          >
            {loading ? "⏳ Validating..." : "🚀 Validate Idea"}
          </button>
        </form>

        {result && (
          <div
            className={`mt-6 p-4 rounded-xl text-center font-semibold ${
              result.valid ? "text-green-600 bg-green-100" : "text-red-600 bg-red-100"
            }`}
          >
            {result.valid ? "✅ Valid Idea: " : "❌ Invalid Idea: "}
            {result.feedback}
          </div>
        )}

        {error && <p className="mt-4 text-red-500 text-center">{error}</p>}
      </div>
    </div>
  );
};

export default App;
