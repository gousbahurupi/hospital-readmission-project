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
      const [predictionResult, explanationResult] = await Promise.all([
        api.predict(patient),
        api.explain(patient)
      ]);
      setPrediction(predictionResult);
      setExplanation(explanationResult);
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
