"use client";

import { useState, useEffect, useRef } from "react";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "next-themes";
import axios from "axios";
import {
  Send,
  Moon,
  Sun,
  LogOut,
  Menu,
  Plus,
  User,
  X,
} from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export default function Chat() {
  const { user, token, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState("default");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    loadHistory();
  }, [token, sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    adjustTextareaHeight();
  }, [input]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px";
    }
  };

  const loadHistory = async () => {
    if (!token) return;
    try {
      const response = await axios.get(`${API_URL}/api/chat/history`, {
        params: { session_id: sessionId, token },
      });
      setMessages(response.data);
    } catch (error) {
      console.error("Failed to load history:", error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/api/chat/query`,
        {
          message: input,
          session_id: sessionId,
        },
        {
          params: { token },
        }
      );

      const assistantMessage: Message = {
        role: "assistant",
        content: response.data.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setSessionId(`chat_${Date.now()}`);
  };

  return (
    <div className="flex h-screen bg-white dark:bg-black">
      {/* Sidebar */}
      <div
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } transition-all duration-300 bg-white dark:bg-black border-r border-gray-200 dark:border-zinc-800 flex flex-col overflow-hidden`}
      >
        <div className="p-3 space-y-2">
          <button
            onClick={startNewChat}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg border border-gray-200 dark:border-zinc-800 hover:bg-gray-50 dark:hover:bg-zinc-900 transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span className="text-sm font-medium">New chat</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2"></div>

        <div className="p-3 border-t border-gray-200 dark:border-zinc-800 space-y-1">
          <div className="flex items-center gap-3 px-3 py-2 text-sm">
            <User className="w-4 h-4" />
            <span className="truncate">{user?.name}</span>
          </div>
          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-zinc-900 transition-colors text-sm"
          >
            <LogOut className="w-4 h-4" />
            <span>Log out</span>
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="h-14 border-b border-gray-200 dark:border-zinc-800 flex items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
            >
              {sidebarOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </button>
            <span className="font-semibold text-lg">SearchMind</span>
          </div>

          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 hover:bg-gray-100 dark:hover:bg-zinc-900 rounded-lg transition-colors"
          >
            {theme === "dark" ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center px-4">
              <div className="w-12 h-12 bg-black dark:bg-white rounded-xl flex items-center justify-center mb-6">
                <div className="w-6 h-6 border-2 border-white dark:border-black rounded-full"></div>
              </div>
              <h2 className="text-2xl font-semibold mb-2">
                How can I help you today?
              </h2>
              <p className="text-gray-600 dark:text-zinc-400 text-center max-w-md">
                Ask me anything or let me help with your research
              </p>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
              {messages.map((message, idx) => (
                <div
                  key={idx}
                  className="flex gap-4"
                >
                  {message.role === "assistant" && (
                    <div className="w-8 h-8 bg-black dark:bg-white rounded-lg flex items-center justify-center flex-shrink-0">
                      <div className="w-4 h-4 border-2 border-white dark:border-black rounded-full"></div>
                    </div>
                  )}
                  <div className="flex-1 space-y-2 pt-1">
                    <div className="font-medium text-sm text-gray-900 dark:text-white">
                      {message.role === "assistant" ? "SearchMind" : user?.name}
                    </div>
                    <p className="text-gray-800 dark:text-zinc-200 whitespace-pre-wrap leading-relaxed">
                      {message.content}
                    </p>
                  </div>
                  {message.role === "user" && (
                    <div className="w-8 h-8 bg-gray-200 dark:bg-zinc-800 rounded-lg flex items-center justify-center flex-shrink-0">
                      <User className="w-4 h-4" />
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex gap-4">
                  <div className="w-8 h-8 bg-black dark:bg-white rounded-lg flex items-center justify-center">
                    <div className="w-4 h-4 border-2 border-white dark:border-black rounded-full"></div>
                  </div>
                  <div className="flex-1 pt-1">
                    <div className="font-medium text-sm mb-2">SearchMind</div>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 dark:bg-zinc-600 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-400 dark:bg-zinc-600 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-400 dark:bg-zinc-600 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 dark:border-zinc-800 bg-white dark:bg-black">
          <div className="max-w-3xl mx-auto px-4 py-4">
            <form onSubmit={handleSendMessage} className="relative">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message SearchMind..."
                disabled={loading}
                rows={1}
                className="w-full resize-none bg-gray-50 dark:bg-zinc-900 border border-gray-200 dark:border-zinc-800 rounded-2xl pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-black dark:focus:ring-white focus:border-transparent text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-zinc-600 disabled:opacity-50 max-h-[200px] overflow-y-auto"
                style={{ minHeight: "48px" }}
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="absolute right-2 bottom-2 w-8 h-8 flex items-center justify-center bg-black dark:bg-white hover:bg-gray-800 dark:hover:bg-gray-100 disabled:bg-gray-200 dark:disabled:bg-zinc-800 disabled:cursor-not-allowed rounded-lg transition-colors"
              >
                <Send className="w-4 h-4 text-white dark:text-black" />
              </button>
            </form>
            <p className="text-xs text-center text-gray-500 dark:text-zinc-600 mt-2">
              SearchMind can make mistakes. Check important info.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
