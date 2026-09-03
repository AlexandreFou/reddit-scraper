import React, { useState } from "react";
import { SAMPLE_REPORT_DATA, OpportunityItem } from "../data/mockData";
import {
  Trophy,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  Flame,
  Clock,
  DollarSign,
  Cpu,
  Layers,
  FileText,
  Copy,
  Check,
  ChevronDown,
  ChevronUp
} from "lucide-react";

export const ReportView: React.FC = () => {
  const [selectedSub, setSelectedSub] = useState<string>("all");
  const [expandedId, setExpandedId] = useState<string | null>("opp-1");
  const [copied, setCopied] = useState(false);
  const [showRawMarkdown, setShowRawMarkdown] = useState(false);

  const filteredOpps = SAMPLE_REPORT_DATA.opportunities.filter((opp) => {
    if (selectedSub === "all") return true;
    return opp.source_subreddits.includes(selectedSub);
  });

  const handleCopyMarkdown = () => {
    // Generate text
    const md = `# Reddit Entrepreneurial Opportunities — ${SAMPLE_REPORT_DATA.date}\n\n... (voir reports/${SAMPLE_REPORT_DATA.date}.md)`;
    navigator.clipboard.writeText(md);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getMedalBadge = (index: number) => {
    if (index === 0) return { icon: "🥇", label: "Top 1", bg: "bg-amber-100 text-amber-800 border-amber-300" };
    if (index === 1) return { icon: "🥈", label: "Top 2", bg: "bg-slate-200 text-slate-800 border-slate-300" };
    if (index === 2) return { icon: "🥉", label: "Top 3", bg: "bg-orange-100 text-orange-800 border-orange-300" };
    return { icon: `#${index + 1}`, label: `Top ${index + 1}`, bg: "bg-gray-100 text-gray-800 border-gray-200" };
  };

  return (
    <div className="space-y-6">
      {/* Header Stat Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Posts analysés (24h)</div>
          <div className="text-2xl font-bold text-slate-900 mt-1">{SAMPLE_REPORT_DATA.scraped_total}</div>
          <div className="text-xs text-slate-600 mt-1">1 seul run Apify</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Posts qualifiés</div>
          <div className="text-2xl font-bold text-emerald-600 mt-1">{SAMPLE_REPORT_DATA.filtered_total}</div>
          <div className="text-xs text-slate-600 mt-1">Pré-filtrage anti-bruit</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Analysés par LLM</div>
          <div className="text-2xl font-bold text-indigo-600 mt-1">{SAMPLE_REPORT_DATA.llm_analyzed}</div>
          <div className="text-xs text-slate-600 mt-1">Sortie structurée</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Opportunités validées</div>
          <div className="text-2xl font-bold text-amber-600 mt-1">{SAMPLE_REPORT_DATA.opportunities.length}</div>
          <div className="text-xs text-slate-600 mt-1">Scorées &gt;= 75/100</div>
        </div>
      </div>

      {/* Subreddit Filter Bar & Actions */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-slate-500">Filtrer par Subreddit :</span>
          <div className="flex flex-wrap gap-1.5">
            {["all", "r/Entrepreneur", "r/startups", "r/smallbusiness"].map((sub) => (
              <button
                key={sub}
                onClick={() => setSelectedSub(sub)}
                className={`px-3 py-1 text-xs rounded-lg font-medium transition-all ${
                  selectedSub === sub
                    ? "bg-slate-900 text-white shadow-xs"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {sub === "all" ? "Tous les subreddits" : sub}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowRawMarkdown(!showRawMarkdown)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
          >
            <FileText className="w-3.5 h-3.5 text-slate-500" />
            {showRawMarkdown ? "Masquer Markdown brut" : "Voir Markdown brut"}
          </button>
          <button
            onClick={handleCopyMarkdown}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-lg transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-indigo-600" />}
            {copied ? "Copié !" : "Copier le Markdown"}
          </button>
        </div>
      </div>

      {/* Raw Markdown view if toggled */}
      {showRawMarkdown && (
        <div className="bg-slate-900 text-slate-200 p-5 rounded-xl text-xs font-mono overflow-x-auto max-h-96 border border-slate-800">
          <div className="flex justify-between items-center pb-2 mb-3 border-b border-slate-800 text-slate-400">
            <span>Fichier : reports/{SAMPLE_REPORT_DATA.date}.md</span>
            <span className="text-emerald-400">Généré le matin à 07:00 Paris</span>
          </div>
          <pre className="whitespace-pre-wrap leading-relaxed">
{`# Reddit Entrepreneurial Opportunities — ${SAMPLE_REPORT_DATA.date}

## Résumé de la veille quotidienne
- Publications analysées (24h) : ${SAMPLE_REPORT_DATA.scraped_total}
- Publications qualifiées : ${SAMPLE_REPORT_DATA.filtered_total}
- Opportunités validées : ${SAMPLE_REPORT_DATA.opportunities.length}

${SAMPLE_REPORT_DATA.opportunities.map((o, i) => `### ${i + 1}. ${o.title}
Score : ${o.scoring.total_score}/100
Problème : ${o.problem}
Cible : ${o.target_customer}
Solution : ${o.proposed_solution}
Monétisation : ${o.monetization}`).join("\n\n")}`}
          </pre>
        </div>
      )}

      {/* Opportunities List */}
      <div className="space-y-4">
        {filteredOpps.map((opp, index) => {
          const medal = getMedalBadge(index);
          const isExpanded = expandedId === opp.id;
          const score = opp.scoring.total_score;

          return (
            <div
              key={opp.id}
              className="bg-white rounded-xl border border-slate-200 shadow-xs hover:border-slate-300 transition-all overflow-hidden"
            >
              {/* Card Header */}
              <div
                onClick={() => setExpandedId(isExpanded ? null : opp.id)}
                className="p-5 cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-4 select-none"
              >
                <div className="flex items-start gap-3.5">
                  <div className={`flex items-center gap-1 px-2.5 py-1 rounded-lg border text-xs font-semibold ${medal.bg} shrink-0`}>
                    <span>{medal.icon}</span>
                    <span>{medal.label}</span>
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-slate-900 hover:text-indigo-600 transition-colors">
                      {opp.title}
                    </h3>
                    <div className="flex flex-wrap items-center gap-2 mt-1.5">
                      <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-mono">
                        {opp.source_subreddits.join(", ")}
                      </span>
                      <span className="text-xs text-slate-500">•</span>
                      <span className="text-xs text-slate-600">
                        Cible : <strong className="text-slate-800">{opp.target_customer}</strong>
                      </span>
                      <span className="text-xs text-slate-500">•</span>
                      <span className="text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                        Signal : {opp.signal_count} post{opp.signal_count > 1 ? "s" : ""} concordant{opp.signal_count > 1 ? "s" : ""}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4 self-end md:self-center shrink-0">
                  <div className="text-right">
                    <div className="text-xs font-medium text-slate-500">Score Global</div>
                    <div className="text-2xl font-black text-indigo-600">
                      {score}<span className="text-xs font-normal text-slate-400">/100</span>
                    </div>
                  </div>
                  <button className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100">
                    {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Card Details (Collapsible) */}
              {isExpanded && (
                <div className="border-t border-slate-100 p-5 bg-slate-50/50 space-y-5 text-sm">
                  {/* Score Breakdown Bar */}
                  <div className="bg-white p-4 rounded-xl border border-slate-200">
                    <div className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                      Grille de scoring détaillée (/100) — {opp.scoring.score_reasoning}
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 text-xs">
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Intensité</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.problem_intensity}/20</div>
                      </div>
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Demande</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.observable_demand}/20</div>
                      </div>
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Monétisation</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.monetization_potential}/15</div>
                      </div>
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Marché / Niche</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.market_size_niche}/15</div>
                      </div>
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Concurrence</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.competition_saturation}/10</div>
                      </div>
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Facilité MVP</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.launch_ease}/10</div>
                      </div>
                      <div className="bg-slate-50 p-2 rounded border border-slate-100">
                        <div className="text-slate-500 text-[11px]">Potentiel IA</div>
                        <div className="font-bold text-slate-900 mt-0.5">{opp.scoring.ai_automation_potential}/10</div>
                      </div>
                    </div>
                  </div>

                  {/* Core Problem & Solution Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <div className="flex items-center gap-1.5 text-xs font-bold text-rose-700 uppercase tracking-wider mb-1.5">
                        <Flame className="w-3.5 h-3.5" />
                        Problème réel observé
                      </div>
                      <p className="text-slate-700 leading-relaxed">{opp.problem}</p>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-700 uppercase tracking-wider mb-1.5">
                        <Layers className="w-3.5 h-3.5" />
                        Solution possible & MVP
                      </div>
                      <p className="text-slate-700 leading-relaxed">{opp.proposed_solution}</p>
                    </div>
                  </div>

                  {/* Business Characteristics */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200">
                      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 mb-1">
                        <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
                        Monétisation
                      </div>
                      <div className="text-xs font-medium text-slate-800">{opp.monetization}</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200">
                      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 mb-1">
                        <Clock className="w-3.5 h-3.5 text-amber-600" />
                        Difficulté de lancement
                      </div>
                      <div className="text-xs font-medium text-slate-800">{opp.launch_difficulty}</div>
                    </div>
                    <div className="bg-white p-3.5 rounded-xl border border-slate-200">
                      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-500 mb-1">
                        <Cpu className="w-3.5 h-3.5 text-indigo-600" />
                        Avantage IA
                      </div>
                      <div className="text-xs font-medium text-slate-800">{opp.ai_automation_potential}</div>
                    </div>
                  </div>

                  {/* Demand Signals & Concrete Validation Steps */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <div className="text-xs font-bold text-emerald-700 uppercase tracking-wider mb-2">
                        Signaux de demande observés
                      </div>
                      <ul className="space-y-1.5">
                        {opp.demand_signals.map((signal, sIdx) => (
                          <li key={sIdx} className="flex items-start gap-2 text-xs text-slate-700">
                            <span className="text-emerald-500 mt-0.5">•</span>
                            <span>{signal}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <div className="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-2">
                        Plan de validation concret (Sans coder)
                      </div>
                      <ol className="space-y-1.5">
                        {opp.validation_steps.map((step, stepIdx) => (
                          <li key={stepIdx} className="flex items-start gap-2 text-xs text-slate-700">
                            <CheckCircle2 className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                            <span>{step}</span>
                          </li>
                        ))}
                      </ol>
                    </div>
                  </div>

                  {/* Sources Reddit */}
                  <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-200 text-xs text-slate-500">
                    <div className="flex items-center gap-2">
                      <span>Sources d'origine :</span>
                      {opp.source_urls.map((url, uIdx) => (
                        <a
                          key={uIdx}
                          href={url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-800 underline font-mono text-[11px]"
                        >
                          Reddit Post #{uIdx + 1}
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      ))}
                    </div>
                    <div>
                      {opp.risks.length > 0 && (
                        <span className="text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                          ⚠️ Risque principal : {opp.risks[0]}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Rejected Ideas Section */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-1">
          Filtre anti-bruit : Exemples de publications écartées
        </h3>
        <p className="text-xs text-slate-500 mb-3">
          Pour éviter le gaspillage de crédits LLM et les biais, les publications motivationnelles et promotionnelles sont filtrées en amont.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SAMPLE_REPORT_DATA.rejected_ideas.map((rej, rIdx) => (
            <div key={rIdx} className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-xs">
              <div className="flex items-center justify-between gap-2 mb-1">
                <span className="font-semibold text-slate-800 truncate">{rej.title_or_topic}</span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-200 text-slate-700 shrink-0">
                  {rej.category}
                </span>
              </div>
              <p className="text-slate-600 text-[11px]">{rej.reason}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
