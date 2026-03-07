'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('overview')
  const router = useRouter()

  // Mock data - will connect to API later
  const credits = 250000 // $2,500 in cents
  const revenue = 84250 // $842.50
  const calls = 127
  const conversions = 43

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'funding', label: 'Credit Funding' },
    { id: 'bids', label: 'Manage Bids' },
    { id: 'leads', label: 'Lead Marketplace' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'payouts', label: 'Payouts' },
  ]

  if (!localStorage.getItem('ringo-user')) {
    router.push('/login')
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <nav className="bg-white shadow-lg border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-purple-600">
              🚀 Ringo
            </Link>
            <div className="flex items-center space-x-6">
              <div className="text-right">
                <div className="text-sm text-gray-500">Available Credits</div>
                <div className="text-xl font-bold text-green-600">
                  ${ (credits / 100).toLocaleString() }
                </div>
              </div>
              <button
                onClick={() => router.push('/dashboard/payouts')}
                className="text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Tabs */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6">
          <div className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-4 font-medium transition ${
                  activeTab === tab.id
                    ? 'text-purple-600 border-b-2 border-purple-600'
                    : 'text-gray-600 hover:text-purple-600'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-8">
        {activeTab === 'overview' && (
          <>
            <h1 className="text-3xl font-bold mb-8">Dashboard Overview</h1>
            
            {/* Stats Grid */}
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="text-sm text-gray-500 mb-2">Available Credits</div>
                <div className="text-3xl font-bold text-green-600">
                  ${ (credits / 100).toLocaleString() }
                </div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="text-sm text-gray-500 mb-2">Total Revenue</div>
                <div className="text-3xl font-bold text-blue-600">
                  ${ (revenue / 100).toLocaleString() }
                </div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="text-sm text-gray-500 mb-2">Calls Connected</div>
                <div className="text-3xl font-bold text-purple-600">
                  {calls}
                </div>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <div className="text-sm text-gray-500 mb-2">Conversions</div>
                <div className="text-3xl font-bold text-orange-600">
                  {conversions}
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
                <div className="space-y-3">
                  <button
                    onClick={() => setActiveTab('funding')}
                    className="w-full bg-green-600 text-white py-3 rounded-lg font-bold hover:bg-green-700 transition"
                  >
                    Add Credits
                  </button>
                  <button
                    onClick={() => setActiveTab('bids')}
                    className="w-full bg-purple-600 text-white py-3 rounded-lg font-bold hover:bg-purple-700 transition"
                  >
                    Create New Bid
                  </button>
                  <button
                    onClick={() => setActiveTab('leads')}
                    className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition"
                  >
                    Browse Leads
                  </button>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
                <h2 className="text-xl font-bold mb-4">Top Performing Categories</h2>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="font-medium">Commercial Auto</span>
                      <span className="text-green-600 font-bold">$3,250</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-green-600 h-2 rounded-full" style={{ width: '85%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="font-medium">Health Insurance</span>
                      <span className="text-blue-600 font-bold">$2,180</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-600 h-2 rounded-full" style={{ width: '65%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="font-medium">Personal Auto</span>
                      <span className="text-orange-600 font-bold">$1,875</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-orange-600 h-2 rounded-full" style={{ width: '55%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {activeTab === 'funding' && (
          <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold mb-8">Credit Funding</h1>
            <div className="bg-white p-8 rounded-xl shadow-md border border-gray-100">
              <p className="text-gray-600 mb-6">
                Add credits to your account to start bidding on leads. Minimum $100.
              </p>
              <div className="grid grid-cols-4 gap-4 mb-6">
                {[100, 250, 500, 1000].map((amount) => (
                  <button
                    key={amount}
                    className="border-2 border-purple-600 text-purple-600 py-3 rounded-lg font-bold hover:bg-purple-50 transition"
                  >
                    ${amount}
                  </button>
                ))}
              </div>
              <button className="w-full bg-purple-600 text-white py-4 rounded-lg font-bold text-xl hover:bg-purple-700 transition">
                Continue to Payment
              </button>
            </div>
          </div>
        )}

        {activeTab === 'bids' && (
          <div>
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold">Manage Bids</h1>
              <button className="bg-purple-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-purple-700 transition">
                + Create New Bid
              </button>
            </div>
            
            {/* Active Bids */}
            <div className="bg-white rounded-xl shadow-md border border-gray-100 mb-8">
              <div className="p-6 border-b">
                <h2 className="text-xl font-bold">Active Bids</h2>
              </div>
              <div className="divide-y">
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-lg">Commercial Auto Insurance</h3>
                      <span className="text-sm text-gray-500">Category ID: cat-001</span>
                    </div>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">
                      Active
                    </span>
                  </div>
                  <div className="grid md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <div className="text-sm text-gray-500">Bid Amount</div>
                      <div className="font-bold text-lg">$8.50/call</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Monthly Quota</div>
                      <div className="font-bold text-lg">500 calls</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Used</div>
                      <div className="font-bold text-lg">127/500</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Status</div>
                      <div className="font-bold text-lg text-green-600">Active</div>
                    </div>
                  </div>
                  <div className="flex space-x-3">
                    <button className="text-purple-600 font-bold hover:underline">Edit</button>
                    <button className="text-red-600 font-bold hover:underline">Cancel</button>
                  </div>
                </div>
                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-lg">Health Insurance</h3>
                      <span className="text-sm text-gray-500">Category ID: cat-002</span>
                    </div>
                    <span className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm font-bold">
                      Pending
                    </span>
                  </div>
                  <div className="grid md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <div className="text-sm text-gray-500">Bid Amount</div>
                      <div className="font-bold text-lg">$7.25/call</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Monthly Quota</div>
                      <div className="font-bold text-lg">300 calls</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Used</div>
                      <div className="font-bold text-lg">0/300</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Status</div>
                      <div className="font-bold text-lg text-yellow-600">Pending</div>
                    </div>
                  </div>
                  <div className="flex space-x-3">
                    <button className="text-purple-600 font-bold hover:underline">Edit</button>
                    <button className="text-red-600 font-bold hover:underline">Cancel</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'leads' && (
          <div>
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold">Lead Marketplace</h1>
              <div className="flex space-x-3">
                <select className="border rounded-lg px-4 py-2">
                  <option>All Categories</option>
                  <option>Personal Auto</option>
                  <option>Commercial Auto</option>
                  <option>Health Insurance</option>
                  <option>Life Insurance</option>
                </select>
                <select className="border rounded-lg px-4 py-2">
                  <option>Status: All</option>
                  <option>Qualified</option>
                  <option>Dropped</option>
                  <option>No Answer</option>
                </select>
              </div>
            </div>

            {/* Leads Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
                  <div className="flex justify-between items-start mb-4">
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">
                      Qualified
                    </span>
                    <span className="text-sm text-gray-500">2 minutes ago</span>
                  </div>
                  <h3 className="font-bold text-lg mb-2">Commercial Auto</h3>
                  <div className="space-y-2 mb-4">
                    <div className="text-sm">
                      <span className="text-gray-500">Caller:</span>
                      <span className="font-medium">John Mitchell</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Phone:</span>
                      <span className="font-medium">+1 (555) 123-4567</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Needs:</span>
                      <span className="font-medium">Fleet insurance for 12 trucks</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Budget:</span>
                      <span className="font-medium text-green-600">$5,000-7,500/month</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Timeframe:</span>
                      <span className="font-medium">Within 2 weeks</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center pt-4 border-t">
                    <div className="text-sm text-gray-500">
                      Lead Score: <span className="font-bold text-green-600">0.92</span>
                    </div>
                    <button className="text-purple-600 font-bold hover:underline">View Details →</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div>
            <h1 className="text-3xl font-bold mb-8">Analytics</h1>
            
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 mb-8">
              <h2 className="text-xl font-bold mb-4">Performance Overview</h2>
              <div className="grid md:grid-cols-4 gap-6">
                <div>
                  <div className="text-sm text-gray-500 mb-2">Total Revenue (30d)</div>
                  <div className="text-2xl font-bold text-green-600">$8,425.00</div>
                  <div className="text-sm text-green-600 mt-1">↑ 12.5% from last month</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500 mb-2">Total Calls (30d)</div>
                  <div className="text-2xl font-bold text-purple-600">1,247</div>
                  <div className="text-sm text-green-600 mt-1">↑ 8.3% from last month</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500 mb-2">Conversion Rate</div>
                  <div className="text-2xl font-bold text-blue-600">34.4%</div>
                  <div className="text-sm text-red-600 mt-1">↓ 2.1% from last month</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500 mb-2">Avg. Revenue/Call</div>
                  <div className="text-2xl font-bold text-orange-600">$6.76</div>
                  <div className="text-sm text-green-600 mt-1">↑ 4.2% from last month</div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
              <h2 className="text-xl font-bold mb-4">Revenue by Category</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">Commercial Auto</span>
                    <span className="font-bold">$3,250 (38.6%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-green-600 h-3 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">Health Insurance</span>
                    <span className="font-bold">$2,180 (25.9%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-blue-600 h-3 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">Personal Auto</span>
                    <span className="font-bold">$1,875 (22.2%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-orange-600 h-3 rounded-full" style={{ width: '55%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="font-medium">Life Insurance</span>
                    <span className="font-bold">$1,120 (13.3%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-purple-600 h-3 rounded-full" style={{ width: '40%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'payouts' && (
          <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold mb-8">Payouts</h1>
            
            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 mb-6">
              <h2 className="text-xl font-bold mb-2">Available Balance</h2>
              <p className="text-gray-600 mb-4">Instant payouts available - no waiting!</p>
              <div className="text-4xl font-bold text-green-600 mb-6">
                $2,847.50
              </div>
              <button className="w-full bg-green-600 text-white py-4 rounded-lg font-bold text-xl hover:bg-green-700 transition">
                Request Instant Payout
              </button>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
              <h2 className="text-xl font-bold mb-4">Payout History</h2>
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                    <div>
                      <div className="font-bold">Payout #{1024 - i}</div>
                      <div className="text-sm text-gray-500">${(i * 500).toLocaleString()}.00 • March {15 - i}, 2026</div>
                    </div>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-bold">
                      Completed
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
