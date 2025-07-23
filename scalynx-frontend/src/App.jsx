import { useState } from "react";

export default function BusinessIdeaValidator() {
  const [idea, setIdea] = useState("");
  const [targetMarket, setTargetMarket] = useState("");
  const [location, setLocation] = useState("");
  const [response, setResponse] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponse(""); // Clear previous response
    setAnalysis(null); // Clear analysis result

    const res = await fetch("http://127.0.0.1:5000/api/validate-idea", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea, targetMarket, location }),
    });

    const data = await res.json();
    if (data.error) {
      setResponse(`❌ ${data.error}`);
    } else if (data.verdict) {
      setResponse(`✅ ${data.verdict} (Rating: ${data.rating})`);
    } else {
      setResponse(`ℹ️ ${data.message}`);
    }
  };

  const analyzeIdea = async () => {
    setAnalysis(null); // Clear previous analysis
    const res = await fetch("http://127.0.0.1:5000/api/analyze-idea", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea }),
    });

    const data = await res.json();
    if (!data.error) {
      setAnalysis(data);
    } else {
      setResponse(`❌ ${data.error}`);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-[#0f2027] via-[#203a43] to-[#2c5364]">
      <div className="backdrop-blur-lg bg-white/10 border border-white/30 shadow-2xl rounded-3xl p-8 w-full max-w-lg transform transition-transform duration-500 hover:scale-105">
        <h1 className="text-4xl font-bold text-center text-white mb-6 tracking-wide drop-shadow-lg">
          💡 Business Idea Validator
        </h1>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="💭 Business Idea"
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            className="w-full px-4 py-3 border border-white/30 rounded-xl bg-white/10 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all duration-300"
            required
          />
          <input
            type="text"
            placeholder="🎯 Target Market"
            value={targetMarket}
            onChange={(e) => setTargetMarket(e.target.value)}
            className="w-full px-4 py-3 border border-white/30 rounded-xl bg-white/10 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-pink-400 transition-all duration-300"
            required
          />
          <input
            type="text"
            placeholder="📍 Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full px-4 py-3 border border-white/30 rounded-xl bg-white/10 text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-green-400 transition-all duration-300"
            required
          />
          <div className="flex gap-4">
            <button
              type="submit"
              className="flex-1 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold rounded-xl shadow-md hover:shadow-xl hover:scale-105 transition-transform duration-300"
            >
              ✅ Validate Idea
            </button>
            <button
              type="button"
              onClick={analyzeIdea}
              className="flex-1 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white font-semibold rounded-xl shadow-md hover:shadow-xl hover:scale-105 transition-transform duration-300"
            >
              🔍 Analyze Idea
            </button>
          </div>
        </form>

        {/* Validation result */}
        {response && (
          <div className="mt-6 p-4 bg-green-100/20 border-l-4 border-green-400 text-green-100 rounded shadow">
            {response}
          </div>
        )}

        {/* Analysis result */}
        {analysis && (
          <div className="mt-6 p-4 bg-gradient-to-r from-gray-800 to-gray-700 text-white rounded-xl shadow-inner">
            <h2 className="text-xl font-bold mb-3">📊 Analysis Result:</h2>
            <div className="mb-2">
              <p className="font-semibold">✅ Strengths:</p>
              <ul className="list-disc list-inside text-green-300">
                {analysis.strengths.map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>
            <div className="mb-2">
              <p className="font-semibold">⚠️ Weaknesses:</p>
              <ul className="list-disc list-inside text-red-300">
                {analysis.weaknesses.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
            <div className="mt-3">
              <p className="font-semibold">🎯 Success Probability:</p>
              <div className="w-full bg-gray-600 rounded-full h-4 mt-1">
                <div
                  className="bg-green-500 h-4 rounded-full text-xs text-center text-white"
                  style={{
                    width: analysis.success_probability.replace("%", "") + "%",
                  }}
                >
                  {analysis.success_probability}
                </div>
              </div>
            </div>
            <div className="mt-3">
              <p className="font-semibold">💡 Advice:</p>
              <p className="italic text-cyan-300">{analysis.advice}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
