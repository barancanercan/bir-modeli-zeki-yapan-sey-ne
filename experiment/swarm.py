import json
import asyncio
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import sys
import logging

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

console = Console()


class ExperimentLogger:
    """Log all experiment outputs to file"""
    
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"experiment_{timestamp}.log"
        
        # Setup logging
        self.logger = logging.getLogger("experiment")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(self.log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        # Console handler for real-time output
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def debug(self, msg):
        self.logger.debug(msg)
    
    def log_experiment(self, query: Dict, model_level: str, orch: str, knowledge: str, result: Dict):
        """Log experiment details"""
        self.logger.info("=" * 60)
        self.logger.info(f"SORU: {query['query']}")
        self.logger.info(f"Model: {model_level} | Orkestrasyon: {orch} | Bilgi: {knowledge}")
        self.logger.info("-" * 40)
        
        if result.get("success"):
            res = result.get("result", {})
            
            # Extract answer based on orchestration type
            if "final_answer" in res:
                answer = res["final_answer"]
            elif "response" in res:
                answer = res["response"].get("answer", str(res["response"]))
            elif "revised_answer" in res:
                answer = res["revised_answer"]
            else:
                answer = str(res)
            
            self.logger.info(f"CEVAP:\n{answer[:1000]}...")
            self.logger.info(f"Süre: {result.get('elapsed_seconds')}s")
            self.logger.info(f"Başarılı: {result.get('success')}")
        else:
            self.logger.error(f"HATA: {result.get('error')}")
        
        self.logger.info("=" * 60)


# Global logger
logger = ExperimentLogger()


class AgentWorkflow:
    """Agent workflow durumu"""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    
    def __init__(self, name: str):
        self.name = name
        self.status = self.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.status = self.RUNNING
        self.start_time = datetime.now()
    
    def complete(self, result: Any):
        self.status = self.COMPLETED
        self.result = result
        self.end_time = datetime.now()
    
    def fail(self, error: str):
        self.status = self.FAILED
        self.error = error
        self.end_time = datetime.now()
    
    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0


class MetaAgentSwarm:
    """
    Agent 4: Meta-Agent Swarm Orchestrator
    
    Koordinasyon:
    1. Initialize → Agent 1 (Knowledge)
    2. Validate  → Agent 2 (Science)
    3. Execute   → Agent 3 (Code)
    4. Analyze   → Agent 2 (Stats)
    5. Report    → Agent 1 (Documentation)
    
    Özellikler:
    - Self-correction loop
    - Human-in-the-loop checkpoints
    - Adaptive parameter tuning
    - Multi-model voting
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.models = self.config["models"]
        self.orchestrations = self.config["orchestrations"]
        self.knowledge_levels = self.config["knowledge_levels"]
        
        # Logger
        self.logger = ExperimentLogger()
        
        # Workflow state
        self.workflows: Dict[str, AgentWorkflow] = {}
        self.experiment_results: List[Dict] = []
        self.analysis_results: Dict = {}
        
        # Agents (lazy loaded)
        self._politics_expert = None
        self._science_expert = None
        self._code_expert = None
    
    @property
    def politics_expert(self):
        if self._politics_expert is None:
            from experiment.agents.politics_expert import PoliticsExpert
            self._politics_expert = PoliticsExpert()
        return self._politics_expert
    
    @property
    def science_expert(self):
        if self._science_expert is None:
            from experiment.agents.science_expert import ScienceExpert
            self._science_expert = ScienceExpert()
        return self._science_expert
    
    @property
    def code_expert(self):
        if self._code_expert is None:
            from experiment.agents.code_expert import CodeExpert
            self._code_expert = CodeExpert()
        return self._code_expert
    
    async def run(self, limit_queries: int = None):
        """Tüm swarm'ı çalıştır"""
        
        console.print("\n[bold cyan]👑 Meta-Agent Swarm Başlıyor[/bold cyan]\n")
        
        # Phase 1: Initialize Knowledge Base
        await self._phase_initialize()
        
        # Phase 2: Validate Design
        await self._phase_validate()
        
        # Phase 3: Run Experiments
        await self._phase_execute(limit_queries)
        
        # Phase 4: Analyze Results
        await self._phase_analyze()
        
        # Phase 5: Generate Report
        await self._phase_report()
        
        console.print("\n[bold green]✅ Swarm Tamamlandı![/bold green]\n")
        
        return {
            "workflows": {k: {"status": v.status, "duration": v.duration} 
                         for k, v in self.workflows.items()},
            "experiment_count": len(self.experiment_results),
            "analysis": self.analysis_results
        }
    
    async def _phase_initialize(self):
        """Phase 1: Knowledge Base hazırla"""
        workflow = AgentWorkflow("Initialize Knowledge Base")
        workflow.start()
        self.workflows["init"] = workflow
        
        console.print("[yellow]📚 Phase 1: Knowledge Base hazırlanıyor...[/yellow]")
        
        try:
            # Build FAISS index
            self.politics_expert.build_index()
            workflow.complete({"status": "FAISS index built"})
            console.print("[green]  ✓ Knowledge Base hazır[/green]")
        except Exception as e:
            workflow.fail(str(e))
            console.print(f"[red]  ✗ Hata: {e}[/red]")
    
    async def _phase_validate(self):
        """Phase 2: Deney tasarımını doğrula"""
        workflow = AgentWorkflow("Validate Experiment Design")
        workflow.start()
        self.workflows["validate"] = workflow
        
        console.print("[yellow]🔬 Phase 2: Deney tasarımı doğrulanıyor...[/yellow]")
        
        # Check config
        validation = {
            "models": list(self.models.keys()),
            "orchestrations": self.orchestrations,
            "knowledge_levels": self.knowledge_levels
        }
        
        # Check FAISS index
        index_path = Path("data/faiss_index/politics.index")
        validation["faiss_index_exists"] = index_path.exists()
        
        workflow.complete(validation)
        console.print(f"[green]  ✓ Konfigürasyon doğrulandı: {len(self.models)} model[/green]")
    
    async def _phase_execute(self, limit_queries: int = None):
        """Phase 3: Deneyleri çalıştır"""
        workflow = AgentWorkflow("Execute Experiments")
        workflow.start()
        self.workflows["execute"] = workflow
        
        console.print("[yellow]🚀 Phase 3: Deneyler çalışıyor...[/yellow]")
        
        # Load test queries
        queries_file = Path(self.config["experiment"]["test_queries_file"])
        with open(queries_file, "r", encoding="utf-8") as f:
            queries = json.load(f)
        
        if limit_queries:
            queries = queries[:limit_queries]
        
        # Calculate total experiments
        total = len(queries) * len(self.models) * len(self.orchestrations) * len(self.knowledge_levels)
        
        # Check for checkpoint to resume
        checkpoint_file = Path("results/checkpoint.json")
        completed_experiments = set()
        
        if checkpoint_file.exists():
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                checkpoint_data = json.load(f)
                completed_experiments = set(checkpoint_data.get("completed", []))
                self.experiment_results = checkpoint_data.get("results", [])
                console.print(f"[yellow]  ⚠ Yarım kalan deneyden devam ediliyor... {len(completed_experiments)} tamamlanmış[/yellow]")
        
        console.print(f"  Toplam: {total} deney")
        console.print(f"  Modeller: {list(self.models.keys())}")
        console.print(f"  Orkestrasyonlar: {self.orchestrations}")
        console.print(f"  Bilgi Seviyeleri: {self.knowledge_levels}\n")
        
        count = len(completed_experiments)
        current_query = None
        
        with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
            task = progress.add_task("Deney çalışıyor...", total=total)
            progress.update(task, advance=count)  # Resume from checkpoint
            
            for query in queries:
                for model_level in self.models.keys():
                    for orch in self.orchestrations:
                        for knowledge_level in self.knowledge_levels:
                            # Check if already completed (checkpoint)
                            exp_key = f"{query['id']}_{model_level}_{orch}_{knowledge_level}"
                            
                            if exp_key in completed_experiments:
                                count += 1
                                progress.update(task, advance=1)
                                continue
                            
                            # Show detailed progress
                            exp_info = f"Q{query['id']}|{model_level}|{orch}|{knowledge_level}"
                            
                            # Print current experiment info
                            if current_query != query['id']:
                                console.print(f"\n[dim]Soru {query['id']}: {query['query'][:50]}...[/dim]")
                                current_query = query['id']
                            
                            console.print(f"  → {exp_info}")
                            
                            result = await self._run_single_experiment(
                                query, model_level, orch, knowledge_level
                            )
                            self.experiment_results.append(result)
                            
                            # Save checkpoint every 10 experiments
                            exp_key = f"{query['id']}_{model_level}_{orch}_{knowledge_level}"
                            completed_experiments.add(exp_key)
                            
                            if count % 10 == 0:
                                self._save_checkpoint(completed_experiments)
                            
                            count += 1
                            progress.update(task, advance=1)
        
        # Final checkpoint save
        self._save_checkpoint(completed_experiments, final=True)
        
        workflow.complete({"count": count})
        console.print(f"\n[green]  ✓ {count} deney tamamlandı[/green]")
    
    def _save_checkpoint(self, completed: set, final: bool = False):
        """Save checkpoint to resume if interrupted"""
        checkpoint_dir = Path("results")
        checkpoint_dir.mkdir(exist_ok=True)
        checkpoint_file = checkpoint_dir / "checkpoint.json"
        
        checkpoint_data = {
            "completed": list(completed),
            "results": self.experiment_results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        
        if final:
            console.print(f"[green]  ✓ Checkpoint kaydedildi (final)[/green]")
        elif completed:
            console.print(f"[dim]  💾 Checkpoint: {len(completed)} deney tamamlandı[/dim]")
    
    async def _run_single_experiment(self, query: Dict, model_level: str,
                                     orchestration: str, knowledge_level: str) -> Dict:
        """Tek bir deney çalıştır"""
        from experiment.agents.code_expert import ToolCallingReAct
        from pathlib import Path
        import json
        import time
        
        model = self.models[model_level]
        
        # Load knowledge (basic for now, can use FAISS)
        kb_dir = Path(self.config["experiment"]["knowledge_base_dir"])
        kb_file = kb_dir / knowledge_level / "politics.json"
        
        knowledge = []
        if kb_file.exists():
            with open(kb_file, "r", encoding="utf-8") as f:
                knowledge = json.load(f)
        
        # Run with tool calling
        try:
            orchestrator = ToolCallingReAct(model, max_iterations=3)
            start_time = time.time()
            result = orchestrator.run(query["query"], knowledge)
            elapsed = time.time() - start_time
            
            exp_result = {
                "timestamp": datetime.now().isoformat(),
                "query_id": query["id"],
                "query": query["query"],
                "category": query.get("category", "unknown"),
                "model_level": model_level,
                "model_name": model,
                "orchestration": orchestration,
                "knowledge_level": knowledge_level,
                "success": True,
                "result": result,
                "elapsed_seconds": round(elapsed, 2),
                "user_score": None
            }
            
            # Log detailed output
            self.logger.log_experiment(query, model_level, orchestration, knowledge_level, exp_result)
            
            # Also print to console
            res = result
            if "final_answer" in res:
                answer = res["final_answer"]
            elif "response" in res:
                answer = res["response"].get("answer", str(res["response"]))
            elif "revised_answer" in res:
                answer = res["revised_answer"]
            else:
                answer = str(res)
            
            console.print(f"\n[cyan]══════════════════════════════════════════════════[/cyan]")
            console.print(f"[bold]Soru:[/bold] {query['query'][:80]}...")
            console.print(f"[dim]→ {model_level} | {orchestration} | {knowledge_level} | {elapsed:.1f}s[/dim]")
            console.print(f"\n[green]Cevap:[/green]")
            console.print(answer[:500] + "..." if len(answer) > 500 else answer)
            console.print(f"[cyan]══════════════════════════════════════════════════[/cyan]\n")
            
            return exp_result
            
        except Exception as e:
            exp_result = {
                "timestamp": datetime.now().isoformat(),
                "query_id": query["id"],
                "model_level": model_level,
                "orchestration": orchestration,
                "knowledge_level": knowledge_level,
                "success": False,
                "error": str(e),
                "elapsed_seconds": 0,
                "user_score": None
            }
            
            self.logger.log_experiment(query, model_level, orchestration, knowledge_level, exp_result)
            console.print(f"[red]✗ Hata: {e}[/red]")
            
            return exp_result
    
    async def _phase_analyze(self):
        """Phase 4: Sonuçları analiz et"""
        workflow = AgentWorkflow("Analyze Results")
        workflow.start()
        self.workflows["analyze"] = workflow
        
        console.print("[yellow]📊 Phase 4: Sonuçlar analiz ediliyor...[/yellow]")
        
        # Save raw results
        results_dir = Path(self.config["experiment"]["results_dir"])
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"swarm_results_{timestamp}.json"
        
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(self.experiment_results, f, ensure_ascii=False, indent=2)
        
        # Run statistical analysis
        try:
            self.analysis_results = self.science_expert.save_report(
                self.experiment_results,
                f"swarm_analysis_{timestamp}.json"
            )
            console.print(f"[green]  ✓ Analiz tamamlandı[/green]")
        except Exception as e:
            console.print(f"[yellow]  ⚠ Analiz atlandı: {e}[/yellow]")
            self.analysis_results = {"error": str(e)}
        
        workflow.complete(self.analysis_results)
    
    async def _phase_report(self):
        """Phase 5: Rapor oluştur"""
        workflow = AgentWorkflow("Generate Report")
        workflow.start()
        self.workflows["report"] = workflow
        
        console.print("[yellow]📝 Phase 5: Rapor oluşturuluyor...[/yellow]")
        
        # Summary
        total = len(self.experiment_results)
        successful = sum(1 for r in self.experiment_results if r.get("success"))
        
        summary = {
            "total_experiments": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "workflows": {k: {"status": v.status, "duration": v.duration} 
                         for k, v in self.workflows.items()}
        }
        
        console.print(f"[green]  ✓ Rapor hazır: {successful}/{total} başarılı[/green]")
        
        # Show log file location
        console.print(f"\n[cyan]📁 Log dosyası:[/cyan] {self.logger.log_file}")
        
        workflow.complete(summary)
    
    def interactive_scoring(self):
        """Interaktif puanlama"""
        console.print("\n[bold cyan]🎯 Puanlama Modu[/bold cyan]")
        
        from rich.prompt import Prompt
        
        unscored = [r for r in self.experiment_results 
                   if r.get("success") and r.get("user_score") is None]
        
        if not unscored:
            console.print("[yellow]Puanlanacak sonuç yok[/yellow]")
            return
        
        console.print(f"{len(unscored)} sonuç puanlanacak\n")
        
        for r in unscored:
            key = f"{r['query_id']}_{r['model_level']}_{r['orchestration']}_{r['knowledge_level']}"
            
            console.print(f"[bold]Soru {r['query_id']}:[/bold] {r['query'][:60]}...")
            console.print(f"  [{r['model_level']}] {r['orchestration']} + {r['knowledge_level']}")
            
            answer = r.get("result", {}).get("final_answer", "N/A")[:100]
            console.print(f"  Cevap: {answer}...")
            
            score = Prompt.ask("  Puan (1-10)", default="5")
            try:
                score = int(score)
                if 1 <= score <= 10:
                    r["user_score"] = score
            except:
                pass
            console.print("")
        
        # Save updated results
        results_dir = Path(self.config["experiment"]["results_dir"])
        results_files = sorted(results_dir.glob("swarm_results_*.json"))
        if results_files:
            with open(results_files[-1], "w", encoding="utf-8") as f:
                json.dump(self.experiment_results, f, ensure_ascii=False, indent=2)
        
        console.print("[green]Puanlar kaydedildi![/green]")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Meta-Agent Swarm")
    parser.add_argument("--limit", type=int, default=None, help="Limit queries")
    parser.add_argument("--score", action="store_true", help="Run scoring after")
    parser.add_argument("--clear", action="store_true", help="Clear checkpoint and start fresh")
    args = parser.parse_args()
    
    # Clear checkpoint if requested
    if args.clear:
        checkpoint_file = Path("results/checkpoint.json")
        if checkpoint_file.exists():
            checkpoint_file.unlink()
            print("✓ Checkpoint temizlendi")
    
    swarm = MetaAgentSwarm()
    
    # Run swarm
    result = asyncio.run(swarm.run(limit_queries=args.limit))
    
    print("\n" + "="*50)
    print("SWARM ÖZETİ")
    print("="*50)
    print(json.dumps(result, indent=2))
    
    # Interactive scoring if requested
    if args.score:
        swarm.interactive_scoring()


if __name__ == "__main__":
    main()
