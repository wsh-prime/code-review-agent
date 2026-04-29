# Code Review Agent Harness 2.0 瀹炵幇璁″垝

> 鏃ユ湡锛?026-04-24

---

## 1. 鍘熷垯

**鍙仛 review harness锛屼笉鍋氬ぇ鑰屽叏 agent銆?* 闈㈣瘯鏃舵湁浠峰€肩殑鏄?鑳芥妸 context銆乪vidence銆佽鎶ユ帶鍒跺拰 eval 鍋氬嚭鏉?锛岃€屼笉鏄?鎺ヤ簡涓€涓?API"銆?
**闆剁涓夋柟杩愯鏃朵緷璧栥€?* 鏍囧噯搴擄細`ast` `pathlib` `json` `dataclasses` `re` `difflib` `subprocess`銆傜湡瀹?LLM backend 鍚庣疆銆?
**姣忎釜妯″潡璺熺潃娴嬭瘯璧般€?* 鏂版ā鍧椾笂绾垮墠娴嬭瘯鍏堥€氥€?
**榛樿鍙銆?* 鎵€鏈夊懡浠ゅ彧鍐?`--out` 鐩綍锛屼笉淇敼琚垎鏋愪粨搴撱€?
---

## 2. 褰撳墠鐘舵€?
宸插畬鎴愶紙涓嶉渶瑕侀噸鍋氾級锛?
- Python package skeleton銆丆LI 鍏ュ彛
- `models.py` 鍩虹 dataclass
- `hygiene/`锛歴canner銆乪vidence銆乧lassifier銆乼axonomy銆乴lm_classifier銆乸lanner
- 杈撳嚭 Markdown/JSON
- 鍩虹娴嬭瘯

鐪熸缂虹殑锛?
- `context/repo_map.py`锛歊epoMap 鍜?StyleBaseline
- `review/diff_parser.py`锛歶nified diff 鈫?缁撴瀯鍖?hunks
- `review/changed_entity.py`锛歨unk 鈫?function/class/method
- `review/risk.py`锛歞eterministic risk tags
- `review/evidence.py`锛欵videncePackage builder
- `review/rules.py`锛歳ules-only findings
- `review/pipeline.py`锛氫覆璧锋潵鐨?review 鍛戒护
- `eval/`锛歜enchmark + deterministic oracle

---

## 3. 鐩綍缁撴瀯

```
src/code_review_agent/
  cli.py
  models.py

  context/
    __init__.py
    repo_map.py
    test_discovery.py
    # references.py 鈥?post-MVP锛宑all graph 杞婚噺鐗堬紱MVP 闃舵鐢?repo_map.imported_by 瑕嗙洊

  hygiene/
    scanner.py  evidence.py  classifier.py
    llm_classifier.py  planner.py  taxonomy.py

  review/
    __init__.py
    diff_parser.py
    changed_entity.py
    risk.py
    evidence.py
    rules.py
    pipeline.py
    filter.py
    agents.py           # Protocol + FakeLLM
    prompts/
      review_agent.md
      critic_agent.md

  output/
    __init__.py
    json_report.py
    review_markdown.py
    hygiene_markdown.py

  eval/
    __init__.py
    cases.py
    metrics.py
    runner.py
```

---

## 4. 鎵ц椤哄簭

```
Phase 0   鏂囨。鍐荤粨 + README 瀹氫綅
Phase 1   models.py 鍗囩骇
Phase 2   Diff Parser
Phase 3   Minimal RepoMap Builder
Phase 4   Changed Entity Extraction
Phase 5   Risk Classification
Phase 6   Evidence Package Builder
Phase 7   Rules-only Review
Phase 8   Review Pipeline CLI
Phase 9   Micro Eval Benchmark
Phase 10  Markdown/JSON 杈撳嚭瀹屽杽
Phase 11  Review Filter / Critic
Phase 12  Fake/Hybrid Agent Interface锛圥rotocol + FakeLLM锛?Phase 13  Full Eval Benchmark
Phase 14  Demo Polish
```

涓嶈鍏堝仛锛氱湡瀹?LLM SDK銆丟itHub PR comment銆佽嚜鍔ㄤ慨澶嶃€佸璇█ AST銆丏raft鈫扜round鈫扖ritic 閲嶆瀯銆?
---

## 5. Phase 0锛氭枃妗ｅ喕缁?
**鐩爣**锛氭柟鍚戝浐瀹氾紝涓嶅啀鍙樺姩锛屽紑濮嬪啓浠ｇ爜銆?
- [x] 鍦?README 鍐欎竴鍙ヨ瘽瀹氫綅锛歟vidence-first local PR quality gate for AI-generated patches銆?- [x] 鍦?README 鍔犱竴琛?Design Rationale 閾炬帴鍒伴」鐩柟妗堢 8 鑺傘€?- [x] 纭鍛戒护鍚嶏細`map` / `hygiene` / `review` / `eval`锛宍summary` 鍚堝苟杩?`map`銆?- [x] 鏇存柊 `CodeReviewAgent_TODO.md`锛屾爣璁版棫鏂瑰悜宸茶皟鏁淬€?
瀹屾垚鏍囧噯锛歊EADME 鍙锛屽紑鍙戦『搴忔槑纭紝鏃ф柟妗堜笌鏂版柟妗堝叧绯昏娓呮銆?
---

## 6. Phase 1锛氭牳蹇冩暟鎹ā鍨嬪崌绾?
**鐩爣**锛氬厛瀹氭暟鎹粨鏋勶紝鍚庡啓閫昏緫銆?
**鏂板鍒?`models.py`**锛?
```
SymbolSummary
PythonModuleSummary
RepoMap
StyleBaseline      # 瑙佹柟妗堢 9 鑺傚畬鏁?dataclass
DiffLine
DiffHunk
DiffFileChange
ChangedEntity
RiskSignal
EvidencePackage锛堟垨鐢?dict锛屽叿浣撶粨鏋勮鏂规绗?12 鑺傜ず渚嬶級
AgentRun
```

**鎵╁睍宸叉湁妯″瀷**锛?
- `ReviewEvidence`锛氬姞 `id` / `kind` / `source`
- `ReviewIssue`锛氬姞 `confidence` 鍜?`evidence_ids`
- `ReviewIssue` 涓嶅祵濂楀畬鏁?`ReviewEvidence`锛屽畬鏁磋瘉鎹粺涓€鏀惧湪 `EvidencePackage.evidence_index`

**娴嬭瘯**锛歚pytest tests/test_models.py -v`

娴嬭瘯鐐癸細
- 姣忎釜 dataclass 浣跨敤 `slots=True`
- 姣忎釜妯″瀷鏈?`to_dict()`锛岃緭鍑虹ǔ瀹?JSON-friendly dict
- nested model 姝ｇ‘搴忓垪鍖?- `ReviewIssue` 鑳芥惡甯?`confidence` 鍜?`evidence_ids`
- `ReviewIssue.evidence_ids` 鍙鍚庣画 filter 鏍￠獙
- `StyleBaseline` 涓虹┖/闆舵椂涓嶉樆濉炰富娴佺▼

**瀹屾垚鏍囧噯**锛?- [x] 鎵€鏈夋柊澧炴ā鍨嬪彲瀵煎叆
- [x] `to_dict()` 娴嬭瘯閫氳繃
- [x] `python -m pytest tests/test_models.py -v` 閫氳繃

---

## 7. Phase 2锛欴iff Parser

**鐩爣**锛氳В鏋?unified diff锛屼骇鍑虹粨鏋勫寲 changed files 鍜?hunks銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/diff_parser.py
tests/test_review_diff_parser.py
```

鏀寔鏍煎紡锛歚diff --git a/path b/path` / `--- a/path` / `+++ b/path` / `@@ -old,count +new,count @@ section`锛屼互鍙?added / deleted / modified / renamed 鍥涚鏂囦欢鍙樻洿绫诲瀷銆?
`DiffLine` 璁板綍锛歚line_type`锛坈ontext/added/removed锛夈€乣old_lineno`銆乣new_lineno`銆乣content`銆?
閿欒澶勭悊锛氱┖ diff 缁欏嚭娓呮櫚閿欒锛沵alformed hunk 璺宠繃骞惰褰?warning锛沚inary diff 璁板綍 file change锛屼笉杩涘叆 hunk parsing銆?
**瀹屾垚鏍囧噯**锛?- [x] 鑳借鍙?`examples/demo_repo/demo.patch`
- [x] 杈撳嚭 changed files 鍜?hunks锛岃鍙锋纭?
---

## 8. Phase 3锛歁inimal RepoMap Builder

**鐩爣**锛氫负 Python 浠撳簱鏋勫缓 changed entity mapping 鎵€闇€鐨勬渶灏忔満鍣ㄥ彲璇讳笂涓嬫枃銆係tyleBaseline 绗竴鐗堝厑璁镐负绌烘垨鍙寘鍚交閲忓瓧娈碉紝閬垮厤 RepoMap 闃舵杩囬噸銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/context/repo_map.py
src/code_review_agent/context/test_discovery.py
tests/test_context_repo_map.py
tests/test_context_test_discovery.py
```

**`repo_map.py` 绗竴鐗堣礋璐?*锛?
- 澶嶇敤 hygiene scanner 鐨?ignore 瑙勫垯銆?- 鎵弿 Python 鏂囦欢銆?- 鐢?`ast.parse()` 鎻愬彇 module docstring銆?- 鐢?`ast.parse()` 鎻愬彇 imports銆?- 鐢?`ast.parse()` 鎻愬彇 classes / functions / methods銆?- 璁板綍 symbol `line_start` / `line_end`銆?- 寤虹珛鏈€灏?`imports` map銆?- `StyleBaseline` 鍏佽涓虹┖锛屼笉闃诲涓绘祦绋嬶紱褰撳墠瀹炵幇宸叉敹闆?docstring 瑕嗙洊鐜囥€乮mport 椋庢牸銆佹祴璇曞懡鍚嶉鏍硷紝寮傚父澶勭悊妯″紡鏆備负 `mixed`銆?
**鏆傜紦鍒板悗缁寮?*锛?
- 鏇寸簿缁嗙殑 `imported_by` 鍙嶅悜鍥撅紙褰撳墠宸叉湁鍩虹鏈湴妯″潡鍙嶆煡锛夈€?- 鏇寸簿缁嗙殑 public 鍑芥暟 docstring 瑕嗙洊鐜囩瓥鐣ワ紙褰撳墠宸叉湁杞婚噺缁熻锛岃烦杩囨祴璇曟枃浠讹級銆?- import 椋庢牸鍗犳瘮闃堝€肩粺璁°€?- 寮傚父澶勭悊妯″紡缁熻銆?
**`test_discovery.py` 绗竴鐗堣礋璐?*锛?
- 璺緞鍖归厤锛歚tests/test_<module>.py` / `test_<name>.py` / `<name>_test.py`
- 杞婚噺 import + symbol name 鍏宠仈
- 杈撳嚭 `related_tests: dict[str, list[str]]`

**CLI**锛?
```powershell
code-review-agent map --repo examples/demo_repo --out outputs/map
```

杈撳嚭锛歚outputs/map/repo_map.json` + `outputs/map/repo_map.md`

**瀹屾垚鏍囧噯**锛?- [x] 鑳藉 demo repo 杈撳嚭 `repo_map.json`
- [x] Python symbol 琛屽彿鍙敤浜?changed entity mapping
- [x] style_baseline 涓虹┖鏃朵笉褰卞搷涓绘祦绋?
瀹炵幇璁板綍锛歚src/code_review_agent/context/repo_map.py`銆乣context/test_discovery.py` 鍜?`map` CLI 宸茶惤鍦帮紱`PythonModuleSummary` 鏂板 `methods` 瀛楁锛岄伩鍏嶆柟娉曞綊灞炴贩鍏?classes/functions銆?
---

## 9. Phase 4锛欳hanged Entity Extraction

**鐩爣**锛氭妸 diff hunk 鏄犲皠鍒板嚱鏁?绫?鏂规硶鎴?module-level change銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/changed_entity.py
tests/test_review_changed_entity.py
```

鏄犲皠瑙勫垯锛?
- hunk added/modified lines 钀藉湪 function/method 鑼冨洿鍐?鈫?鏄犲皠鍒版渶鍐呭眰 symbol
- 钀藉湪 class body 浣嗕笉鍦?method 鈫?鏄犲皠鍒?class
- 钀藉湪 import / constant / module docstring 鈫?鏄犲皠鍒?module
- 鏂囦欢鍒犻櫎鎴栨棤娉曡В鏋?AST 鈫?file-level entity锛堝綋鍓?`ChangedEntity` schema 鏆傛棤 reason 瀛楁锛?
绗竴鐗堜笉澶勭悊锛氬鏉?nested function銆乨ecorator 绮剧粏褰掑睘銆佽娉曢敊璇枃浠剁殑 AST锛堥€€鍖栧埌 module-level锛夈€?
**瀹屾垚鏍囧噯**锛?- [x] 姣忎釜 hunk 鑷冲皯鏄犲皠鍒颁竴涓?entity
- [x] 鏃犳硶绮剧‘鏄犲皠鏃朵笉宕╂簝
- [x] 杈撳嚭鍖呭惈 hunk id 鍜?line range

瀹炵幇璁板綍锛歚src/code_review_agent/review/changed_entity.py` 宸茶惤鍦帮紱鍚屼竴 hunk 涓?module-level 鍜?symbol-level 鍙樻洿浼氬垎鍒繚鐣欙紝澶氫釜 hunk 鍛戒腑鍚屼竴瀹炰綋鏃跺悎骞?`hunk_ids`銆?
---

## 10. Phase 5锛歊isk Classification

**鐩爣**锛氱敤纭畾鎬ц鍒欑粰 changed entities 鍜?files 鎵?risk tags銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/risk.py
tests/test_review_risk.py
```

鏀寔鐨?tags 鍜岃Е鍙戣鍒欒椤圭洰鏂规绗?10 鑺傘€?
`design_constraint_violation` 瑙﹀彂鏉′欢锛堜笁鏉′箣涓€婊¤冻鍗宠Е鍙戯紝浣?`total_public_functions < 5` 鏃跺叏閮ㄨ烦杩囷級锛?- [x] 鏂板/淇敼 public function 缂哄皯 docstring锛屼笖浠撳簱 `docstring_coverage_ratio >= 0.70`
- [x] 鏂板娴嬭瘯鏂囦欢鍛藉悕涓嶇鍚?`test_naming_pattern`锛坧attern 瀛樺湪鏃讹級
- [x] 鏂板 import 椋庢牸涓?`dominant_import_style` 涓嶄竴鑷达紝涓旇椋庢牸鍗犳瘮 `>= 0.80`锛堝綋鍓?RepoMap 鍙湁鍏ㄩ噺鍗曚竴椋庢牸鏃舵墠缁欏嚭闈?`mixed`锛屽洜姝や繚瀹堣Е鍙戯級

姣忎釜 `RiskSignal` 杈撳嚭锛歚tag` / `confidence` / `reason` / `evidence_ids`

**瀹屾垚鏍囧噯**锛?- [x] `test_gap` 鑳藉湪 demo patch 涓Е鍙?- [x] `doc_only` patch 涓嶈緭鍑?code risk
- [x] `design_constraint_violation` 鍙湪浣庤鎶ヨ鍒欐弧瓒虫椂瑙﹀彂

瀹炵幇璁板綍锛歚src/code_review_agent/review/risk.py` 宸茶惤鍦帮紝鎵€鏈?Phase5 tag 鍧囨湁绗竴鐗堢‘瀹氭€ц鍒欙紱杈撳嚭浠呬负 `RiskSignal`锛屾寮?finding 鐣欑粰 Phase7 rules銆?
---

## 11. Phase 6锛欵vidence Package Builder

**鐩爣**锛氭妸 diff銆丷epoMap銆乧hanged entities銆乺isk tags銆乭ygiene signals 姹囨€绘垚 ReviewAgent 鍙秷璐圭殑缁撴瀯鍖栦笂涓嬫枃銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/evidence.py
tests/test_review_evidence.py
```

姣忔潯 evidence 鏈夌ǔ瀹?id锛屾牸寮忥細

```
diff:src/shop/service.py:35
entity:src/shop/service.py:create_order
risk:test_gap:src/shop/service.py
test_discovery:tests/test_service.py
hygiene:src/shop/debug_flow.py
```

Metadata redaction 瑙勫垯锛堣椤圭洰鏂规绗?11 鑺傦級锛歅R title/commit message/author 涓嶈繘鍏?EvidencePackage锛屾湰鍦?diff MVP 閫氬父娌℃湁杩欎簺瀛楁锛屼絾 schema 棰勭暀 redacted 鏍囪浣嶃€?
**瀹屾垚鏍囧噯**锛?- [x] 姣忎釜 changed file 鑳界敓鎴?EvidencePackage
- [x] risk signals 鍜?evidence id 浜掔浉寮曠敤
- [x] JSON 鍙簭鍒楀寲

瀹炵幇璁板綍锛歚src/code_review_agent/review/evidence.py` 宸茶惤鍦帮紝鐢熸垚 diff/entity/risk/test_discovery/hygiene 浜旂被 `ReviewEvidence`锛沗find_missing_evidence_ids()` 棰勭暀缁?Phase8 inline filter 鍜?Phase11 姝ｅ紡 filter 澶嶇敤銆?
---

## 12. Phase 7锛歊ules-only Review

**鐩爣**锛氬湪娌℃湁鐪熷疄 LLM 鐨勬儏鍐典笅璺戦€?review pipeline銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/rules.py
tests/test_review_rules.py
```

绗竴鐗堝彧鍋氬洓鏉￠珮淇″彿瑙勫垯锛?
**Rule 1 鈥?Test Gap**锛氶潪娴嬭瘯浠ｇ爜鍙樻洿 + related tests 瀛樺湪 + patch 娌℃湁鏀逛换浣?related test 鈫?`test_gap` / medium / confidence 0.75鈥?.9

**Rule 2 鈥?Process Artifact Added To Mainline**锛歱atch 鏂板鏂囦欢 + 鏂囦欢鍦?`src/` 鎴栨牴鐩綍 + hygiene 鍒ゆ柇涓?experiment/debug/demo/tmp/generated 鈫?`experiment_artifact` / low-medium / confidence 0.7鈥?.9

**Rule 3 鈥?Broad Exception Handling**锛歛dded lines 鍚?`except Exception` 鎴?bare `except` + 闈炴祴璇?Python 鏂囦欢 鈫?`error_handling` / medium / confidence 0.7鈥?.85

**Rule 4 鈥?Dependency Change**锛歞ependency file 鍙樻洿 + 鏃?lock/test/config 璇存槑 鈫?`dependency_change` / low / confidence 0.6鈥?.75锛岄粯璁ゆ斁鍏?`needs_human_review`

**瀹屾垚鏍囧噯**锛?- [x] 涓嶄緷璧?LLM 涔熻兘杈撳嚭 review report
- [x] demo case 鑳借Е鍙?`test_gap` 鍜?`experiment_artifact`
- [x] no-finding patch 鑳戒繚鎸佹棤姝ｅ紡 finding

瀹炵幇璁板綍锛歚src/code_review_agent/review/rules.py` 宸茶惤鍦帮紝杈撳嚭 `RulesReviewResult(findings, needs_human_review)`銆傚綋鍓嶆寮?findings 瑕嗙洊 `test_gap`銆乣experiment_artifact` 鍜屾柊澧?broad exception锛沗dependency_change` 榛樿杩涘叆 `needs_human_review`銆?
---

## 13. Phase 8锛歊eview Pipeline CLI

**鐩爣**锛氭妸鍓嶉潰妯″潡涓叉垚鍙敤鐨?`review` 鍛戒护銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/pipeline.py
tests/test_review_pipeline.py
```

鏇存柊锛歚src/code_review_agent/cli.py`

**鍛戒护**锛?
```powershell
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001.patch --out outputs/review
# 鍙€夊弬鏁帮細
--hygiene outputs/hygiene/project_hygiene.json
--repo-map outputs/map/repo_map.json
--mode rules|hybrid-fake
```

Phase 8 绗竴鐗堝彧闇€鏀寔 `--mode rules`锛汸hase 12 宸茶ˉ涓?`--mode hybrid-fake`銆?
**Pipeline 姝ラ**锛?
```
parse diff
build / load repo map
load optional hygiene
extract changed entities
classify risks
build evidence packages
run rules
inline filter锛堜粎涓ゆ潯锛氫涪寮?evidence_ids 涓虹┖鐨?finding锛屼涪寮?file 涓嶅湪 changed_files 涓殑 finding锛?write report
```

> Phase 8 鍙仛涓ゆ潯鍐呰仈杩囨护銆傚畬鏁?filter 閫昏緫锛坈onfidence threshold銆乨uplicate 鍚堝苟銆乨owngrade锛夊湪 Phase 11 姝ｅ紡瀹炵幇锛孭hase 8 涓嶄緷璧?Phase 11銆?
**瀹屾垚鏍囧噯**锛?- [x] 涓€鏉″懡浠ゅ彲浠ヨ窇瀹?demo patch
- [x] 杈撳嚭 changed files / changed entities / risk tags / findings
- [x] 鏃?LLM 鐜鍙繍琛?- [x] 榛樿涓嶄慨鏀?repo

瀹炵幇璁板綍锛歚src/code_review_agent/review/pipeline.py` 鍜?`code-review-agent review` CLI 宸茶惤鍦般€侾hase 10 鍚庯紝鎶ュ憡鍐欏叆宸插鎵樼粰 `output/json_report.py` 鍜?`output/review_markdown.py`銆?
---

## 14. Phase 9锛歁icro Eval Benchmark

**鐩爣**锛氬湪 rules-only review pipeline 璺戦€氬悗锛岀珛鍒诲姞鍏ユ渶灏忓洖褰掗泦锛岄伩鍏?risk/rules/filter 鍚庣画璋冩暣鏃惰涓烘紓绉汇€?
**鏂板鎴栧鐢ㄦ枃浠?*锛?
```
examples/eval_cases/patches/case_001_test_gap.patch
examples/eval_cases/patches/case_002_error_handling.patch
examples/eval_cases/patches/case_003_no_finding_doc_only.patch
examples/eval_cases/ground_truth/case_001_test_gap.json
examples/eval_cases/ground_truth/case_002_error_handling.json
examples/eval_cases/ground_truth/case_003_no_finding_doc_only.json
src/code_review_agent/eval/metrics.py
tests/test_eval_metrics.py
```

**绗竴鐗堝彧鍋?3 涓?case**锛?
- `test_gap`
- `error_handling`
- `no_finding_doc_only`

**瀹屾垚鏍囧噯**锛?- [x] micro eval 鍙互鍦ㄦ湰鍦板揩閫熻繍琛?- [x] oracle 浣跨敤 file equality銆乧ategory equality銆乴ine range overlap
- [x] no-finding case 鍗曠嫭璁＄畻鍑嗙‘鎬?- [x] 涓嶄緷璧?LLM judge

瀹炵幇璁板綍锛歚src/code_review_agent/eval/metrics.py` 宸茶惤鍦帮紝鏂板 3 涓?micro eval patch / ground truth fixtures銆傚綋鍓?Phase 9 鍙疄鐜?metrics 鍜?fixtures锛屽畬鏁?`eval` CLI 鐣欑粰 Phase 13銆?
---

## 15. Phase 10锛歁arkdown/JSON 杈撳嚭瀹屽杽

**鐩爣**锛氳鎶ュ憡閫傚悎 README 鎴浘鍜岄潰璇曞睍绀恒€?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/output/json_report.py
src/code_review_agent/output/review_markdown.py
tests/test_output_review_markdown.py
```

Markdown 缁撴瀯锛?
```markdown
# Review Report

## Summary
## Findings
## Needs Human Review
## Changed Files
## Changed Entities
## Risk Signals
## Evidence Index
```

- Findings 鍦ㄦ渶鍓?- 姣忔潯 finding 蹇呴』鏈?file / line / severity / confidence / evidence list
- No Finding 瑕佽鏄庢鏌ヤ簡浠€涔堛€佷负浠€涔堟病鏈夎緭鍑?- Evidence Index 涓嶈杩囬暱

**瀹屾垚鏍囧噯**锛?- [x] report 閫傚悎鏀捐繘 README
- [x] JSON 瀛楁绋冲畾
- [x] Markdown snapshot 娴嬭瘯閫氳繃

瀹炵幇璁板綍锛歚src/code_review_agent/output/json_report.py` 鍜?`output/review_markdown.py` 宸茶惤鍦帮紱`review/pipeline.py` 宸叉敼涓鸿皟鐢?output 妯″潡鍐?`review_report.json` / `review_report.md`銆侾hase 11/12 鍚庯紝褰撳墠 JSON schema 鐗堟湰涓?`1.1`銆?
---

## 16. Phase 11锛歊eview Filter / Critic

**鐩爣**锛氭寮忓疄鐜拌鎶ユ帶鍒跺眰銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/filter.py
tests/test_review_filter.py
```

杩囨护/闄嶇骇瑙勫垯锛?
- missing evidence
- evidence id 涓嶅瓨鍦?- confidence 浣庝簬闃堝€?- file 涓嶅湪 changed files锛屼篃鏃?related evidence
- line 涓?changed hunk/entity 瀹屽叏鏃犲叧
- message 鏄函椋庢牸鍋忓ソ
- duplicate issues

杈撳嚭鍒嗗尯锛歚findings` / `needs_human_review` / `discarded`锛坄discarded` 鍙啓 JSON锛屼笉鍦?Markdown 涓绘姤鍛婂睍绀猴級

**瀹屾垚鏍囧噯**锛?- [x] filter 鑳介樆姝㈡棤璇佹嵁 issue
- [x] low confidence issue 杩涘叆 needs_human_review
- [x] duplicate finding 琚悎骞?
瀹炵幇璁板綍锛歚src/code_review_agent/review/filter.py` 宸叉寮忔帴鍏?pipeline銆傝繃婊ゅ眰浼氫涪寮?missing/invalid evidence銆佺函椋庢牸鍋忓ソ銆佹棤 changed-file 鍏宠仈鐨?issue锛涗細鎶婁綆缃俊搴︺€佽鍙蜂笌 changed hunk/entity 鏃犲叧銆乫ile 涓嶅湪 changed files 浣嗕粛鏈夌浉鍏?evidence 鐨?issue 闄嶇骇鍒?`needs_human_review`锛沝uplicate finding 浼氬悎骞?evidence ids 骞朵繚鐣欒緝楂樼疆淇″害銆俙discarded` 鍙繘鍏?JSON 鎶ュ憡銆?
---

## 17. Phase 12锛欶ake/Hybrid Agent Interface

**鐩爣**锛氬湪 pipeline 鍜屾寮?filter 绋冲畾鍚庡姞鍏ュ彲閫?fake/hybrid agent锛屽睍绀?agent harness 鎺ュ彛鍜岄槻骞昏鏈哄埗锛屼絾涓嶈鏍稿績鍔熻兘渚濊禆鐪熷疄 API銆?
**鏂板鏂囦欢**锛?
```
src/code_review_agent/review/agents.py
src/code_review_agent/review/prompts/review_agent.md
src/code_review_agent/review/prompts/critic_agent.md
tests/test_review_agents_fake.py
```

**Protocol**锛?
```python
class ReviewAgent(Protocol):
    def review(self, package: EvidencePackage) -> list[ReviewIssue]: ...

class CriticAgent(Protocol):
    def filter(self, issues: list[ReviewIssue], package: EvidencePackage) -> list[ReviewIssue]: ...
```

**FakeLLM 绛栫暐**锛堝繀椤诲尯鍒嗭紝鐢ㄤ簬 eval 灞曠ず correlated failure锛夛細

| 绛栫暐 | 琛屼负 |
|---|---|
| `recall_biased_reviewer` | 鍊惧悜鎻愬嚭鍊欓€?finding锛屾ā鎷熼珮鍙洖 reviewer |
| `precision_biased_critic` | 鍊惧悜璐ㄧ枒銆侀檷绾ф垨杩囨护锛屾ā鎷熼珮绮惧害 critic |
| `same_strategy` | reviewer 鍜?critic 鐢ㄥ悓涓€绛栫暐锛屽睍绀?correlated failure 椋庨櫓 |
| `cross_strategy` | reviewer 鍜?critic 鐢ㄤ笉鍚岀瓥鐣ワ紝灞曠ず harness 鐨勮繃婊や环鍊?|

**Prompt Export**锛堟棤 API 鏃朵篃鑳藉睍绀轰笂涓嬫枃鍑嗗锛夛細

```powershell
code-review-agent review --repo . --diff changes.patch --out outputs/review --export-prompts
```

杈撳嚭 `outputs/review/prompts/review_agent_input.json` + `review_agent_prompt.md`銆?
鐪熷疄 LLM backend 浣滀负鍚庣画 Phase锛屼笉杩涘叆 MVP銆?
**瀹屾垚鏍囧噯**锛?- [x] 鏀寔 `--mode rules` 鍜?`--mode hybrid-fake`
- [x] Fake LLM finding 缁忚繃 evidence validator
- [x] invalid evidence id 琚繃婊ゆ垨闄嶇骇
- [x] prompt 鏂囦欢鏈?hash

瀹炵幇璁板綍锛歚src/code_review_agent/review/agents.py` 宸茶惤鍦帮紝鍖呭惈 `ReviewAgent` / `CriticAgent` Protocol銆乺ecall-biased fake reviewer銆乸recision-biased fake critic銆乣same_strategy` / `cross_strategy` harness锛屼互鍙?prompt hash/export 宸ュ叿銆俙code-review-agent review` 宸叉敮鎸?`--mode hybrid-fake` 鍜?`--export-prompts`锛屽鍑?`review_agent_input.json`銆乣review_agent_prompt.md`銆乣critic_agent_input.json`銆乣critic_agent_prompt.md`銆?
---

## 18. Phase 13锛欶ull Eval Benchmark

**鐩爣**锛氱敤灏忓瀷 benchmark 璇佹槑椤圭洰涓嶆槸 toy銆傚繀椤讳娇鐢?deterministic oracle锛屼笉浣跨敤 LLM judge銆?
**鏂板鏂囦欢**锛?
```
examples/eval_cases/demo_repo/src/shop/...
examples/eval_cases/patches/case_001_test_gap.patch ... case_007_design_constraint.patch
examples/eval_cases/ground_truth/case_001_test_gap.json ... case_007_design_constraint.json
src/code_review_agent/eval/__init__.py
src/code_review_agent/eval/cases.py
src/code_review_agent/eval/metrics.py
src/code_review_agent/eval/runner.py
tests/test_eval_metrics.py
```

**Deterministic Oracle**锛?
```
finding.file == ground_truth.file
AND finding.category == ground_truth.category
AND line_range_overlap(finding, ground_truth) >= threshold
```

**鍛戒护**锛?
```powershell
code-review-agent eval --cases examples/eval_cases --out outputs/eval --mode rules
```

**Threshold Profiles**锛歚strict` / `balanced` / `recall`锛堣椤圭洰鏂规绗?12 鑺傦級

**瀹屾垚鏍囧噯**锛?- [ ] 鑷冲皯 5 涓?eval cases
- [ ] 鑷冲皯 2 涓?no-finding cases锛坉oc-only 鍜?test-only锛?- [ ] eval 鍛戒护鍙窇閫?- [ ] oracle 浣跨敤 planted bug + line range overlap
- [ ] eval 涓嶄緷璧?LLM judge
- [ ] 鎶ュ憡灞曠ず strict/balanced/recall frontier 琛?- [ ] README 鍙互灞曠ず涓€寮犳寚鏍囪〃
- [ ] 鑳藉姣?rules-only 涓?fake/evidence-backed variant

---

## 19. Phase 14锛欴emo Polish

**鐩爣**锛氳椤圭洰閫傚悎鎶曠畝鍘嗐€佸綍灞忋€侀潰璇曡瑙ｃ€?
**README 蹇呴』鍖呭惈**锛?
- 涓€鍙ヨ瘽瀹氫綅
- 涓轰粈涔堜笉鏄櫘閫?AI Review Bot锛堜笁琛屽唴璁叉竻妤氾級
- 鏋舵瀯鍥?- demo 鍛戒护
- sample report 鎴浘鎴栨枃鏈墖娈?- eval 鎸囨爣琛?- 褰撳墠闄愬埗锛堝彧鍋?Python锛屾棤鐪熷疄 LLM锛?
**Demo 鍛戒护锛堝繀椤诲彲澶嶇幇锛?*锛?
```powershell
pip install -e ".[dev]"
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map     --repo examples/demo_repo --out outputs/demo-map
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
code-review-agent eval    --cases examples/eval_cases --out outputs/demo-eval
```

**闈㈣瘯璁茶В椤哄簭**锛?
1. AI coding 鐢熸垚 PR 瓒婃潵瓒婂锛岄棶棰樻槸淇′换鍜岃鎶?2. 瑁?LLM review 鏄?`diff 鈫?comments`锛屼笉鍙帶锛屼笖鍚屾簮澶辫触
3. 鎴戠殑绯荤粺锛歚diff + repo 鈫?evidence 鈫?constrained agent 鈫?verified report`
4. 灞曠ず test gap case 鐨?finding + evidence index
5. 灞曠ず eval metrics 鍜?frontier 琛?6. 瑙ｉ噴 hygiene 妯″潡濡備綍璇嗗埆杩囩▼璧勪骇姹℃煋

**瀹屾垚鏍囧噯**锛?- [ ] README 鑳藉湪 3 鍒嗛挓鍐呰娓呮椤圭洰
- [ ] demo 鍛戒护鍙鐜?- [ ] 鎶ュ憡閲屾湁鑷冲皯涓€涓珮璐ㄩ噺 finding 鍜屼竴涓?No Finding case
- [ ] eval 杈撳嚭鑳芥敮鎾?涓嶆槸 toy"鐨勫彊浜?
---

## 20. 娴嬭瘯鏂囦欢瀵圭収琛?
| 妯″潡 | 娴嬭瘯鏂囦欢 |
|---|---|
| `context/repo_map.py` | `tests/test_context_repo_map.py` |
| `context/test_discovery.py` | `tests/test_context_test_discovery.py` |
| `review/diff_parser.py` | `tests/test_review_diff_parser.py` |
| `review/changed_entity.py` | `tests/test_review_changed_entity.py` |
| `review/risk.py` | `tests/test_review_risk.py` |
| `review/evidence.py` | `tests/test_review_evidence.py` |
| `review/rules.py` | `tests/test_review_rules.py` |
| `review/pipeline.py` | `tests/test_review_pipeline.py` |
| `output/review_markdown.py` | `tests/test_output_review_markdown.py` |
| `review/agents.py` | `tests/test_review_agents_fake.py` |
| `review/filter.py` | `tests/test_review_filter.py` |
| `eval/metrics.py` | `tests/test_eval_metrics.py` |

---

## 21. 楠屾敹鏍囧噯

杈惧埌浠ヤ笅鍏ㄩ儴鏍囧噯锛岄」鐩彲浣滀负绠€鍘嗕富鐗堟湰锛?
- [x] `hygiene` 鑳借瘑鍒繃绋嬭祫浜у苟杈撳嚭鎶ュ憡
- [x] `map` 鑳借緭鍑?Python RepoMap
- [x] `review` 鑳借В鏋?diff 骞跺畾浣?changed entities
- [x] `review` 鑳借緭鍑?risk tags
- [x] `review` 鑳借緭鍑?evidence-backed findings 鎴?No Finding
- [x] 姣忔潯 finding 閮芥湁 evidence
- [x] 鏃?LLM/API key 鐜鍙繍琛?- [ ] 鑷冲皯 5 涓?eval cases锛岃嚦灏?2 涓?no-finding cases
- [ ] eval 浣跨敤 deterministic oracle锛屼笉渚濊禆 LLM judge
- [ ] eval 鑳借緭鍑?precision / recall / false positives / key bug inclusion
- [ ] eval 鑳藉睍绀?strict/balanced/recall 鐨?trade-off frontier
- [ ] README 鏈夊彲澶嶇幇 demo 鍛戒护鍜?sample report

---

## 22. 鍚庣画澧炲己锛圡VP 鍚庡啀鑰冭檻锛?
**鐪熷疄 LLM Backend**锛歄penAI-compatible API锛孉PI key 鍙鐜鍙橀噺锛宲rompt hash锛宮odel 璁板綍锛宼imeout/fallback锛宻chema validation銆俽eviewer 鍜?critic 鍙€変娇鐢ㄤ笉鍚屾ā鍨嬫棌浣滀负 correlated failure 闃插尽澧炲己銆?
**Draft 鈫?Ground 鈫?Critic Pipeline**锛欴raftAgent 杈撳嚭 CandidateFinding锛孏roundingVerifier 缁戝畾 evidence id锛孋riticFilter 鍋氭渶缁堣繃婊ゃ€備笉杩涘叆 MVP锛岄伩鍏嶈繃鏃╁鍔?pipeline 鐘舵€佸拰娴嬭瘯澶嶆潅搴︺€?
**GitHub Integration**锛氳緭鍏?PR URL锛屾媺鍙?diff锛宒ry-run report锛屽彲閫夊彂甯?PR comment銆?
**MCP / Tool Protocol**锛氭毚闇?repo_map / review report / hygiene scan锛屼緵 Codex/Cursor 璋冪敤銆?
**澶氳瑷€**锛欽avaScript/TypeScript銆丟o銆丣ava銆傚缓绔嬪湪 evidence-first review harness 绋冲畾鍚庛€?
---

## 23. 椋庨櫓涓庢帶鍒?
| 椋庨櫓 | 鎺у埗 |
|---|---|
| 鑼冨洿杩囧ぇ | 鍏堝畬鎴?Python + local CLI + rules-only |
| 璇姤澶 | 鍙緭鍑洪珮璇佹嵁 finding锛屼綆缃俊搴﹂檷绾?|
| LLM 鎴愪负椤圭洰鐡堕 | MVP 涓嶄緷璧栫湡瀹?API |
| Demo 涓嶅彲淇?| 鍋?eval cases 鍜?no-finding case |
| Eval 琚川鐤?| planted bug + deterministic oracle锛屼笉鐢?LLM judge |
| LLM 琚?metadata 璇卞 | prompt/export 榛樿 metadata redaction |
| 鏂囨。澶氫簬浠ｇ爜 | 姣忎釜 Phase 閮芥湁鍙繍琛屽懡浠ゅ拰娴嬭瘯 |
| AST 鏄犲皠澶嶆潅 | 鍏堝鐞嗗父瑙?function/class/method锛屽け璐ユ椂 module-level fallback |

---

## 24. 鏈€灏忓彲婕旂ず鐗堟湰

濡傛灉鏃堕棿鏋佺揣锛屽彧闇€瑕侊細

```
review/diff_parser.py
context/repo_map.py
review/changed_entity.py
review/risk.py
review/evidence.py
review/rules.py
review_report.md + json
3 涓?demo patches
deterministic eval oracle
2 涓?no-finding cases
```

鏈€灏?demo 鍛戒护锛?
```powershell
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
```

鏈€灏?demo 鎶ュ憡蹇呴』灞曠ず锛歝hanged files / changed entity / `test_gap` risk / evidence / no-finding case銆?
