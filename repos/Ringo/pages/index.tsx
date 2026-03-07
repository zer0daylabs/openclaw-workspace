"use client"

import Link from 'next/link'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 text-white">
      <div className="container mx-auto px-4 py-16">
        <nav className="flex justify-between items-center mb-16">
          <h1 className="text-4xl font-bold">🚀 Ringo</h1>
          <div className="space-x-4">
            <Link href="/login" className="px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-gray-100 transition">
              Login
            </Link>
            <Link href="/register" className="px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-gray-100 transition">
              Sign Up
            </Link>
          </div>
        </nav>

        <div className="text-center mb-16">
          <h2 className="text-6xl font-bold mb-6">Real-Time Lead Marketplace</h2>
          <p className="text-2xl mb-8 opacity-90">
            Where buyers bid on high-quality calls and sellers get paid instantly
          </p>
          <Link 
            href="/register" 
            className="inline-block px-8 py-4 bg-white text-purple-600 text-xl font-bold rounded-lg hover:bg-gray-100 transition transform hover:scale-105 shadow-xl"
          >
            Start Selling Leads Today
          </Link>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl border border-white/20">
            <h3 className="text-2xl font-bold mb-4">⚡ Fast Routing</h3>
            <p className="opacity-80">Sub-50ms call routing powered by Redis caching</p>
          </div>
          <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl border border-white/20">
            <h3 className="text-2xl font-bold mb-4">🤖 AI Pre-Screening</h3>
            <p className="opacity-80">Real-time call qualification and lead enrichment</p>
          </div>
          <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl border border-white/20">
            <h3 className="text-2xl font-bold mb-4">💰 Instant Payouts</h3>
            <p className="opacity-80">Get paid the same day through Stripe</p>
          </div>
        </div>
      </div>
    </div>
  )
}
