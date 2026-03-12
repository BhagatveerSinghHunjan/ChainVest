"use client";

import { useState, type FormEvent } from "react";

import type { ChainVestResult } from "@/components/types";

type Props = {
  onResult: (data: ChainVestResult) => void;
};

export default function InputForm({ onResult }: Props) {
  const [mode, setMode] = useState("vc");
  const [revenue, setRevenue] = useState("");
  const [burn, setBurn] = useState("");
  const [cash, setCash] = useState("");
  const [businessDescription, setBusinessDescription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
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
        business_description: businessDescription,
      }),
    });

    const data = await res.json();
    onResult(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h2 className="text-xl font-semibold text-gray-900">VC Intake</h2>
        <p className="text-sm text-gray-600">
          Enter the core startup metrics and a short business summary. This is the
          baseline information a VC typically uses to decide whether a company is
          worth taking into diligence.
        </p>
      </div>

      <div className="grid gap-3 rounded-xl border border-emerald-100 bg-emerald-50 p-4 md:grid-cols-4">
        <MetricHint title="Revenue Quality" text="Consistent monthly revenue, healthy growth, repeatability." />
        <MetricHint title="Burn Control" text="Burn that is proportionate to growth and product traction." />
        <MetricHint title="Cash Runway" text="Enough cash to execute, usually 12-18 months is safer." />
        <MetricHint title="Narrative" text="Clear market, wedge, customer pain, and why now." />
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-800">Evaluation Mode</span>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-gray-900 focus:ring-2 focus:ring-emerald-500"
            >
              <option value="vc">VC Mode</option>
              <option value="loan">Loan Mode</option>
            </select>
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-800">Monthly Revenue</span>
            <input
              type="number"
              placeholder="e.g. 125000"
              value={revenue}
              onChange={(e) => setRevenue(e.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-gray-900 focus:ring-2 focus:ring-emerald-500"
              required
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-800">Monthly Burn</span>
            <input
              type="number"
              placeholder="e.g. 80000"
              value={burn}
              onChange={(e) => setBurn(e.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-gray-900 focus:ring-2 focus:ring-emerald-500"
              required
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-medium text-gray-800">Cash Available</span>
            <input
              type="number"
              placeholder="e.g. 950000"
              value={cash}
              onChange={(e) => setCash(e.target.value)}
              className="w-full rounded-xl border border-gray-300 bg-white px-3 py-2 text-gray-900 focus:ring-2 focus:ring-emerald-500"
              required
            />
          </label>
        </div>

        <label className="block space-y-2">
          <span className="text-sm font-medium text-gray-800">Brief Business Description</span>
          <textarea
            placeholder="Describe what the company does, who the customer is, what problem it solves, how it makes money, and any traction that matters."
            value={businessDescription}
            onChange={(e) => setBusinessDescription(e.target.value)}
            rows={6}
            className="w-full resize-none rounded-2xl border border-gray-300 bg-white px-4 py-3 text-gray-900 focus:ring-2 focus:ring-emerald-500"
          />
        </label>

        <button className="w-full rounded-xl bg-emerald-600 py-3 font-medium text-white transition hover:bg-emerald-700">
          {loading ? "Analyzing..." : "Run VC Analysis"}
        </button>
      </form>
    </div>
  );
}

function MetricHint({ title, text }: { title: string; text: string }) {
  return (
    <div className="rounded-lg border border-emerald-200 bg-white/80 p-3">
      <p className="text-sm font-semibold text-gray-900">{title}</p>
      <p className="mt-1 text-xs leading-5 text-gray-600">{text}</p>
    </div>
  );
}
