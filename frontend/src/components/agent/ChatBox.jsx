import { useState, useRef, useEffect } from "react";

export function ChatBox({ messages, pending, onSend }) {
  const [draft, setDraft] = useState("");
  const listRef = useRef(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, pending]);

  function handleSubmit(e) {
    e.preventDefault();
    if (!draft.trim() || pending) return;
    onSend(draft);
    setDraft("");
  }

  return (
    <div className="flex flex-col h-[28rem]">
      <div ref={listRef} className="flex-1 overflow-y-auto space-y-3 pr-1 no-scrollbar">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-sm px-3 py-2 text-sm leading-relaxed ${
                m.role === "user" ? "bg-teal-500 text-white" : "bg-teal-50 text-ink"
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
        {pending && (
          <div className="flex justify-start">
            <div className="bg-teal-50 text-ink/50 text-sm rounded-sm px-3 py-2">Thinking…</div>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="mt-3 flex gap-2 border-t border-line pt-3">
        <input
          type="text"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="e.g. Why is this score high?"
          className="flex-1 border border-line rounded-sm px-3 py-2 text-sm focus:border-teal-500"
        />
        <button
          type="submit"
          disabled={pending || !draft.trim()}
          className="bg-teal-500 text-white text-sm font-medium px-4 py-2 rounded-sm hover:bg-teal-600 disabled:opacity-50"
        >
          Ask
        </button>
      </form>
    </div>
  );
}
