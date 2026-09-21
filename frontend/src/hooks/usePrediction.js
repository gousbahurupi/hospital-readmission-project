import { useState, useCallback } from "react";
import { api } from "../services/api.js";

/**
 * Runs prediction + explanation together and tracks request state.
 */
export function usePrediction() {
  const [status, setStatus] = useState("idle"); // idle | loading | success | error
  const [prediction, setPrediction] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [error, setError] = useState(null);
  const [lastPatient, setLastPatient] = useState(null);

  const run = useCallback(async (patient) => {
    setStatus("loading");
    setError(null);
    setLastPatient(patient);
    try {
      const result = await api.assess(patient);
      const probability = result.prediction.model_estimated_probability;
      setPrediction({
        riskScore: probability,
        riskLevel: probability >= 0.5 ? "high" : probability >= 0.25 ? "medium" : "low",
        prediction: result.prediction
      });
      setExplanation({
        summary: result.explanation.answer,
        contributions: (result.explanation.prediction?.top_contributing_factors || []).map((factor) => ({
          factor,
          direction: "increases",
          detail: "Included in the assistant's model-result context."
        })),
        recommendations: result.explanation.suggested_questions || [],
        disclaimer: result.explanation.disclaimer
      });
      setStatus("success");
    } catch (err) {
      setError(err.message || "Something went wrong while generating the prediction.");
      setStatus("error");
    }
  }, []);

  const reset = useCallback(() => {
    setStatus("idle");
    setPrediction(null);
    setExplanation(null);
    setError(null);
    setLastPatient(null);
  }, []);

  return { status, prediction, explanation, error, lastPatient, run, reset };
}
