"use client";

import { useState } from "react";

type Props = {
  onResult: (data: any) => void;
};

export default function InputForm({ onResult }: Props) {
  const [mode, setMode] = useState("vc");
  const [revenue, setRevenue] = useState("");
  const [burn, setBurn] = useState("");
  const [cash, setCash] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        mode,
        revenue: Number(revenue),
        burn: Number(burn),
        cash: Number(cash),
      }),
    });

    const data = await res.json();
    onResult(data);
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">

      <h2 className="text-lg font-semibold text-gray-900">Run Analysis</h2>

      <select
        value={mode}
        onChange={(e) => setMode(e.target.value)}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-indigo-500"
      >
        <option value="vc">VC Mode</option>
        <option value="loan">Loan Mode</option>
      </select>

      <input
        type="number"
        placeholder="Monthly Revenue"
        value={revenue}
        onChange={(e) => setRevenue(e.target.value)}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-indigo-500"
        required
      />

      <input
        type="number"
        placeholder="Monthly Burn"
        value={burn}
        onChange={(e) => setBurn(e.target.value)}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-indigo-500"
        required
      />

      <input
        type="number"
        placeholder="Cash Available"
        value={cash}
        onChange={(e) => setCash(e.target.value)}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-indigo-500"
        required
      />

      <button className="w-full bg-indigo-600 text-white py-2 rounded-lg font-medium hover:bg-indigo-700 transition">
        {loading ? "Analyzing..." : "Analyze"}
      </button>

    </form>
  );
}