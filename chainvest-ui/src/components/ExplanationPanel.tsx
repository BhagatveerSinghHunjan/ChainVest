import type { ChainVestResult } from "@/components/types";

type Props = { result: ChainVestResult };

export default function ExplanationPanel({ result }: Props) {
  const reasoning = result?.decision_reasoning;

  const reasoningPanel = reasoning ? (
    <div className="mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Decision Reasoning</h2>
      <p className="text-gray-800 mb-3">{reasoning.summary}</p>
      <p className="text-sm text-gray-600 mb-4">{reasoning.threshold_context}</p>

      <div className="grid gap-4 md:grid-cols-3 mb-5">
        <ScoreCard title="Overall" value={reasoning.score_breakdown?.overall_score} />
        <ScoreCard title="Financial" value={reasoning.score_breakdown?.financial_score} />
        <ScoreCard title="Unit" value={reasoning.score_breakdown?.unit_score} />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h3 className="font-semibold text-gray-900 mb-2">Why It Works</h3>
          <ul className="list-disc ml-6 text-gray-800 space-y-1">
            {reasoning.highlights?.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-semibold text-gray-900 mb-2">What Needs Attention</h3>
          <ul className="list-disc ml-6 text-gray-800 space-y-1">
            {reasoning.concerns?.map((item: string, i: number) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  ) : null;

  if (result?.llm_trace?.provider === "disabled") {
    return (
      <div>
        {reasoningPanel}
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Cerebrum</h2>
        <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
          <p className="text-sm font-medium text-amber-900">
            Cerebrum is not connected.
          </p>
          <p className="mt-1 text-sm text-amber-800">
            Configure an OpenAI-compatible Cerebrum endpoint with
            <code> CEREBRUM_BASE_URL </code>
            and optionally any dummy <code>OPENAI_API_KEY</code> value if the
            provider requires the client field to be present.
          </p>
        </div>
      </div>
    );
  }

  if (result?.llm_trace?.provider === "error") {
    return (
      <div>
        {reasoningPanel}
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Cerebrum</h2>
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-4">
          <p className="text-sm font-medium text-rose-900">
            Cerebrum failed to generate an explanation.
          </p>
          <p className="mt-1 text-sm text-rose-800">
            {result.llm_trace.error || "Unknown model error."}
          </p>
        </div>
      </div>
    );
  }

  if (!result?.llm_explanation) {
    return reasoningPanel;
  }

  const exp = result.llm_explanation;

  return (
    <div>
      {reasoningPanel}
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Cerebrum</h2>

      <p className="text-gray-800 mb-4">{exp.summary}</p>

      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h3 className="font-semibold text-gray-900 mb-2">Strengths</h3>
          <ul className="list-disc ml-6 text-gray-800 space-y-1">
            {exp.strengths?.map((s: string, i: number) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-semibold text-gray-900 mb-2">Weaknesses</h3>
          <ul className="list-disc ml-6 text-gray-800 space-y-1">
            {exp.weaknesses?.map((w: string, i: number) => (
              <li key={i}>{w}</li>
            ))}
          </ul>
        </div>
      </div>

      <p className="mt-6 text-gray-800">{exp.final_explanation}</p>
    </div>
  );
}

function ScoreCard({ title, value }: { title: string; value: number | string | null | undefined }) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="mt-1 text-xl font-semibold text-gray-900">
        {value ?? "N/A"}
      </p>
    </div>
  );
}
