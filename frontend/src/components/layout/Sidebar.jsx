import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/", label: "Overview", end: true },
  { to: "/assessment", label: "New assessment" },
  { to: "/agent", label: "Ask the agent" },
  { to: "/model-info", label: "About the model" }
];

export function Sidebar() {
  return (
    <aside className="w-60 shrink-0 border-r border-line bg-white flex flex-col">
      <div className="px-5 py-5 border-b border-line">
        <p className="font-display text-xl leading-tight text-ink">Readmission<br />Risk Console</p>
      </div>
      <nav className="flex-1 px-3 py-4 flex flex-col gap-1">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              `px-3 py-2 rounded-sm text-sm font-medium transition-colors ${
                isActive ? "bg-teal-500 text-white" : "text-ink/80 hover:bg-teal-50"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="px-5 py-4 border-t border-line text-xs text-ink/50 leading-relaxed">
        Decision support only. Confirm findings against the patient chart before acting.
      </div>
    </aside>
  );
}
