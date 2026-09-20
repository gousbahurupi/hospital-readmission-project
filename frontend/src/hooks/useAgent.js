import { useState, useCallback } from "react";
import { api } from "../services/api.js";

const OPENING_MESSAGE = {
  role: "agent",
  text: "Ask me about a risk score, a specific factor, or what a recommendation means."
};

/**
 * Manages a simple turn-by-turn conversation with the rule-based agent.
 * @param {import('../types').PatientInput=} context - optional patient context to ground answers
 */
export function useAgent(context) {
  const [messages, setMessages] = useState([OPENING_MESSAGE]);
  const [pending, setPending] = useState(false);

  const send = useCallback(
    async (question) => {
      const trimmed = question.trim();
      if (!trimmed) return;

      setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
      setPending(true);
      try {
        const result = await api.askAgent(trimmed, context);
        setMessages((prev) => [
          ...prev,
          { role: "agent", text: result?.answer || "I don't have a rule that covers that yet." }
        ]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { role: "agent", text: `I couldn't reach the agent service: ${err.message}` }
        ]);
      } finally {
        setPending(false);
      }
    },
    [context]
  );

  return { messages, pending, send };
}
