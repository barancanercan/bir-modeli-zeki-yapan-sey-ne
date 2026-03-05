import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table


console = Console()


def load_results(results_dir: str = "results") -> dict:
    results_files = list(Path(results_dir).glob("results_*.json"))
    if not results_files:
        console.print("[red]Sonuç dosyası bulunamadı![/red]")
        return None
    
    latest = sorted(results_files)[-1]
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


def score_results(results: list):
    scoring_results = [r for r in results if r.get("success") and r.get("user_score") is None]
    
    if not scoring_results:
        console.print("[yellow]Puanlanacak yeni sonuç yok![/yellow]")
        return {}
    
    console.print(f"\n[bold cyan]📝 Puanlama: {len(scoring_results)} sonuç[/bold cyan]")
    console.print("Her cevabı 1-10 arası puanlayın (1=çok kötü, 10=mükemmel)\n")
    
    scores = {}
    current_query_id = None
    
    for r in scoring_results:
        if current_query_id != r["query_id"]:
            console.print(f"\n[bold]Soru {r['query_id']}:[/bold] {r['query'][:80]}...")
            current_query_id = r["query_id"]
        
        key = f"{r['query_id']}_{r['model_level']}_{r['orchestration']}_{r['knowledge_level']}"
        
        info = f"[{r['model_level']}] {r['orchestration']} + {r['knowledge_level']} | {r['elapsed_seconds']}s"
        
        console.print(f"\n  {info}")
        
        answer = r.get("result", {})
        if isinstance(answer, dict):
            if "response" in answer:
                text = answer["response"].get("answer", str(answer))[:200]
            elif "final_answer" in answer:
                text = answer.get("final_answer", str(answer))[:200]
            elif "revised_answer" in answer:
                text = answer.get("revised_answer", str(answer))[:200]
            else:
                text = str(answer)[:200]
        else:
            text = str(answer)[:200]
        
        console.print(f"  Cevap: {text}...")
        
        while True:
            try:
                score = Prompt.ask("  Puan (1-10)", default="5")
                score = int(score)
                if 1 <= score <= 10:
                    scores[key] = score
                    break
                else:
                    console.print("[red]Lütfen 1-10 arasında girin[/red]")
            except ValueError:
                console.print("[red]Geçerli bir sayı girin[/red]")
    
    return scores


def show_summary(results: list):
    scored = [r for r in results if r.get("user_score") is not None]
    
    if not scored:
        console.print("[yellow]Henüz puanlanmış sonuç yok![/yellow]")
        return
    
    table = Table(title="📊 Kullanıcı Puanları Özeti")
    table.add_column("Model", style="cyan")
    table.add_column("Orkestrasyon", style="magenta")
    table.add_column("Bilgi", style="green")
    table.add_column("Ortalama Puan", style="yellow")
    
    from collections import defaultdict
    by_model = defaultdict(list)
    by_orch = defaultdict(list)
    by_knowledge = defaultdict(list)
    
    for r in scored:
        by_model[r["model_level"]].append(r["user_score"])
        by_orch[r["orchestration"]].append(r["user_score"])
        by_knowledge[r["knowledge_level"]].append(r["user_score"])
    
    for level, scores in by_model.items():
        avg = sum(scores) / len(scores)
        table.add_row(level, "-", "-", f"{avg:.2f}")
    
    for orch, scores in by_orch.items():
        avg = sum(scores) / len(scores)
        table.add_row("-", orch, "-", f"{avg:.2f}")
    
    for kb, scores in by_knowledge.items():
        avg = sum(scores) / len(scores)
        table.add_row("-", "-", kb, f"{avg:.2f}")
    
    console.print(table)
    
    console.print(f"\n[bold]Genel Ortalama:[/bold] {sum(r['user_score'] for r in scored) / len(scored):.2f}")


def main():
    results = load_results()
    if not results:
        return
    
    while True:
        console.print("\n[bold cyan]🎯 Scoring Sistemi[/bold cyan]")
        console.print("1. Yeni sonuçları puanla")
        console.print("2. Özet görüntüle")
        console.print("3. Çıkış")
        
        choice = Prompt.ask("Seçim", choices=["1", "2", "3"], default="3")
        
        if choice == "1":
            scores = score_results(results)
            if scores:
                for r in results:
                    key = f"{r['query_id']}_{r['model_level']}_{r['orchestration']}_{r['knowledge_level']}"
                    if key in scores:
                        r["user_score"] = scores[key]
                
                output_files = list(Path("results").glob("results_*.json"))
                latest = sorted(output_files)[-1]
                with open(latest, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                console.print("[green]Puanlar kaydedildi![/green]")
        elif choice == "2":
            show_summary(results)
        else:
            break


if __name__ == "__main__":
    main()
