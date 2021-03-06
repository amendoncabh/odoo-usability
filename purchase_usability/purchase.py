# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_type_id = fields.Many2one(track_visibility='onchange')
    dest_address_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    incoterm_id = fields.Many2one(track_visibility='onchange')
    partner_ref = fields.Char(track_visibility='onchange')
    # field 'partner_id': native value for track_visibility='always'
    partner_id = fields.Many2one(track_visibility='onchange')
    # for report
    delivery_partner_id = fields.Many2one(
        'res.partner', compute='_compute_delivery_partner_id', readonly=True)

    @api.multi
    @api.depends('dest_address_id', 'picking_type_id')
    def _compute_delivery_partner_id(self):
        for o in self:
            delivery_partner_id = False
            if o.dest_address_id:
                delivery_partner_id = o.dest_address_id
            elif (
                    o.picking_type_id.warehouse_id and
                    o.picking_type_id.warehouse_id.partner_id):
                delivery_partner_id = o.picking_type_id.warehouse_id.partner_id
            o.delivery_partner_id = delivery_partner_id


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Field added to have a clickable link from picking to PO
    purchase_id = fields.Many2one(
        related='move_lines.purchase_line_id.order_id', readonly=True,
        string='Purchase Order')
