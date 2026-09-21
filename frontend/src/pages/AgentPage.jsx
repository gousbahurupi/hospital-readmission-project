import { TopBar } from "../components/layout/TopBar.jsx";
import { Card } from "../components/common/Card.jsx";
import { ChatBox } from "../components/agent/ChatBox.jsx";
import { useAgent } from "../hooks/useAgent.js";

const SUGGESTIONS = [
  "Why is this patient's risk high?",
  "What does discharge disposition affect?",
  "What are the model's limitations?",
  "What should be monitored after discharge?",
  "How can the risk be reduced?",
  "How does the model work?",
  "Is patient data stored?",
  "Can you recalculate the risk with different values?"
];

export function AgentPage() {
  const { messages, pending, send } = useAgent();

  return (
    <div className="flex-1 flex flex-col">
      <TopBar
        title="Ask the agent"
        subtitle="A rule-based assistant that explains predictions in plain language. It does not replace clinical judgment."
      />
      <div className="p-8 grid grid-cols-5 gap-5">
        <Card title="Conversation" className="col-span-3">
          <ChatBox messages={messages} pending={pending} onSend={send} />
        </Card>
        <Card title="Try asking" eyebrow="Suggestions" className="col-span-2 h-fit">
          <ul className="space-y-2">
            {SUGGESTIONS.map((s) => (
              <li key={s}>
                <button
                  onClick={() => send(s)}
                  className="w-full text-left text-sm text-ink/80 border border-line rounded-sm px-3 py-2 hover:border-teal-500 hover:text-ink transition-colors"
                >
                  {s}
                </button>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
}
