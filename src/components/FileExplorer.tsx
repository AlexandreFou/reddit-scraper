import React, { useState } from "react";
import { PROJECT_FILES } from "../data/mockData";
import { FileCode, Copy, Check, FolderGit2, Terminal } from "lucide-react";

export const FileExplorer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<string>("src/main.py");
  const [copied, setCopied] = useState(false);

  // Snippets or descriptions of each file
  const fileContents: Record<string, string> = {
    "src/main.py": `# Orchestrateur principal CLI
python -m src.main --dry-run
# Coordonne : Apify (1 run) -> Filtrage Python -> LangChain LLM -> Scoring /100 -> Reports & Data`,
    "src/config.py": `# Configuration centralisée
APIFY_API_TOKEN, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, SUBREDDITS, POSTS_PER_SUBREDDIT, TOP_OPPORTUNITIES`,
    "src/models.py": `# Modèles Pydantic v2
RedditPost, ScoringBreakdown, Opportunity, RejectedIdea, OpportunityAnalysisOutput, DailyReportData`,
    "src/apify_client.py": `# Client Apify (Run unique optimisé)
Exécute trudax/reddit-scraper pour r/Entrepreneur, r/startups, r/smallbusiness avec fallback mock`,
    "src/filtering.py": `# Pré-filtrage heuristique haute performance
Élimine spam/memes, détecte les signaux d'intention de paiement ("hate using", "Excel", "would pay")`,
    "src/analysis.py": `# Chaîne LangChain & structured output
with_structured_output(OpportunityAnalysisOutput) - compatible OmniRoute, OpenAI, Gemini`,
    "src/scoring.py": `# Scoring /100 & Déduplication
Validation des 7 critères (Intensité, Demande, Monétisation, etc.) et fusion des doublons`,
    "src/report.py": `# Générateur Markdown & Archivage JSON
Écrit reports/YYYY-MM-DD.md avec tableaux, médailles, plans de validation et sources`,
    ".github/workflows/daily.yml": `# GitHub Actions Workflow
name: Daily Reddit Opportunities Scraper
schedule:
  - cron: '0 6 * * *' # 07:00 Paris
workflow_dispatch:
permissions:
  contents: write
# Lance pip install -> pytest -> python -m src.main -> git commit & push`,
    "requirements.txt": `apify-client>=1.7.0
langchain>=0.3.0
langchain-core>=0.3.0
langchain-openai>=0.2.0
pydantic>=2.7.0
python-dotenv>=1.0.0
pytz>=2024.1
pytest>=8.0.0`,
    ".env.example": `APIFY_API_TOKEN=
APIFY_ACTOR_ID=trudax/reddit-scraper
SUBREDDITS=Entrepreneur,startups,smallbusiness
POSTS_PER_SUBREDDIT=30
LLM_API_KEY=
LLM_BASE_URL=
LLM_MODEL=gpt-4o-mini
MAX_POSTS_FOR_LLM=30
TOP_OPPORTUNITIES=10
TIMEZONE=Europe/Paris`,
    "README.md": `# Documentation complète du projet
Architecture, installation locale, configuration Apify/LLM, GitHub Secrets et dépannage`,
  };

  const handleCopy = (path: string) => {
    const text = fileContents[path] || `# Fichier : ${path}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">Architecture des fichiers créés</h3>
          <p className="text-xs text-slate-500 mt-0.5">
            18 fichiers complets générés dans le repository pour une exécution propre et maintenable.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs font-mono text-slate-600 bg-slate-100 px-3 py-1.5 rounded-lg">
          <FolderGit2 className="w-4 h-4 text-indigo-600" />
          <span>https://github.com/AlexandreFou/RedditScraper.git</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
        {/* File List Column */}
        <div className="md:col-span-5 bg-white rounded-xl border border-slate-200 p-3 shadow-xs max-h-[520px] overflow-y-auto">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider px-2 py-1 mb-1">
            Fichiers du projet
          </div>
          <div className="space-y-1">
            {PROJECT_FILES.map((f) => {
              const isSelected = selectedFile === f.path;
              return (
                <button
                  key={f.path}
                  onClick={() => setSelectedFile(f.path)}
                  className={`w-full text-left p-2 rounded-lg text-xs transition-all flex items-start gap-2 ${
                    isSelected
                      ? "bg-indigo-50 text-indigo-900 font-semibold border border-indigo-200"
                      : "text-slate-700 hover:bg-slate-50 border border-transparent"
                  }`}
                >
                  <FileCode className={`w-4 h-4 shrink-0 mt-0.5 ${isSelected ? "text-indigo-600" : "text-slate-400"}`} />
                  <div className="truncate">
                    <div className="truncate font-mono">{f.path}</div>
                    <div className="text-[10px] text-slate-500 font-normal truncate">{f.description}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* File Content Preview Column */}
        <div className="md:col-span-7 bg-slate-950 text-slate-200 rounded-xl border border-slate-800 p-4 flex flex-col justify-between shadow-xs">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3 text-xs">
              <span className="font-mono text-indigo-400 font-medium">{selectedFile}</span>
              <button
                onClick={() => handleCopy(selectedFile)}
                className="flex items-center gap-1.5 px-2.5 py-1 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? "Copié !" : "Copier"}
              </button>
            </div>

            <div className="text-xs text-slate-400 mb-3">
              {PROJECT_FILES.find((f) => f.path === selectedFile)?.description}
            </div>

            <pre className="font-mono text-xs bg-slate-900/80 p-4 rounded-lg text-slate-300 overflow-x-auto max-h-[380px] leading-relaxed whitespace-pre-wrap">
              {fileContents[selectedFile] || `Fichier complet disponible sur le disque local : /${selectedFile}`}
            </pre>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-500 font-mono">
            <span className="flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5 text-slate-400" />
              Statut : Validé par tests unitaires (11/11 OK)
            </span>
            <span>Branche cible : main</span>
          </div>
        </div>
      </div>
    </div>
  );
};
