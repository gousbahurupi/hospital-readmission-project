import { Link } from "react-router-dom";
import { TopBar } from "../components/layout/TopBar.jsx";
import { Card } from "../components/common/Card.jsx";

export function Dashboard() {
  return (
    <div className="flex-1 flex flex-col">
      <TopBar
        title="Overview"
        subtitle="A clinical decision-support tool that estimates 30-day readmission risk and explains the reasoning behind each score."
      />
      <div className="p-8 grid grid-cols-3 gap-5">
        <Card title="New assessment" eyebrow="Step 1" className="col-span-2">
          <p className="text-sm text-ink/70 mb-4 max-w-prose">
            Enter a patient's clinical and administrative details to generate a readmission risk
            score, along with the factors driving that score.
          </p>
          <Link
            to="/assessment"
            className="inline-block bg-teal-500 text-white text-sm font-medium px-4 py-2 rounded-sm hover:bg-teal-600"
          >
            Start an assessment
          </Link>
        </Card>

        <Card title="Ask the agent" eyebrow="Step 2">
          <p className="text-sm text-ink/70 mb-4">
            Once you have a result, ask plain-language questions about what it means.
          </p>
          <Link to="/agent" className="text-sm font-medium text-teal-500 hover:text-teal-600">
            Open the agent →
          </Link>
        </Card>

        <Card title="How predictions are made" className="col-span-3">
          <ol className="grid grid-cols-3 gap-6 text-sm text-ink/70">
            <li>
              <p className="font-medium text-ink mb-1">1. Preprocessing</p>
              Patient fields are validated and transformed to match the model's training format.
            </li>
            <li>
              <p className="font-medium text-ink mb-1">2. Prediction</p>
              A trained scikit-learn model scores the readmission probability.
            </li>
            <li>
              <p className="font-medium text-ink mb-1">3. Explanation</p>
              The rule-based agent translates the score into contributing factors and next steps.
            </li>
          </ol>
        </Card>
      </div>
    </div>
  );
}
