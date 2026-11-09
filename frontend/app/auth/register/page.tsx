"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const router = useRouter();
  const { theme, setTheme } = useTheme();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await register(name, email, password);
      router.push("/");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white dark:bg-black px-4">
      <button
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        className="fixed top-6 right-6 p-2.5 rounded-full hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors"
      >
        {theme === "dark" ? (
          <Sun className="w-5 h-5 text-zinc-400" />
        ) : (
          <Moon className="w-5 h-5 text-gray-600" />
        )}
      </button>

      <div className="max-w-md w-full">
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-black dark:bg-white rounded-xl mb-6">
            <div className="w-6 h-6 border-2 border-white dark:border-black rounded-full"></div>
          </div>
          <h1 className="text-3xl font-semibold text-black dark:text-white mb-2">
            Create your account
          </h1>
          <p className="text-gray-600 dark:text-zinc-400">
            Get started with SearchMind
          </p>
        </div>

        <div className="bg-white dark:bg-black border border-gray-200 dark:border-zinc-800 rounded-2xl p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/50 text-red-800 dark:text-red-400 rounded-xl text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-900 dark:text-zinc-100 mb-2"
              >
                Full name
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white dark:bg-black border border-gray-200 dark:border-zinc-800 rounded-xl focus:ring-2 focus:ring-black dark:focus:ring-white focus:border-transparent outline-none text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-zinc-600"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-900 dark:text-zinc-100 mb-2"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white dark:bg-black border border-gray-200 dark:border-zinc-800 rounded-xl focus:ring-2 focus:ring-black dark:focus:ring-white focus:border-transparent outline-none text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-zinc-600"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-900 dark:text-zinc-100 mb-2"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                className="w-full px-4 py-3 bg-white dark:bg-black border border-gray-200 dark:border-zinc-800 rounded-xl focus:ring-2 focus:ring-black dark:focus:ring-white focus:border-transparent outline-none text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-zinc-600"
                placeholder="At least 6 characters"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-black dark:bg-white hover:bg-gray-800 dark:hover:bg-gray-100 text-white dark:text-black font-medium rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Creating account..." : "Continue"}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-zinc-400 text-sm">
              Already have an account?{" "}
              <Link
                href="/auth/login"
                className="text-black dark:text-white font-medium hover:underline"
              >
                Log in
              </Link>
            </p>
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-gray-500 dark:text-zinc-600">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
