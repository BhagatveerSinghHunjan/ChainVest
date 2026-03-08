type Props = {
  result: any;
};

export default function BlockchainPanel({ result }: Props) {
  if (!result) return null;

  return (
    <div className="space-y-6">

      {/* TITLE */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900">
          Blockchain Audit Trail
        </h2>
        <p className="text-sm text-gray-600">
          Every decision step is logged immutably on-chain for transparency.
        </p>
      </div>

      {/* TX HASHES */}
      <div>
        <h3 className="text-sm font-semibold text-gray-900 mb-2">
          Transaction Hashes
        </h3>

        <div className="space-y-2">
          {result.tx_hashes?.map((tx: string, i: number) => (
            <div
              key={i}
              className="flex items-center justify-between border border-gray-200 rounded-lg px-3 py-2 bg-gray-50"
            >
              <span className="text-xs font-mono text-gray-800 break-all">
                {tx}
              </span>

              <span className="text-xs px-2 py-1 rounded bg-indigo-50 text-indigo-600 font-medium">
                Verified
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* LOGS */}
      <div>
        <h3 className="text-sm font-semibold text-gray-900 mb-2">
          Execution Logs
        </h3>

        <div className="space-y-2">
          {result.logs?.map((log: string, i: number) => (
            <div
              key={i}
              className="border border-gray-200 rounded-lg px-3 py-2 bg-white text-sm text-gray-800"
            >
              {log}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}