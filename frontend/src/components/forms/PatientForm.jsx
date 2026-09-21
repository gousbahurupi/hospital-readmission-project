import { useState } from "react";

const INITIAL = {
  age: "[50-60)",
  gender: "Female",
  admission_type_id: "1",
  admission_source_id: "7",
  discharge_disposition_id: "1",
  diag_1_group: "Circulatory",
  diag_2_group: "Diabetes",
  diag_3_group: "Other",
  A1Cresult: "None",
  max_glu_serum: "None",
  diabetesMed: "Yes",
  change: "No",
  insulin: "No",
  time_in_hospital: "4",
  num_lab_procedures: "40",
  num_procedures: "1",
  num_medications: "12",
  number_diagnoses: "7"
};

const SELECTS = [
  ["age", "Age band", ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)", "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"]],
  ["gender", "Gender", ["Female", "Male"]],
  ["admission_type_id", "Admission type", ["1", "2", "3", "4", "5", "6", "7", "8"]],
  ["admission_source_id", "Admission source", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "13", "17", "20", "22", "25"]],
  ["discharge_disposition_id", "Discharge disposition", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "22", "23", "24", "25", "27", "28"]],
  ["diag_1_group", "Primary diagnosis group", ["Blood", "Circulatory", "Congenital", "Diabetes", "Digestive", "Endocrine_Metabolic", "External_Cause", "Genitourinary", "Infectious", "Injury", "Mental", "Musculoskeletal", "Neoplasms", "Nervous_System", "Pregnancy", "Respiratory", "Skin", "Supplementary", "Symptoms_IllDefined", "Unknown"]],
  ["diag_2_group", "Secondary diagnosis group", ["Blood", "Circulatory", "Congenital", "Diabetes", "Digestive", "Endocrine_Metabolic", "External_Cause", "Genitourinary", "Infectious", "Injury", "Mental", "Musculoskeletal", "Neoplasms", "Nervous_System", "Pregnancy", "Respiratory", "Skin", "Supplementary", "Symptoms_IllDefined", "Unknown"]],
  ["diag_3_group", "Third diagnosis group", ["Blood", "Circulatory", "Congenital", "Diabetes", "Digestive", "Endocrine_Metabolic", "External_Cause", "Genitourinary", "Infectious", "Injury", "Mental", "Musculoskeletal", "Neoplasms", "Nervous_System", "Pregnancy", "Respiratory", "Skin", "Supplementary", "Symptoms_IllDefined", "Unknown"]],
  ["A1Cresult", "A1C result", ["None", ">7", ">8", "Norm"]],
  ["max_glu_serum", "Maximum glucose", ["None", ">200", ">300", "Norm"]],
  ["diabetesMed", "Diabetes medication", ["No", "Yes"]],
  ["change", "Medication change", ["No", "Ch"]],
  ["insulin", "Insulin", ["No", "Down", "Steady", "Up"]]
];

const NUMBERS = [
  ["time_in_hospital", "Time in hospital", 0, 365],
  ["num_lab_procedures", "Lab procedures", 0, 200],
  ["num_procedures", "Procedures", 0, 100],
  ["num_medications", "Medications", 0, 100],
  ["number_diagnoses", "Number of diagnoses", 0, 50]
];

export function PatientForm({ onSubmit, disabled }) {
  const [values, setValues] = useState(INITIAL);
  const [touched, setTouched] = useState(false);
  const update = (name, value) => setValues((current) => ({ ...current, [name]: value }));

  function submit(event) {
    event.preventDefault();
    setTouched(true);
    if (Object.values(values).some((value) => value === "")) return;
    onSubmit({
      ...values,
      ...Object.fromEntries(NUMBERS.map(([name]) => [name, Number(values[name])])),
      admission_type_id: Number(values.admission_type_id),
      admission_source_id: Number(values.admission_source_id),
      discharge_disposition_id: Number(values.discharge_disposition_id)
    });
  }

  const inputClass = "w-full rounded-lg border border-line bg-white px-3 py-2.5 text-sm text-ink shadow-sm focus:border-teal-500";
  return (
    <form onSubmit={submit} className="space-y-7">
      <div>
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-teal-600">Patient profile</p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {SELECTS.slice(0, 2).map(([name, label, options]) => (
            <label key={name} className="text-sm font-medium text-ink/80">
              {label}
              <select className={`${inputClass} mt-1.5`} value={values[name]} onChange={(event) => update(name, event.target.value)}>
                {options.map((option) => <option key={option}>{option}</option>)}
              </select>
            </label>
          ))}
        </div>
      </div>
      <div>
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-teal-600">Admission details</p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {SELECTS.slice(2, 8).map(([name, label, options]) => (
            <label key={name} className="text-sm font-medium text-ink/80">
              {label}
              <select className={`${inputClass} mt-1.5`} value={values[name]} onChange={(event) => update(name, event.target.value)}>
                {options.map((option) => <option key={option}>{option}</option>)}
              </select>
            </label>
          ))}
        </div>
      </div>
      <div>
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-teal-600">Clinical and medication details</p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {SELECTS.slice(8).map(([name, label, options]) => (
            <label key={name} className="text-sm font-medium text-ink/80">
              {label}
              <select className={`${inputClass} mt-1.5`} value={values[name]} onChange={(event) => update(name, event.target.value)}>
                {options.map((option) => <option key={option}>{option}</option>)}
              </select>
            </label>
          ))}
        </div>
      </div>
      <div>
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-teal-600">Utilization measures</p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {NUMBERS.map(([name, label, min, max]) => (
            <label key={name} className="text-sm font-medium text-ink/80">
              {label}
              <input className={`${inputClass} mt-1.5`} type="number" min={min} max={max} value={values[name]} onChange={(event) => update(name, event.target.value)} />
              {touched && values[name] === "" && <span className="mt-1 block text-xs text-risk-high">Required.</span>}
            </label>
          ))}
        </div>
      </div>
      <div className="flex items-center gap-3 border-t border-line pt-5">
        <button type="submit" disabled={disabled} className="rounded-lg bg-teal-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:opacity-50">
          {disabled ? "Generating assessment…" : "Generate assessment"}
        </button>
        <button type="button" onClick={() => { setValues(INITIAL); setTouched(false); }} className="rounded-lg px-4 py-3 text-sm font-medium text-ink/60 transition hover:bg-teal-50 hover:text-ink">
          Clear form
        </button>
      </div>
    </form>
  );
}
