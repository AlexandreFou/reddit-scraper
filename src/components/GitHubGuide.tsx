import React, { useState } from "react";
import {
  KeyRound,
  GitBranch,
  ShieldCheck,
  Check,
  Copy,
  ExternalLink,
  HelpCircle,
  Clock,
  Sparkles
} from "lucide-react";

export const GitHubGuide: React.FC = () => {
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);

  const gitCommands = `git init
git branch -M main
git remote add origin https://github.com/AlexandreFou/RedditScraper.git
git add .
git commit -m "feat: initial commit - Reddit Opportunity Scraper via Apify & LangChain"
git push -u origin main`;

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCmd(id);
    setTimeout(() => setCopiedCmd(null), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Intro Banner */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white p-6 rounded-2xl shadow-sm border border-slate-800">
        <div className="flex items-center gap-2 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-2">
          <Sparkles className="w-4 h-4" />
          Déploiement Automatisé 100% Clé en Main
        </div>
        <h2 className="text-xl font-bold">
          Guide de configuration pour GitHub Actions
        </h2>
        <p className="text-slate-300 text-xs mt-1.5 max-w-2xl leading-relaxed">
          Suivez ces 4 étapes simples pour relier votre projet à votre repository GitHub{" "}
          <code className="bg-slate-800/80 px-2 py-0.5 rounded text-indigo-300 font-mono text-[11px]">
            AlexandreFou/RedditScraper
          </code>{" "}
          et recevoir automatiquement chaque matin votre rapport d'opportunités sans rien toucher.
        </p>
      </div>

      {/* Step 1: Push Code to GitHub */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2.5">
            <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
              1
            </span>
            <h3 className="text-sm font-bold text-slate-900">
              Pousser les fichiers vers votre repository GitHub
            </h3>
          </div>
          <button
            onClick={() => handleCopy(gitCommands, "git-cmd")}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 rounded-lg border border-indigo-200 transition-colors"
          >
            {copiedCmd === "git-cmd" ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            {copiedCmd === "git-cmd" ? "Commandes copiées !" : "Copier les 6 commandes"}
          </button>
        </div>
        <p className="text-xs text-slate-600 mb-3">
          Ouvrez votre terminal dans le dossier du projet et exécutez ces commandes :
        </p>
        <pre className="bg-slate-950 text-slate-200 p-4 rounded-xl text-xs font-mono overflow-x-auto leading-relaxed border border-slate-800">
          {gitCommands}
        </pre>
      </div>

      {/* Step 2: Configure GitHub Secrets */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-2.5 mb-3">
          <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
            2
          </span>
          <h3 className="text-sm font-bold text-slate-900">
            Configurer les Secrets GitHub (Settings &gt; Secrets &gt; Actions)
          </h3>
        </div>
        <p className="text-xs text-slate-600 mb-4">
          Sur GitHub, rendez-vous dans{" "}
          <strong className="text-slate-800">Settings &gt; Secrets and variables &gt; Actions</strong>, puis cliquez sur{" "}
          <strong className="text-slate-800">New repository secret</strong> pour ajouter :
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50 text-slate-500 font-semibold">
                <th className="py-2 px-3">Nom du Secret</th>
                <th className="py-2 px-3">Obligatoire ?</th>
                <th className="py-2 px-3">Description</th>
                <th className="py-2 px-3">Exemple</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              <tr>
                <td className="py-2.5 px-3 font-mono font-bold text-indigo-700">APIFY_API_TOKEN</td>
                <td className="py-2.5 px-3"><span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-medium">Oui</span></td>
                <td className="py-2.5 px-3">Votre token de compte Apify (utilisé 1 fois/jour)</td>
                <td className="py-2.5 px-3 font-mono text-slate-500">apify_api_...</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-mono font-bold text-indigo-700">LLM_API_KEY</td>
                <td className="py-2.5 px-3"><span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-medium">Oui</span></td>
                <td className="py-2.5 px-3">Clé d'API du fournisseur (OmniRoute, OpenAI, OpenRouter, etc.)</td>
                <td className="py-2.5 px-3 font-mono text-slate-500">sk-...</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-mono font-bold text-indigo-700">LLM_BASE_URL</td>
                <td className="py-2.5 px-3"><span className="text-slate-500 bg-slate-100 px-2 py-0.5 rounded">Optionnel</span></td>
                <td className="py-2.5 px-3">URL d'endpoint pour OmniRoute ou OpenRouter</td>
                <td className="py-2.5 px-3 font-mono text-slate-500">https://api.omniroute.ai/v1</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-mono font-bold text-indigo-700">LLM_MODEL</td>
                <td className="py-2.5 px-3"><span className="text-slate-500 bg-slate-100 px-2 py-0.5 rounded">Optionnel</span></td>
                <td className="py-2.5 px-3">Modèle exact supporté par votre fournisseur (évite l'erreur 400)</td>
                <td className="py-2.5 px-3 font-mono text-slate-500">gpt-4o-mini</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Step 3: Workflow Permissions */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-2.5 mb-3">
          <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
            3
          </span>
          <h3 className="text-sm font-bold text-slate-900">
            Autoriser le Bot GitHub Actions à committer les rapports
          </h3>
        </div>
        <div className="bg-amber-50 border border-amber-200 p-3.5 rounded-xl text-xs text-amber-900 space-y-1">
          <div className="font-semibold flex items-center gap-1.5 text-amber-800">
            <ShieldCheck className="w-4 h-4" />
            Étape cruciale pour éviter l'erreur de push :
          </div>
          <p>
            Allez dans <strong>Settings &gt; Actions &gt; General &gt; Workflow permissions</strong>.
          </p>
          <p>
            Cochez <strong>Read and write permissions</strong>, puis cliquez sur <strong>Save</strong>.
          </p>
        </div>
      </div>

      {/* Step 4: Test with workflow_dispatch */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-2.5 mb-3">
          <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
            4
          </span>
          <h3 className="text-sm font-bold text-slate-900">
            Tester immédiatement via déclenchement manuel (workflow_dispatch)
          </h3>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Pour vérifier que tout fonctionne avant demain matin sans attendre le cron de 07:00 :
        </p>
        <ol className="list-decimal list-inside text-xs text-slate-700 mt-2 space-y-1.5">
          <li>Ouvrez l'onglet <strong>Actions</strong> de votre repository GitHub.</li>
          <li>Dans la colonne de gauche, cliquez sur <strong>Daily Reddit Opportunities Scraper</strong>.</li>
          <li>Cliquez sur le bouton <strong>Run workflow</strong> &gt; <strong>Run workflow</strong>.</li>
          <li>Observez l'exécution en temps réel : le bot va scraper, filtrer, analyser et committer le nouveau rapport dans <code className="bg-slate-100 px-1 py-0.5 rounded text-indigo-700 font-mono">reports/</code> !</li>
        </ol>
      </div>

      {/* Note on Error 400 fix */}
      <div className="bg-indigo-50 border border-indigo-200 p-4 rounded-xl text-xs text-indigo-950">
        <div className="font-bold flex items-center gap-1.5 text-indigo-900 mb-1">
          <HelpCircle className="w-4 h-4 text-indigo-600" />
          Comment l'erreur 400 "Invalid model" a été résolue :
        </div>
        <p className="leading-relaxed">
          Dans la version précédente, le modèle était codé en dur. Désormais, le modèle est lu dynamiquement depuis la variable <code className="font-mono font-semibold">LLM_MODEL</code> avec repli propre sur <code className="font-mono">gpt-4o-mini</code>. Si vous utilisez OmniRoute ou un proxy personnalisé, vous pouvez simplement ajuster <code className="font-mono">LLM_MODEL</code> sans jamais modifier le code source Python !
        </p>
      </div>
    </div>
  );
};
