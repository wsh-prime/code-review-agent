# Code Review Agent Harness 2.0 TODO

> 鏃ユ湡锛?026-04-25  
> 涓荤嚎锛歟vidence-first review harness 鈫?鐪熷疄 LLM 鍚庣疆  
> 渚濇嵁锛歚CodeReviewAgent_2.0椤圭洰鏂规.md` 路 `CodeReviewAgent_2.0瀹炵幇璁″垝.md`

**瑙勫垯**锛氭柊妯″潡蹇呴』鍚屾鍔犳祴璇曘€侻VP 鍙啓 `--out` 鐩綍锛屼笉淇敼琚垎鏋愪粨搴擄紝涓嶄緷璧栫湡瀹?LLM銆?
---

## 鎵ц椤哄簭

```
1  鏍稿績鏁版嵁妯″瀷      models.py 鍗囩骇
2  Diff Parser       unified diff 鈫?缁撴瀯鍖?hunks
3  RepoMap Builder   Python AST 鈫?symbols + imports + tests
4  Changed Entity    hunk 鈫?function/class/method
5  Risk              deterministic risk tags
6  Evidence          EvidencePackage builder
7  Rules Review      rules-only findings锛屾棤 LLM 涔熻兘璺?8  Pipeline CLI      review 鍛戒护涓茶捣鍏ㄩ摼璺?9  Micro Eval        3 涓?case锛宲ipeline 璺戦€氬悗绔嬪埢鍔狅紝闃插洖褰?10 Report Output     Markdown/JSON 鎶ュ憡
11 Filter            璇姤鎺у埗灞?12 Fake Agent        Protocol + FakeLLM
13 Full Eval         7 涓?case + frontier profiles
14 Demo Polish       README + demo 鍛戒护
```

鍋氬埌绗?8 姝ワ細鏈€灏忓彲婕旂ず review harness銆? 
鍋氬埌绗?9 姝ワ細鏈夐槻鍥炲綊淇濇姢銆? 
鍋氬埌绗?13 姝ワ細鏈?涓嶆槸 toy"鐨?eval 鍙俊搴︺€?
---

## Phase 0 鈥?鏂瑰悜鍐荤粨

- [x] 纭涓荤嚎鍛戒护锛歚map` / `hygiene` / `review` / `eval`
- [x] `summary` 涓嶈繘 MVP锛屽悗缁綔涓?`map --format markdown` 鐨勮緭鍑?- [x] 椤圭洰鏂规绗?8 鑺傚姞鍏?Design Rationale 琛?- [x] 鐪熷疄 LLM 鍜?Draft鈫扜round鈫扖ritic 涓嶈繘 MVP
- [x] `README.md` 鏇存柊涓€鍙ヨ瘽瀹氫綅锛歟vidence-first local PR quality gate for AI-generated patches

---

## Phase 1 鈥?鏍稿績鏁版嵁妯″瀷

鏂囦欢锛歚src/code_review_agent/models.py` 路 `tests/test_models.py`

**鏂板**锛?
- [x] `SymbolSummary` 鈥?path / symbol_type / name / qualified_name / line_start / line_end
- [x] `PythonModuleSummary` 鈥?path / module_docstring / imports / classes / functions
- [x] `RepoMap` 鈥?root / files / python_modules / imports / imported_by / related_tests / style_baseline
- [x] `StyleBaseline` 鈥?鍏佽涓虹┖/闆讹紝`total_public_functions < 5` 鏃惰烦杩?design_constraint 妫€娴?- [x] `DiffLine` 鈥?line_type / old_lineno / new_lineno / content
- [x] `DiffHunk` 鈥?old_start / old_count / new_start / new_count / section_header / lines
- [x] `DiffFileChange` 鈥?old_path / new_path / change_type / hunks
- [x] `ChangedEntity` 鈥?path / entity_type / name / qualified_name / line_start / line_end / hunk_ids
- [x] `RiskSignal` 鈥?tag / confidence / reason / evidence_ids
- [x] `EvidencePackage` 鈥?changed files / changed entities / risk signals / evidence index
- [x] `AgentRun` 鈥?agent_name / model / prompt_hash / input_evidence_ids / output_issue_ids / fallback_used

**鎵╁睍宸叉湁**锛?
- [x] `ReviewEvidence`锛氬凡鏈?id / kind / source / message锛堟湰娆″凡瀹屾垚锛?- [x] `ReviewIssue`锛氬凡鍔?confidence / evidence_ids锛堟湰娆″凡瀹屾垚锛?
**瀹屾垚鏍囧噯**锛?- [x] `python -m pytest tests/test_models.py -v` 鍏ㄩ€?- [x] 鎵€鏈夋ā鍨嬪彲浠?`code_review_agent.models` 瀵煎叆
- [x] `StyleBaseline` 涓虹┖鏃朵笉闃诲涓绘祦绋?
---

## Phase 2 鈥?Diff Parser

鏂囦欢锛歚src/code_review_agent/review/diff_parser.py` 路 `tests/test_review_diff_parser.py`

- [x] 瑙ｆ瀽 `diff --git` / `--- a/` / `+++ b/` / `@@ -old,count +new,count @@`
- [x] 鏀寔 modified / added / deleted / renamed锛堣交閲忥級
- [x] 姣忚璁板綍 old_lineno 鍜?new_lineno
- [x] 绌?diff 缁欏嚭娓呮櫚閿欒锛沚inary diff 鍙褰?file change锛屼笉杩?hunk parsing
- [x] malformed hunk 璺宠繃骞惰褰?warning

**瀹屾垚鏍囧噯**锛?- [x] 鍗曟枃浠?/ 澶氭枃浠?/ added / deleted diff 娴嬭瘯閫氳繃
- [x] hunk 琛屽彿鍙敤浜?report 瀹氫綅

---

## Phase 3 鈥?Minimal RepoMap Builder

鏂囦欢锛歚src/code_review_agent/context/repo_map.py` 路 `context/test_discovery.py` 路 瀵瑰簲娴嬭瘯

绗竴鐗堢洰鏍囷細鑳芥敮鎾?changed entity mapping锛孲tyleBaseline 鍙互涓虹┖銆?
- [x] 澶嶇敤 hygiene scanner 鐨?ignore 瑙勫垯
- [x] `ast.parse()` 鎻愬彇锛歮odule docstring / imports / classes / functions / methods / line_start / line_end
- [x] 寤虹珛 `imports` map 鍜屽熀纭€ `imported_by` map
- [x] `test_discovery.py`锛氳矾寰勫尮閰?`tests/test_<module>.py` / `test_<name>.py` / `<name>_test.py`
- [x] `StyleBaseline` 杞婚噺鏀堕泦锛堝彲涓虹┖锛屼笉闃诲涓绘祦绋嬶級锛歞ocstring 瑕嗙洊鐜?/ import 椋庢牸 / 娴嬭瘯鍛藉悕椋庢牸 / 寮傚父澶勭悊妯″紡

**鏆傜紦**锛氬畬鏁?imported_by 鍙嶅悜鍥?/ import 椋庢牸鍋忓ソ缁熻 / 寮傚父澶勭悊妯″紡缁熻锛圫tyleBaseline 鍏佽闆跺€硷級

CLI锛歚code-review-agent map --repo <repo> --out <out>` 鈫?`repo_map.json` + `repo_map.md`

**瀹屾垚鏍囧噯**锛?- [x] demo repo 鑳界敓鎴?`repo_map.json`
- [x] symbol line range 鍙敤浜?diff hunk 鏄犲皠
- [x] 瑙ｆ瀽澶辫触鏂囦欢涓嶅鑷存暣涓?map 宕╂簝

瀹炵幇璁板綍锛歚map` CLI 宸茶緭鍑?`repo_map.json` / `repo_map.md`锛沗PythonModuleSummary` 澧炲姞 `methods` 瀛楁锛岄伩鍏嶆妸鏂规硶娣峰叆 class/function 鍒楄〃锛涜В鏋愬け璐ユ垨闈?UTF-8 Python 鏂囦欢浼氳烦杩囪妯″潡鎽樿浣嗕繚鐣欐枃浠剁骇鎵弿缁撴灉銆?
---

## Phase 4 鈥?Changed Entity Extraction

鏂囦欢锛歚src/code_review_agent/review/changed_entity.py` 路 `tests/test_review_changed_entity.py`

- [x] hunk added/modified lines 钀藉湪 function/method 鑼冨洿 鈫?鏄犲皠鍒版渶鍐呭眰 symbol
- [x] 钀藉湪 class body 浣嗕笉鍦?method 鈫?class
- [x] 钀藉湪 import / constant / module docstring 鈫?module
- [x] 鏂板鍑芥暟 鈫?鏄犲皠鍒版柊 symbol锛涘垹闄ゅ嚱鏁?鈫?鑷冲皯淇濈暀 file-level entity
- [x] AST 瑙ｆ瀽澶辫触 鈫?fallback module-level锛堝綋鍓?`ChangedEntity` schema 鏆傛棤 reason 瀛楁锛?
**瀹屾垚鏍囧噯**锛?- [x] 姣忎釜 hunk 鑷冲皯鏈変竴涓?changed entity
- [x] 娴嬭瘯瑕嗙洊 function / method / class / module 鍥涚被鏄犲皠

瀹炵幇璁板綍锛歚extract_changed_entities()` 浼氬悎骞跺悓涓€瀹炰綋鐨勫涓?hunk id锛涘悓涓€ hunk 鍐呭鏋滃悓鏃舵敼鍒?module-level 甯搁噺鍜屽嚱鏁?鏂规硶锛屼細淇濈暀澶氫釜 changed entity銆?
---

## Phase 5 鈥?Risk Classification

鏂囦欢锛歚src/code_review_agent/review/risk.py` 路 `tests/test_review_risk.py`

鏀寔鐨?tags锛堣Е鍙戣鍒欒椤圭洰鏂规绗?10 鑺傦級锛?
`api_change` 路 `behavior_change` 路 `test_gap` 路 `config_change` 路 `dependency_change` 路 `error_handling_change` 路 `security_sensitive` 路 `doc_only` 路 `experiment_artifact` 路 `design_constraint_violation`

`design_constraint_violation` 瑙﹀彂鏉′欢锛坄total_public_functions < 5` 鏃跺叏閮ㄨ烦杩囷級锛?- [x] 鏂板/淇敼 public function 缂?docstring锛屼笖浠撳簱 `docstring_coverage_ratio >= 0.70`
- [x] 鏂板娴嬭瘯鏂囦欢鍛藉悕涓嶇鍚?`test_naming_pattern`
- [x] 鏂板 import 椋庢牸涓?`dominant_import_style` 涓嶄竴鑷达紝涓斿崰姣?`>= 0.80`锛堝綋鍓?RepoMap 鍙湁鍏ㄩ噺鍗曚竴椋庢牸鏃舵墠缁欏嚭闈?`mixed`锛岀瓑浠蜂簬淇濆畧瑙﹀彂锛?
**瀹屾垚鏍囧噯**锛?- [x] `test_gap` 鑳藉湪 demo patch 涓Е鍙?- [x] `doc_only` patch 涓嶈緭鍑?code risk
- [x] `design_constraint_violation` 鍙湪浣庤鎶ヨ鍒欐弧瓒虫椂瑙﹀彂

瀹炵幇璁板綍锛歚review/risk.py` 宸叉敮鎸?`api_change` / `behavior_change` / `test_gap` / `config_change` / `dependency_change` / `error_handling_change` / `security_sensitive` / `doc_only` / `experiment_artifact` / `design_constraint_violation`銆傛瘡涓?`RiskSignal` 寮曠敤绋冲畾 evidence id锛屼笉鐩存帴鐢熸垚 issue銆?
---

## Phase 6 鈥?Evidence Package Builder

鏂囦欢锛歚src/code_review_agent/review/evidence.py` 路 `tests/test_review_evidence.py`

- [x] 涓烘瘡绫讳俊鍙风敓鎴?stable evidence id锛?  - `diff:src/shop/service.py:35`
  - `entity:src/shop/service.py:create_order`
  - `risk:test_gap:src/shop/service.py`
  - `test_discovery:tests/test_service.py`
  - `hygiene:src/shop/debug_flow.py`
- [x] issue 鍙兘寮曠敤 evidence_index 涓瓨鍦ㄧ殑 id
- [x] evidence source 鍙拷韪埌鏂囦欢/琛屽彿鎴栫郴缁熸鏌?- [x] prompt/export 榛樿 redact PR title / description / commit message / author锛堟湰鍦?diff MVP 閫氬父鏃犳绫诲瓧娈碉紝schema 棰勭暀鏍囪浣嶅嵆鍙級

**瀹屾垚鏍囧噯**锛?- [x] EvidencePackage 鍙?JSON 搴忓垪鍖?- [x] invalid evidence id 鑳借 filter 鎹曟崏

瀹炵幇璁板綍锛歚review/evidence.py` 宸茬敓鎴?diff/entity/risk/test_discovery/hygiene 浜旂被 `ReviewEvidence`锛屽苟鎻愪緵 `find_missing_evidence_ids()` 渚?Phase11 filter 鎴?Phase8 inline filter 澶嶇敤銆?
---

## Phase 7 鈥?Rules-only Review

鏂囦欢锛歚src/code_review_agent/review/rules.py` 路 `tests/test_review_rules.py`

鍥涙潯瑙勫垯锛堝彧鍋氶珮淇″彿锛屽畞灏戝嬁婊ワ級锛?
| Rule | 鏉′欢 | tag | severity | confidence |
|---|---|---|---|---|
| Test Gap | 闈炴祴璇曚唬鐮佹敼鍔?+ related tests 瀛樺湪 + patch 鏈敼浠讳綍鐩稿叧娴嬭瘯 | `test_gap` | medium | 0.75鈥?.9 |
| Process Artifact Added | patch 鏂板鏂囦欢 + 鍦?`src/` 鎴栨牴鐩綍 + hygiene 鍒ゆ柇涓鸿繃绋嬭祫浜?| `experiment_artifact` | low-medium | 0.7鈥?.9 |
| Broad Exception | added lines 鍚?`except Exception` 鎴?bare `except` + 闈炴祴璇曟枃浠?| `error_handling_change` | medium | 0.7鈥?.85 |
| Dependency Change | 渚濊禆鏂囦欢鍙樻洿 + 鏃?lock/test/config 璇存槑 | `dependency_change` | low | 0.6鈥?.75 鈫?`needs_human_review` |

**瀹屾垚鏍囧噯**锛?- [x] 涓嶄緷璧?LLM 涔熻兘杈撳嚭 review report
- [x] `test_gap` 鍜?`experiment_artifact` 鑳藉湪 demo case 涓Е鍙?- [x] no-finding patch锛坉oc-only / test-only锛変笉杈撳嚭姝ｅ紡 finding

瀹炵幇璁板綍锛歚review/rules.py` 宸茶惤鍦般€俙test_gap` / `experiment_artifact` / broad `error_handling_change` 浼氱敓鎴愭寮?finding锛沗dependency_change` 杩涘叆 `needs_human_review`锛沝oc-only patch 淇濇寔鏃犳寮?finding銆?
---

## Phase 8 鈥?Review Pipeline CLI

鏂囦欢锛歚src/code_review_agent/review/pipeline.py` 路 `tests/test_review_pipeline.py` 路 鏇存柊 `cli.py`

鍛戒护锛?
```powershell
code-review-agent review --repo <repo> --diff <patch> --out <out>
# 鍙€夛細--repo-map <repo_map.json>  --hygiene <project_hygiene.json>  --mode rules|hybrid-fake
```

绗竴鐗堝彧鏀寔 `--mode rules`銆?
Pipeline 姝ラ锛?
```
parse diff 鈫?build/load repo map 鈫?load optional hygiene 鈫?extract changed entities 鈫?classify risks 鈫?build evidence packages 鈫?run rules 鈫?inline filter锛堜袱鏉★細涓㈠純 evidence_ids 涓虹┖ / file 涓嶅湪 changed_files锛夆啋
write report
```

**瀹屾垚鏍囧噯**锛?- [x] 涓€鏉″懡浠よ窇瀹?demo patch
- [x] 杈撳嚭 changed files / changed entities / risk tags / findings / evidence index
- [x] 鏃?LLM 鐜鍙繍琛岋紝榛樿涓嶄慨鏀?repo

瀹炵幇璁板綍锛歚review/pipeline.py` 鍜?`review` CLI 宸茶惤鍦般€傚懡浠よ緭鍑?`review_report.json` / `review_report.md`锛孭hase 8 浠呭仛涓ゆ潯 inline filter锛氫涪寮?`evidence_ids` 涓虹┖鐨?issue锛屼互鍙婁涪寮?`file` 涓嶅湪 changed files 涓殑 issue銆?
---

## Phase 9 鈥?Micro Eval Benchmark

鏂囦欢锛歟val case fixtures + `src/code_review_agent/eval/metrics.py` 路 `tests/test_eval_metrics.py`

鍏堝仛 3 涓?case锛宲ipeline 璺戦€氬悗绔嬪埢鍔狅紝鐢ㄤ簬闃插洖褰掞細

| Case | 绫诲瀷 |
|---|---|
| `case_001_test_gap` | 搴旀湁 finding |
| `case_002_error_handling` | 搴旀湁 finding |
| `case_003_no_finding_doc_only` | 搴斾繚鎸佹矇榛?|

Oracle锛歚file == ground_truth.file AND category == ground_truth.category AND line_range_overlap >= threshold`锛屼笉鐢?LLM judge銆?
**瀹屾垚鏍囧噯**锛?- [x] micro eval 鏈湴蹇€熻繍琛岋紙< 5s锛?- [x] no-finding case 鍗曠嫭璁＄畻鍑嗙‘鎬?- [x] risk / rules / filter 浠绘剰璋冩暣鍚?micro eval 鑳藉彂鐜板洖褰?
瀹炵幇璁板綍锛歚eval/metrics.py` 宸茶惤鍦帮紝鎻愪緵 deterministic oracle锛歠ile equality銆乧ategory equality銆乴ine range overlap锛屽苟鏀寔 no-finding accuracy銆傚凡鍔犲叆 3 涓?micro eval fixtures锛歚case_001_test_gap`銆乣case_002_error_handling`銆乣case_003_no_finding_doc_only`銆?
---

## Phase 10 鈥?Report Output

鏂囦欢锛歚src/code_review_agent/output/json_report.py` 路 `output/review_markdown.py` 路 `tests/test_output_review_markdown.py`

Markdown 缁撴瀯锛堥『搴忓浐瀹氾級锛?
```
# Review Report
## Summary
## Findings
## Needs Human Review
## Changed Files
## Changed Entities
## Risk Signals
## Evidence Index
```

- Findings 鍦ㄦ渶鍓嶏紝姣忔潯蹇呴』鏈?file / line / severity / confidence / evidence list
- No Finding 瑕佽鏄庢鏌ヤ簡浠€涔堛€佷负浠€涔堟病鏈夎緭鍑?- Evidence Index 淇濇寔绠€鐭?
**瀹屾垚鏍囧噯**锛?- [x] sample report 鍙洿鎺ユ斁杩?README
- [x] JSON 瀛楁绋冲畾锛孧arkdown 鍏抽敭瀛楃涓叉祴璇曢€氳繃

瀹炵幇璁板綍锛歚output/json_report.py` 涓?`output/review_markdown.py` 宸茶惤鍦帮紝`review_report.json` 澧炲姞 `schema_version`锛孧arkdown 鍥哄畾杈撳嚭 Summary / Findings / Needs Human Review / Changed Files / Changed Entities / Risk Signals / Evidence Index銆俙review/pipeline.py` 宸叉敼涓轰娇鐢?output 妯″潡銆?
---

## Phase 11 鈥?Review Filter

鏂囦欢锛歚src/code_review_agent/review/filter.py` 路 `tests/test_review_filter.py`

杩囨护/闄嶇骇瑙勫垯锛?
- [x] missing evidence 鈫?涓㈠純
- [x] evidence id 涓嶅瓨鍦?鈫?涓㈠純
- [x] confidence 浣庝簬闃堝€?鈫?`needs_human_review`
- [x] file 涓嶅湪 changed files 涓旀棤 related evidence 鈫?杩囨护
- [x] line 涓?changed hunk/entity 瀹屽叏鏃犲叧 鈫?闄嶇骇
- [x] duplicate issues 鈫?鍚堝苟

杈撳嚭鍒嗗尯锛歚findings` / `needs_human_review` / `discarded`锛坄discarded` 鍙啓 JSON锛?
**瀹屾垚鏍囧噯**锛?- [x] filter 鑳介樆姝㈡棤璇佹嵁 issue
- [x] low confidence issue 杩涘叆 needs_human_review
- [x] duplicate finding 琚悎骞?
瀹炵幇璁板綍锛歚review/filter.py` 宸插崌绾т负姝ｅ紡璇姤鎺у埗灞傦紝杈撳嚭 `FilterResult(findings, needs_human_review, discarded)`锛沗discarded` 璁板綍 `filter_reason` 骞跺彧鍐欏叆 JSON銆俙review/pipeline.py` 宸叉帴鍏ユ寮?filter锛屾姤鍛?summary 澧炲姞 `discarded_count`銆?
---

## Phase 12 鈥?Fake/Hybrid Agent Interface

鏂囦欢锛歚src/code_review_agent/review/agents.py` 路 `prompts/review_agent.md` 路 `prompts/critic_agent.md` 路 `tests/test_review_agents_fake.py`

Protocol锛?
```python
class ReviewAgent(Protocol):
    def review(self, package: EvidencePackage) -> list[ReviewIssue]: ...

class CriticAgent(Protocol):
    def filter(self, issues: list[ReviewIssue], package: EvidencePackage) -> list[ReviewIssue]: ...
```

FakeLLM 绛栫暐锛堝繀椤诲尯鍒嗭紝鐢ㄤ簬 eval 灞曠ず correlated failure锛夛細

| 绛栫暐 | 琛屼负 |
|---|---|
| `recall_biased_reviewer` | 鍊惧悜鎻愬嚭鍊欓€?finding锛屾ā鎷熼珮鍙洖 reviewer |
| `precision_biased_critic` | 鍊惧悜璐ㄧ枒銆侀檷绾с€佽繃婊わ紝妯℃嫙楂樼簿搴?critic |
| `same_strategy` | reviewer + critic 鍚岀瓥鐣ワ紝灞曠ず correlated failure 椋庨櫓 |
| `cross_strategy` | reviewer + critic 寮傜瓥鐣ワ紝灞曠ず harness 鐨勮繃婊や环鍊?|

- [x] `--mode hybrid-fake` 鍙繍琛?- [x] `--export-prompts` 杈撳嚭 prompt hash + input JSON
- [x] invalid evidence id 琚?filter 闄嶇骇鎴栦涪寮?
瀹炵幇璁板綍锛歚review/agents.py` 宸插姞鍏?`ReviewAgent` / `CriticAgent` Protocol銆乣FakeLLMReviewAgent`銆乣FakeLLMCriticAgent` 鍜?`run_fake_hybrid_agents()`锛沗review` CLI 鏀寔 `--mode hybrid-fake` 涓?`--export-prompts`锛宲rompt 瀵煎嚭鍖呭惈 prompt hash 鍜?redacted input JSON銆?
---

## Phase 13 鈥?Full Eval Benchmark

鏂囦欢锛歚examples/eval_cases/` + `src/code_review_agent/eval/` + `tests/test_eval_metrics.py`

7 涓?case锛堣嚦灏?2 涓?no-finding锛夛細

| Case | 绫诲瀷 |
|---|---|
| `case_001_test_gap` | finding |
| `case_002_api_change` | finding |
| `case_003_error_handling` | finding |
| `case_004_artifact_pollution` | finding |
| `case_005_no_finding_doc_only` | no finding |
| `case_006_no_finding_test_only` | no finding |
| `case_007_design_constraint` | finding |

Threshold profiles锛歚strict` / `balanced` / `recall`

鍛戒护锛歚code-review-agent eval --cases examples/eval_cases --out outputs/eval --mode rules`

**瀹屾垚鏍囧噯**锛?- [ ] eval 鍛戒护鍙窇閫氾紝杈撳嚭 `metrics.json` + `eval_report.md` + `case_results.json`
- [ ] oracle 浣跨敤 planted bug + line range overlap锛屼笉鐢?LLM judge
- [ ] eval report 灞曠ず profile frontier 琛?- [ ] 鑳藉姣?rules-only 涓?fake/evidence-backed variant

---

## Phase 14 鈥?Demo Polish

- [ ] `examples/demo_repo/` 鍍忕湡瀹?Python 椤圭洰锛堜笉鏄鐗囨枃浠讹級
- [ ] demo patch 瑕嗙洊锛歵est gap / artifact pollution / error handling / no-finding doc-only / no-finding test-only
- [ ] README 鍖呭惈锛氫竴鍙ヨ瘽瀹氫綅 / 涓轰粈涔堜笉鏄櫘閫?Review Bot / 鏋舵瀯鍥?/ demo 鍛戒护 / sample report / eval 鎸囨爣琛?/ 褰撳墠闄愬埗

Demo 鍛戒护锛堝繀椤诲彲澶嶇幇锛夛細

```powershell
pip install -e ".[dev]"
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map     --repo examples/demo_repo --out outputs/demo-map
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
code-review-agent eval    --cases examples/eval_cases --out outputs/demo-eval
```

**瀹屾垚鏍囧噯**锛?- [ ] README 3 鍒嗛挓鍐呰娓呮椤圭洰浠峰€?- [ ] demo 鍛戒护鍙鐜?- [ ] report 閲屾湁鑷冲皯涓€涓珮璐ㄩ噺 finding 鍜屼竴涓?No Finding case

---

## Post-MVP

涓嶉樆濉?MVP 鐨勬柟鍚戯紝鎸変环鍊兼帓搴忥細

- [ ] 鐪熷疄 OpenAI-compatible LLM backend锛坮eviewer / critic 鍙€変笉鍚屾ā鍨嬫棌锛?- [ ] Draft 鈫?Ground 鈫?Critic 涓夐樁娈?pipeline
- [ ] GitHub PR URL 杈撳叆 + dry-run comment
- [ ] MCP tools锛堟毚闇?repo_map / review report / hygiene scan锛?- [ ] `apply` 鍛戒护锛堢‘璁ゅ悗绉诲姩杩囩▼璧勪骇锛?- [ ] 澶氳瑷€锛圝S/TS 鈫?Go 鈫?Java锛?- [ ] `references.py`锛坈all graph 杞婚噺鐗堬級
