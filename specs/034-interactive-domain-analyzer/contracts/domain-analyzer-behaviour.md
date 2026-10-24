# Contract: `speckit.spectra.domain-analyzer` behaviour

A command file is a prompt, so its contract is textual: each item below is something
`spectra/commands/domain-analyzer.md` (or its template) must say. Tests in `tests/test_domain_analyzer_flow.py`
(`F`) and `tests/test_doc_output_paths.py` (`P`) pin them; item 25 binds `spectra/commands/review-pr.md`. "Gap" marks an item the working tree does not yet
satisfy.

| # | Behaviour | FR | Pinned by |
|---|---|---|---|
| 1 | First output states constitution found/none and the goal: generate or update | FR-001 | F `TheGoalIsStatedFirst.test_step_zero_reports_the_constitution_before_anything_else` |
| 2 | The goal reaches the front matter and selects the handoff wording | FR-001, FR-016 | F `test_the_goal_reaches_the_front_matter_and_the_handoff` |
| 3 | All seven lenses are named, and "never omit a lens" | FR-002 | F `SevenLensesAlwaysWorked.test_every_lens_is_named`, `test_no_lens_is_omitted` |
| 4 | The template has one section per lens | FR-002, FR-021 | F `test_every_lens_has_a_template_section` |
| 5 | Testing and deployment are referred to their agents, not proposed | FR-004 | F `test_testing_and_deployment_are_referred_not_proposed` |
| 6 | Every candidate carries `observed` or `aspirational` | FR-005 | F `test_every_candidate_says_whether_the_code_already_does_it` |
| 7 | Eight questions, one per turn, numbered "Question N of 8" | FR-008 | F `TheClarificationRound.test_eight_questions_one_per_turn` |
| 8 | ≥4 distinct options, exactly one recommended, one always Skip | FR-009 | F `test_at_least_four_options_one_recommended_one_skip` |
| 9 | A coinciding option is replaced by Choose individually | FR-010 | F `test_coinciding_options_are_replaced_not_dropped` |
| 10 | A question with nothing to choose becomes a four-option confirmation and keeps its number | FR-011 | F `test_a_question_with_nothing_to_choose_becomes_a_confirmation` |
| 11 | Skip and unanswered adopt nothing; "use your defaults" is `default_taken` | FR-012 | F `test_only_a_human_choice_adopts` |
| 12 | Written once, after the round, never before | FR-013 | F `test_nothing_is_written_before_the_round_ends` |
| 13 | Written to `<artifact-root>/DOMAIN_ANALYSIS.md`, default `docs/DOMAIN_ANALYSIS.md`, no sequence number | FR-013 | P `SingletonOutputPaths` |
| 14 | Earlier location `.specify/memory/domain-analysis.md` read and left alone | FR-020 | P `test_each_singleton_reads_its_earlier_location` |
| 15 | Candidate record keys in fixed order | FR-014 | F `TheDocument.test_the_candidate_record_keys_in_order` |
| 16 | Constitution input = accepted and not adopted | FR-015 | F `test_the_constitution_input_holds_only_accepted_unadopted_items` |
| 17 | Constitution input written even if a template override omits it | FR-021 | F `test_the_template_cannot_drop_the_constitution_input` |
| 18 | Never writes the constitution | FR-017 | F `TheHandoff.test_the_constitution_is_never_written` |
| 19 | Create and amend ready prompts, linked to the written path | FR-016 | F `test_both_ready_prompts_name_the_constitution_input`; P `test_the_domain_analyzer_hands_off_with_a_ready_prompt` |
| 20 | No prompt when Constitution input is empty | FR-016 | F `test_no_prompt_is_given_when_nothing_is_left_to_adopt` |
| 21 | IDs frozen; matched by recorded ID or same intent in the same section | FR-018 | F `IdentifiersAreFrozen`, `ReRunsRespectDecisions.test_a_regenerated_original_wording_matches_by_id`, `test_a_reworded_guardrail_matches_by_intent_within_its_section` |
| 22 | Re-run pre-fills answers, never re-offers declined, never deletes, adopted never reverted | FR-019 | F `ReRunsRespectDecisions` (remaining tests) |
| 23 | Legacy checkbox file: ticked = accepted, unticked = **undecided**, re-offered marked "unticked in the earlier version" | FR-020 | F `test_a_legacy_checkbox_file_is_read` — **Gap**: command, test, README, and CHANGELOG still say unticked = declined |
| 24 | Non-interactive: never inferred, asks none, gives no handoff command | FR-012, FR-016 | F `NonInteractive.test_never_inferred_and_adopts_nothing` |
| 25 | `review-pr` cites only `accepted` guardrails from the analysis; a `declined`, `skipped`, or `not_asked` entry is never a finding source | FR-022 | `tests/test_review_pr_flow.py` (new) — **Gap** |

FR-003 (lens → section mapping), FR-006 (five-candidate cap), and FR-007 (suppress / `amends:` against an
existing constitution) are stated in Step 4 of the command and checked by reading in the quickstart; they
are judgment rules with no reliable phrase to pin beyond what items 3 and 15 already cover.
