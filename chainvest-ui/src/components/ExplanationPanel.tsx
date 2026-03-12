import type { ChainVestResult } from "@/components/types";

type Props = { result: ChainVestResult };

export default function ExplanationPanel({ result }: Props) {
  const reasoning = result?.decision_reasoning;

  return (
    reasoning ? (
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Decision Reasoning</h2>
        <p className="text-gray-800 mb-3">{reasoning.summary}</p>
        <p className="text-sm text-gray-600 mb-4">{reasoning.threshold_context}</p>

        <div className="grid gap-4 md:grid-cols-4 mb-5">
          <ScoreCard title="Overall" value={reasoning.score_breakdown?.overall_score} />
          <ScoreCard title="Financial" value={reasoning.score_breakdown?.financial_score} />
          <ScoreCard title="Unit" value={reasoning.score_breakdown?.unit_score} />
          <ScoreCard title="Business" value={reasoning.score_breakdown?.business_score} />
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
    ) : null
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
