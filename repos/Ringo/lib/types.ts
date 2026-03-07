// lib/types.ts

export interface User {
  id: string
  name: string
  email: string
  role: 'buyer' | 'seller' | 'both'
  creditBalance: number
}

export interface PhoneNumber {
  id: string
  number: string
  status: 'active' | 'inactive' | 'reserved'
  campaigns: Campaign[]
}

export interface Campaign {
  id: string
  name: string
  number: string
  categories: LeadCategory[]
  volumeQuota: number
  isActive: boolean
}

export interface LeadCategory {
  id: string
  name: string
  premium: number
  subcategories?: LeadCategory[]
}

export interface Bid {
  id: string
  categoryId: string
  categoryName: string
  amountPerCall: number
  amountPerMinute: number
  quota: number
  usedQuota: number
  status: 'active' | 'paused' | 'completed'
}

export interface Lead {
  id: string
  category: string
  callerName: string
  phoneNumber: string
  needs: string
  budget: string
  timeframe: string
  score: number
  status: 'qualified' | 'dropped' | 'no-answer'
  timestamp: string
}

export interface Analytics {
  revenue: number
  calls: number
  conversions: number
  avgRevenuePerCall: number
  byCategory: { name: string; revenue: number; percentage: number }[]
}
