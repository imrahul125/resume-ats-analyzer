import type { ReactNode } from 'react'

interface FeatureCardProps {
  number: string
  title: string
  description: string
  icon: ReactNode
}

export default function FeatureCard({
  number,
  title,
  description,
  icon,
}: FeatureCardProps) {
  return (
    <article className="group rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm shadow-slate-200/40 transition duration-200 hover:-translate-y-1 hover:border-indigo-200 hover:shadow-lg hover:shadow-indigo-100/50">
      <div className="flex items-start justify-between">
        <span className="flex size-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-700">
          {icon}
        </span>
        <span className="font-mono text-xs tracking-wide text-slate-400">{number}</span>
      </div>
      <h3 className="mt-5 text-lg font-semibold tracking-tight text-slate-900">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-slate-600">{description}</p>
    </article>
  )
}
