"use client";
import { useState, useEffect } from 'react';

interface ConfidenceItem {
  label: string;
  checked: boolean;
}


export default function ConfidenceMeter() {
    const [items, setItems] = useState<ConfidenceItem[]>([
    { label: "Budget", checked: false },
    { label: "Team Size", checked: false },
    { label: "Timeline", checked: false },
    { label: "Authority", checked: false },
  ]);

  useEffect(() => {
    const fetchScore = async () => {
      try {
        const res = await fetch('/api/score');
        const data = await res.json();
        setItems([
          { label: "Budget", checked: data.budget },
          { label: "Team Size", checked: data.teamSize },
          { label: "Timeline", checked: data.timeline },
          { label: "Authority", checked: data.authority },
        ]);
      } catch (error) {
        console.error('Failed to fetch score:', error);
      }
    };
    fetchScore();
    const interval = setInterval(fetchScore, 2000);
    return () => clearInterval(interval);
  }, []);
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