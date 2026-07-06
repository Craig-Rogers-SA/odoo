# -*- coding: utf-8 -*-
"""
Characterization tests for sale.order._compute_partner_credit_warning.

CHARACTERIZATION CONTRACT
─────────────────────────
These tests record what the method CURRENTLY returns for each behavioral branch.
They do not assert what the output *should* be — only what it *is*.

If a test fails after a refactor:
  1. Confirm the new output is intentional.
  2. Update the assertEqual string to the new output.
  3. Commit both the implementation change and the test update together.

Do NOT convert these to assertIn / assertRegex — full-string equality is the point.
"""

from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.sale.tests.common import TestSaleCommon


@tagged('post_install', '-at_install')
class TestCharacterizeCreditWarning(TestSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.account_use_credit_limit = True
        cls.partner_a.credit_limit = 100.0

    def setUp(self):
        super().setUp()
        # Lock language so translation never changes the captured strings.
        self.env = self.env(context=dict(self.env.context, lang='en_US'))

    # ------------------------------------------------------------------ helpers

    def _draft_order(self, amount=0.0):
        """Return a new draft sale.order for partner_a.

        amount=0 produces an order with no lines (amount_total=0).
        """
        lines = []
        if amount:
            lines = [Command.create({
                'product_id': self.company_data['product_order_no'].id,
                'price_unit': amount,
                'product_uom_qty': 1,
                'tax_id': False,
            })]
        return self.env['sale.order'].create({
            'partner_id': self.partner_a.id,
            'order_line': lines,
        })

    def _confirmed_order(self, amount):
        """Confirm a SO for partner_a, which drives credit_to_invoice upward."""
        order = self._draft_order(amount)
        order.action_confirm()
        self.partner_a.invalidate_recordset(['credit', 'credit_to_invoice'])
        return order

    def _post_invoice(self, amount):
        """Create and post a customer invoice, which drives partner.credit upward."""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_a.id,
            'invoice_line_ids': [Command.create({
                'name': 'characterization setup',
                'account_id': self.company_data['default_account_revenue'].id,
                'quantity': 1,
                'price_unit': amount,
                'tax_ids': False,
            })],
        })
        invoice.action_post()
        self.partner_a.invalidate_recordset(['credit', 'credit_to_invoice'])
        return invoice

    # ──────────────────────────────────────────────────────────────────────────
    # Gate 1 — feature switch
    # ──────────────────────────────────────────────────────────────────────────

    def test_branch_feature_disabled(self):
        """account_use_credit_limit=False gates every branch → ''."""
        self.env.company.account_use_credit_limit = False
        order = self._draft_order(amount=500.0)
        self.assertEqual(order.partner_credit_warning, '')

    # ──────────────────────────────────────────────────────────────────────────
    # Gate 2 — state machine
    # ──────────────────────────────────────────────────────────────────────────

    def test_branch_state_draft_does_not_suppress(self):
        """state='draft' is inside the warning window — warning CAN appear."""
        order = self._draft_order(amount=200.0)
        # 200 > 100 limit, no prior credit — warning expected
        self.assertEqual(
            order.partner_credit_warning,
            "partner_a has reached its credit limit of: $\xa0100.00\n"
            "Total amount due (including this document): $\xa0200.00",
        )

    def test_branch_state_sent_does_not_suppress(self):
        """state='sent' is inside the warning window — warning CAN appear."""
        order = self._draft_order(amount=200.0)
        order.action_lock()   # draft → sent (quotation sent)
        order.invalidate_recordset(['partner_credit_warning'])
        self.assertEqual(
            order.partner_credit_warning,
            "partner_a has reached its credit limit of: $\xa0100.00\n"
            "Total amount due (including this document): $\xa0200.00",
        )

    def test_branch_state_sale_suppresses(self):
        """state='sale' (confirmed) is outside the window → ''."""
        order = self._draft_order(amount=500.0)
        order.action_confirm()
        order.invalidate_recordset(['partner_credit_warning'])
        self.assertEqual(order.partner_credit_warning, '')

    # ──────────────────────────────────────────────────────────────────────────
    # Gate 3 — threshold
    # ──────────────────────────────────────────────────────────────────────────

    def test_branch_under_limit(self):
        """total_credit < credit_limit → ''."""
        order = self._draft_order(amount=50.0)  # 50 < 100
        self.assertEqual(order.partner_credit_warning, '')

    def test_branch_exactly_at_limit(self):
        """total_credit == credit_limit → '' (boundary: <= does not warn)."""
        order = self._draft_order(amount=100.0)  # 100 == 100
        self.assertEqual(order.partner_credit_warning, '')

    def test_branch_zero_credit_limit_means_unlimited(self):
        """credit_limit=0.0 is falsy → treated as no limit → ''."""
        self.partner_a.credit_limit = 0.0
        order = self._draft_order(amount=500.0)
        self.assertEqual(order.partner_credit_warning, '')

    # ──────────────────────────────────────────────────────────────────────────
    # Warning branches (threshold exceeded)
    # ──────────────────────────────────────────────────────────────────────────

    def test_branch_both_credit_to_invoice_and_current_amount(self):
        """credit_to_invoice > 0 AND current_amount > 0 → 'including sales orders and this document'."""
        # confirmed SO → credit_to_invoice = 110
        self._confirmed_order(110.0)
        # draft SO with lines → current_amount = 20; total = 0+110+20 = 130
        order = self._draft_order(amount=20.0)
        self.assertEqual(
            order.partner_credit_warning,
            "partner_a has reached its credit limit of: $\xa0100.00\n"
            "Total amount due (including sales orders and this document): $\xa0130.00",
        )

    def test_branch_credit_to_invoice_only(self):
        """credit_to_invoice > 0, current_amount == 0 → 'including sales orders'."""
        # confirmed SO → credit_to_invoice = 150
        self._confirmed_order(150.0)
        # empty draft SO → amount_total=0 → current_amount=0; total = 0+150+0 = 150
        order = self._draft_order()
        self.assertEqual(
            order.partner_credit_warning,
            "partner_a has reached its credit limit of: $\xa0100.00\n"
            "Total amount due (including sales orders): $\xa0150.00",
        )

    def test_branch_current_amount_only(self):
        """credit_to_invoice == 0, current_amount > 0 → 'including this document'."""
        # no confirmed SOs → credit_to_invoice = 0
        order = self._draft_order(amount=200.0)  # current_amount=200; total=200
        self.assertEqual(
            order.partner_credit_warning,
            "partner_a has reached its credit limit of: $\xa0100.00\n"
            "Total amount due (including this document): $\xa0200.00",
        )

    def test_branch_existing_credit_only(self):
        """partner.credit > limit, credit_to_invoice == 0, current_amount == 0 → base message only."""
        # posted invoice → partner.credit = 150
        self._post_invoice(150.0)
        # empty draft SO → current_amount=0, credit_to_invoice=0; total=150+0+0=150
        order = self._draft_order()
        self.assertEqual(
            order.partner_credit_warning,
            "partner_a has reached its credit limit of: $\xa0100.00\n"
            "Total amount due: $\xa0150.00",
        )
