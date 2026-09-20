export function Card({ title, eyebrow, action, children, className = "" }) {
  return (
    <section className={`bg-white border border-line rounded-sm ${className}`}>
      {(title || action) && (
        <header className="flex items-baseline justify-between gap-4 px-5 pt-4 pb-3 border-b border-line">
          <div>
            {eyebrow && <p className="text-xs text-teal-500 font-medium mb-0.5">{eyebrow}</p>}
            {title && <h2 className="font-display text-lg text-ink">{title}</h2>}
          </div>
          {action}
        </header>
      )}
      <div className="px-5 py-4">{children}</div>
    </section>
  );
}
