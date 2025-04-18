from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    payment_certificate_ids = fields.One2many('payment.certificate', 'project_id', string='Payment Certificates')

    def action_create_payment_certificate(self):
        self.ensure_one()
        payment_certificate = self.env['payment.certificate'].create({
            'project_id': self.id,
            'amount': 0.0,
            'currency_id': self.env.company.currency_id.id,
        })
        return {
            'name': 'Payment Certificate',
            'type': 'ir.actions.act_window',
            'res_model': 'payment.certificate',
            'view_mode': 'form',
            'res_id': payment_certificate.id,
            'target': 'new',
        }
