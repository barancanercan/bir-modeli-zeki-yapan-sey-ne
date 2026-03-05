import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from scipy import stats
from scipy.stats import f_oneway, ttest_ind, pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')


class StatisticalAnalyzer:
    """
    İstatistiksel analiz motoru
    
    Özellikler:
    - ANOVA testi
    - t-test
    - Effect size (Cohen's d)
    - Confidence intervals
    - Consistency scoring
    """
    
    @staticmethod
    def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
        """Cohen's d effect size hesapla"""
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        return (np.mean(group1) - np.mean(group2)) / pooled_std
    
    @staticmethod
    def confidence_interval(data: np.ndarray, confidence: float = 0.95) -> Tuple[float, float]:
        """Confidence interval hesapla"""
        n = len(data)
        mean = np.mean(data)
        se = stats.sem(data)
        
        if se == 0:
            return (mean, mean)
        
        h = se * stats.t.ppf((1 + confidence) / 2, n - 1)
        return (mean - h, mean + h)
    
    @staticmethod
    def anova_test(groups: List[np.ndarray]) -> Dict[str, Any]:
        """One-way ANOVA testi"""
        if len(groups) < 2:
            return {"error": "En az 2 grup gerekli"}
        
        # Remove empty groups
        groups = [g for g in groups if len(g) > 0]
        
        if len(groups) < 2:
            return {"error": "Yeterli grup yok"}
        
        f_stat, p_value = f_oneway(*groups)
        
        # Effect size (eta-squared)
        ss_between = sum(len(g) * (np.mean(g) - np.mean(np.concatenate(groups)))**2 for g in groups)
        ss_total = sum(np.sum((g - np.mean(np.concatenate(groups)))**2) for g in groups)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        return {
            "test": "One-way ANOVA",
            "f_statistic": float(f_stat),
            "p_value": float(p_value),
            "eta_squared": float(eta_squared),
            "significant": p_value < 0.05,
            "interpretation": "Significant" if p_value < 0.05 else "Not significant"
        }
    
    @staticmethod
    def t_test(group1: np.ndarray, group2: np.ndarray, 
               equal_var: bool = True) -> Dict[str, Any]:
        """Independent t-test"""
        t_stat, p_value = ttest_ind(group1, group2, equal_var=equal_var)
        
        d = StatisticalAnalyzer.cohens_d(group1, group2)
        
        ci1 = StatisticalAnalyzer.confidence_interval(group1)
        ci2 = StatisticalAnalyzer.confidence_interval(group2)
        
        return {
            "test": "Independent t-test",
            "t_statistic": float(t_stat),
            "p_value": float(p_value),
            "cohens_d": d,
            "significant": p_value < 0.05,
            "group1_mean": float(np.mean(group1)),
            "group2_mean": float(np.mean(group2)),
            "group1_ci": (float(ci1[0]), float(ci1[1])),
            "group2_ci": (float(ci2[0]), float(ci2[1]))
        }
    
    @staticmethod
    def correlation_analysis(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Pearson ve Spearman korelasyon analizi"""
        pearson_r, pearson_p = pearsonr(x, y)
        spearman_r, spearman_p = spearmanr(x, y)
        
        return {
            "pearson": {
                "r": float(pearson_r),
                "p_value": float(pearson_p),
                "significant": pearson_p < 0.05
            },
            "spearman": {
                "rho": float(spearman_r),
                "p_value": float(spearman_p),
                "significant": spearman_p < 0.05
            }
        }


class ScienceExpert:
    """
    Agent 2: Bilimsel Denetim Uzmanı
    
    Görevler:
    - Deney tasarımı iyileştirme
    - İstatistiksel analiz
    - Metrik sistemi kurma
    - Raporlama
    """
    
    def __init__(self):
        self.analyzer = StatisticalAnalyzer()
        self.results_dir = Path("results")
        
    def load_results(self, filename: str = None) -> List[Dict]:
        """Sonuçları yükle"""
        if filename:
            results_files = [Path(filename)]
        else:
            results_files = sorted(self.results_dir.glob("results_*.json"))
        
        if not results_files:
            return []
        
        latest = results_files[-1]
        with open(latest, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def analyze_by_model(self, results: List[Dict]) -> Dict[str, Any]:
        """Model bazlı analiz"""
        # Group by model level
        model_scores = {}
        for r in results:
            if r.get("user_score") is None:
                continue
            
            level = r["model_level"]
            if level not in model_scores:
                model_scores[level] = []
            model_scores[level].append(r["user_score"])
        
        if len(model_scores) < 2:
            return {"error": "Yeterli veri yok"}
        
        groups = [np.array(scores) for scores in model_scores.values()]
        
        # ANOVA
        anova_result = self.analyzer.anova_test(groups)
        
        # Pairwise t-tests
        pairwise = []
        levels = list(model_scores.keys())
        for i in range(len(levels)):
            for j in range(i + 1, len(levels)):
                t_result = self.analyzer.t_test(groups[i], groups[j])
                pairwise.append({
                    "comparison": f"{levels[i]} vs {levels[j]}",
                    **t_result
                })
        
        return {
            "groups": {k: len(v) for k, v in model_scores.items()},
            "means": {k: float(np.mean(v)) for k, v in model_scores.items()},
            "anova": anova_result,
            "pairwise": pairwise
        }
    
    def analyze_by_orchestration(self, results: List[Dict]) -> Dict[str, Any]:
        """Orkestrasyon bazlı analiz"""
        orch_scores = {}
        for r in results:
            if r.get("user_score") is None:
                continue
            
            orch = r["orchestration"]
            if orch not in orch_scores:
                orch_scores[orch] = []
            orch_scores[orch].append(r["user_score"])
        
        if len(orch_scores) < 2:
            return {"error": "Yeterli veri yok"}
        
        groups = [np.array(scores) for scores in orch_scores.values()]
        anova_result = self.analyzer.anova_test(groups)
        
        return {
            "groups": {k: len(v) for k, v in orch_scores.items()},
            "means": {k: float(np.mean(v)) for k, v in orch_scores.items()},
            "anova": anova_result
        }
    
    def analyze_by_knowledge(self, results: List[Dict]) -> Dict[str, Any]:
        """Bilgi seviyesi bazlı analiz"""
        knowledge_scores = {}
        for r in results:
            if r.get("user_score") is None:
                continue
            
            level = r["knowledge_level"]
            if level not in knowledge_scores:
                knowledge_scores[level] = []
            knowledge_scores[level].append(r["user_score"])
        
        if len(knowledge_scores) < 2:
            return {"error": "Yeterli veri yok"}
        
        groups = [np.array(scores) for scores in knowledge_scores.values()]
        anova_result = self.analyzer.anova_test(groups)
        
        return {
            "groups": {k: len(v) for k, v in knowledge_scores.items()},
            "means": {k: float(np.mean(v)) for k, v in knowledge_scores.items()},
            "anova": anova_result
        }
    
    def calculate_consistency(self, results: List[Dict]) -> Dict[str, Any]:
        """Tutarlılık skoru hesapla (aynı query x3)"""
        from collections import defaultdict
        
        # Group by query_id + model + orch + knowledge
        query_groups = defaultdict(list)
        for r in results:
            if r.get("user_score") is None:
                continue
            
            key = f"{r['query_id']}_{r['model_level']}_{r['orchestration']}_{r['knowledge_level']}"
            query_groups[key].append(r["user_score"])
        
        # Only keep groups with multiple scores
        consistency_scores = []
        for key, scores in query_groups.items():
            if len(scores) >= 2:
                variance = np.var(scores)
                consistency_scores.append({
                    "key": key,
                    "scores": scores,
                    "variance": variance,
                    "std": np.std(scores)
                })
        
        if not consistency_scores:
            return {"error": "Yeterli tutarlılık verisi yok"}
        
        avg_variance = np.mean([c["variance"] for c in consistency_scores])
        
        return {
            "num_groups": len(consistency_scores),
            "avg_variance": float(avg_variance),
            "consistency_score": float(1 / (1 + avg_variance)),  # Higher is better
            "details": consistency_scores[:5]  # First 5 examples
        }
    
    def analyze_latency(self, results: List[Dict]) -> Dict[str, Any]:
        """Latency analizi"""
        latencies = {level: [] for level in ["smart", "medium", "dumb"]}
        
        for r in results:
            if r.get("elapsed_seconds"):
                latencies[r["model_level"]].append(r["elapsed_seconds"])
        
        return {
            level: {
                "mean": float(np.mean(times)) if times else 0,
                "std": float(np.std(times)) if times else 0,
                "min": float(np.min(times)) if times else 0,
                "max": float(np.max(times)) if times else 0,
                "count": len(times)
            }
            for level, times in latencies.items()
        }
    
    def generate_report(self, results: List[Dict]) -> Dict[str, Any]:
        """Tam analiz raporu oluştur"""
        scored_results = [r for r in results if r.get("user_score") is not None]
        
        if not scored_results:
            return {"error": "Puanlanmış sonuç yok"}
        
        return {
            "summary": {
                "total_experiments": len(results),
                "scored_experiments": len(scored_results),
                "overall_mean_score": float(np.mean([r["user_score"] for r in scored_results])),
                "overall_std": float(np.std([r["user_score"] for r in scored_results]))
            },
            "model_analysis": self.analyze_by_model(scored_results),
            "orchestration_analysis": self.analyze_by_orchestration(scored_results),
            "knowledge_analysis": self.analyze_by_knowledge(scored_results),
            "consistency": self.calculate_consistency(scored_results),
            "latency": self.analyze_latency(results)
        }
    
    def save_report(self, results: List[Dict], filename: str = None):
        """Raporu kaydet"""
        report = self.generate_report(results)
        
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.json"
        
        output_dir = self.results_dir / "analysis"
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report


def main():
    expert = ScienceExpert()
    results = expert.load_results()
    
    if not results:
        print("Sonuç dosyası bulunamadı")
        return
    
    report = expert.save_report(results)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
