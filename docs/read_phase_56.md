# Read Guide: Phase 5 + 6锛坮isk + evidence锛?
> 鐩爣锛氬府鍔╀綘蹇€熺湅鎳傚綋鍓?Phase 5/6 浠ｇ爜锛屽苟鑳界嫭绔嬫墿灞曡鍒欍€?> 
> 褰撳墠鐘舵€侊細`review/risk.py`銆乣review/evidence.py` 宸插疄鐜帮紝鐩稿叧娴嬭瘯閫氳繃銆?
---

## 0. 鍏堝缓绔嬪績鏅烘ā鍨?
Phase 5/6 鍦?review pipeline 閲岀殑浣嶇疆锛?
```text
diff_parser -> changed_entity -> risk -> evidence -> (rules reviewer / agent)
```

浣犺璁颁綇涓ゅ彞璇濓細

1. **Phase 5 (`risk.py`)**锛氫粠缁撴瀯鍖?diff + repo context 閲屾墦 deterministic risk tags銆?2. **Phase 6 (`evidence.py`)**锛氭妸 diff/entity/risk/test/hygiene 鏁寸悊鎴愮粺涓€ `EvidencePackage`锛屽苟妫€鏌ヨ瘉鎹紩鐢ㄦ槸鍚﹀畬鏁淬€?
---

## 1. 鍏堣杈撳叆/杈撳嚭锛堜笉瑕佸厛璇荤粏鑺傦級

### Phase 5 涓诲嚱鏁?
```python
classify_risks(
    changes: list[DiffFileChange],
    repo_map: RepoMap,
    changed_entities: list[ChangedEntity],
    hygiene_classifications: list[FileClassification] | None = None,
) -> list[RiskSignal]
```

杈撳叆鏄洓鍧楋細`diff`銆乣repo_map`銆乣changed_entities`銆佸彲閫?`hygiene`銆?杈撳嚭鏄?`list[RiskSignal]`锛堟瘡鏉″繀椤诲甫 `evidence_ids`锛夈€?
### Phase 6 涓诲嚱鏁?
```python
build_evidence_package(
    repo_path,
    changes,
    changed_entities,
    risk_signals,
    repo_map,
    hygiene_classifications=None,
) -> EvidencePackage
```

杈撳嚭鏄竴涓畬鏁村彲杩借釜涓婁笅鏂囧寘锛?- `changed_files`
- `changed_entities`
- `risk_signals`
- `evidence_index: dict[id, ReviewEvidence]`
- `metadata`锛堝惈 redaction 淇℃伅锛?
---

## 2. 闃呰椤哄簭锛堟帹鑽?45 鍒嗛挓锛?
## Step A锛氳 `risk.py` 椤堕儴甯搁噺锛? 鍒嗛挓锛?
鍏堢湅鎵€鏈?tag 甯搁噺鍜?token 甯搁噺锛?- 椋庨櫓鏍囩锛歚API_CHANGE`銆乣BEHAVIOR_CHANGE`銆乣TEST_GAP`銆乣CONFIG_CHANGE`銆乣DEPENDENCY_CHANGE`銆乣ERROR_HANDLING_CHANGE`銆乣SECURITY_SENSITIVE`銆乣DOC_ONLY`銆乣EXPERIMENT_ARTIFACT`銆乣DESIGN_CONSTRAINT_VIOLATION`
- 璺緞/鍏抽敭璇嶈〃锛歚CONFIG_PATHS`銆乣DEPENDENCY_FILES`銆乣SECURITY_TOKENS`銆乣EXPERIMENT_MARKERS`

杩欎竴姝ョ殑鐩殑锛氬厛鐭ラ亾鈥滃畠浼氫骇鍑哄摢浜涢闄┾€濓紝鍐嶇湅鈥滄€庝箞浜у嚭鈥濄€?
## Step B锛氳 `classify_risks()` 涓绘祦绋嬶紙10 鍒嗛挓锛?
涓绘祦绋嬫槸涓€涓仛鍚堝櫒锛岄『搴忓涓嬶細

1. `doc_only` 蹇€熺煭璺紙绾枃妗?patch 鐩存帴杩斿洖锛?2. config/dependency 椋庨櫓
3. API 鍙樺寲
4. 琛屼负鍙樺寲锛堝嚱鏁?鏂规硶閫昏緫鍙樺姩锛?5. test gap锛堟敼浜嗘簮鐮佷絾娌℃敼鍏宠仈娴嬭瘯锛?6. hunk 鍐呭椋庨櫓锛坋rror handling / security token锛?7. experiment artifact锛堣矾寰?+ hygiene 鑱斿悎鍒ゅ畾锛?8. design constraint锛堝熀浜?style baseline锛?9. 鍘婚噸 `_deduplicate_signals()`

娉ㄦ剰锛氭瘡涓瓙鍑芥暟閮界洿鎺ユ瀯閫?`RiskSignal(evidence_ids=[...])`锛屼笉鍏佽鈥滄棤璇佹嵁椋庨櫓鈥濄€?
## Step C锛氳鏈€鍏抽敭鐨?4 鏉¤鍒欙紙15 鍒嗛挓锛?
鎸夋敹鐩婁紭鍏堥槄璇伙細

1. `_test_gap_risks()`
   - 鍙?`repo_map.related_tests[path]`
   - 鑻?source 鏀逛簡銆佺浉鍏虫祴璇曞瓨鍦ㄤ絾鏈湪 patch 涓敼鍔?-> `TEST_GAP`
   - 璇佹嵁浼氶檮甯?`test_discovery:*` 鍜?`diff:*`

2. `_api_change_risks()`
   - 鍏紑绛惧悕鍙樻洿锛坄def/class` 涓旈潪 `_private`锛夎Е鍙?`API_CHANGE`
   - `__init__.py` 鐨勫鍑哄彉鍖栦篃瑙﹀彂

3. `_design_constraint_risks()`
   - baseline 涓嶅彲闈狅紙`total_public_functions < 5`锛夌洿鎺ヨ烦杩?   - docstring coverage 楂樻椂锛屾柊澧?淇敼 public function/method 鏃?docstring 瑙﹀彂
   - 鏂版祴璇曞懡鍚嶉鏍煎拰 import 椋庢牸鍋忕鍩虹嚎涔熶細瑙﹀彂

4. `_experiment_artifact_risks()`
   - `added` 鏂囦欢涓旇矾寰勫儚 experiment锛屾垨 hygiene 鍒嗙被鍦?`PROCESS_CATEGORIES`
   - 鍚屾椂闄?`hygiene:*` 璇佹嵁锛堝鏋滄湁锛?
## Step D锛氳 `evidence.py`锛?0鈥?5 鍒嗛挓锛?
鍏堢湅 `build_evidence_package()` 鐨?5 涓?`_add_many()`锛?
- `_diff_evidence()`锛氭妸鏂板/鍒犻櫎琛岃浆鎴?`diff:path:line`
- `_entity_evidence()`锛氭妸 changed entity 杞垚 `entity:path:qualified_name`
- `_test_discovery_evidence()`锛氫粠 `repo_map.related_tests` 鐢熸垚 `test_discovery:*`
- `_hygiene_evidence()`锛氭妸 hygiene 鍒嗙被鏀惧叆璇佹嵁绱㈠紩
- `_risk_evidence()`锛氭瘡鏉?risk 鐢熸垚涓€涓?`risk:tag:path` 璇佹嵁

鏈€鍚庤 `find_missing_evidence_ids()`锛?- 褰撳墠鍙牎楠?`risk_signals[*].evidence_ids` 鏄惁瀛樺湪浜?`evidence_index`
- 杩欐槸鍚庣画 filter/verifier 鐨勫熀纭€鍓嶇疆妫€鏌?
---

## 3. 閰嶅娴嬭瘯鎬庝箞璇伙紙鏈€鐪佹椂闂达級

寤鸿涓ユ牸鎸変笅闈㈤『搴忥細

1. `tests/test_review_risk.py`
   - 鐪嬫瘡涓?test 鍚嶅氨鏄竴鏉￠渶姹傝鏄?   - 閲嶇偣锛?     - `test_test_gap_triggers_when_related_tests_are_not_changed`
     - `test_design_constraint_triggers_only_when_baseline_is_reliable`
     - `test_experiment_artifact_uses_path_or_hygiene_classification`

2. `tests/test_review_evidence.py`
   - 鐪?`test_build_evidence_package_indexes_diff_entity_risk_and_tests`
   - 鍐嶇湅 `test_find_missing_evidence_ids_reports_invalid_references`

璇绘硶锛氬厛鐪嬫柇瑷€锛屽啀鍥炲ご鐪?fixture 鏋勯€狅紝鍐嶅洖婧愮爜銆備綘浼氭洿蹇悊瑙ｂ€滀负浠€涔堣繖涔堣璁♀€濄€?
---

## 4. 浣犲彲浠ユ墜鍔ㄥ仛鐨?3 涓涔犵粌涔?
### 缁冧範 1锛氬姞涓€涓?security token

鍦?`SECURITY_TOKENS` 澧炲姞涓€涓瘝锛屾瘮濡?`pickle.loads`锛屽啓涓€涓渶灏忔祴璇曠‘璁や細瑙﹀彂 `SECURITY_SENSITIVE`銆?
### 缁冧範 2锛氶獙璇?evidence 寮曠敤闂幆

鎵嬪伐鏋勯€犱竴涓?`RiskSignal(evidence_ids=["diff:foo.py:999"])`锛岃皟鐢?`find_missing_evidence_ids()`锛岀‘璁よ兘鎶ュ嚭缂哄け椤广€?
### 缁冧範 3锛氱悊瑙?design constraint 鐨勯棬妲?
鎶?baseline 鐨?`total_public_functions` 鏀规垚 4锛岃瀵?`DESIGN_CONSTRAINT_VIOLATION` 瑙勫垯琚暣浣撹烦杩囥€?
---

## 5. 褰撳墠瀹炵幇鐨勪紭鐐逛笌娉ㄦ剰鐐?
### 浼樼偣

- 鍏?deterministic锛屽彲閲嶅
- 姣忔潯椋庨櫓閮藉彲杩藉埌 `evidence_ids`
- 涓?hygiene 鑱斿姩浣嗕笉寮鸿€﹀悎
- test 棰楃矑搴﹀ソ锛屽洖褰掍繚鎶ゆ湁鏁?
### 娉ㄦ剰鐐癸紙闈為樆鏂級

- `find_missing_evidence_ids()` 褰撳墠鍙鏌?`risk_signals`锛屽悗缁紩鍏?`ReviewIssue` 鏃跺缓璁墿灞曞埌 issue 绾ф牎楠?- `SECURITY_TOKENS` 鏄叧閿瘝鍖归厤锛屽睘浜庤交閲忓惎鍙戝紡锛屽悗缁彲閫愭鍗囩骇涓?AST 妯″紡
- `risk.py` 浣撻噺杈冨ぇ锛屽悗缁彲鎸夎鍒欑粍鎷嗗垎涓哄瓙妯″潡锛堜繚鎸佹帴鍙ｄ笉鍙橈級

---

## 6. 蹇€熷畾浣嶇储寮?
- 椋庨櫓涓诲叆鍙ｏ細`src/code_review_agent/review/risk.py` -> `classify_risks()`
- 璇佹嵁涓诲叆鍙ｏ細`src/code_review_agent/review/evidence.py` -> `build_evidence_package()`
- 璇佹嵁瀹屾暣鎬ф鏌ワ細`src/code_review_agent/review/evidence.py` -> `find_missing_evidence_ids()`
- 椋庨櫓娴嬭瘯锛歚tests/test_review_risk.py`
- 璇佹嵁娴嬭瘯锛歚tests/test_review_evidence.py`

---

*寤鸿锛氭瘡娆?Phase 5/6 瑙勫垯鏈夋柊澧烇紝閮藉湪鏈枃浠惰拷鍔犫€滄柊澧炶鍒?鈫?瀵瑰簲娴嬭瘯鍚?鈫?椋庨櫓鏍囩 鈫?璇佹嵁ID鏍煎紡鈥濄€?
