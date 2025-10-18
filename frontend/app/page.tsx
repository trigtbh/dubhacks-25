'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiStatus {
  message: string;
  status: string;
  timestamp?: string;
}

export default function Home() {
  const [data, setData] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<ApiStatus>(`${API_URL}/`);
      setData(response.data);
    } catch (err) {
      setError('Failed to connect to backend. Make sure the API is running.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post<{ message: string; input: string }>(
        `${API_URL}/unfreeze`,
        { text: inputValue }
      );
      setData({
        message: response.data.message,
        status: 'success',
      });
      setInputValue('');
    } catch (err) {
      setError('Failed to process request');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Unfreeze
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Break through barriers and unleash your potential
            </p>
          </div>

          {/* Main Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
            {/* API Status */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200">
                  Backend Status
                </h2>
                <button
                  onClick={fetchData}
                  disabled={loading}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 transition-colors duration-200"
                >
                  {loading ? 'Checking...' : 'Refresh'}
                </button>
              </div>
              
              {error && (
                <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                  <p className="text-red-600 dark:text-red-400">{error}</p>
                </div>
              )}
              
              {data && !error && (
                <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                  <p className="text-green-800 dark:text-green-300 font-medium">
                    {data.message}
                  </p>
                  {data.timestamp && (
                    <p className="text-sm text-green-600 dark:text-green-400 mt-2">
                      {data.timestamp}
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Interactive Form */}
            <div className="border-t border-gray-200 dark:border-gray-700 pt-8">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
                Try It Out
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label
                    htmlFor="input"
                    className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                  >
                    Enter some text to unfreeze
                  </label>
                  <input
                    id="input"
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Type something..."
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white transition-all duration-200"
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading || !inputValue.trim()}
                  className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 font-medium transition-all duration-200 transform hover:scale-105 disabled:scale-100"
                >
                  {loading ? 'Processing...' : 'Unfreeze'}
                </button>
              </form>
            </div>
          </div>

          {/* Info Cards */}
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">
                Fast
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Built with Next.js and FastAPI for optimal performance
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <div className="text-3xl mb-3">🔒</div>
              <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">
                Secure
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Ready for Supabase integration with authentication
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
              <div className="text-3xl mb-3">🎨</div>
              <h3 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-200">
                Modern
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Beautiful UI with Tailwind CSS and TypeScript
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

