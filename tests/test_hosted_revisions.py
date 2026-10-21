import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from proofpress.hosted import revisions
from proofpress.hosted.control_plane import HostedControlPlane
from proofpress.kernel import operations as ops
from proofpress.kernel.events import SQLiteEventStore, using_event_store
from test_hosted_authority import evidence_payload, operation


class RevisionJourneyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.control = HostedControlPlane(Path(self.tmp.name) / 'test.db')
        self.owner = self.control.bootstrap('workspace:test', 'human:owner')['token']
        self.agent = self.control.issue_agent_credential(self.owner, 'agent:codex', 'Codex')['token']
        self.context = self.control.authenticate(self.owner)
        evidence = self.control.execute(self.agent, operation('evidence.submit', {'payload': evidence_payload()}))
        self.parent = self.control.execute(self.agent, operation('claim.propose', {
            'statement': 'The report supports a broad conclusion.', 'title': 'Original finding',
            'evidence_refs': evidence['result']['evidence'], 'scope': 'test',
            'qualifiers': {'observed_at': '2026-10-16', 'custom': 'keep'},
            'proposer': 'agent:codex'}))['result']['claim']
        with using_event_store(SQLiteEventStore(self.control.database, 'workspace:test', 'agent:codex')):
            evidence = ops.v2_projection()['evidence'][self.parent['evidence_refs'][0]]
            ops.describe_evidence_v1(self.parent['id'], evidence['id'], evidence['digest'],
                {'filename': 'report.md', 'location': 'Summary', 'fields': [{'name': 'Section', 'value': 'Summary'}]}, 'agent:codex')
        self.record = self.control._policy('workspace:test')
        self.record['settings'].update(mode='automatic', provider='managed_gmi', external_consent=True)
        self.result = {'status': 'revised', 'statement': 'The report supports only this bounded observation.',
                       'title': 'Bounded finding', 'reason': 'Narrowed to the supplied report.'}

    def request(self):
        response = self.control.execute(self.owner, operation('claim.review', {
            'claim_id': self.parent['id'], 'decision': 'request_changes', 'reviewer': 'human:owner',
            'note': 'Narrow this to what the report actually says.'}))
        self.assertTrue(response['ok'], response)
        with patch.object(self.control, '_policy', return_value=self.record), patch('proofpress.hosted.revisions.threading.Thread'):
            revisions.enqueue(self.control, self.context, self.parent['id'])
        return response

    def run_job(self, generator=None):
        with patch.object(self.control, '_policy', return_value=self.record), patch.object(self.control, '_current_policy', return_value=self.record), patch.object(self.control, '_provider_credential', return_value='test-only'), patch.object(self.control, '_schedule_judge'), patch('proofpress.hosted.revisions.generate', side_effect=generator or (lambda *a: self.result)) as generate:
            revisions.drain(self.control, 'workspace:test')
        with self.control._db() as connection:
            job = dict(connection.execute('SELECT * FROM hosted_revision_jobs').fetchone())
        return job, generate

    def test_request_generates_linked_candidate_and_never_approves(self):
        self.request()
        job, generate = self.run_job()
        self.assertEqual(job['state'], 'completed', job)
        packet = generate.call_args.args[0]
        self.assertEqual(packet['owner_note'], 'Narrow this to what the report actually says.')
        receipt = self.control.execute(self.owner, operation('review.receipt', {'claim_id': job['successor_id']}))['result']
        self.assertEqual(receipt['state'], 'needs_review')
        self.assertEqual(receipt['claim']['proposer'], revisions.ACTOR)
        self.assertEqual(receipt['claim']['qualifiers']['revision_of'], self.parent['id'])
        self.assertEqual(receipt['claim']['qualifiers']['custom'], 'keep')
        self.assertEqual(receipt['claim']['evidence_refs'], self.parent['evidence_refs'])
        self.assertEqual(receipt['claim']['scope'], self.parent['scope'])
        self.assertIsNotNone(receipt['evaluation'])
        self.assertEqual(next(iter(receipt['evidence_details'].values()))['details']['filename'], 'report.md')
        parent = self.control.execute(self.owner, operation('review.receipt', {'claim_id': self.parent['id']}))['result']
        self.assertEqual(parent['claim']['statement'], self.parent['statement'])
        self.assertEqual(parent['revision_job']['successor_id'], job['successor_id'])
        with using_event_store(SQLiteEventStore(self.control.database, 'workspace:test', 'system:test')), ops.using_policy(self.record['policy']):
            result = ops.auto_admit_v2(job['successor_id'], 'human:owner', 1, 'test', '', ops.v2_head())
        self.assertIn('human approval', result['skipped'])
        # Completed jobs do not call the model again.
        _, repeated = self.run_job()
        repeated.assert_not_called()

    def test_missing_evidence_produces_no_claim(self):
        self.request()
        self.result = {'status': 'needs_evidence', 'reason': 'Supply the later pricing series.'}
        job, _ = self.run_job()
        self.assertEqual(job['state'], 'needs_evidence')
        self.assertIsNone(job['successor_id'])

    def test_changed_request_while_model_runs_discards_response(self):
        self.request()
        def generate(*args):
            self.control.execute(self.owner, operation('claim.review', {
                'claim_id': self.parent['id'], 'decision': 'reject', 'reviewer': 'human:owner', 'note': 'Withdraw this request.'}))
            return self.result
        job, _ = self.run_job(generate)
        self.assertEqual(job['state'], 'skipped', job)
        self.assertIsNone(job['successor_id'])

    def test_provider_failure_does_not_leak_and_original_request_survives(self):
        self.request()
        def fail(*args):
            raise ValueError('SECRET provider body')
        job, _ = self.run_job(fail)
        self.assertEqual(job['state'], 'failed')
        self.assertNotIn('SECRET', job['detail'])
        self.assertIsNone(job['successor_id'])

    def test_agent_cannot_enqueue_and_workspace_status_isolated(self):
        with self.assertRaisesRegex(ValueError, 'review authority'):
            revisions.enqueue(self.control, self.control.authenticate(self.agent), self.parent['id'])
        self.request()
        with self.control._db() as connection:
            self.assertIsNone(revisions.status(connection, 'other', self.parent['id'], 'anything'))

    def test_no_consent_blocks_model(self):
        self.record['settings']['external_consent'] = False
        self.request()
        job, model = self.run_job()
        self.assertEqual(job['state'], 'blocked')
        model.assert_not_called()

    def test_duplicate_enqueue_is_one_job(self):
        self.request()
        with patch.object(self.control, '_policy', return_value=self.record), patch('proofpress.hosted.revisions.threading.Thread'):
            revisions.enqueue(self.control, self.context, self.parent['id'])
        with self.control._db() as connection:
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM hosted_revision_jobs').fetchone()[0], 1)

    def test_restart_marks_running_interrupted(self):
        self.request()
        with self.control._db() as connection:
            connection.execute("UPDATE hosted_revision_jobs SET state='running'")
        with patch('proofpress.hosted.revisions.threading.Thread'):
            revisions.resume(self.control, 'workspace:test')
        job, model = self.run_job()
        self.assertEqual(job['state'], 'interrupted')
        model.assert_not_called()

    def test_policy_disable_while_model_runs_discards_response(self):
        self.request()
        def generate(*args):
            self.record['settings']['external_consent'] = False
            return self.result
        job, _ = self.run_job(generate)
        self.assertEqual(job['state'], 'skipped')
        self.assertIsNone(job['successor_id'])

    def test_model_adapter_rejects_truncation_and_oversized_title(self):
        from io import BytesIO
        def opener(payload):
            return lambda *a, **k: BytesIO(json.dumps(payload).encode())
        truncated = {'choices': [{'finish_reason': 'length', 'message': {'content': '{}'}}]}
        with self.assertRaisesRegex(ValueError, 'truncated'):
            revisions.generate({}, 'test-only', opener=opener(truncated))
        invalid = {'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps({**self.result, 'title': 'x' * 121})}}]}
        with self.assertRaisesRegex(ValueError, 'invalid revision field'):
            revisions.generate({}, 'test-only', opener=opener(invalid))


if __name__ == '__main__':
    unittest.main()
