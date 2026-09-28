import BrandMark from '../components/BrandMark'
import FeatureCard from '../components/FeatureCard'

const features = [
  {
    number: '01',
    title: 'Job-specific match',
    description:
      'See how your experience lines up with the role you chose, with a score you can trace back to clear factors.',
    icon: (
      <svg aria-hidden="true" className="size-5" fill="none" viewBox="0 0 24 24">
        <path d="M5 19V9m7 10V5m7 14v-7" stroke="currentColor" strokeLinecap="round" strokeWidth="2" />
      </svg>
    ),
  },
  {
    number: '02',
    title: 'Skill gap detection',
    description:
      'Separate matched, partial, and missing requirements so you can see where your evidence is strongest.',
    icon: (
      <svg aria-hidden="true" className="size-5" fill="none" viewBox="0 0 24 24">
        <path d="m5 12 4 4L19 6" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    ),
  },
  {
    number: '03',
    title: 'ATS-style checks',
    description:
      'Catch detectable structure and text issues that can make a resume harder for software to read.',
    icon: (
      <svg aria-hidden="true" className="size-5" fill="none" viewBox="0 0 24 24">
        <path d="M7 4.75h7l4 4v10.5H7z" stroke="currentColor" strokeLinejoin="round" strokeWidth="1.8" />
        <path d="M14 5v4h4M10 13h5M10 16h5" stroke="currentColor" strokeLinecap="round" strokeWidth="1.8" />
      </svg>
    ),
  },
  {
    number: '04',
    title: 'Clear recommendations',
    description:
      'Get practical suggestions grounded in your resume, with unsupported job requirements called out honestly.',
    icon: (
      <svg aria-hidden="true" className="size-5" fill="none" viewBox="0 0 24 24">
        <path d="M12 3.75v2m0 12.5v2M4.6 6.6 6 8m12 12 1.4 1.4M3.75 12h2m12.5 0h2M4.6 17.4 6 16m12-12 1.4-1.4" stroke="currentColor" strokeLinecap="round" strokeWidth="1.8" />
        <circle cx="12" cy="12" r="4.2" stroke="currentColor" strokeWidth="1.8" />
      </svg>
    ),
  },
  {
    number: '05',
    title: 'Truthful tailoring',
    description:
      'Bring relevant existing experience forward and improve clarity without making up skills or achievements.',
    icon: (
      <svg aria-hidden="true" className="size-5" fill="none" viewBox="0 0 24 24">
        <path d="m14.5 5.5 4 4M4.5 19.5l3.7-.8L19 7.9a2.8 2.8 0 0 0-4-4L4.2 14.7l.3 4.8Z" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" />
      </svg>
    ),
  },
  {
    number: '06',
    title: 'ATS-friendly PDF',
    description:
      'Export a clean, readable resume with standard headings and a simple layout designed for text parsing.',
    icon: (
      <svg aria-hidden="true" className="size-5" fill="none" viewBox="0 0 24 24">
        <path d="M6 3.75h8l4 4v12.5H6z" stroke="currentColor" strokeLinejoin="round" strokeWidth="1.8" />
        <path d="M14 4v4h4M9 14h6m-6 3h6" stroke="currentColor" strokeLinecap="round" strokeWidth="1.8" />
      </svg>
    ),
  },
]

function SampleMatchCard() {
  return (
    <div className="relative mx-auto w-full max-w-[490px]">
      <div aria-hidden="true" className="absolute -inset-5 rounded-[2rem] bg-gradient-to-br from-indigo-200/60 via-sky-100/30 to-emerald-100/70 blur-2xl" />
      <article className="relative overflow-hidden rounded-[1.75rem] border border-white/80 bg-white p-6 shadow-2xl shadow-slate-300/50 sm:p-7">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">Example analysis</p>
            <h2 className="mt-1 text-lg font-semibold tracking-tight text-slate-900">Product Engineer</h2>
          </div>
          <span className="rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-[11px] font-semibold text-indigo-700">Sample data</span>
        </div>

        <div className="mt-6 flex items-center gap-5 rounded-2xl bg-slate-50 p-4 sm:p-5">
          <div className="relative flex size-[94px] shrink-0 items-center justify-center rounded-full bg-[conic-gradient(#4f46e5_0deg_295deg,#e2e8f0_295deg_360deg)] p-[7px]">
            <div className="flex size-full flex-col items-center justify-center rounded-full bg-white">
              <span className="text-[26px] font-bold leading-none tracking-tight text-slate-900">82</span>
              <span className="mt-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400">of 100</span>
            </div>
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">Strong starting match</p>
            <p className="mt-1 text-xs leading-5 text-slate-500">A job-specific estimate, explained by each factor below.</p>
          </div>
        </div>

        <div className="mt-6 space-y-4">
          <ScoreRow label="Skills & keywords" value={84} color="bg-indigo-500" />
          <ScoreRow label="Required experience" value={77} color="bg-sky-500" />
          <ScoreRow label="Resume structure" value={92} color="bg-emerald-500" />
        </div>

        <div className="mt-6 border-t border-slate-100 pt-5">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">Skills at a glance</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <SkillPill kind="matched" label="React" />
            <SkillPill kind="matched" label="SQL" />
            <SkillPill kind="partial" label="REST APIs" />
            <SkillPill kind="missing" label="AWS" />
          </div>
        </div>
      </article>
      <p className="relative mt-3 text-center text-[11px] text-slate-400">Illustrative example only — not a candidate result</p>
    </div>
  )
}

function ScoreRow({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between text-xs">
        <span className="font-medium text-slate-600">{label}</span>
        <span className="font-semibold tabular-nums text-slate-800">{value}</span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-slate-100">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  )
}

function SkillPill({ label, kind }: { label: string; kind: 'matched' | 'partial' | 'missing' }) {
  const style = {
    matched: 'border-emerald-100 bg-emerald-50 text-emerald-700',
    partial: 'border-amber-100 bg-amber-50 text-amber-700',
    missing: 'border-rose-100 bg-rose-50 text-rose-700',
  }[kind]

  return <span className={`rounded-full border px-2.5 py-1 text-[11px] font-medium ${style}`}>{label}</span>
}

export default function LandingPage() {
  return (
    <div className="min-h-screen overflow-hidden bg-[#f8f9fd] text-slate-900">
      <header className="relative z-10 border-b border-slate-200/70 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
          <a aria-label="ResumeLens home" className="no-underline" href="#top">
            <BrandMark />
          </a>
          <nav aria-label="Main navigation" className="hidden items-center gap-8 md:flex">
            <a className="text-sm font-medium text-slate-600 transition hover:text-indigo-700" href="#features">What you get</a>
            <a className="text-sm font-medium text-slate-600 transition hover:text-indigo-700" href="#how-it-works">How it works</a>
          </nav>
          <a className="inline-flex items-center gap-2 rounded-full bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" href="#analysis">
            Analyze my resume
            <span aria-hidden="true">→</span>
          </a>
        </div>
      </header>

      <main id="top">
        <section className="relative mx-auto grid max-w-7xl items-center gap-12 px-5 pb-20 pt-14 sm:px-8 sm:pt-20 lg:grid-cols-[1.05fr_0.95fr] lg:gap-8 lg:pb-28 lg:pt-24">
          <div aria-hidden="true" className="pointer-events-none absolute -left-56 top-0 size-[480px] rounded-full bg-indigo-200/30 blur-3xl" />
          <div className="relative">
            <div className="inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-white/80 px-3 py-1.5 text-xs font-semibold text-indigo-700 shadow-sm shadow-indigo-100/70">
              <span className="size-1.5 rounded-full bg-emerald-500" />
              Built around the job you want
            </div>
            <h1 className="mt-6 max-w-2xl text-[2.7rem] font-semibold leading-[1.06] tracking-[-0.055em] text-slate-950 sm:text-6xl lg:text-[4.2rem]">
              Analyze your resume <span className="text-indigo-600">against the job.</span>
            </h1>
            <p className="mt-6 max-w-xl text-base leading-7 text-slate-600 sm:text-lg sm:leading-8">
              Upload your resume. Paste the job description. See what matches, what is missing, and how to improve it.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
              <a className="inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-200/80 transition hover:-translate-y-0.5 hover:bg-indigo-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" href="#analysis">
                Analyze My Resume <span aria-hidden="true">→</span>
              </a>
              <a className="inline-flex items-center justify-center rounded-full px-5 py-3.5 text-sm font-semibold text-slate-600 transition hover:bg-white hover:text-slate-900" href="#how-it-works">
                See how it works
              </a>
            </div>
            <p className="mt-6 flex items-start gap-2 text-xs leading-5 text-slate-500 sm:text-sm">
              <svg aria-hidden="true" className="mt-0.5 size-4 shrink-0 text-indigo-600" fill="none" viewBox="0 0 20 20">
                <path d="m4.5 10.2 3.4 3.3 7.6-7.2" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" />
              </svg>
              Your score is based on the specific job description you provide — not a universal ATS score.
            </p>
          </div>

          <div className="relative lg:pl-3">
            <SampleMatchCard />
          </div>
        </section>

        <section className="border-y border-slate-200/80 bg-white" id="how-it-works">
          <div className="mx-auto grid max-w-7xl gap-8 px-5 py-12 sm:px-8 md:grid-cols-3 md:gap-0">
            <Step number="01" title="Bring the role" text="Start with the job description you actually plan to apply for." />
            <Step number="02" title="Compare evidence" text="See where your experience supports the role and where it does not." />
            <Step number="03" title="Choose your next move" text="Use clear recommendations to improve your application truthfully." />
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8 sm:py-24" id="features">
          <div className="mx-auto max-w-2xl text-center">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-600">A clearer application process</p>
            <h2 className="mt-4 text-3xl font-semibold tracking-[-0.04em] text-slate-950 sm:text-4xl">Understand the match. Improve the story.</h2>
            <p className="mt-4 text-base leading-7 text-slate-600">ResumeLens shows its reasoning, so you can decide what to change — and what should stay true to your experience.</p>
          </div>
          <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => <FeatureCard key={feature.number} {...feature} />)}
          </div>
        </section>

        <section className="px-5 pb-20 sm:px-8 sm:pb-24" id="analysis">
          <div className="mx-auto max-w-5xl overflow-hidden rounded-[2rem] bg-slate-950 px-6 py-9 text-white shadow-xl shadow-slate-300/50 sm:px-10 sm:py-12">
            <div className="grid items-center gap-8 md:grid-cols-[1fr_auto]">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-300">Analysis workspace</p>
                <h2 className="mt-3 max-w-2xl text-2xl font-semibold tracking-[-0.04em] sm:text-3xl">Your resume and job description will meet here.</h2>
                <p className="mt-3 max-w-xl text-sm leading-6 text-slate-300">The upload and analysis flow is being connected next. This page is a product preview; it does not upload or store a resume.</p>
              </div>
              <span className="inline-flex w-fit items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-xs font-medium text-slate-200">
                <span className="size-1.5 rounded-full bg-amber-300" />
                Coming in the next build phase
              </span>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-5 py-6 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-8">
          <BrandMark />
          <p>The Job Match Score is an estimate based on the job description you provide.</p>
        </div>
      </footer>
    </div>
  )
}

function Step({ number, title, text }: { number: string; title: string; text: string }) {
  return (
    <div className="flex gap-4 md:px-8 first:md:pl-0 last:md:pr-0 md:border-r md:border-slate-200 last:md:border-r-0">
      <span className="font-mono text-xs font-semibold text-indigo-600">{number}</span>
      <div>
        <h3 className="text-sm font-semibold text-slate-900">{title}</h3>
        <p className="mt-1.5 text-sm leading-6 text-slate-500">{text}</p>
      </div>
    </div>
  )
}
