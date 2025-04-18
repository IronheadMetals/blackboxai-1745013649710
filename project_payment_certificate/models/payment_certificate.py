from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PaymentCertificate(models.Model):
    _name = 'payment.certificate'
    _description = 'Payment Certificate'

    name = fields.Char(string='Certificate Reference', required=True, copy=False, readonly=True, default='New')
    project_id = fields.Many2one('project.project', string='Project', required=True)
    delivery_note_id = fields.Many2one('stock.picking', string='Delivery Note')
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    amount = fields.Monetary(string='Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled')
    ], string='Status', readonly=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.certificate') or 'New'
        return super(PaymentCertificate, self).create(vals)

    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_('Invoice is already created for this payment certificate.'))
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.project_id.partner_id.id if self.project_id.partner_id else False,
            'invoice_date': self.date,
            'invoice_origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': _('Payment Certificate %s') % self.name,
                'quantity': 1,
                'price_unit': self.amount,
                'account_id': self.env['account.account'].search([('user_type_id.type', '=', 'receivable')], limit=1).id,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        self.state = 'invoiced'
        return invoice.action_post()
