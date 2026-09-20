import { useState } from "react";

const EMPTY_PATIENT = {
  age: "",
  gender: "female",
  lengthOfStay: "",
  numDiagnoses: "",
  numMedications: "",
  numPriorAdmissions: "",
  primaryDiagnosis: "",
  hasDiabetes: false,
  hasHeartFailure: false,
  dischargeDisposition: "home"
};

const NUMBER_FIELDS = [
  { name: "age", label: "Age (years)", min: 0, max: 120 },
  { name: "lengthOfStay", label: "Length of stay (days)", min: 0, max: 365 },
  { name: "numDiagnoses", label: "Number of diagnoses", min: 0, max: 50 },
  { name: "numMedications", label: "Number of medications", min: 0, max: 60 },
  { name: "numPriorAdmissions", label: "Prior admissions (12 mo)", min: 0, max: 30 }
];

export function PatientForm({ onSubmit, disabled }) {
  const [patient, setPatient] = useState(EMPTY_PATIENT);
  const [touched, setTouched] = useState(false);

  const update = (field, value) => setPatient((prev) => ({ ...prev, [field]: value }));

  const missingRequired = NUMBER_FIELDS.some((f) => patient[f.name] === "") || !patient.primaryDiagnosis.trim();

  function handleSubmit(e) {
    e.preventDefault();
    setTouched(true);
    if (missingRequired) return;
    onSubmit({
      ...patient,
      age: Number(patient.age),
      lengthOfStay: Number(patient.lengthOfStay),
      numDiagnoses: Number(patient.numDiagnoses),
      numMedications: Number(patient.numMedications),
      numPriorAdmissions: Number(patient.numPriorAdmissions)
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        {NUMBER_FIELDS.map((f) => (
          <div key={f.name}>
            <label className="block text-sm font-medium text-ink/80 mb-1" htmlFor={f.name}>
              {f.label}
            </label>
            <input
              id={f.name}
              type="number"
              min={f.min}
              max={f.max}
              value={patient[f.name]}
              onChange={(e) => update(f.name, e.target.value)}
              className="w-full border border-line rounded-sm px-3 py-2 text-sm focus:border-teal-500"
            />
            {touched && patient[f.name] === "" && (
              <p className="text-xs text-risk-high mt-1">Required.</p>
            )}
          </div>
        ))}

        <div>
          <label className="block text-sm font-medium text-ink/80 mb-1" htmlFor="gender">
            Gender
          </label>
          <select
            id="gender"
            value={patient.gender}
            onChange={(e) => update("gender", e.target.value)}
            className="w-full border border-line rounded-sm px-3 py-2 text-sm bg-white focus:border-teal-500"
          >
            <option value="female">Female</option>
            <option value="male">Male</option>
            <option value="other">Other / unspecified</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-ink/80 mb-1" htmlFor="dischargeDisposition">
            Discharge disposition
          </label>
          <select
            id="dischargeDisposition"
            value={patient.dischargeDisposition}
            onChange={(e) => update("dischargeDisposition", e.target.value)}
            className="w-full border border-line rounded-sm px-3 py-2 text-sm bg-white focus:border-teal-500"
          >
            <option value="home">Home</option>
            <option value="home_health">Home with home health</option>
            <option value="snf">Skilled nursing facility</option>
            <option value="rehab">Rehabilitation facility</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-ink/80 mb-1" htmlFor="primaryDiagnosis">
          Primary diagnosis
        </label>
        <input
          id="primaryDiagnosis"
          type="text"
          placeholder="e.g. Congestive heart failure"
          value={patient.primaryDiagnosis}
          onChange={(e) => update("primaryDiagnosis", e.target.value)}
          className="w-full border border-line rounded-sm px-3 py-2 text-sm focus:border-teal-500"
        />
        {touched && !patient.primaryDiagnosis.trim() && (
          <p className="text-xs text-risk-high mt-1">Required.</p>
        )}
      </div>

      <div className="flex gap-6">
        <label className="flex items-center gap-2 text-sm text-ink/80">
          <input
            type="checkbox"
            checked={patient.hasDiabetes}
            onChange={(e) => update("hasDiabetes", e.target.checked)}
            className="h-4 w-4 accent-teal-500"
          />
          Diabetes
        </label>
        <label className="flex items-center gap-2 text-sm text-ink/80">
          <input
            type="checkbox"
            checked={patient.hasHeartFailure}
            onChange={(e) => update("hasHeartFailure", e.target.checked)}
            className="h-4 w-4 accent-teal-500"
          />
          Heart failure history
        </label>
      </div>

      <div className="flex items-center gap-3 pt-2">
        <button
          type="submit"
          disabled={disabled}
          className="bg-teal-500 text-white text-sm font-medium px-5 py-2.5 rounded-sm hover:bg-teal-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {disabled ? "Generating…" : "Generate prediction"}
        </button>
        <button
          type="button"
          onClick={() => {
            setPatient(EMPTY_PATIENT);
            setTouched(false);
          }}
          className="text-sm text-ink/60 hover:text-ink px-3 py-2.5"
        >
          Clear form
        </button>
      </div>
    </form>
  );
}
