import json
import yaml
import time
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from experiment.orchestrations import ChainOfThought, ReAct, ReWOO, Reflexion


console = Console()


class ExperimentRunner:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.models = self.config["models"]
        self.orchestrations = self.config["orchestrations"]
        self.knowledge_levels = self.config["knowledge_levels"]
        self.experiment_config = self.config["experiment"]
        
        self.test_queries = self._load_test_queries()
        self.results = []
        
    def _load_test_queries(self) -> List[Dict]:
        with open(self.experiment_config["test_queries_file"], "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _load_knowledge(self, level: str) -> List[Dict]:
        path = Path(self.experiment_config["knowledge_base_dir"]) / level / "politics.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _get_orchestration(self, name: str, model: str):
        temp = self.experiment_config.get("temperature", 0.7)
        max_iter = self.experiment_config.get("max_iterations", 10)
        
        if name == "cot":
            return ChainOfThought(model, temp)
        elif name == "react":
            return ReAct(model, temp, max_iter)
        elif name == "rewoo":
            return ReWOO(model, temp)
        elif name == "reflexion":
            return Reflexion(model, temp)
        else:
            raise ValueError(f"Unknown orchestration: {name}")
    
    def run_single(
        self, 
        query: Dict, 
        model_level: str, 
        orchestration: str, 
        knowledge_level: str
    ) -> Dict[str, Any]:
        model = self.models[model_level]
        knowledge = self._load_knowledge(knowledge_level)
        orch = self._get_orchestration(orchestration, model)
        
        start_time = time.time()
        try:
            result = orch.run(query["query"], knowledge)
            success = True
            error = None
        except Exception as e:
            result = {"error": str(e)}
            success = False
            error = str(e)
        
        elapsed = time.time() - start_time
        
        return {
            "timestamp": datetime.now().isoformat(),
            "query_id": query["id"],
            "query": query["query"],
            "category": query["category"],
            "model_level": model_level,
            "model_name": model,
            "orchestration": orchestration,
            "knowledge_level": knowledge_level,
            "success": success,
            "error": error,
            "result": result,
            "elapsed_seconds": round(elapsed, 2),
            "user_score": None  # Kullanıcı puanlaması için
        }
    
    def run_all(self, limit_queries: int = None, limit_combinations: bool = False):
        queries = self.test_queries[:limit_queries] if limit_queries else self.test_queries
        
        total = len(queries) * len(self.models) * len(self.orchestrations) * len(self.knowledge_levels)
        
        console.print(f"\n[bold cyan]🚀 Deney Başlıyor[/bold cyan]")
        console.print(f"Toplam kombinasyon: {total}")
        console.print(f"  - Sorular: {len(queries)}")
        console.print(f"  - Modeller: {list(self.models.keys())}")
        console.print(f"  - Orkestrasyonlar: {self.orchestrations}")
        console.print(f"  - Bilgi seviyeleri: {self.knowledge_levels}\n")
        
        count = 0
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deney çalışıyor...", total=total)
            
            for query in queries:
                for model_level in self.models.keys():
                    for orch in self.orchestrations:
                        for knowledge_level in self.knowledge_levels:
                            if limit_combinations and knowledge_level != "comprehensive":
                                continue
                                
                            result = self.run_single(query, model_level, orch, knowledge_level)
                            self.results.append(result)
                            count += 1
                            progress.update(task, advance=1)
        
        console.print(f"\n[bold green]✅ Tamamlandı! {count} sonuç[/bold green]")
        self._save_results()
        return self.results
    
    def _save_results(self):
        output_dir = Path(self.experiment_config["results_dir"])
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"results_{timestamp}.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        console.print(f"[dim]Sonuçlar kaydedildi: {output_file}[/dim]")
    
    def get_summary_table(self) -> Table:
        table = Table(title="Deney Özeti")
        
        table.add_column("Metrik", style="cyan")
        table.add_column("Değer", style="magenta")
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        avg_time = sum(r["elapsed_seconds"] for r in self.results) / total if total > 0 else 0
        
        table.add_row("Toplam Deney", str(total))
        table.add_row("Başarılı", f"{successful} ({100*successful/total:.1f}%)")
        table.add_row("Ortalama Süre", f"{avg_time:.2f}s")
        
        return table
    
    def get_results_for_scoring(self) -> List[Dict]:
        return [r for r in self.results if r["success"]]
    
    def save_user_scores(self, scores: Dict[str, int]):
        for r in self.results:
            key = f"{r['query_id']}_{r['model_level']}_{r['orchestration']}_{r['knowledge_level']}"
            if key in scores:
                r["user_score"] = scores[key]
        
        self._save_results()
        console.print("[green]Kullanıcı puanları kaydedildi![/green]")
    
    def export_csv(self, filename: str = None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results_{timestamp}.csv"
        
        import csv
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            if not self.results:
                return
            
            fieldnames = [
                "query_id", "category", "model_level", "orchestration", 
                "knowledge_level", "success", "elapsed_seconds", "user_score"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for r in self.results:
                row = {k: r.get(k) for k in fieldnames}
                writer.writerow(row)
        
        console.print(f"[green]CSV dışa aktarıldı: {filename}[/green]")


def main():
    runner = ExperimentRunner()
    runner.run_all()
    
    console.print(runner.get_summary_table())
    
    scoring_results = runner.get_results_for_scoring()
    console.print(f"\n[yellow]Puanlanacak {len(scoring_results)} sonuç var.[/yellow]")
    console.print("Her sonuç için 1-10 arası puan verin.")


if __name__ == "__main__":
    main()
