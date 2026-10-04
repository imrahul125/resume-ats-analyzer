export type SkillStatus = 'matched' | 'partial' | 'missing'
export type RequirementKind = 'required' | 'preferred'

export interface MetricResult {
  key: string
  label: string
  score: number
  weight: number
  explanation: string
}

export interface SkillResult {
  name: string
  status: SkillStatus
  requirement: RequirementKind
}

export interface RecommendationResult {
  priority: 'high' | 'medium' | 'low'
  category: string
  message: string
}

export interface AnalysisResult {
  id: string
  overall_score: number
  resume_text_length: number
  metrics: MetricResult[]
  skills: SkillResult[]
  recommendations: RecommendationResult[]
}
