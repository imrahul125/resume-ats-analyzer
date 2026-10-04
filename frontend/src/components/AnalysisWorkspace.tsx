import { useState, type FormEvent } from 'react'
import ApiStatusBadge from './ApiStatusBadge'
import { analyzeResume } from '../services/api'
import type { AnalysisResult, SkillStatus } from '../types/analysis'

const MAX_UPLOAD_BYTES = 10 * 1024 * 1024

const skillStyles: Record<SkillStatus, string> = {
  matched: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  partial: 'border-amber-200 bg-amber-50 text-amber-800',
  missing: 'border-rose-200 bg-rose-50 text-rose-800',
}

export default function AnalysisWorkspace() {
  const [file, setFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [jobTitle, setJobTitle] = useState('')
  const [company, setCompany] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<AnalysisResult | null>(null)

  function chooseFile(candidate: File | undefined) {
    setError('')
    setResult(null)
    if (!candidate) {
      setFile(null)
      return
    }
    const extension = candidate.name.split('.').pop()?.toLowerCase()
    if (extension !== 'pdf' && extension !== 'docx') {
      setFile(null)
      setError('Choose a PDF or DOCX resume.')
      return
    }
    if (candidate.size > MAX_UPLOAD_BYTES) {
      setFile(null)
      setError('The resume must be 10 MB or smaller.')
      return
    }
    setFile(candidate)
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setResult(null)
    if (!file) {
      setError('Choose a PDF or DOCX resume to continue.')
      return
    }
    if (!jobDescription.trim()) {
      setError('Paste the job description to continue.')
      return
    }

    setBusy(true)
    try {
      const response = await analyzeResume({ file, jobDescription, jobTitle, company })
      setResult(response)
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Analysis failed. Please try again.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="px-5 pb-20 sm:px-8 sm:pb-24" id="analysis">
      <div className="mx-auto max-w-5xl overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-xl shadow-slate-200/60">
        <div className="flex flex-col gap-5 border-b border-slate-200 bg-slate-950 px-6 py-8 text-white sm:flex-row sm:items-center sm:justify-between sm:px-10">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-300">Analysis workspace</p>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">Compare your resume with a job</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Your Job Match Score is an explainable estimate based on this job description, not a universal ATS score.</p>
          </div>
          <ApiStatusBadge />
        </div>

        <form className="grid gap-6 p-6 sm:p-10" onSubmit={submit}>
          <div>
            <label className="mb-2 block text-sm font-semibold text-slate-800" htmlFor="resume-file">Resume file</label>
            <input
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              className="block w-full rounded-xl border border-slate-300 bg-slate-50 p-3 text-sm text-slate-700 file:mr-4 file:rounded-full file:border-0 file:bg-indigo-600 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-indigo-700 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600"
              id="resume-file"
              onChange={(event) => chooseFile(event.currentTarget.files?.[0])}
              type="file"
            />
            <p className="mt-2 text-xs text-slate-500">PDF or DOCX, up to 10 MB. The uploaded file is processed temporarily and is not stored.</p>
            {file && <p className="mt-2 text-sm font-medium text-slate-700">Selected: {file.name}</p>}
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-800" htmlFor="job-title">Job title <span className="font-normal text-slate-500">(optional)</span></label>
              <input className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" id="job-title" maxLength={255} onChange={(event) => setJobTitle(event.target.value)} placeholder="e.g. Product Engineer" value={jobTitle} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-800" htmlFor="company">Company <span className="font-normal text-slate-500">(optional)</span></label>
              <input className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" id="company" maxLength={255} onChange={(event) => setCompany(event.target.value)} placeholder="Company name" value={company} />
            </div>
          </div>

          <div>
            <label className="mb-2 block text-sm font-semibold text-slate-800" htmlFor="job-description">Job description</label>
            <textarea className="min-h-52 w-full rounded-xl border border-slate-300 px-4 py-3 text-sm leading-6 outline-none transition placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100" id="job-description" maxLength={50000} onChange={(event) => setJobDescription(event.target.value)} placeholder="Paste the complete job description here…" required value={jobDescription} />
            <p className="mt-2 text-xs text-slate-500">The analyzer uses a defined skill list and transparent text-based rules. It can miss requirements that need human judgment.</p>
          </div>

          {error && <div aria-live="polite" className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800" role="alert">{error}</div>}

          <div className="flex flex-col items-start gap-3 border-t border-slate-100 pt-5 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-xs leading-5 text-slate-500">The uploaded file and extracted resume text are not saved. The job description and analysis results are saved for this MVP.</p>
            <button className="inline-flex min-w-48 items-center justify-center gap-2 rounded-full bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-md shadow-indigo-200 transition hover:bg-indigo-700 disabled:cursor-wait disabled:opacity-60" disabled={busy} type="submit">
              {busy ? 'Analyzing resume…' : 'Analyze my resume'}
              {!busy && <span aria-hidden="true">→</span>}
            </button>
          </div>
        </form>

        {result && <AnalysisResults result={result} />}
      </div>
    </section>
  )
}

function AnalysisResults({ result }: { result: AnalysisResult }) {
  const groups: { status: SkillStatus; title: string; symbol: string }[] = [
    { status: 'matched', title: 'Matched', symbol: '✓' },
    { status: 'partial', title: 'Partial match', symbol: '△' },
    { status: 'missing', title: 'Not found', symbol: '×' },
  ]

  return (
    <section aria-labelledby="results-heading" className="border-t border-slate-200 bg-slate-50/70 p-6 sm:p-10">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center">
        <div aria-label={`Job Match Score ${result.overall_score} out of 100`} className="flex size-32 shrink-0 flex-col items-center justify-center rounded-full border-[9px] border-indigo-100 bg-white shadow-sm">
          <span className="text-4xl font-bold tracking-tight text-slate-950">{result.overall_score}</span>
          <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">of 100</span>
        </div>
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-indigo-700">Job Match Score</p>
          <h3 className="mt-1 text-2xl font-semibold tracking-tight text-slate-950" id="results-heading">Your analysis is ready</h3>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">This internal estimate is derived from the listed factors below. It does not reproduce any employer's ATS algorithm.</p>
          <p className="mt-2 text-xs text-slate-500">Analysis ID: <span className="font-mono">{result.id}</span></p>
        </div>
      </div>

      <div className="mt-9 grid gap-3 md:grid-cols-2">
        {result.metrics.map((metric) => (
          <article className="rounded-2xl border border-slate-200 bg-white p-4" key={metric.key}>
            <div className="flex items-center justify-between gap-4 text-sm">
              <h4 className="font-semibold text-slate-800">{metric.label}</h4>
              <span className="font-semibold tabular-nums text-slate-950">{metric.score}<span className="text-slate-400"> / 100</span></span>
            </div>
            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100" role="meter" aria-label={metric.label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={metric.score}>
              <div className="h-full rounded-full bg-indigo-500" style={{ width: `${metric.score}%` }} />
            </div>
            <p className="mt-2 text-xs leading-5 text-slate-500">Weight: {Math.round(metric.weight * 100)}%. {metric.explanation}</p>
          </article>
        ))}
      </div>

      <div className="mt-9">
        <h4 className="text-lg font-semibold text-slate-900">Job requirements</h4>
        <p className="mt-1 text-sm text-slate-600">Required/preferred labels are inferred from wording and headings in the job description.</p>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          {groups.map((group) => {
            const skills = result.skills.filter((skill) => skill.status === group.status)
            return (
              <div className="rounded-2xl border border-slate-200 bg-white p-4" key={group.status}>
                <h5 className="text-sm font-semibold text-slate-800">{group.title} <span className="text-slate-400">({skills.length})</span></h5>
                {skills.length ? (
                  <ul className="mt-3 flex flex-wrap gap-2">
                    {skills.map((skill) => <li className={`rounded-full border px-3 py-1.5 text-xs font-medium ${skillStyles[skill.status]}`} key={skill.name}>{group.symbol} {skill.name} · {skill.requirement}</li>)}
                  </ul>
                ) : <p className="mt-3 text-xs text-slate-500">No requirements in this group.</p>}
              </div>
            )
          })}
        </div>
      </div>

      <div className="mt-9">
        <h4 className="text-lg font-semibold text-slate-900">Recommendations</h4>
        {result.recommendations.length ? (
          <ul className="mt-3 space-y-3">
            {result.recommendations.map((item, index) => (
              <li className="rounded-xl border border-slate-200 bg-white p-4" key={`${item.category}-${index}`}>
                <span className={`mr-2 inline-block rounded-full px-2.5 py-1 text-[11px] font-bold uppercase ${item.priority === 'high' ? 'bg-rose-100 text-rose-800' : item.priority === 'medium' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'}`}>{item.priority} priority</span>
                <span className="text-sm leading-6 text-slate-700">{item.message}</span>
              </li>
            ))}
          </ul>
        ) : <p className="mt-3 rounded-xl bg-white p-4 text-sm text-slate-600">No immediate gaps were found by these deterministic checks. Review the job description manually as well.</p>}
      </div>
    </section>
  )
}
