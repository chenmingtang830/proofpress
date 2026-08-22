export const H4_STAGE_IDS = Object.freeze(["S1", "S2", "S3", "S4"]);

export class StageController {
  #schedule;
  #index = 0;
  #firstSession = null;
  #secondSession = null;

  constructor(schedule) {
    validateSchedule(schedule);
    this.#schedule = schedule.map((stage) => ({ ...stage }));
  }

  releaseNext({ sessionToken, boundaryEvidence = null }) {
    if (this.#index >= this.#schedule.length) throw new Error("H4 stage schedule is complete");
    if (typeof sessionToken !== "string" || !sessionToken) throw new Error("sessionToken is required");

    const stage = this.#schedule[this.#index];
    if (this.#index === 0) this.#firstSession = sessionToken;
    if (this.#index < 2 && sessionToken !== this.#firstSession) {
      throw new Error("S1 and S2 must use the same worker session");
    }
    if (this.#index === 2) {
      if (sessionToken === this.#firstSession) throw new Error("S3 requires a fresh worker session");
      if (!validBoundaryEvidence(boundaryEvidence)) throw new Error("S3 requires valid cold-boundary evidence");
      this.#secondSession = sessionToken;
    }
    if (this.#index > 2 && sessionToken !== this.#secondSession) {
      throw new Error("S3 and S4 must use the same fresh worker session");
    }

    this.#index += 1;
    return { ...stage, sequence: this.#index };
  }

  get state() {
    return {
      next_stage: this.#schedule[this.#index]?.stage_id ?? null,
      completed_stages: this.#schedule.slice(0, this.#index).map((stage) => stage.stage_id),
      complete: this.#index === this.#schedule.length,
      sessions_used: [this.#firstSession, this.#secondSession].filter(Boolean),
    };
  }
}

export function validateSchedule(schedule) {
  if (!Array.isArray(schedule) || schedule.length !== 4) throw new Error("H4 schedule must contain exactly four stages");
  const ids = schedule.map((stage) => stage.stage_id);
  if (JSON.stringify(ids) !== JSON.stringify(H4_STAGE_IDS)) throw new Error("H4 stages must be S1, S2, S3, S4");
  const boundaries = schedule.filter((stage) => stage.cold_boundary_before === true).map((stage) => stage.stage_id);
  if (JSON.stringify(boundaries) !== JSON.stringify(["S3"])) throw new Error("H4 requires exactly one cold boundary before S3");
  if (schedule.some((stage) => typeof stage.release_file !== "string" || !stage.release_file)) {
    throw new Error("Every H4 stage requires one deterministic release file");
  }
  return true;
}

function validBoundaryEvidence(evidence) {
  return Boolean(
    evidence &&
    evidence.valid === true &&
    evidence.pre_transfer_inventory_empty === true &&
    evidence.only_declared_transfer_package === true &&
    evidence.sender_worker_exited === true &&
    evidence.sender_workspace_removed === true &&
    evidence.worker_pid_changed === true &&
    evidence.previous_git_absent === true &&
    evidence.sender_ledger_absent === true &&
    evidence.session_state_absent === true &&
    evidence.transcript_absent === true &&
    evidence.conversation_absent === true &&
    evidence.hidden_memory_absent === true &&
    evidence.orchestrator_state_absent === true
  );
}
