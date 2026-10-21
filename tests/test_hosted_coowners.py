import tempfile
import unittest
from pathlib import Path

from proofpress.hosted.control_plane import HostedControlPlane, HostedAuthError
from test_hosted_authority import operation, evidence_payload


class CoOwnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.control = HostedControlPlane(Path(self.tmp.name) / 'hosted.db')
        self.richard = self.control.bootstrap('workspace:cury', 'human:richard')
        self.agent = self.control.issue_agent_credential(self.richard['token'], 'agent:codex', 'Codex')

    def add_owner(self):
        return self.control.issue_owner_credential(self.richard['token'], 'human:cury', 'Cury Owner')

    def test_independent_owner_keys_both_administer_and_keep_recovery_target(self):
        cury = self.add_owner()
        for principal, token in [('human:richard', self.richard['token']), ('human:cury', cury['token'])]:
            context = self.control.authenticate(token)
            self.assertEqual(context.role, 'owner')
            self.assertEqual(context.principal_id, principal)
            self.assertIn('*', context.permissions)
            self.control.get_review_policy(token)
            self.control.list_credentials(token)
        self.assertNotEqual(cury['token'], self.richard['token'])
        with self.control._db() as connection:
            self.assertEqual(connection.execute('SELECT bootstrap_principal_id FROM hosted_recovery').fetchone()[0], 'human:richard')
        self.control.issue_agent_credential(cury['token'], 'agent:cury', 'Cury Codex')
        audit = self.control.list_audit(self.richard['token'])
        self.assertTrue(any(row['operation'] == 'credential.issue.owner' and row['principal_id'] == 'human:richard' for row in audit))
        listing = self.control.list_credentials(cury['token'])
        self.assertFalse(any('token' in row or 'secret_hash' in row for row in listing))

    def test_coowner_review_uses_own_identity(self):
        cury = self.add_owner()
        evidence = self.control.execute(self.agent['token'], operation('evidence.submit', {'payload':evidence_payload()}))['result']['evidence']
        claim = self.control.execute(self.agent['token'], operation('claim.propose', {
            'statement':'The report states a one-year cap.', 'title':'Cap', 'scope':'test',
            'evidence_refs':evidence, 'proposer':'agent:codex'}))['result']['claim']
        reviewed = self.control.execute(cury['token'], operation('claim.review', {
            'claim_id':claim['id'], 'decision':'request_changes', 'reviewer':'human:richard', 'note':'Narrow attribution.'}))
        self.assertTrue(reviewed['ok'], reviewed)
        self.assertEqual(reviewed['result']['review']['reviewer'], 'human:cury')

    def test_agent_and_reviewer_cannot_grant_owner(self):
        reviewer = self.control.issue_reviewer_credential(self.richard['token'], 'human:reader', 'Reviewer')
        for token in [self.agent['token'], reviewer['token']]:
            with self.assertRaises(HostedAuthError):
                self.control.issue_owner_credential(token, 'human:bad', 'Forbidden')
        for principal in ['agent:cury', 'human:richard', 'human:reader']:
            with self.assertRaises(ValueError):
                self.control.issue_owner_credential(self.richard['token'], principal, 'No promotion')

    def test_owner_key_still_cannot_authorize_agent_mcp(self):
        cury = self.add_owner()
        with self.assertRaisesRegex(HostedAuthError, 'owner credentials cannot authorize MCP'):
            self.control.create_oauth_code(cury['token'], 'unused', 'http://127.0.0.1', 'https://example.com/mcp', 'x'*43)

    def test_revoke_coowner_does_not_remove_original_owner_or_allow_cross_workspace(self):
        cury = self.add_owner()
        other_control = HostedControlPlane(Path(self.tmp.name) / 'other.db')
        other = other_control.bootstrap('workspace:other', 'human:other')
        with self.assertRaises(ValueError):
            other_control.revoke_credential(other['token'], cury['credential_id'])
        with self.assertRaises(ValueError):
            self.control.revoke_credential(cury['token'], self.richard['credential_id'])
        self.control.revoke_credential(self.richard['token'], cury['credential_id'])
        with self.assertRaises(HostedAuthError):
            self.control.authenticate(cury['token'])
        self.assertEqual(self.control.authenticate(self.richard['token']).role, 'owner')


if __name__ == '__main__':
    unittest.main()
