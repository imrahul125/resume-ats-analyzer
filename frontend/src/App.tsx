import LandingPage from './pages/LandingPage'

export default function App() {
  return (
    <>
      <LandingPage />
      <div className="border-t border-slate-200 bg-white px-5 py-3 text-center text-xs text-slate-500">
        Built by <a className="font-semibold text-slate-700 transition hover:text-indigo-600" href="https://github.com/imrahul125" rel="noreferrer" target="_blank">Rahul Bhagwat</a>
      </div>
    </>
  )
}
