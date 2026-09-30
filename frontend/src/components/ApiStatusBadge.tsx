import { useEffect, useState } from 'react'

import { checkDatabaseHealth } from '../services/api'

type ServiceStatus = 'checking' | 'connected' | 'unavailable'

const statusStyles: Record<ServiceStatus, string> = {
  checking: 'bg-amber-300',
  connected: 'bg-emerald-400',
  unavailable: 'bg-rose-400',
}

const statusLabels: Record<ServiceStatus, string> = {
  checking: 'Checking analysis service…',
  connected: 'Analysis service connected',
  unavailable: 'Analysis service unavailable',
}

export default function ApiStatusBadge() {
  const [status, setStatus] = useState<ServiceStatus>('checking')

  useEffect(() => {
    let active = true

    const refreshStatus = async () => {
      try {
        await checkDatabaseHealth()
        if (active) setStatus('connected')
      } catch {
        if (active) setStatus('unavailable')
      }
    }

    void refreshStatus()
    const intervalId = window.setInterval(() => void refreshStatus(), 30_000)

    return () => {
      active = false
      window.clearInterval(intervalId)
    }
  }, [])

  return (
    <span
      aria-live="polite"
      className="inline-flex w-fit items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-xs font-medium text-slate-200"
      role="status"
      title="Checks that the API can reach PostgreSQL"
    >
      <span aria-hidden="true" className={`size-1.5 rounded-full ${statusStyles[status]}`} />
      {statusLabels[status]}
    </span>
  )
}
