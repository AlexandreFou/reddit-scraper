import React, { useState } from "react";
import {
  Play,
  RotateCcw,
  CheckCircle,
  Clock,
  Sparkles,
  Filter,
  Layers,
  FileCheck
} from "lucide-react";

interface Step {
  id: number;
  name: string;
  desc: string;
  icon: any;
  status: "idle" | "running" | "done";
  details?: string;
}

export const PipelineSimulator: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(-1);
  const [logs, setLogs] = useState<string[]>([
    "[READY] Prêt à simuler l'exécution du workflow quotidien (Mode 0 Crédit / Dry Run)",
  ]);

  const [steps, setSteps] = useState<Step[]>([
    {
      id: 1,
      name: "1. Apify Single Run",
      desc: "Récupère r/Entrepreneur, r/startups, r/smallbusiness en 1 run unique",
      icon: Layers,
      status: "idle",
      details: "86 posts bruts récupérés via trudax/reddit-scraper"
    },
    {
      id: 2,
      name: "2. Filtrage Heuristique",
      desc: "Élimine memes, grindset et spam en Python pur (0 coût LLM)",
      icon: Filter,
      status: "idle",
      details: "32 posts qualifiés avec signaux d'intention de paiement"
    },
    {
      id: 3,
      name: "3. Analyse LangChain & LLM",
      desc: "Extraction structurée Pydantic sans hallucination de métriques",
      icon: Sparkles,
      status: "idle",
      details: "3 opportunités majeures identifiées et analysées"
    },
    {
      id: 4,
      name: "4. Scoring & Déduplication",
      desc: "Évaluation sur la grille /100 et fusion des signaux récurrents",
      icon: CheckCircle,
      status: "idle",
      details: "Top 3 opportunités classées (Meilleur score: 90/100)"
    },
    {
      id: 5,
      name: "5. Génération & Push Git",
      desc: "Sauvegarde dans reports/YYYY-MM-DD.md et commit automatique",
      icon: FileCheck,
      status: "idle",
      details: "Rapport formaté avec tableaux et liens Reddit sources"
    }
  ]);

  const runSimulation = () => {
    if (isRunning) return;
    setIsRunning(true);
    setCurrentStepIndex(0);
    setLogs(["[INFO] Démarrage du pipeline RedditScraper quotidien..."]);

    const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

    const execute = async () => {
      // Step 1
      setSteps((prev) =>
        prev.map((s, i) => (i === 0 ? { ...s, status: "running" } : { ...s, status: "idle" }))
      );
      setLogs((l) => [
        ...l,
        "[INFO] Initialisation du client Apify (acteur 'trudax/reddit-scraper')",
        "[INFO] URLs injectées : r/Entrepreneur, r/startups, r/smallbusiness",
        "[INFO] Exécution du run unique Apify (max 90 posts, 5 comms/post)..."
      ]);
      await delay(900);
      setSteps((prev) =>
        prev.map((s, i) => (i === 0 ? { ...s, status: "done" } : s))
      );
      setLogs((l) => [...l, "[INFO] Run Apify achevé. 86 publications récupérées au total."]);

      // Step 2
      setCurrentStepIndex(1);
      setSteps((prev) =>
        prev.map((s, i) => (i === 1 ? { ...s, status: "running" } : s))
      );
      setLogs((l) => [
        ...l,
        "[INFO] Lancement du pré-filtrage heuristique anti-bruit (Python)...",
        "[INFO] Élimination de 54 publications (memes, motivation, spam crypto)",
        "[INFO] 32 publications avec signal de douleur ou demande qualifiées."
      ]);
      await delay(800);
      setSteps((prev) =>
        prev.map((s, i) => (i === 1 ? { ...s, status: "done" } : s))
      );

      // Step 3
      setCurrentStepIndex(2);
      setSteps((prev) =>
        prev.map((s, i) => (i === 2 ? { ...s, status: "running" } : s))
      );
      setLogs((l) => [
        ...l,
        "[INFO] Envoi de 25 publications au LLM (modèle configuré : gpt-4o-mini / OmniRoute)...",
        "[INFO] Application de la chaîne LangChain avec with_structured_output()...",
        "[INFO] Règle stricte appliquée : distinction faits (citations) vs hypothèses."
      ]);
      await delay(1100);
      setSteps((prev) =>
        prev.map((s, i) => (i === 2 ? { ...s, status: "done" } : s))
      );

      // Step 4
      setCurrentStepIndex(3);
      setSteps((prev) =>
        prev.map((s, i) => (i === 3 ? { ...s, status: "running" } : s))
      );
      setLogs((l) => [
        ...l,
        "[INFO] Validation mathématique de la grille de notation sur 100 points...",
        "[INFO] Déduplication : regroupement des signaux concordants sur la facturation artisans (3 posts liés)",
        "[INFO] Classement : 🥇 90/100 (Facturation artisans) | 🥈 86/100 (Prix restos) | 🥉 78/100 (SOC2 freelances)"
      ]);
      await delay(800);
      setSteps((prev) =>
        prev.map((s, i) => (i === 3 ? { ...s, status: "done" } : s))
      );

      // Step 5
      setCurrentStepIndex(4);
      setSteps((prev) =>
        prev.map((s, i) => (i === 4 ? { ...s, status: "running" } : s))
      );
      setLogs((l) => [
        ...l,
        "[INFO] Écriture du rapport Markdown dans reports/2026-09-03.md",
        "[INFO] Archivage des données brutes dans data/2026-09-03.json",
        "[INFO] GitHub Actions : git commit -m '📊 Daily Reddit Opportunities Report' && git push",
        "[SUCCESS] Workflow terminé avec succès en 3.6s (Simulé sans coût externe)"
      ]);
      await delay(700);
      setSteps((prev) =>
        prev.map((s, i) => (i === 4 ? { ...s, status: "done" } : s))
      );

      setIsRunning(false);
      setCurrentStepIndex(5);
    };

    execute();
  };

  const resetSimulation = () => {
    setIsRunning(false);
    setCurrentStepIndex(-1);
    setSteps((prev) => prev.map((s) => ({ ...s, status: "idle" })));
    setLogs(["[READY] Simulateur réinitialisé. Prêt pour un nouveau test."]);
  };

  return (
    <div className="space-y-6">
      {/* Simulation Controls Card */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">
            Simulateur d'Exécution Quotidienne
          </h2>
          <p className="text-xs text-slate-600 mt-1 max-w-xl">
            Testez en direct chaque étape du pipeline (Apify → Filtrage → LangChain → Scoring → Git Push)
            sans dépenser de crédit d'API externe.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={resetSimulation}
            disabled={isRunning}
            className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors disabled:opacity-50"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Réinitialiser
          </button>
          <button
            onClick={runSimulation}
            disabled={isRunning}
            className="flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm transition-all disabled:opacity-50 cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            {isRunning ? "Exécution en cours..." : "Lancer le pipeline simulé"}
          </button>
        </div>
      </div>

      {/* Step by Step Visual Pipeline */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          const isDone = step.status === "done";
          const isRunningStep = step.status === "running";

          return (
            <div
              key={step.id}
              className={`p-4 rounded-xl border transition-all ${
                isRunningStep
                  ? "bg-indigo-50/70 border-indigo-300 ring-2 ring-indigo-500/20"
                  : isDone
                  ? "bg-emerald-50/40 border-emerald-200"
                  : "bg-white border-slate-200 opacity-80"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center ${
                    isRunningStep
                      ? "bg-indigo-600 text-white animate-pulse"
                      : isDone
                      ? "bg-emerald-600 text-white"
                      : "bg-slate-100 text-slate-500"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <span className="text-[11px] font-semibold text-slate-400">Étape {step.id}</span>
              </div>

              <h4 className="text-xs font-bold text-slate-900 mb-1">{step.name}</h4>
              <p className="text-[11px] text-slate-600 leading-tight mb-2">{step.desc}</p>

              <div className="pt-2 border-t border-slate-100 text-[10px] font-medium">
                {isDone ? (
                  <span className="text-emerald-700 flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> Terminé avec succès
                  </span>
                ) : isRunningStep ? (
                  <span className="text-indigo-600 flex items-center gap-1">
                    <Clock className="w-3 h-3 animate-spin" /> En cours...
                  </span>
                ) : (
                  <span className="text-slate-400">En attente</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Terminal Live Output Console */}
      <div className="bg-slate-950 text-slate-200 rounded-xl p-5 border border-slate-800 shadow-md">
        <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800 text-xs">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-mono text-slate-400 font-semibold">Console d'exécution CLI (python -m src.main)</span>
          </div>
          <span className="text-[11px] font-mono text-slate-500">{logs.length} lignes enregistrées</span>
        </div>

        <div className="font-mono text-xs space-y-1.5 max-h-64 overflow-y-auto pr-2">
          {logs.map((log, index) => {
            const isError = log.includes("[ERROR]");
            const isWarn = log.includes("[WARN]");
            const isSuccess = log.includes("[SUCCESS]");
            const isInfo = log.includes("[INFO]");

            let colorClass = "text-slate-300";
            if (isError) colorClass = "text-rose-400 font-semibold";
            else if (isWarn) colorClass = "text-amber-400";
            else if (isSuccess) colorClass = "text-emerald-400 font-bold";
            else if (isInfo) colorClass = "text-sky-300";

            return (
              <div key={index} className={`leading-relaxed ${colorClass}`}>
                {log}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
