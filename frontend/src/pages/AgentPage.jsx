import { useState } from "react";
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
  "Can you recalculate the risk with different values?",
  "What is the patient's readmission probability?",
  "What does this risk level mean?",
  "Will this patient be readmitted?",
  "What are the top contributing factors?",
  "What is the most important factor?",
  "What does A1C mean?",
  "How does A1C affect readmission risk?",
  "Why does time in hospital matter?",
  "What does length of stay tell us?",
  "What does the number of diagnoses mean?",
  "How do medications affect the risk?",
  "Does insulin use affect the prediction?",
  "Does age affect readmission risk?",
  "Does the admission type affect the risk?",
  "What does the discharge destination mean?",
  "What follow-up should be arranged?",
  "What should the care team review before discharge?",
  "What warning signs should be monitored?",
  "What should caregivers know after discharge?",
  "How can follow-up reduce readmission risk?",
  "What are the next steps for the care team?",
  "How should pending lab results be followed up?",
  "What should be included in the discharge plan?",
  "How can medication review help?",
  "What support may be needed at home?",
  "How are the contributing factors identified?",
  "What data does the model use?",
  "Can I trust this prediction?",
  "How accurate is the model?",
  "What are false positives and false negatives?",
  "What patient information does the model need?",
  "Does this model replace a clinician?",
  "Can you give a medical diagnosis?",
  "What should I do in a medical emergency?"
];

export function AgentPage() {
  const { messages, pending, send } = useAgent();
  const [showAllQuestions, setShowAllQuestions] = useState(false);
  const visibleSuggestions = showAllQuestions ? SUGGESTIONS : SUGGESTIONS.slice(0, 8);

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
            {visibleSuggestions.map((s) => (
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
          <button
            type="button"
            onClick={() => setShowAllQuestions((visible) => !visible)}
            className="mt-3 w-full rounded-sm border border-teal-500 px-3 py-2 text-sm font-medium text-teal-600 hover:bg-teal-50 transition-colors"
          >
            {showAllQuestions ? "Show fewer questions" : `Show more questions (${SUGGESTIONS.length - 8} more)`}
          </button>
        </Card>
      </div>
    </div>
  );
}
