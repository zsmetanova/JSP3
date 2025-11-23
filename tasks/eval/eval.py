import argparse
import json

def evaluate(target,gold):
    correct = 0
    total = 0
    tag_type_total = {}
    tag_correct_total = {}
    
    for group_t, group_g  in zip(target["conc"].values(), gold["conc"].values()):
        for item_t, item_g in zip(group_t.values(),group_g.values()):
            tag_t = item_t.get("tag")
            tag_g = item_g.get("tag")

            if not tag_g or not tag_t:  
                continue
        
            total += 1
            
            g_key = tag_g[-1] if "-" in tag_g else tag_g
            t_key = tag_g[-1] if "-" in tag_t else tag_t 

            tag_type_total[g_key] = tag_type_total.get(g_key, 0) + 1

            if tag_t == tag_g:
                correct += 1
                tag_correct_total[g_key] = tag_correct_total.get(g_key,0) + 1 

    accuracy = correct / total 

    print(f"\n---Total accuracy---")
    print(f"{accuracy:.2%} correct\n")
    print(f"---Break down results by tag type---")
    for tag in tag_type_total:
        correct_type = tag_correct_total.get(tag, 0) 
        total_correct = tag_type_total[tag] 
        accuracy_tag = correct_type / total_correct
        print(f"{tag}: {accuracy_tag:.2%} correct ({correct_type}/{total_correct})")
    print("\n---Confusion matrix---")
    
    
        
def main():
    parser = argparse.ArgumentParser(description="Evaluate how well this works EVAL")
    parser.add_argument("--target", required=True, help="Path to model output JSON ")
    parser.add_argument("--gold", required=True, help="Path to human-annotated JSON ")
    args = parser.parse_args()

    with open(args.target, "r", encoding="utf-8") as f:
        target = json.load(f)
    with open(args.gold, "r", encoding="utf-8") as f:
        gold = json.load(f)
    
    evaluate(target, gold)

if __name__ == "__main__":
    main()
