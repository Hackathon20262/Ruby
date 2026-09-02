"use client";

interface ConfidenceItem {
  label: string;
  checked: boolean;
}

const items: ConfidenceItem[] = [
  { label: "Budget", checked: false },
  { label: "Team Size", checked: false },
  { label: "Timeline", checked: false },
  { label: "Authority", checked: false },
];

export default function ConfidenceMeter() {
  return (
    <div className="rounded-xl border border-neutral-700 bg-neutral-900 p-4 w-full">
      <h3 className="text-sm font-semibold text-neutral-300 mb-3">
        Qualification Confidence
      </h3>
      <div className="flex flex-col gap-2">
        {items.map((item) => (
          <div key={item.label} className="flex items-center gap-2">
            <div
              className={`h-4 w-4 rounded border flex items-center justify-center ${
                item.checked
                  ? "bg-green-500 border-green-500"
                  : "border-neutral-600 bg-neutral-800"
              }`}
            >
              {item.checked && (
                <span className="text-white text-xs leading-none">✓</span>
              )}
            </div>
            <span className="text-sm text-neutral-300">{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}