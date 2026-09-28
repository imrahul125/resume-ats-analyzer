export default function BrandMark() {
  return (
    <span className="inline-flex items-center gap-2.5 font-semibold tracking-tight text-slate-950">
      <span className="flex size-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-sm shadow-indigo-200">
        <svg
          aria-hidden="true"
          className="size-5"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle cx="10.8" cy="10.8" r="6.4" stroke="currentColor" strokeWidth="2" />
          <path d="m15.5 15.5 4.2 4.2" stroke="currentColor" strokeLinecap="round" strokeWidth="2" />
          <path d="M8.2 11.1h5.2M10.8 8.5v5.2" stroke="#c7d2fe" strokeLinecap="round" strokeWidth="1.6" />
        </svg>
      </span>
      <span className="text-[17px]">ResumeLens</span>
    </span>
  )
}
