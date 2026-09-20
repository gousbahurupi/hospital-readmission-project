/**
 * @typedef {Object} PatientInput
 * @property {number} age
 * @property {string} gender
 * @property {number} lengthOfStay
 * @property {number} numDiagnoses
 * @property {number} numMedications
 * @property {number} numPriorAdmissions
 * @property {string} primaryDiagnosis
 * @property {boolean} hasDiabetes
 * @property {boolean} hasHeartFailure
 * @property {string} dischargeDisposition
 */

/**
 * @typedef {Object} PredictionResult
 * @property {number} riskScore        // 0-1 probability of readmission
 * @property {"low"|"medium"|"high"} riskLevel
 * @property {string[]} topFactors
 * @property {string} modelVersion
 */

/**
 * @typedef {Object} ExplanationResult
 * @property {string} summary
 * @property {{ factor: string, direction: "increases"|"decreases", detail: string }[]} contributions
 * @property {string[]} recommendations
 */

/**
 * @typedef {Object} AgentMessage
 * @property {"user"|"agent"} role
 * @property {string} text
 */

export {};
