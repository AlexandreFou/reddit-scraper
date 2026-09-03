import React, { useState } from "react";
import { ReportView } from "./components/ReportView";
import { PipelineSimulator } from "./components/PipelineSimulator";
import { FileExplorer } from "./components/FileExplorer";
import { GitHubGuide } from "./components/GitHubGuide";
import {
  FileText,
  Play,
  FolderGit2,
  BookOpen,
  CheckCircle2,
  TrendingUp,
  Flame,
  Layers,
  Sparkles,
  ExternalLink
} from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState<"report" | "simulator" | "files" | "guide">("report");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Top Navbar */}
      <header className="sticky top-0 z-30 bg-white border-b border-slate-200 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo & Title */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center text-white shadow-sm shrink-0">
                <Flame className="w-5 h-5 text-amber-300" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-base font-bold text-slate-900 tracking-tight">
                    Reddit Opportunity Scraper
                  </h1>
                  <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    Actif • Cron 07:00 Paris
                  </span>
                </div>
                <p className="text-xs text-slate-500 truncate">
                  r/Entrepreneur • r/startups • r/smallbusiness → Apify + LangChain
                </p>
              </div>
            </div>

            {/* Target Repo Link */}
            <div className="flex items-center gap-3">
              <a
                href="https://github.com/AlexandreFou/RedditScraper"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 transition-colors"
              >
                <FolderGit2 className="w-3.5 h-3.5 text-indigo-600" />
                <span className="hidden md:inline">AlexandreFou/</span>
                <span>RedditScraper</span>
                <ExternalLink className="w-3 h-3 text-slate-400" />
              </a>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex overflow-x-auto space-x-1 border-t border-slate-100 py-1">
          <button
            onClick={() => setActiveTab("report")}
            className={`flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "report"
                ? "bg-indigo-600 text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            Rapports & Opportunités
          </button>
          <button
            onClick={() => setActiveTab("simulator")}
            className={`flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "simulator"
                ? "bg-indigo-600 text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Play className="w-3.5 h-3.5" />
            Simulateur de Pipeline (0 Crédit)
          </button>
          <button
            onClick={() => setActiveTab("files")}
            className={`flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "files"
                ? "bg-indigo-600 text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            Architecture & Fichiers Python
          </button>
          <button
            onClick={() => setActiveTab("guide")}
            className={`flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "guide"
                ? "bg-indigo-600 text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            Guide Déploiement GitHub & Secrets
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === "report" && <ReportView />}
        {activeTab === "simulator" && <PipelineSimulator />}
        {activeTab === "files" && <FileExplorer />}
        {activeTab === "guide" && <GitHubGuide />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Projet RedditScraper — Apify + LangChain + GitHub Actions</span>
          <span>Surveillance : r/Entrepreneur • r/startups • r/smallbusiness</span>
        </div>
      </footer>
    </div>
  );
}
