type Props = { result: any };

export default function ExplanationPanel({ result }: Props) {
  if (!result?.llm_explanation) return null;

  const exp = result.llm_explanation;

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Explanation</h2>

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